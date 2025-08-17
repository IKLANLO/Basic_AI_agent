# primero es necesario en un terminal ejecutar ollama serve, para que el modelo pueda ser invocado, luego se puede ejecutar
# este script para invocar el modelo ('streamlit run basic_ai_agent.py' para la interfaz web)
from langchain_ollama import OllamaLLM
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.prompts import PromptTemplate 
import streamlit as st
import subprocess
import time
import os
import requests

# -----------------------------
max_reintentos = 5
reintentos = 0

# Función para verificar si ollama ha iniciado correctamente
def ollama_started(log_path="ollama_output.txt", timeout=30):
    start = time.time()
    while time.time() - start < timeout:
        if os.path.exists(log_path):
            with open(log_path, "r") as f:
                for line in f:
                    if "Listening on 127.0.0.1:11434" in line:
                        return True
        time.sleep(1)
    return False

# Intentar iniciar Ollama hasta que esté listo
while not ollama_started() and reintentos < max_reintentos:
    st.warning(f"Intentando iniciar... (Intento {reintentos+1})")
    # Solo intenta iniciar si Ollama no está corriendo
    try:
        r = requests.get("http://localhost:11434/api/tags")
        if r.status_code == 200:
            break
    except Exception:
        subprocess.Popen(["python", "start_ollama.py"])
        time.sleep(5)
        reintentos += 1

if not ollama_started():
    st.error("No se pudo iniciar Ollama después de varios intentos. Revisa el archivo de log o inicia Ollama manualmente.")
    st.stop()

# -------------------------------
# Configuración del modelo
model = OllamaLLM(model="mistral")

# inicializar el historial de mensajes
if "chat_history" not in st.session_state:
    st.session_state.chat_history = ChatMessageHistory()

# Crear un prompt template
prompt_template = PromptTemplate(
    input_variables=["question", "chat_history"],
    template="Conversación previa:\n{chat_history}\n\nPregunta: {question}\nRespuesta:"
)

# Configurar el modelo con el historial de mensajes y el prompt template
def run_model(question):
    chat_history_text = "\n".join([f"{msg.type.capitalize()}: {msg.content}" for msg in st.session_state.chat_history.messages])

    # Generar la respuesta del modelo
    response = model.invoke(prompt_template.format(question=question, chat_history=chat_history_text))

    # Agregar la pregunta y respuesta al historial
    st.session_state.chat_history.add_user_message(question)
    st.session_state.chat_history.add_ai_message(response)

    return response

# Interfaz de usuario
col_title, col_btn = st.columns([7.5,2])
with col_title:
    st.markdown("""
        <style>
            .block-container {padding-top: 60px; max-height:fit-content !important;}
            .st-emotion-cache-1mvaqe2.e1f1d6gn3 {margin-top: 20px;}
        </style>
        <h1 style='margin-top:-7px; padding-top:0; padding-bottom:0; max-width:fit-content; color:cyan;'>Agente de IA con Memoria</h1>
        """, unsafe_allow_html=True)
with col_btn:
    if st.session_state.chat_history.messages:
        if st.button("Limpiar historial"):
            st.session_state.chat_history.clear()

# Mostrar el historial de conversación
historial = ""
if st.session_state.chat_history.messages:
    for msg in st.session_state.chat_history.messages:
        if msg.type.lower() == "human":
            historial += f"<div style='margin-bottom:10px;'><b style='color:cyan;'>Pregunta:</b> {msg.content}</div>"
        elif msg.type.lower() == "ai":
            historial += f"<b style='color:cyan;'>Respuesta:</b><span style='font-style:italic;font-size:90%;'>{msg.content}</span><hr style='margin-top:10px; margin-bottom:10px; border:0.1px dashed #033d82;'>"
    st.markdown(
        f"""
        <div style="border:2px solid #4A90E2; border-radius:10px; padding:15px; max-height: 60vh; overflow-y: auto;">
            {historial}
        </div>
        """,
        unsafe_allow_html=True
    )

col_input, col_btn = st.columns([12,1])
with col_input:
    question = st.text_area(
        'label', 
        key="input_pregunta", 
        placeholder="Escribe tu pregunta aquí...", 
        label_visibility="collapsed",
        height=68
    )
with col_btn:
    st.markdown("""
        <style>
        div.stButton > button {
            color: white;
            border-radius: 8px;
            border: 1px solid #005eb1;
            background-color: #04203b;
        }
        div.stButton > button:hover {
            background-color: #293133;
            border: 1px solid cyan;
            color: #fff;
        }
        </style>
    """, unsafe_allow_html=True)
    enviar = st.button("🚀")

if enviar and st.session_state.input_pregunta:
    response = run_model(st.session_state.input_pregunta)
    del st.session_state.input_pregunta  # Eliminar la variable del estado
    st.rerun()



