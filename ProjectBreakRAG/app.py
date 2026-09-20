
import streamlit as st

from src.rag import responder

st.set_page_config(
    page_title="RAG Becas MEC",
    page_icon="🎓",
    layout="wide"
)

st.title("🎓 Asistente RAG sobre Becas MEC")

st.write(
    "Consulta información del corpus oficial de becas MEC."
)

k = st.sidebar.slider(
    "Top K",
    1,
    10,
    3
)

pregunta = st.chat_input("Escribe tu pregunta...")

if "historial" not in st.session_state:
    st.session_state.historial = []

if pregunta:
    resultado = responder(pregunta, k=k)
    st.session_state.historial.append(
        (pregunta, resultado)
    )

for pregunta, resultado in st.session_state.historial:
    with st.chat_message("user"):
        st.write(pregunta)

    with st.chat_message("assistant"):
        st.write(resultado["respuesta"])

        with st.expander("📄 Fuentes"):
            for fuente in resultado["fuentes"]:
                st.write(
                    f"**{fuente['source']}** · página {fuente['page']}"
                )

        with st.expander("🧩 Chunks recuperados"):
            for i, chunk in enumerate(resultado["chunks"], 1):
                st.markdown(f"### Chunk {i}")

                st.write(
                    f"**Fuente:** {chunk.metadata.get('source')}"
                )

                st.write(
                    f"**Página:** {chunk.metadata.get('page')}"
                )

                st.text(chunk.page_content)

st.sidebar.divider()
st.sidebar.subheader("Métricas")

st.sidebar.metric("Modelo", "Gemini 3.6 Flash")
st.sidebar.metric("Top K", k)
st.sidebar.metric("Historial", len(st.session_state.historial))
