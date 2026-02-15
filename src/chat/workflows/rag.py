#Reference: https://docs.langchain.com/oss/python/langgraph/agentic-rag
from langchain_core.tools import tool
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage
from langgraph.graph import MessagesState, StateGraph, START, END
from langgraph.prebuilt import ToolNode, tools_condition
from typing import Literal, List

from chat_persist import gen_checkpointer
from common import base_ollama_url
from output_models.grade_documents import GradeDocuments
from prompts import GRADE_PROMPT, REWRITE_PROMPT, GENERATE_PROMPT


from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

embedding_function = HuggingFaceEmbeddings(model="sentence-transformers/all-mpnet-base-v2")
vector_store = Chroma(
    #collection_name="nike-sentence-transformers",
    collection_name="chat_rmg",
    embedding_function=embedding_function,
    persist_directory="/rag-data/chroma_db",
)

retriever = vector_store.as_retriever()

response_model = ChatOllama(model='qwen3:8b', temperature=0, base_url=base_ollama_url, reasoning=True)
grader_model = ChatOllama(model='qwen3:8b', temperature=0, base_url=base_ollama_url, reasonsing=True)

@tool
def retrieve_docs(query: str) -> List[dict]:
    """Search and return information about information technology policies and procedures."""
    docs = retriever.invoke(query)
    return [{'page_content': doc.page_content,
             'metadata': doc.metadata} 
             for doc in docs]

def generate_query_or_respond(state: MessagesState):
    """Call the model to generate a response based on the current state.  Given the question,
    it will decide to retrieve using the retriever tool, or simply respond to the user."""
    response = (
        response_model.bind_tools([retrieve_docs]).invoke(state['messages'])
    )
    return {'messages':[response]}

def grade_documents(state: MessagesState) -> Literal['generate_answer', 'rewrite_question']:
    """Determine whether the retrieved documents are relevant to the question."""
    question = state['messages'][0].content
    context = state['messages'][-1].content
    
    prompt = GRADE_PROMPT.format(context=context, question=question)
    response = grader_model.with_structured_output(GradeDocuments).invoke([{'role':'user', 'content':prompt}])
    score = response.binary_score
    return 'generate_answer' if score == 'yes' else 'rewrite_question'

def rewrite_question(state: MessagesState):
    """Rewrite the original user question."""
    messages = state['messages']
    question = messages[0].content
    prompt = REWRITE_PROMPT.format(question=question)
    response = response_model.invoke([{'role':'user', 'content':prompt}])
    return {'messages': [HumanMessage(content=response.content)]}

def generate_answer(state: MessagesState):
    """Generate an answer"""
    question = state['messages'][0].content
    context = state['messages'][-1].content
    
    prompt = GENERATE_PROMPT.format(context=context, question=question)
    response = response_model.invoke([{'role':'user', 'content':prompt}])
    return {'messages':[response]}

#Assemble the RAG Graph
workflow = StateGraph(MessagesState)

#Node definition
workflow.add_node(generate_query_or_respond)
workflow.add_node("retrieve", ToolNode([retrieve_docs]))
workflow.add_node(rewrite_question)
workflow.add_node(generate_answer)


#Edge definition
workflow.add_edge(START, "generate_query_or_respond")
#Decide whether to retrieve
workflow.add_conditional_edges(
    "generate_query_or_respond",
    #Assess LLM decision (call 'retrieve_docss' tool or respond to the user)
    tools_condition,
    {
        #Translate condition outputs to nodes in our graph
        "tools":"retrieve",
        END: END,
    }
)

#Edges taken after 'action' node is called.
workflow.add_conditional_edges(
    "retrieve",
    grade_documents #Assess agent decision
)

workflow.add_edge("generate_answer", END)
workflow.add_edge("rewrite_question", "generate_query_or_respond")
graph = workflow.compile(checkpointer=gen_checkpointer(False))