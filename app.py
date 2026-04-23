import streamlit as st
import google.generativeai as genai

# 1. Configuración básica
st.set_page_config(page_title="Resumidor IA", page_icon="📝")
st.title("📝 Mi Resumidor Mágico")

# 2. Conexión con la llave
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
except Exception as e:
    st.error("Error con la API Key en Streamlit Cloud")

# 3. Entrada de texto
text = st.text_area("Pega tu texto aquí:", height=200)

# 4. Botón y Magia
if st.button("Resumir ahora"):
    if text:
        try:
            # Usamos el modelo más estándar del mundo
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            # Instrucción súper clara
            prompt = f"Resume este texto en español en 3 frases cortas: {text}"
            
            # Generar contenido
            response = model.generate_content(prompt)
            
            # Mostrar resultado
            st.subheader("Resumen:")
            st.write(response.text)
            
        except Exception as e:
            st.error(f"Error técnico de Google: {e}")
    else:
        st.warning("Escribe algo primero.")
        
