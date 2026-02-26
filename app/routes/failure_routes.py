from fastapi import APIRouter

from app.agents.failure_agent import (
    build_lightning_risk_model,
    detect_clusters,
    monthly_failure_forecast,
    station_risk_analysis,
)
from app.database import engine
from app.services.data_loader import FailureDataLoader

router = APIRouter(prefix="/failures", tags=["failures"])


@router.get("/station-risk")
def get_station_risk():
    df = FailureDataLoader.from_database(engine)
    result = station_risk_analysis(df)
    return result.to_dict(orient="records")


@router.get("/clusters")
def get_clusters(window_minutes: int = 5, threshold: int = 3):
    df = FailureDataLoader.from_database(engine)
    return detect_clusters(df, window_minutes=window_minutes, threshold=threshold)


@router.get("/forecast")
def get_monthly_forecast(steps: int = 3):
    df = FailureDataLoader.from_database(engine)
    return monthly_failure_forecast(df, steps=steps)


@router.get("/lightning-risk-model")
def get_lightning_risk_model():
    df = FailureDataLoader.from_database(engine)
    return build_lightning_risk_model(df)
