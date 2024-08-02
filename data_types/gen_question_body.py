from pydantic import BaseModel


class GenQuestionBody(BaseModel):
    topic: str
    difficulty: str | None = None
