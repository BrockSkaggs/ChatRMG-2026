from langchain_core.documents import Document

def convert_documents_to_dict(relevant_documents):
    """
    Convert a list of relevant documents to a list of dictionaries.

    Parameters
    ----------
    relevant_documents : list of Document objects
        The list of relevant documents to convert.

    Returns
    -------
    list of dict
        The list of dictionaries containing the page content and metadata of each document.
    """
    docs_dict = [
        {"page_content": doc.page_content, "metadata": doc.metadata}
        for doc in relevant_documents
    ]

    return docs_dict


def convert_dict_to_documents(docs_dict):
    """
    Convert a list of dictionaries to a list of Document objects.

    Parameters
    ----------
    docs_dict : list of dict
        The list of dictionaries to convert.

    Returns
    -------
    list of Document objects
        The list of Document objects created from the dictionaries.
    """
    # take the dictionary of documents and convert them to Document objects
    docs = [Document(**doc) for doc in docs_dict]

    return docs