from langchain_ollama import ChatOllama
from langgraph.graph import StateGraph, START, END, MessagesState
from langgraph.prebuilt import ToolNode
from langgraph.prebuilt import tools_condition
from langgraph.checkpoint.memory import MemorySaver #TODO: Will need to switch to PostgresSaver for production

from common import base_ollama_url

def multiply(a:int, b:int) -> int:
    """Multiply a and b.

    Args:
        a: first int
        b: second int
    """
    return a*b

memory = MemorySaver()
llm = ChatOllama(model='qwen3:8b', base_url=base_ollama_url, reasoning=True)
llm_with_tools = llm.bind_tools([multiply])

#Nodes
def tool_calling_llm(state: MessagesState):
    return {'messages': [llm_with_tools.invoke(state['messages'])]}

#Graph
builder = StateGraph(MessagesState)
builder.add_node("tool_calling_llm", tool_calling_llm)
builder.add_node("tools", ToolNode([multiply]))
builder.add_edge(START, "tool_calling_llm")
builder.add_conditional_edges(
    "tool_calling_llm",
    tools_condition
)
builder.add_edge("tools", END)
graph = builder.compile(checkpointer=memory)