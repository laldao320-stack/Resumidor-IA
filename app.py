import streamlit as st
import google.generativeai as genai
import os

# Esto obliga a Streamlit a olvidar la versión 'beta'
os.environ["GOOGLE_API_VERSION"] = "v1"

st.title("📝 Mi Resumidor Mágico")

# Configuración simplificada al máximo
try:
    llave = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=llave)
    # Cambiamos el nombre del modelo al 'latest'
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
except Exception as e:
    st.error(f"Error de configuración: {e}")

text = st.text_area("Pega tu texto aquí:")

if st.button("Resumir ahora"):
    if text:
        try:
            # Petición directa
            res = model.generate_content(f"Resume en 3 frases: {text}")
            st.success("¡Lo conseguí!")
            st.write(res.text)
        except Exception as e:
            st.error(f"Error técnico: {e}")