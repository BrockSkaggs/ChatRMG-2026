import os

import platform
from dotenv import load_dotenv, find_dotenv
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_ollama import ChatOllama
from langchain_core.documents import Document
from langchain_chroma import Chroma
from langgraph.types import StateSnapshot
import re
from typing import List

from logs import get_logger

import chat.workflows.multiply_tool as multiply_tool
import chat.workflows.rag as rag

from common import base_ollama_url


# for eployment on azure, Chroma SQlite version is out oof date, over write
# inspired from: https://gist.github.com/defulmere/8b9695e415a44271061cc8e272f3c300
if platform.system() == "Linux":
    # these three lines swap the stdlib sqlite3 lib with the pysqlite3 package
    __import__('pysqlite3')
    import sys
    sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

logger = get_logger(__name__)

load_dotenv(find_dotenv())

# chat_model = ChatOllama(model='llama3.2:latest')
chat_model = ChatOllama(model='qwen3:8b', base_url=base_ollama_url)

def connect_to_vectorstore():
    """
    Connect to the VectorStore and return a VectorStore object.
    Returns
    -------
    VectorStore object
        The VectorStore object connected to the VectorStore.
    """
    embedding_function = HuggingFaceEmbeddings(model="sentence-transformers/all-MiniLM-L6-v2")
    chroma_db = Chroma(
        # persist_directory = r'B:\SKAGGS\Professional_Dev\LangChain\Tutorials\data\chroma_db',
        persist_directory= '/rag-data/chroma_db',
        embedding_function = embedding_function,
        collection_name = "nike-sentence-transformers"
    )

    return chroma_db

# Original
def stream_send_messages(prompt: List[dict], model_select: str, conversation_id: str):
    """
    Send a prompt to the OpenAI API and return the response.
    Parameters
        prompt : The prompt to send to the LLM.
    """    
    logger.debug(f"Conversation ID: {conversation_id}")
    config = {'configurable': {'thread_id': conversation_id}}
    if model_select == 'nike-expert':
        return chat_model.stream(prompt)
    elif model_select == 'multiplier':
        return multiply_tool.graph.stream({'messages': prompt}, stream_mode='messages', config=config)
    elif model_select == 'it-rag':
        return rag.graph.stream({'messages': prompt}, stream_mode='messages', config=config)

def get_relevant_documents(
    user_prompt,
    vector_store,
    k=3,
    method="similarity",
):
    """
    Get the most relevant documents from the VectorStore for a given user prompt.

    Parameters
    ----------
    user_prompt : str
        The user prompt to search for in the VectorStore.
    vector_store : Zilliz object
        The object connected to the VectorStore.
    method: str, optional
        The method to use for searching the VectorStore, options are mmr, similarity. Default is "similarity".

    Returns
    -------
    list of Document objects
        The list of relevant documents from the VectorStore.
    """

    if method == "mmr":
        relevant_documents = vector_store.max_marginal_relevance_search(
            query=user_prompt,
            k=k,
            fetch_k=10,
        )

        return relevant_documents
    elif method == "similarity":
        relevant_documents = vector_store.similarity_search_with_score(
            query=user_prompt,
            k=k,
        )
        # take the relavant documents which is a list of tuples of Document, score and convert to a list of Document
        # with a new field in metadata of each document called score
        for doc, score in relevant_documents:
            doc.metadata["score"] = score

        # only keep the documents from the relevant documents tuples, not score
        relevant_documents_with_score = [doc for doc, score in relevant_documents]

        # return selected_relevant_documents
        return relevant_documents_with_score
    else:
        raise ValueError("method must be mmr or similarity")

def convert_documents_to_chat_context(relevant_documents):
    """
    Convert a list of relevant documents to a chat context string.

    Parameters
    ----------
    relevant_documents : list of Document objects
        The list of relevant documents to convert.

    Returns
    -------
    str
        The chat context string created from the relevant documents.
    """
    # combine the page content from the relevant documents into a single string
    context_str = ""
    for i, doc in enumerate(relevant_documents):
        context_str += f"{doc.page_content}\n"

    return context_str

def convert_chat_history_to_string(
    chat_history: dict, include_num_messages: int = 1, questions_only = False
) -> str:
    """
    Convert a chat history dictionary to a string.

    Parameters
    ----------
    chat_history : dict
        A dictionary containing the chat history.

    Returns
    -------
    str
        A string representation of the chat history.

    Notes
    -----
    The chat history dictionary should have the following format:
    {
        "chat_history": [
            {
                "role": "user" or "assistant",
                "content": "message content"
            },
            ...
        ]
    }
    The returned string will have the following format:
    "user: message content\nassistant: message content\n..."

    """
    if questions_only is False:
        start_index = -(2 * include_num_messages) - 1
        chat_history_str = ""
        for line in chat_history["chat_history"][start_index:-1]:
            chat_history_str += f"{line['role']}: {line['content'].strip()}\n"

        logger.debug(f"Chat history: {chat_history_str}")
    elif questions_only is True:
        start_index = -(2 * include_num_messages) - 1
        chat_history_str = ""
        for line in chat_history["chat_history"][start_index:-1]:
            if line['role'] == 'user':
                chat_history_str += f"{line['role']}: {line['content'].strip()}\n"

        logger.debug(f"Chat history: {chat_history_str}")

    return chat_history_str

def recover_chat_history(model_select:str, conversation_id: str) -> List[StateSnapshot]:
    config = {'configurable': {'thread_id': conversation_id}}
    if model_select == 'nike-expert':
        raise NotImplementedError("Recover chat history not implemented for nike-expert model yet.")
    elif model_select == 'multiplier':
        # state_hist = list(multiply_tool.graph.get_state_history(config))   #Gets all states in history
        latest_state = multiply_tool.graph.get_state(config) #Gets only latest state in history
    elif model_select == 'it-rag':
        latest_state = rag.graph.get_state(config)
    
    return latest_state.values['messages']