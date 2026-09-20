import time
from src.logging_utils import guardar_log

from src.generate import obtener_llm
from src.retriever import obtener_retriever

def responder(pregunta, k=3):
    inicio = time.perf_counter()
    retriever = obtener_retriever(k=k)
    documentos = retriever.invoke(pregunta)    
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

    # Extraer solo el texto de la respuesta de Gemini
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
        k=k,
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
