from fastapi import FastAPI, Query
import joblib
from typing import List

app = FastAPI()

# Load the model
try:
    model = joblib.load('app/model.joblib')
    model_loaded = True
except FileNotFoundError:
    model_loaded = False

@app.get("/")
def root():
    if model_loaded:
        return {"message": "Welcome to Valorant Guesser"}
    else:
        return {"error": "Model file not found. Please check the path and try again."}

@app.get("/test")
def predict(input: List[float] = Query(..., description="List of input features for prediction")):
    if not model_loaded:
        return {"error": "Model not loaded. Prediction cannot be made."}
    
    try:
        # Convert input to 2D array for prediction
        prediction = model.predict([input])
        return {"prediction": int(prediction[0])}
    except Exception as e:
        return {"error": str(e)}
