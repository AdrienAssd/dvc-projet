import os
import glob
import mlflow.sklearn
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="MLflow Model API")

# Localise et charge le modèle téléchargé lors du build Docker
model_paths = glob.glob("./model/**/MLmodel", recursive=True)
if not model_paths:
    raise RuntimeError("Fichier MLmodel introuvable dans ./model")

model_dir = os.path.dirname(model_paths[0])
model = mlflow.sklearn.load_model(model_dir)


class PredictionRequest(BaseModel):
    # Liste de vecteurs de caractéristiques (64 valeurs par échantillon pour load_digits)
    features: list[list[float]]


@app.post("/predict")
def predict(request: PredictionRequest):
    predictions = model.predict(request.features)
    return {"predictions": predictions.tolist()}