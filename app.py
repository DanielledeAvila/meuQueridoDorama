import streamlit as st
import google.generativeai as genai

# 1. Configuração da sua página
st.set_page_config(page_title="X1 Doramas", page_icon="🎬", layout="centered")
st.title("🎬 Nunca mais perca nos seus X1 Doramas")
st.write("Seu assistente especializado em Dorama e apostas!")

# 2. Busca a chave guardada em segurança nos Secrets do Streamlit
if "GEMINI_API_KEY" in st.secrets:
    GOOGLE_API_KEY = st.secrets["GEMINI_API_KEY"]
else:
    st.error("Chave de API não configurada nos Secrets do Streamlit.")
    st.stop()

genai.configure(api_key=GOOGLE_API_KEY)

# 3. Definição do Prompt de Sistema (Instruções do seu assistente)
system_instruction = """
Agir como um assistente de apostas focado em Doramas.
Seu objetivo é ajudar o usuário a analisar os dramas coreanos, 
trazer estatísticas de preferência de público e ajudar a vencer debates (X1) sobre doramas.
Seja carismático e use termos do universo de doramas.
"""

# 4. Inicializa o modelo Gemini com as instruções
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=system_instruction
)

# 5. Gerenciamento do histórico do chat na tela limpa
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

if "messages" not in st.session_state:
    st.session_state.messages = []

# Exibe mensagens anteriores
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Campo de entrada de texto do usuário (Barra de chat limpa embaixo)
if user_input := st.chat_input("Pergunte algo sobre seu Dorama favorito..."):
    # Mostra mensagem do usuário
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Envia para o Gemini e gera resposta
    response = st.session_state.chat_session.send_message(user_input)
    
    # Mostra a resposta do assistente
    st.session_state.messages.append({"role": "assistant", "content": response.text})
    with st.chat_message("assistant"):
        st.markdown(response.text)
