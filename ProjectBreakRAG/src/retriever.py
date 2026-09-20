from langchain_chroma import Chroma

from src.embed import obtener_embeddings
from config import CHROMA_PATH, TOP_K, MAX_CHUNKS


def obtener_retriever(k=TOP_K):
    """
    Devuelve un retriever de Chroma.

    TOP_K define el número de chunks recuperados por defecto.
    MAX_CHUNKS limita el número máximo de chunks recuperados.
    """
    if k < 1:
        raise ValueError("k debe ser mayor o igual que 1")

    k = min(k, MAX_CHUNKS)

    embeddings = obtener_embeddings()

    vectorstore = Chroma(
        persist_directory=str(CHROMA_PATH),
        embedding_function=embeddings
    )

    return vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": k}
    )