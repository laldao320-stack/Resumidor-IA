import streamlit as st
import google.generativeai as genai

# Título de la web
st.title("📝 Mi Resumidor Mágico")

# Configurar la API directamente
if "GOOGLE_API_KEY" in st.secrets:
    # Usamos el nombre del modelo sin rutas raras
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.error("Configura la API Key en Streamlit.")

text = st.text_area("Pega tu texto aquí:")

if st.button("Resumir ahora"):
    if text:
        try:
            # Pedimos el resumen directamente
            response = model.generate_content(f"Resume en 3 frases: {text}")
            st.success("¡Hecho!")
            st.write(response.text)
        except Exception as e:
            st.error(f"Error: {e}")