import pickle
import pandas as pd
# loading the model
filename='model/model.pkl'
with open(filename,'rb') as f:
    model=pickle.load(f)
def predicted_output(input_info:dict) :
    df=pd.DataFrame([input_info])
    prediction=model.predict(df)[0]
    return {
        'prediction':prediction
        
    }
           