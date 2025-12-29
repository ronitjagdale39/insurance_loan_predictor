from pydantic import BaseModel,field_validator,computed_field,Field
from typing import Annotated,Optional,Literal
from config.city_tier import tier_1_cities,tier_2_cities
class UserInfo(BaseModel):
    age:Annotated[int,Field(...,description="enter you name here :",examples=[19])]
    weight: Annotated[float, Field(..., gt=0, description='Weight of the user')]
    height: Annotated[float, Field(..., gt=0, lt=2.5, description='Height of the user')]
    income_lpa: Annotated[float, Field(..., gt=0, description='Annual salary of the user in lpa')]
    smoker: Annotated[bool, Field(..., description='Is user a smoker')]
    city: Annotated[str, Field(..., description='The city that the user belongs to')]
    occupation: Annotated[Literal['retired', 'freelancer', 'student', 'government_job',
       'business_owner', 'unemployed', 'private_job'], Field(..., description='Occupation of the user')]
    # normalizing the city input as per our model
    @field_validator('city')
    @classmethod
    def Valid(cls,v:str):
        v=v.strip().title()
        return v
    # computed field that will be calculated the feature engineered columns
    @computed_field
    @property
    def bmi(self)->float:
        bmi=round((self.weight/self.height**2),2)
        return bmi
    @computed_field
    @property
    def city_tier(self)->int:
        if self.city in tier_1_cities:
            return 1
        elif self.city in tier_2_cities:
            return 2
        return 3
    @computed_field
    @property
    def lifestyle(self)->str:
        if self.smoker and self.bmi > 30:
            return "high"
        elif self.smoker or self.bmi > 27:
            return "medium"
        else:
            return "low"
    @computed_field
    @property
    def age_group(self)->str:
        if self.age < 25:
            return "young"
        elif self.age < 45:
            return "adult"
        elif self.age < 60:
            return "middle_aged"
        return "senior"    
    