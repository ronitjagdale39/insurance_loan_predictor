from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from schema.schema import UserInfo
from model.predict import predicted_output
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
