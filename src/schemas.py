from pydantic import BaseModel, Field
from typing import List

class Activity(BaseModel):
    """
    A detailed description of an activity and the role of a candidate in them.
    """
    description: str = Field(description = "What is the activity")
    role: str = Field(description="Role the candidate served on the acitivity")

class Topics(BaseModel):
    """
    Lists of maybe important topics for a candidate
    """
    experiences: List[Activity]
    activities: List[Activity]
    projects: List[Activity]

class Question(BaseModel):
    question: str = Field(description="Question for the candidate")
    target: List[str] = Field(description="topics the question expects to cover.")


class Subjetivas(BaseModel):
    question1: Question
    question2: Question
    question3: Question


class RespostasSub(BaseModel):
    questao: Question
    resposta: str

class InputProfile(BaseModel):
    inputAnalyse: List[RespostasSub]

