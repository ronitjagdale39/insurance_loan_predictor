from app.models import user
from sqlalchemy.orm import Session
from fastapi import FastAPI,Depends
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from app.schemas.schema import UserInfo
from app.services.risk_prediction import predicted_output
from app.db.database import engine,Base,get_db
from app.models.user import User
from app.core.security import hashed_password
from app.auth.dependencies import get_current_user
from app.services.premium_pred import pred
from app.routers.verify_email import router as email_router
from app.schemas.users import UserCreate,UserResponse
from app.models.predictions import Prediction
from app.schemas.predictions import PredictionCreate,PredictionResponse
from app.auth.login import router as auth_router
from app.auth.dependencies import role_required
from app.routers.refresh import router as refresh_router
from app.routers.logout import router as logout_router
from app.routers.chnge_pass import router as change_pass_router
from app.routers.reset_password import router as reset_password_router
from app.routers.forgot_password import router as forgot_password_router
Base.metadata.create_all(bind=engine)
app=FastAPI(title="Insurance premium predictor",version="1.0")
app.include_router(auth_router)
app.include_router(reset_password_router)
app.include_router(forgot_password_router)
app.include_router(change_pass_router)
app.include_router(logout_router)
app.include_router(refresh_router)
app.include_router(email_router)
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
def prediction(user:UserInfo,current_user=Depends(role_required(["admin","agent","customers"]))) :
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
@app.post('/create_user',response_model=UserResponse)
def create_user(user:UserCreate,db:Session=Depends(get_db),current_user=Depends(role_required(["admin"]))):
    users = User(
    name=user.name,
    email=user.email,
    phone_no=user.phone_no,
    hashed_password=hashed_password(user.password),
    role=user.role
    )
    db.add(users)
    db.commit()
    db.refresh(users)
    return users    
@app.post("/predict-premium", response_model=PredictionResponse)
def predict_premium_endpoint(
    data: PredictionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(role_required(['admin','agent','customer']))
):
    prediction=pred(data)
    print(f"prediction=={prediction}")
    premium = float(prediction['premium_charges'])
    explaination=prediction['explaination']

    risk_score = 0

    if data.age > 50:
        risk_score += 20

    if data.bmi > 30:
        risk_score += 20

    if data.smoker == "yes":
        risk_score += 40

    if data.children > 3:
        risk_score += 10

    if data.region == "high_cost_region":
        risk_score += 10

    if risk_score <= 30:
        risk_level = "LOW"
    elif risk_score <= 60:
        risk_level = "MEDIUM"
    else:
        risk_level = "HIGH"

    db_entry = Prediction(
        premium=premium,
        user_id=current_user.id,  
        risk_score=risk_score,
        risk_level=risk_level,
        validity_years=5,

    )

    db.add(db_entry)
    db.commit()
    db.refresh(db_entry)

    return PredictionResponse(
        premium=premium,
        id=db_entry.id,
        risk_score=risk_score,
        risk_level=risk_level,
        validity_years=5,
        explanation=explaination
    )