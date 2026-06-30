from app.models import user
from sqlalchemy.orm import Session
from fastapi import FastAPI,Depends
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from app.schemas.schema import UserInfo
from app.services.risk_prediction import predicted_output
from app.db.database import engine,Base,get_db
from app.models.user import User
from app.auth.dependencies import get_current_user
from app.services.premium_pred import pred
from app.schemas.users import UserCreate,UserResponse
from app.models.predictions import Prediction
from app.schemas.predictions import PredictionCreate,PredictionResponse
from app.auth.login import router as auth_router
from app.auth.dependencies import role_required
Base.metadata.create_all(bind=engine)
app=FastAPI(title="Insurance premium predictor",version="1.0")
app.include_router(auth_router)
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
def prediction(user:UserInfo,) :
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
@app.post('/create_user',response_model=UserCreate)
def create_user(user:UserCreate,db:Session=Depends(get_db),current_user=Depends(role_required(["admin"]))):
    users=User(
        name=user.name,
        email=user.email,
        phone_no=user.phone_no,
        role=user.role or "users"
    )
    db.add(users)
    db.commit()
    db.refresh(users)
    return users    
@app.post(
    "/predict-premium",
    response_model=PredictionResponse
)
def predict_premium_endpoint(user_id:int,data:PredictionCreate,db:Session=Depends(get_db)):
    premium = float(pred(data)['premium_charges'])

    risk_score = int(min(100, premium / 1000))
    

    if risk_score < 30:

        risk_level = "LOW"

    elif risk_score < 70:

        risk_level = "MEDIUM"

    else:

        risk_level = "HIGH"

    validity_years = 5
    db_entry = Prediction(

        premium=premium,
        user_id=user_id,

        risk_score=risk_score,

        risk_level=risk_level,

        validity_years=validity_years

    )

    db.add(db_entry)

    db.commit()

    db.refresh(db_entry)


    return PredictionResponse(

        id=db_entry.id,

        premium=premium,

        risk_score=risk_score,

        risk_level=risk_level,

        validity_years=validity_years

    )