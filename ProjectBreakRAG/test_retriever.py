
from src.retriever import obtener_retriever


pregunta = "¿Qué información aparece sobre la presentación de recursos?"


for k in [1, 3]:

    print(f"\n{'=' * 50}")
    print(f"PRUEBA CON K = {k}")
    print(f"{'=' * 50}")

    retriever = obtener_retriever(k=k)

    resultados = retriever.invoke(pregunta)

    print(f"Resultados encontrados: {len(resultados)}")

    for i, resultado in enumerate(resultados, 1):
        print(f"\n--- Resultado {i} ---")
        print(f"Fuente: {resultado.metadata.get('source')}")
        print(f"Página: {resultado.metadata.get('page')}")
        print(resultado.page_content[:500])

