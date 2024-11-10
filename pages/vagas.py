import streamlit as st
from streamlit import session_state as ss
from src.utils import get_curriculos

st.title("Vagas")
if "files" not in ss:
    ss.files = None

job_description = st.text_area("Insira o job description aqui")
values = st.text_area("Insira os valores da empresa aqui")

if st.button("Criar vaga"):
    if job_description != "" and values != "" and job_description is not None and values is not None:
        st.write("Job description: ", job_description)
        st.write("Values: ", values)

        ss.job_description = job_description
        ss.values = values
        ss.files = get_curriculos(job_description, values)

if job_description=="" or values=="" or job_description is None or values is None:
    st.write("Preencha os campos para criar a vaga")
    ss.files = None

if ss.files is not None:
    for file in ss.files:    
        filepath = file.metadata["source"]
        with open(filepath, "rb") as f:
            btn = st.download_button(
            label=f"Download {filepath}",
            data=f,
            file_name=filepath,
        )