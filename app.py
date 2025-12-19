from fastapi import FastAPI
from fastapi.responses import JSONResponse
app=FastAPI()
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