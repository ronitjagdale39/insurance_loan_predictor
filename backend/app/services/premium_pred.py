
import shap
import pandas as pd
import os
import joblib
import shap

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "../ml/models/model_pred.pkl")


premium_model = joblib.load(MODEL_PATH)
print("MODEL TYPE:", type(premium_model)) 
preprocessor = premium_model.named_steps["preprocess"]

model = premium_model.named_steps["models"]
explainer=shap.TreeExplainer(model)

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
    X=preprocessor.transform(df)
    shap_values = explainer(X)
    features=preprocessor.get_feature_names_out()
    explaination={}
    for feature,value in zip(features,shap_values.values[0]):
        clean_name = (

        feature

        .replace("cat__", "")

        .replace("num__", "")

    )
        if clean_name.startswith("sex_"):
            key="Sex"
        elif clean_name.startswith("smoker_"):
            key="Smoker"
        elif clean_name.startswith('region_'):
            key="Region"
        else:
            key=clean_name.capitalize()
        if key in explaination:
            explaination[key]+=round(float(value),2)
        else:
            explaination[key]=round(float(value),2)
    explaination_real={
        key:{
            "value":value,
            "effect":"positve" if value>0 else "negative"
        }
        for key,value in explaination.items()
    }   
    
    return {
        "premium_charges":res,
        "explaination":explaination_real,
    }