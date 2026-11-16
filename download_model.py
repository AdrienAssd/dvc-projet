import os
import mlflow
from mlflow.tracking import MlflowClient

# URI de suivi de votre dépôt DagsHub
TRACKING_URI = os.getenv(
    "MLFLOW_TRACKING_URI",
    "https://dagshub.com/AdrienAssd/mlflow-projet.mlflow"
)
mlflow.set_tracking_uri(TRACKING_URI)

client = MlflowClient()

# Récupère automatiquement le nom du modèle enregistré dans l'onglet Models
registered_models = client.search_registered_models()
if not registered_models:
    raise RuntimeError("Aucun modèle trouvé dans le Model Registry DagsHub.")

model_name = registered_models[0].name
model_uri = f"models:/{model_name}/latest"

print(f"Téléchargement de {model_uri}...")
mlflow.artifacts.download_artifacts(artifact_uri=model_uri, dst_path="./model")
print(f"Modèle '{model_name}' téléchargé avec succès dans ./model !")