from pathlib import Path

from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader
)

DATA_PATH = Path("data/beca_mec")


def cargar_documentos():
    """
    Lee los PDFs y documentos Markdown del corpus
    y devuelve una lista de documentos.
    """
    documentos = []

    # Cargar PDFs
    for pdf in DATA_PATH.glob("*.pdf"):
        loader = PyPDFLoader(str(pdf))
        documentos.extend(loader.load())

    # Cargar Markdown
    for md in DATA_PATH.glob("*.md"):
        # README_fuentes.md es documentación del corpus,
        # no contenido que queramos indexar.
        if md.name == "README_fuentes.md":
            continue

        loader = TextLoader(
            str(md),
            encoding="utf-8"
        )
        documentos.extend(loader.load())

    return documentos


if __name__ == "__main__":
    docs = cargar_documentos()

    print(f"Se han cargado {len(docs)} documentos/páginas.")

    if docs:
        print("\nPrimeras 500 letras del primer documento:\n")
        print(docs[0].page_content[:500])

        print("\nMetadatos del primer documento:\n")
        print(docs[0].metadata)