if st.button("Resumir ahora"):
    if text:
        try:
            # Prueba con este nombre exacto que incluye 'models/'
            model = genai.GenerativeModel('models/gemini-1.5-flash')
            
            prompt = f"Resume en español y en 3 frases claras: {text}"
            response = model.generate_content(prompt)
            
            st.subheader("Resumen:")
            st.write(response.text)
        except Exception as e:
            st.error(f"Error: {e}")