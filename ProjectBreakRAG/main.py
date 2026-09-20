import argparse

from src.load import cargar_documentos
from src.chunk import crear_chunks
from src.index import crear_indice
from src.rag import responder
from src.retriever import obtener_retriever


def indexar():

    print("Cargando documentos...")
    documentos = cargar_documentos()
    print(f"Documentos cargados: {len(documentos)}")

    print("Creando chunks...")
    chunks = crear_chunks(documentos)
    print(f"Chunks generados: {len(chunks)}")

    print("Generando embeddings y creando índice Chroma...")
    crear_indice(chunks)

    print("Índice creado correctamente.")


def consultar(pregunta, k):

    print(f"\nPregunta: {pregunta}")
    print("\nBuscando información relevante...")

    retriever = obtener_retriever(k)
    resultados = retriever.invoke(pregunta)
    print(f"\nResultados encontrados: {len(resultados)}")

    for i, resultado in enumerate(resultados, 1):

        print(f"\n--- Resultado {i} ---")
        print(f"Fuente: {resultado.metadata.get('source')}")
        print(f"Página: {resultado.metadata.get('page')}")
        print("\nContenido:")
        print(resultado.page_content[:800])


def preguntar_rag(pregunta, k):

    print(f"\nPregunta: {pregunta}")
    print("\nGenerando respuesta...\n")

    resultado = responder(pregunta, k=k)

    print("RESPUESTA")
    print("-" * 40)
    print(resultado["respuesta"])

    print("\nFUENTES")
    print("-" * 40)

    for fuente in resultado["fuentes"]:
        print(f"- {fuente['source']} (página {fuente['page']})")


def main():

    parser = argparse.ArgumentParser(
        description="Sistema RAG sobre becas MEC"
    )

    parser.add_argument(
        "--index",
        action="store_true",
        help="Carga los documentos y crea el índice Chroma"
    )

    parser.add_argument(
        "--query",
        type=str,
        help="Realiza una búsqueda en el índice Chroma"
    )

    parser.add_argument(
        "--ask",
        type=str,
        help="Realiza una consulta RAG completa"
    )

    parser.add_argument(
        "--k",
        type=int,
        default=5,
        help="Número de chunks a recuperar"
    )

    args = parser.parse_args()

    if args.index:
        indexar()

    elif args.query:
        consultar(args.query, args.k)

    elif args.ask:
        preguntar_rag(args.ask, args.k)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()