import json

from src.retriever import obtener_retriever


def cargar_preguntas():
    with open("queries/evaluation.json", "r", encoding="utf-8") as f:
        return json.load(f)


def evaluar(k):
    preguntas = cargar_preguntas()

    # Obtenemos el retriever para poder acceder al vectorstore
    retriever = obtener_retriever(k=k)
    vectorstore = retriever.vectorstore

    resultados = []

    for pregunta in preguntas:
        documentos_con_puntuacion = vectorstore.similarity_search_with_score(
            pregunta["pregunta"],
            k=k
        )

        fuentes = []

        for doc, puntuacion in documentos_con_puntuacion:
            fuentes.append({
                "source": doc.metadata.get("source"),
                "page": doc.metadata.get("page"),
                "score": round(float(puntuacion), 4),
                "chunk": doc.page_content[:250]
            })

        resultados.append({
            "id": pregunta["id"],
            "pregunta": pregunta["pregunta"],
            "k": k,
            "resultados": fuentes
        })

    return resultados


def main():
    resultados_k1 = evaluar(k=1)
    resultados_k3 = evaluar(k=3)

    resultados = resultados_k1 + resultados_k3

    with open("evaluation_results.json", "w", encoding="utf-8") as f:
        json.dump(resultados, f, ensure_ascii=False, indent=2)

    print("\n========== EVALUACIÓN ==========\n")

    for resultado in resultados:
        print(f"Pregunta {resultado['id']} | K={resultado['k']}")
        print(resultado["pregunta"])

        for fuente in resultado["resultados"]:
            print(
                f"  - {fuente['source']} | "
                f"página {fuente['page']} | "
                f"score: {fuente['score']}"
            )

        print()

    print("Resultados guardados en: evaluation_results.json")


if __name__ == "__main__":
    main()