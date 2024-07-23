from pydantic import BaseModel
from typing import List


class QuestionRequest(BaseModel):
    subject: str
    difficulty: str
    answers_count: int


class QuestionResponse(BaseModel):
    question_text: str
    options: List[str]
    details: List[str]
    correct_answer: int
