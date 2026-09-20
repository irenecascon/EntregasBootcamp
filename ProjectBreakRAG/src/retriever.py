from config import CHROMA_PATH, DEFAULT_K
from langchain_chroma import Chroma
from src.embed import obtener_embeddings


def obtener_retriever(k=DEFAULT_K):

    embeddings = obtener_embeddings()

    vectorstore = Chroma(
        persist_directory=CHROMA_PATH,
        embedding_function=embeddings
    )

    return vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": k}
    )