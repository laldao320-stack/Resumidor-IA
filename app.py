import streamlit as st
import google.generativeai as genai

st.title("📝 Mi Resumidor Mágico")

# Configurar API
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

text = st.text_area("Pega tu texto aquí:")

if st.button("Resumir ahora"):
    if text:
        try:
            # El modelo que NUNCA falla en esta versión
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content(f"Resume en 3 frases: {text}")
            st.write(response.text)
        except Exception as e:
            st.error(f"Error: {e}")