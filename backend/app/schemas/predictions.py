
from pydantic import BaseModel
from typing import Dict

class PredictionCreate(BaseModel):
    age: int
    sex: str
    bmi: float
    children: int
    smoker: str
    region: str
class Explaination(BaseModel):
    value:float
    effect:str

class PredictionResponse(BaseModel):
    id: int
    premium: float
    risk_score: int
    risk_level: str
    validity_years: int
    explanation: Dict[str, Explaination]

    class Config:
        from_attributes = True