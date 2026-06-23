
import pandas as pd
import os
import joblib

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "../ml/model_store/model_pred.pkl")

premium_model = joblib.load(MODEL_PATH)
print("MODEL TYPE:", type(premium_model)) 

def pred(data):
    smoker = 1 if data.smoker.lower() == "yes" else 0
    df = pd.DataFrame([{

        "age": data.age,

        "bmi": data.bmi,

        "children": data.children,
        "sex":data.sex,

        "smoker": data.smoker,

        "region": data.region

    }])
    res=premium_model.predict(df)[0]
    return {
        "premium_charges":res
    }