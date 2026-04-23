import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Resumidor IA", page_icon="📝")
st.title("📝 Mi Resumidor Mágico")

# Conexión segura
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("Configura la API Key en Streamlit")

text = st.text_area("Pega tu texto aquí:", height=200)

if st.button("Resumir ahora"):
    if text:
        try:
            # Este es el nombre "universal" que debería aceptar
            model = genai.GenerativeModel('gemini-pro')
            
            prompt = f"Resume en español y en 3 frases: {text}"
            response = model.generate_content(prompt)
            
            st.subheader("Resumen:")
            st.write(response.text)
        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.warning("Escribe algo primero.")

