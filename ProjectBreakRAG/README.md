# 🎓 ProjectBreakRAG - Asistente RAG sobre Becas MEC

Sistema RAG desarrollado durante el Bootcamp de AI Engineering para consultar información oficial sobre las Becas MEC mediante búsqueda semántica, ChromaDB y Gemini.

El asistente responde únicamente utilizando información contenida en el corpus documental y se abstiene cuando la información no aparece en los documentos.

---

## Características

- Pipeline completo RAG.
- ChromaDB persistente.
- CLI para indexar y consultar.
- Streamlit con chat interactivo.
- Visualización de fuentes y chunks recuperados.
- Logging de consultas.
- Evaluación con distintos valores de Top-K.

---

## Arquitectura

```
Documentos
    ↓
Carga (PyPDFLoader)
    ↓
Chunking
    ↓
Embeddings
    ↓
ChromaDB
    ↓
Retriever (Top-K)
    ↓
Prompt
    ↓
Gemini 3.6 Flash
    ↓
Respuesta
```

---

## Estructura del proyecto

```text
ProjectBreakRAG/
├── README.md
├── requirements.txt
├── .env.example
├── .gitignore
├── config.py
├── main.py
├── app.py
├── data/
│   └── beca_mec/
├── queries/
│   ├── evaluation.json
│   └── evaluate.py
├── logs/
├── chroma/
├── entregables/
│   └── informe_decisiones.md
└── src/
    ├── load.py
    ├── chunk.py
    ├── embed.py
    ├── index.py
    ├── retriever.py
    ├── generate.py
    ├── rag.py
    └── logging_utils.py
```

---

## Corpus

El proyecto utiliza documentación oficial del Ministerio de Educación sobre Becas MEC.

### Fuentes

- Convocatoria oficial publicada en el BOE.
- Libro oficial de Becas MEC.

### Formatos utilizados

- PDF (corpus principal).

---

## Tecnologías

- Python
- LangChain
- ChromaDB
- HuggingFace Embeddings
- Google Gemini
- Streamlit

---

## Instalación

### 1. Clonar

```bash
git clone <repositorio>
cd ProjectBreakRAG
```

### 2. Crear entorno virtual

Windows:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar API

Crear `.env` a partir de `.env.example`.

`.env.example`

```env
GOOGLE_API_KEY=tu_api_key_aqui
```

---

## Configuración

El archivo `config.py` centraliza los parámetros principales.

```python
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
DEFAULT_K = 3
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
LLM_MODEL = "gemini-3.6-flash"
```

---

## Uso desde CLI

### Indexar el corpus

```bash
python -m main --index
```

Ejemplo:

```
Documentos cargados: 153
Chunks generados: 559
Índice creado correctamente.
```

### Retrieval

```bash
python -m main --query "¿Cómo se pueden presentar las solicitudes?" --k 3
```

Devuelve:

- fuentes
- páginas
- contenido de cada chunk recuperado

### Pregunta completa RAG

```bash
python -m main --ask "¿Cómo se pueden presentar las solicitudes?" --k 3
```

Obtiene una respuesta generada únicamente con el contexto recuperado.

---

## Streamlit

Ejecutar:

```bash
streamlit run app.py
```

La interfaz incluye:

- chat
- selector de Top-K
- respuesta
- fuentes
- chunks recuperados
- métricas

---

## Evaluación

El proyecto incluye un conjunto de 10 preguntas.

- 9 preguntas del corpus
- 1 pregunta fuera del corpus

Se probaron dos configuraciones:

- K=1
- K=3

Los resultados se guardan en:

```
evaluation_results.json
```

---

## Ejemplos

### Dentro del corpus

Pregunta:

> ¿Cómo se pueden presentar las solicitudes?

Respuesta:

- vía telemática
- registros
- oficinas de correos
- oficinas consulares
- artículo 16.4 de la Ley 39/2015

### Fuera del corpus

Pregunta:

> ¿Cuándo se inauguró el Museo del Prado?

Respuesta:

> No está en los documentos.

Este comportamiento evita alucinaciones.

---

## Logging

Cada consulta genera un registro en:

```
logs/queries.log
```

Información almacenada:

- fecha
- pregunta
- K
- número de chunks
- modelo
- tiempo

Ejemplo:

```json
{
  "timestamp":"2026-09-19T10:42:15",
  "pregunta":"¿Cómo se pueden presentar las solicitudes?",
  "k":3,
  "chunks":3,
  "modelo":"gemini-3.6-flash",
  "tiempo_segundos":1.18
}
```

---

## Funciones principales

| Función | Descripción |
|---------|-------------|
| `cargar_documentos()` | carga PDFs |
| `crear_chunks()` | divide documentos |
| `crear_indice()` | genera Chroma |
| `obtener_retriever()` | búsqueda semántica |
| `obtener_llm()` | Gemini |
| `responder()` | pipeline RAG completo |

---

## Limitaciones conocidas

- El corpus está formado únicamente por documentos PDF.
- Algunas preguntas recuperan chunks cercanos pero no el artículo exacto.
- El modelo de embeddings MiniLM prioriza rapidez frente a precisión absoluta.

Estas mejoras se proponen como trabajo futuro.