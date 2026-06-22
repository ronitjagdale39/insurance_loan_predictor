from sqlalchemy.orm import Session
from fastapi import FastAPI,Depends
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from app.schemas.schema import UserInfo
from app.services.prediction import predicted_output
from app.db.database import engine,Base,get_db
from app.models.user import User
from app.schemas.users import UserCreate,UserResponse


Base.metadata.create_all(bind=engine)

app=FastAPI(title="Insurance premium predictor",version="1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
@app.get('/')
def home():
    return {
        'message':'insurance_loan_predictor'
    }
@app.get('/status')
def status():
    return {
        'status':'OK'
    }
@app.post('/prediction')    
def prediction(user:UserInfo) :
    input_info={
        'bmi':user.bmi,
        'age_group':user.age_group,
        'city_tier':user.city_tier,
        'lifestyle':user.lifestyle,
        'income_lpa':user.income_lpa,
        'occupation':user.occupation
    }
    try:
        prediction_out=predicted_output(input_info)
        return JSONResponse(status_code=200,content=prediction_out)
    except Exception as e:
        return JSONResponse(status_code=500,content=str(e))   
@app.post('/create_user')
def create_user(user:UserCreate,db:Session=Depends(get_db)):
    users=User(
        name=user.name,
        email=user.email,
        phone_no=user.phone_no
    )
    db.add(users)
    db.commit()
    db.refresh(users)
    return users    
    
