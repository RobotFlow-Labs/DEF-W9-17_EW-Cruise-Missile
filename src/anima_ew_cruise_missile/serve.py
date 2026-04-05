from __future__ import annotations

from fastapi import FastAPI
from pydantic import BaseModel, Field

from .infer import run_scenario


app = FastAPI(title="anima-ew-cruise-missile", version="0.1.0")


class PredictRequest(BaseModel):
    config: str = Field(default="configs/default.toml")
    scenario: str = Field(default="adaptive")
    episodes: int = Field(default=20, ge=1, le=2000)
    seed: int = Field(default=42)


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.get("/ready")
def ready() -> dict:
    return {"ready": True}


@app.post("/predict")
def predict(req: PredictRequest) -> dict:
    return run_scenario(req.config, req.scenario, req.episodes, req.seed)
