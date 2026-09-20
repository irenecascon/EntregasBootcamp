# Informe de decisiones – ProjectBreakRAG

## 1. Objetivo

Desarrollar un asistente RAG capaz de responder preguntas sobre las Becas MEC utilizando únicamente documentación oficial del Ministerio de Educación.

El sistema debía:

- recuperar información relevante mediante búsqueda semántica;
- generar respuestas apoyadas en el contexto;
- abstenerse cuando la información no estuviera en el corpus.

---

# 2. Corpus

El corpus está compuesto por documentación oficial.

| Documento | Formato |
|-----------|----------|
| Convocatoria BOE | PDF |
| Libro Becas MEC | PDF |

En total:

- 153 páginas
- 559 chunks tras el procesamiento

---

# 3. Chunking

Se utilizó `RecursiveCharacterTextSplitter`.

| Parámetro | Valor |
|-----------|-------|
| Chunk Size | 1000 |
| Overlap | 200 |

## Motivo

- mantener suficiente contexto legal;
- evitar cortar artículos completos;
- reducir pérdida de información entre chunks.

### Resultado

- chunks relativamente completos;
- buena recuperación en artículos largos;
- algunos artículos quedaron divididos entre dos chunks.

---

# 4. Embeddings

Modelo utilizado:

```
sentence-transformers/all-MiniLM-L6-v2
```

### Motivos

- gratuito;
- rápido;
- compatible con LangChain;
- suficiente para documentos administrativos.

---

# 5. Vector Store

Se utilizó ChromaDB persistente.

Se guardan metadatos como:

- source
- page

Esto permite mostrar las fuentes recuperadas tanto en CLI como en Streamlit.

---

# 6. Retriever

Se probaron dos valores de Top-K.

| K | Comportamiento |
|---|----------------|
| 1 | mayor precisión, menos contexto |
| 3 | mejor cobertura, algo más de ruido |

## Ejemplo

Pregunta:

> ¿Cómo se pueden presentar las solicitudes?

### K=1

Recupera únicamente la convocatoria BOE.

### K=3

Recupera además el artículo correspondiente del Libro de Becas.

La respuesta resulta más completa.

---

# 7. Generación

Se utilizó:

```
Gemini 3.6 Flash
```

El prompt obliga al modelo a responder únicamente con el contexto recuperado.

En caso contrario responde exactamente:

> No está en los documentos.

---

# 8. Evaluación

Se creó un conjunto de:

- 10 preguntas
- 9 dentro del corpus
- 1 fuera del corpus

Se evaluó el retrieval con K=1 y K=3.

Los resultados se almacenan en:

```
evaluation_results.json
```

---

# 9. Caso de acierto

Pregunta:

> ¿Cómo se pueden presentar las solicitudes?

El sistema respondió correctamente indicando:

- vía telemática
- registros
- oficinas de correos
- oficinas consulares
- artículo 16.4

La respuesta coincidía con los documentos recuperados.

---

# 10. Caso de abstención

Pregunta:

> ¿Cuándo se inauguró el Museo del Prado?

Respuesta:

> No está en los documentos.

Este comportamiento demuestra que el sistema evita inventar información ajena al corpus.

---

# 11. Tres fallos detectados

## Fallo 1

Pregunta:

> ¿Qué obligaciones tienen las personas beneficiarias?

El retriever recuperaba inicialmente páginas poco relevantes.

### Posible mejora

- aumentar K;
- mejorar embeddings.

---

## Fallo 2

Algunos artículos quedan divididos entre varios chunks.

Ejemplo:

- página 99
- continuación en otro fragmento.

### Posible mejora

Aumentar ligeramente el overlap.

---

## Fallo 3

Algunas preguntas recuperan información relacionada pero no el artículo exacto.

### Posible mejora

- búsqueda híbrida;
- reranking;
- recuperación por encabezados.

---

# 12. Siguientes pasos

Si el proyecto evolucionara hacia Agentes o MLOps podrían incorporarse:

- búsqueda híbrida (BM25 + embeddings);
- reranker;
- múltiples corpus;
- evaluación automática con métricas de grounding;
- despliegue mediante API.