import streamlit as st
import google.generativeai as genai
import os

# 1. FORZAMOS LA VERSIÓN ESTABLE ANTES DE CONFIGURAR
os.environ["GOOGLE_API_VERSION"] = "v1"

st.set_page_config(page_title="IA Resumidora", page_icon="📝")
st.title("📝 Mi Resumidor Mágico")

# 2. CONFIGURACIÓN DE LA LLAVE
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("Falta la API Key en los Secrets de Streamlit")

# 3. INTERFAZ
text = st.text_area("Pega tu texto aquí:", height=200)

if st.button("Resumir ahora"):
    if text:
        try:
            # Usamos el nombre de modelo más fiable
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            prompt = f"Resume este texto en español de forma clara en 3 frases: {text}"
            response = model.generate_content(prompt)
            
            st.subheader("Resumen:")
            st.write(response.text)
        except Exception as e:
            st.error(f"Error de Google: {e}")
    else:
        st.warning("Escribe algo primero.")
        