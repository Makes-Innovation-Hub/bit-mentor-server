from pydantic import BaseModel
from typing import List



class GenQuestionBody(BaseModel):
    topic: str
    difficulty: str | None = None


class QuestionRequest(BaseModel):
    subject: str
    difficulty: str
    answers_count: int


class QuestionResponse(BaseModel):
    question_text: str
    options: List[str]
    details: List[str]
    correct_answer: int

class AnswerCheckRequest(BaseModel):
    question: str
    user_answer: str

class OpenQuestionResponse(BaseModel):
    question:str
    answer:str
    explanation:str

