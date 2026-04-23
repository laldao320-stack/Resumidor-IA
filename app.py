import streamlit as st
import google.generativeai as genai
import os

# Configuración de la página
st.set_page_config(page_title="IA Resumidora", page_icon="📝")

st.title("📝 Mi Resumidor Mágico")
st.write("Pega un texto largo y yo lo haré corto y claro por ti.")

# Configurar la API Key desde los Secrets de Streamlit
api_key = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=api_key)

text = st.text_area("Pega tu texto aquí:", height=200)

if st.button("Resumir ahora"):
    if text:
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # El comando experto para la IA
        prompt = f"Actúa como un experto en síntesis. Resume el siguiente texto en español, usando exactamente 3 frases claras y directas. No repitas frases del original, crea una redacción nueva: {text}"
        
        response = model.generate_content(prompt)
        
        st.subheader("Resumen:")
        st.write(response.text)
    else:
        st.warning("Por favor, pega algún texto primero.")
        