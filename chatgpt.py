import streamlit as st
from groq import Groq
#EL COSO PARA EL STREMLIT python -m streamlit run app2.py
# Configuración inicial
st.set_page_config(page_title="Mi chat de IA", page_icon="🐼")
MODELOS = ['llama3-8b-8192', 'llama3-70b-8192', 'mixtral-8x7b-32768']

# Inicialización de estado
if "mensajes" not in st.session_state:
    st.session_state.mensajes = []

# Funciones auxiliares
def configurar_pagina():
    st.title("Mi chat de IA ❤️‍🩹​")
    st.sidebar.title("Configuración de la IA")
    
    # Aseguramos un `key` único para el selectbox
    modelo = st.sidebar.selectbox(
        'Elegí un Modelo',
        options=MODELOS,
        index=0,
        key="modelo_selectbox_1"
    )
    return modelo

def crear_usuario_groq():
    return Groq(api_key=st.secrets.get("api_key", "default_api_key"))

def configurar_modelo(cliente, modelo, mensajeDeEntrada):
    return cliente.chat.completions.create(
        model=modelo,
        messages=[{"role": "user", "content": mensajeDeEntrada}],
        stream=True
    )

def actualizar_historial(rol, contenido, avatar=""):
    st.session_state.mensajes.append({"role": rol, "content": contenido, "avatar": avatar})

def mostrar_historial():
    for mensaje in st.session_state.mensajes:
        with st.chat_message(mensaje["role"], avatar=mensaje["avatar"]):
            st.markdown(mensaje["content"])

def generar_respuesta(chat_completo):
    respuesta_completa = ""
    for frase in chat_completo:
        if frase.choices[0].delta.content:
            respuesta_completa += frase.choices[0].delta.content
            yield frase.choices[0].delta.content
    return respuesta_completa

# Función principal
def main():
    modelo = configurar_pagina()
    clienteUsuario = crear_usuario_groq()
    
    # Crear el área de chat
    st.container()
    mostrar_historial()

    # Entrada del mensaje del usuario
    mensaje = st.chat_input("Escribí tu mensaje:", key="chat_input_key")

    if mensaje:
        actualizar_historial("user", mensaje, "🙂")
        chat_completo = configurar_modelo(clienteUsuario, modelo, mensaje)
        if chat_completo:
            with st.chat_message("assistant", avatar="🤖"):
                respuesta_completa = st.write_stream(generar_respuesta(chat_completo))
                actualizar_historial("assistant", respuesta_completa, "🤖")
        st.experimental_rerun()

# Ejecuta la aplicación
if __name__ == "__main__":
    main()
