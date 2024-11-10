import streamlit as st
from streamlit import session_state as ss
from src.utils import generate_questions, upload_cv

if "questions" not in ss:
    ss.questions = None

uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None and ss.questions is None:
    basepath = "data/curriculos/"
    with open(basepath+uploaded_file.name, "wb") as f:
        f.write(uploaded_file.getvalue())
    ss.questions = generate_questions(basepath+uploaded_file.name)
elif uploaded_file is None:
    st.write("Upload a file")
    ss.questions = None

if ss.questions is not None:
    question1 = st.text_area(ss.questions.question1)
    question2 = st.text_area(ss.questions.question2)
    question3 = st.text_area(ss.questions.question3)

    if st.button("Enviar respostas"):
        if question1 != "" and question2 != "" and question3 != "":
            text = "\n".join([question1, question2, question3])
            path = "data/curriculos/"+uploaded_file.name
            upload_cv(text, path)
            st.write("Respostas enviadas")
        else:
            st.write("Preencha todos os campos")