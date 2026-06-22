
from pydantic import BaseModel


class PredictionCreate(BaseModel):
    age: int
    sex: str
    bmi: float
    children: int
    smoker: str
    region: str


class PredictionResponse(BaseModel):
    id: int
    premium: float
    risk_score: int
    risk_level: str
    validity_years: int

    class Config:
        from_attributes = True