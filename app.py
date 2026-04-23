import streamlit as st
import google.generativeai as genai

# Configuración de la página (esto debe ir al principio)
st.set_page_config(page_title="Resumidor IA", page_icon="📝")
st.title("📝 Mi Resumidor Mágico")

# Conectar con la llave
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("Falta la API Key en los Secrets de Streamlit")

text = st.text_area("Pega tu texto aquí:", height=200)

if st.button("Resumir ahora"):
    if text:
        try:
            # Usamos este nombre que es el que mejor funciona ahora
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            prompt = f"Resume este texto en español de forma clara en 3 frases: {text}"
            
            response = model.generate_content(prompt)
            
            st.subheader("Resumen:")
            st.write(response.text)
        except Exception as e:
            st.error(f"Hubo un problema con la IA: {e}")
    else:
        st.warning("Escribe algo primero.")