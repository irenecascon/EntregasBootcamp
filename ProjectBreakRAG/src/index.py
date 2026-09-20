from config import CHROMA_PATH
import shutil

from langchain_chroma import Chroma
from src.embed import obtener_embeddings



def crear_indice(chunks, recreate=True):
    """
    Genera los embeddings y guarda el índice en Chroma.
    Si recreate=True, elimina el índice anterior antes de crearlo.
    """

    if recreate and CHROMA_PATH.exists():
        shutil.rmtree(CHROMA_PATH)

    embeddings = obtener_embeddings()

    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=str(CHROMA_PATH)
    )

    return vectorstore