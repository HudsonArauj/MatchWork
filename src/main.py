import streamlit as st 
from utils import generate_questions



st.markdown(
    f"""
    # WorkMatch
    """,
    unsafe_allow_html = True
)



pdf = st.file_uploader("Envie um arquivo PDF para analisarmos", type = ['pdf'])



materia_gerada = ''

button_gerar_materia = st.button(
    label = 'Gerar perguntas',
    type = 'primary'
)
st.title('Saídas geradas:')

if button_gerar_materia:
    
    if pdf:
        if pdf is None:
            st.markdown('Por favor, insira um arquivo PDF para continuar.')
        else:
            with st.spinner('Gerando perguntas...'):
                response = generate_questions(pdf)
                st.write(response)
        