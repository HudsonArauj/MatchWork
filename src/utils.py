##### LLAMAPARSE #####
from llama_parse import LlamaParse
from dotenv import load_dotenv

from groq import Groq
from langchain_groq import ChatGroq

from src.schemas import Topics, Subjetivas, InputProfile

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

import nest_asyncio  # noqa: E402
nest_asyncio.apply()

llm = ChatGroq(temperature=0.3, model_name="llama-3.1-70b-versatile")

def extract_cv(path):
    parsingInstructionsInterviewer = """
        O documento a seguir é um currículode um possível candidato em busca de vagas.
        No documento, haverá uma seção contendo as Experiências do candidato e outra contendo as Atividades Extracurriculares dele.
        Extraia o que conseguir dessas partes e também as informações pessoais do candidato.
    """

    llamaparse = LlamaParse(parsing_instruction=parsingInstructionsInterviewer, result_type="markdown")
    parsed_result = llamaparse.get_json_result(path)

    content_curriculo = "\n".join([md["md"] for md in parsed_result[0]['pages']])

    return content_curriculo

def generate_questions(path):

    messages = [
        (
            "system",
            "You are a helpful assistant that hepls identify a candidate's experience, activities and projects based on the following markdown text: {curriculum}. ",
        ),
        (
            "system",
            "Here are the topics:"
        )
    ]
    prompt = ChatPromptTemplate.from_messages(messages)

    chat_model = llm.with_structured_output(Topics)

    chain_structured = prompt | chat_model
    response = chain_structured.invoke({"curriculum":extract_cv(path)})
    
    messages = [
    (
        "system",
        """You are a helpful assistant that works in the People Departament and must devise meaninful questions based on a candidate's experience, activities and projects.
           Your main role here is to identify how the candidate responds to different forms of interations, the commitement of the candidate to the activity, and what motivated him for the activities.
           You are to create 3 questions based on the following:
           {activities}
           {experiences}
           {projects}

           Remenber, choose questions for topics with the most importance based on leadership, independence, proactivity, personal relations and challenge overcoming.
           Also, add the topics the question expects to cover.
        """,
    ),
    ]

    prompt = ChatPromptTemplate.from_messages(messages)

    chain_structured = prompt | llm.with_structured_output(Subjetivas)

    activities = response.activities
    experiences = response.experiences
    projects = response.projects


    ai_msg = chain_structured.invoke({
        "activities": activities,
        "experiences": experiences,
        "projects": projects
    })
    return ai_msg


def generate_profile(input: InputProfile)-> str:

    llm_answers = ChatGroq(temperature=0.3, model_name="llama-3.1-70b-versatile")

    messages = [
        (
            "system",
            """You are a helpful assistant that works in the People Departament and must analyse the answers of a candidate to a key question, and summarize their ability in: leadership, boldness, commitment, motivation and interest.
            Your main role here is to classify candidate response according the different forms of response he gives for each question.
            
            The question given to the candidate: {question}
            The answer he gave: {answer}
            What the question tried to probe: {target}

            You must give a strict and detailed analyse of the candidate based on this answer and mainly the target aspect of the question, but keep note of the other qualities that may be present on the answer.
            """,
        ),
    ]

    prompt = ChatPromptTemplate.from_messages(messages)

    chain_structured = prompt | llm_answers | StrOutputParser() 

    input = input.inputAnalyse
    input1 = input[0]

    analise1 = chain_structured.invoke(
        {"question": input1.questao.question,
        "answer": input1.resposta,
        "target": input1.questao.target}
    )

    input2 = input[1]
    analise2 = chain_structured.invoke(
        {"question": input2.questao.question,
        "answer": input2.resposta,
        "target": input2.questao.target}
    )

    input3 = input[2]
    analise3 = chain_structured.invoke(
        {"question": input3.questao.question,
        "answer": input3.resposta,
        "target": input3.questao.target}
    )

    messages = [
    (
        "system",
        """
           Right now, you are a profile reviewer for the department of Human Resources, focused on hiring. 
           You will recieve 3 analyses of answers given by the candidate, detailing the capabilities shown by them in each question, your role is to create a professional profile for the candidate, which must describe: 
           - the possible roles the candidate is apt to perform, meaning manager, analist, developer, assistant, head of area, supervisor, and others.
           - Their capabilities in soft skills
           - The main traces of personality
           
           The question analyses of the candidate were: {analyses}
        """,
    ),
    ]

    prompt = ChatPromptTemplate.from_messages(messages)

    chain_analyse = prompt | llm_answers | StrOutputParser()

    ai_msg = chain_analyse.invoke({
        "analyses": "\n\n".join([analise1, analise2, analise3])
    })

    return ai_msg