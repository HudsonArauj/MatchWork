from dotenv import load_dotenv

from groq import Groq
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from fastapi import FastAPI, HTTPException

from src.schemas import Subjetivas, InputProfile
from src.utils import generate_questions, generate_profile
#
import nest_asyncio  # noqa: E402
nest_asyncio.apply()

load_dotenv()

app = FastAPI(
    title = "MatchWork",
    version = "0.1",
    description = "The API for your best job opportunities and contracts",
)


@app.post("/question")
async def get_question(path: str) -> Subjetivas:
    try:
        result = generate_questions(path)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/get_profile")
async def get_profile(input: InputProfile) -> str:
    try:
        profile = generate_profile(input)
        return profile
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

