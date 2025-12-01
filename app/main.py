from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import joblib
import pandas as pd
import os

app = FastAPI()

# 1. Load Artifacts
model_path = "models/model.pkl"
scaler_path = "models/scaler.pkl"

if not os.path.exists(model_path):
    raise RuntimeError("Model not found. Run 'dvc repro' first.")

model = joblib.load(model_path)
scaler = joblib.load(scaler_path)

# 2. Input Schema 
class HouseFeatures(BaseModel):
    Square_Feet: int
    Bedrooms: int
    Bathrooms: int
    Location_Score: int
    Distance_to_City_km: float
    Year_Built: int

# 3. Mount Static Folder (Serves CSS/JS)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# 4. Root Endpoint (Serves HTML)
@app.get("/")
def read_root():
    return FileResponse('app/static/index.html')

# 5. Prediction Endpoint
@app.post("/predict")
def predict_price(features: HouseFeatures):
    try:
        # Feature Engineering
        house_age = 2024 - features.Year_Built

        # Prepare Data
        data = pd.DataFrame([{
            'Square_Feet': features.Square_Feet,
            'Bedrooms': features.Bedrooms,
            'Bathrooms': features.Bathrooms,
            'Location_Score': features.Location_Score,
            'Distance_to_City_km': features.Distance_to_City_km,
            'House_Age': house_age
        }])

        # Scale & Predict
        scaled_data = scaler.transform(data)
        prediction = model.predict(scaled_data)

        return {"predicted_price": round(float(prediction[0]), 2)}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))