from pydantic import BaseModel
from typing import List

class ChoiceBase(BaseModel):
    choice_text: str
    is_correct: bool

class ChoiceResponse(ChoiceBase):
    id: int
    question_id: int

    class Config:
        orm_mode = True

class QuestionBase(BaseModel):
    question_text: str
    choices: List[ChoiceBase]

class QuestionResponse(BaseModel):
    id: int
    question_text: str

    class Config:
        orm_mode = True
