import time

from src.logging_utils import guardar_log
from src.generate import obtener_llm
from src.retriever import obtener_retriever
from config import TOP_K, MAX_CHUNKS


def responder(pregunta, k=TOP_K):
    """
    Realiza una consulta RAG y devuelve la respuesta,
    las fuentes y los chunks recuperados.
    """
    if not pregunta or not pregunta.strip():
        raise ValueError("La pregunta no puede estar vacía")

    inicio = time.perf_counter()

    retriever = obtener_retriever(k=k)

    documentos = retriever.invoke(pregunta)

    # Limitamos los chunks que se envían al modelo.
    documentos = documentos[:MAX_CHUNKS]

    contexto = "\n\n---\n\n".join(
        doc.page_content for doc in documentos
    )

    prompt = f"""
Responde únicamente utilizando el contexto proporcionado.

Si la información no aparece en el contexto responde exactamente:

"No está en los documentos."

--- CONTEXTO ---

{contexto}

--- PREGUNTA ---

{pregunta}
"""

    llm = obtener_llm()
    respuesta = llm.invoke(prompt)

    if isinstance(respuesta.content, list):
        texto = "".join(
            bloque["text"]
            for bloque in respuesta.content
            if isinstance(bloque, dict) and "text" in bloque
        )
    else:
        texto = respuesta.content

    tiempo = time.perf_counter() - inicio

    guardar_log(
        pregunta=pregunta,
        k=min(k, MAX_CHUNKS),
        chunks=len(documentos),
        modelo="gemini-3.6-flash",
        tiempo=tiempo
    )

    return {
        "respuesta": texto,
        "fuentes": [
            {
                "source": doc.metadata.get("source"),
                "page": doc.metadata.get("page")
            }
            for doc in documentos
        ],
        "chunks": documentos
    }