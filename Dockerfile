FROM ghcr.io/astral-sh/uv:python3.10-bookworm-slim

WORKDIR /app

# Arguments passés lors du build pour l'authentification DagsHub
ARG MLFLOW_TRACKING_URI="https://dagshub.com/AdrienAssd/mlflow-projet.mlflow"
ARG MLFLOW_TRACKING_USERNAME
ARG MLFLOW_TRACKING_PASSWORD

ENV MLFLOW_TRACKING_URI=${MLFLOW_TRACKING_URI}
ENV MLFLOW_TRACKING_USERNAME=${MLFLOW_TRACKING_USERNAME}
ENV MLFLOW_TRACKING_PASSWORD=${MLFLOW_TRACKING_PASSWORD}

# Installation des dépendances avec uv
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

ENV PATH="/app/.venv/bin:$PATH"

# Téléchargement de la dernière version du modèle depuis DagsHub
COPY download_model.py .
RUN python download_model.py

# Suppression du token sensible de l'image finale
ENV MLFLOW_TRACKING_PASSWORD=""

# Copie de l'application FastAPI
COPY app.py .

EXPOSE 8000
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]