from fastapi import FastAPI, HTTPException
import mlflow
import mlflow.sklearn
import pandas as pd
import numpy as np
app = FastAPI(title="Forest Cover Type Prediction API")
def load_latest_model():
    mlflow.set_tracking_uri("http://mlflow:5000")
    client = mlflow.tracking.MlflowClient()
    models = client.search_model_versions("name='forest_cover_model'")
    if not models:
        raise HTTPException(status_code=404, detail="No model found")
    
    latest_model = models[0]
    model_uri = f"runs:/{latest_model.run_id}/forest_cover_model"
    
    return mlflow.sklearn.load_model(model_uri)

@app.post("/predict")
async def predict(data: dict):
    try:
        df = pd.DataFrame([data])
        
        model = load_latest_model()
        
        prediction = model.predict(df)
        
        return {"prediction": int(prediction[0])}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    return {"message": "Forest Cover Type Prediction API"}
