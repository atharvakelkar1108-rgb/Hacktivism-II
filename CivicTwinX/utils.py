import joblib
import numpy as np
from sklearn.ensemble import RandomForestRegressor

def train_model():
    import pandas as pd
    df = pd.read_csv("data/civic_data.csv")
    X = df[['traffic', 'pollution', 'power_usage', 'water_use', 'complaints']]
    y = df['stress_index']
    model = RandomForestRegressor()
    model.fit(X, y)
    joblib.dump(model, "model.pkl")

def load_model():
    return joblib.load("model.pkl")

def predict(data):
    model = load_model()
    prediction = model.predict([data])
    return float(prediction[0])
