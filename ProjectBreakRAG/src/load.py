from config import DATA_PATH
from langchain_community.document_loaders import PyPDFLoader


def cargar_documentos():
    """
    Lee todos los PDFs del corpus y devuelve una lista de documentos.
    """
    documentos = []

    for pdf in DATA_PATH.glob("*.pdf"):
        loader = PyPDFLoader(str(pdf))
        documentos.extend(loader.load())

    return documentos


if __name__ == "__main__":
    docs = cargar_documentos()

    print(f"Se han cargado {len(docs)} páginas.")

    if docs:
        print("\nPrimeras 500 letras del primer documento:\n")
        print(docs[0].page_content[:500])

        print("\nMetadatos del primer documento:\n")
        print(docs[0].metadata)

