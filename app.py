import streamlit as st
import google.generativeai as genai

# Configuración de la página
st.set_page_config(page_title="IA Resumidora", page_icon="📝")
st.title("📝 Mi Resumidor Mágico")

# Intentar conectar con la API
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
except:
    st.error("Error: Configura tu GOOGLE_API_KEY en los Secrets de Streamlit.")

text = st.text_area("Pega tu texto aquí:", height=200)

if st.button("Resumir ahora"):
    if text:
        try:
            # He cambiado el nombre a 'gemini-pro' que es el más estable para esta versión
            model = genai.GenerativeModel('gemini-pro')
            
            prompt = f"Resume este texto en español de forma clara en 3 frases. No repitas el original: {text}"
            
            response = model.generate_content(prompt)
            
            st.subheader("Resumen:")
            st.write(response.text)
        except Exception as e:
            # Si falla el 'gemini-pro', intentamos con el otro nombre por si acaso
            try:
                model = genai.GenerativeModel('gemini-1.5-flash-latest')
                response = model.generate_content(prompt)
                st.subheader("Resumen:")
                st.write(response.text)
            except:
                st.error(f"Lo siento, Google no responde. Error técnico: {e}")
    else:
        st.warning("Escribe algo primero.")
        