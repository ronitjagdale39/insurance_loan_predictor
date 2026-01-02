import pickle
import os
import pandas as pd
# loading the model

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "model", "model.pkl")

with open(MODEL_PATH,'rb') as f:
    model=pickle.load(f)
def predicted_output(input_info:dict) :
    df=pd.DataFrame([input_info])
    prediction_data=model.predict(df)[0]
    return {
        'prediction':prediction_data
        
    }
           