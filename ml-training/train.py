import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
import pickle
from sklearn.ensemble import RandomForestClassifier

# Load data
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
df = pd.read_csv(os.path.join(BASE_DIR, 'insurance-2.csv'))

# Feature engineering
df['bmi'] = df['weight'] / df['height']**2

tier_1_cities = ["Mumbai", "Delhi", "Bangalore", "Chennai", "Kolkata", "Hyderabad", "Pune"]
tier_2_cities = [
    "Jaipur", "Chandigarh", "Indore", "Lucknow", "Patna", "Ranchi", "Visakhapatnam", "Coimbatore",
    "Bhopal", "Nagpur", "Vadodara", "Surat", "Rajkot", "Jodhpur", "Raipur", "Amritsar", "Varanasi",
    "Agra", "Dehradun", "Mysore", "Jabalpur", "Guwahati", "Thiruvananthapuram", "Ludhiana", "Nashik",
    "Allahabad", "Udaipur", "Aurangabad", "Hubli", "Belgaum", "Salem", "Vijayawada", "Tiruchirappalli",
    "Bhavnagar", "Gwalior", "Dhanbad", "Bareilly", "Aligarh", "Gaya", "Kozhikode", "Warangal",
    "Kolhapur", "Bilaspur", "Jalandhar", "Noida", "Guntur", "Asansol", "Siliguri"
]

def city_tier(city):
    if city in tier_1_cities:
        return 1
    elif city in tier_2_cities:
        return 2
    else:
        return 3
df['city_tier'] = df['city'].apply(city_tier)  

def age_group(age) -> str:
    if age < 25:
        return 'young'
    elif age < 45:
        return 'adult'
    elif age < 60:
        return 'middle-age'
    return 'old'
df['age_group'] = df['age'].apply(age_group)  

def lifestyle(row) -> str:
    if row['smoker'] and row['bmi'] > 30:
        return 'high'
    elif row['smoker'] and row['bmi'] > 27:
        return 'medium'
    else:
        return 'low'
df['lifestyle'] = df.apply(lifestyle, axis=1) 

# Splitting dataset
X = df[['bmi', 'income_lpa', 'occupation', 'city_tier', 'lifestyle', 'age_group']]
y = df['insurance_premium_category']

categorical_data = ['occupation', 'lifestyle', 'age_group', 'city_tier']
numerical_data = ['bmi', 'income_lpa']               
preprocessing = ColumnTransformer([
    ('t1', OneHotEncoder(), categorical_data),
    ('t2', 'passthrough', numerical_data)
])

pipeline = Pipeline(steps=[
    ('preprocess', preprocessing),
    ('fc', RandomForestClassifier(random_state=42))
])

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33)
pipeline.fit(X_train, y_train)

# Save the trained model to model.pkl
# Note: Usually we output to backend/app/ml/model_store/model.pkl
model_output_path = os.path.join(BASE_DIR, '..', 'backend', 'app', 'ml', 'models', 'model.pkl')
with open(model_output_path, 'wb') as f:
    pickle.dump(pipeline, f)

print(f"Model trained and saved to {model_output_path} successfully!")
