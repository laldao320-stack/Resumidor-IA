import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="IA Resumidora", page_icon="📝")
st.title("📝 Mi Resumidor Mágico")

# Configuración de la API
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("Falta la API Key en los Secrets")

text = st.text_area("Pega tu texto aquí:", height=200)

if st.button("Resumir ahora"):
    if text:
        try:
            # Forzamos el uso del modelo flash más reciente
            model = genai.GenerativeModel(model_name='gemini-1.5-flash')
            
            prompt = f"Resume este texto en español en 3 frases: {text}"
            response = model.generate_content(prompt)
            
            st.subheader("Resumen:")
            st.write(response.text)
        except Exception as e:
            st.error(f"Error de Google: {e}")
    else:
        st.warning("Escribe algo primero.")