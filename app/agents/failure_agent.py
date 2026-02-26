from datetime import timedelta

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from statsmodels.tsa.arima.model import ARIMA


def station_risk_analysis(df: pd.DataFrame) -> pd.DataFrame:
    grouped = df.groupby("location", dropna=False).agg(
        failure_count=("failure_on", "count"),
        avg_duration=("duration", "mean"),
    ).reset_index()

    grouped["avg_duration"] = grouped["avg_duration"].fillna(0)
    grouped["risk_score"] = grouped["failure_count"] * 0.6 + grouped["avg_duration"] * 0.4
    grouped["action_required"] = np.where(grouped["risk_score"] >= grouped["risk_score"].quantile(0.8), "Immediate", "Monitor")

    return grouped.sort_values("risk_score", ascending=False)


def detect_clusters(df: pd.DataFrame, window_minutes: int = 5, threshold: int = 3) -> list[dict]:
    ordered = df.sort_values("failure_on").dropna(subset=["failure_on"])  # type: ignore[arg-type]
    clusters: list[dict] = []

    for i in range(len(ordered)):
        start = ordered.iloc[i]["failure_on"]
        end = start + timedelta(minutes=window_minutes)
        window = ordered[(ordered["failure_on"] >= start) & (ordered["failure_on"] <= end)]

        if len(window) >= threshold:
            clusters.append(
                {
                    "start_time": start,
                    "count": int(len(window)),
                    "locations": sorted(window["location"].dropna().unique().tolist()),
                    "probable_cause": infer_probable_cause(window),
                }
            )
    return clusters


def infer_probable_cause(window_df: pd.DataFrame) -> str:
    if "cause" in window_df.columns and not window_df["cause"].dropna().empty:
        return str(window_df["cause"].mode().iloc[0])
    if "lightning_index" in window_df.columns and window_df["lightning_index"].mean() > 0.7:
        return "Weather/Lightning"
    return "Unknown"


def monthly_failure_forecast(df: pd.DataFrame, steps: int = 3, arima_order: tuple[int, int, int] = (2, 1, 2)) -> dict:
    monthly_series = (
        df.dropna(subset=["failure_on"])
        .set_index("failure_on")
        .resample("MS")
        .size()
        .astype(float)
    )

    if len(monthly_series) < 6:
        raise ValueError("Need at least 6 monthly observations for a stable 3-month forecast.")

    model = ARIMA(monthly_series, order=arima_order)
    model_fit = model.fit()
    forecast = model_fit.forecast(steps=steps)

    return {
        "history": {idx.strftime("%Y-%m"): float(val) for idx, val in monthly_series.items()},
        "forecast": {idx.strftime("%Y-%m"): float(max(val, 0)) for idx, val in forecast.items()},
    }


def build_lightning_risk_model(df: pd.DataFrame) -> dict:
    working = df.copy()
    working["month"] = working["failure_on"].dt.month
    working["is_monsoon"] = working["month"].isin([6, 7, 8, 9]).astype(int)

    location_counts = working.groupby("location")["id"].transform("count")
    working["station_failure_density"] = location_counts

    if "lightning_index" not in working.columns:
        working["lightning_index"] = 0.0

    threshold = working["duration"].fillna(0).quantile(0.75)
    working["is_high_risk"] = (working["duration"].fillna(0) >= threshold).astype(int)

    features = ["lightning_index", "is_monsoon", "station_failure_density"]
    x = working[features].fillna(0)
    y = working["is_high_risk"]

    model = Pipeline(
        [
            ("scaler", StandardScaler()),
            ("clf", LogisticRegression(max_iter=1000)),
        ]
    )
    model.fit(x, y)

    coefficients = model.named_steps["clf"].coef_[0]
    importance = dict(zip(features, [float(c) for c in coefficients]))

    return {
        "features": features,
        "duration_threshold": float(threshold),
        "feature_importance": importance,
        "intercept": float(model.named_steps["clf"].intercept_[0]),
    }
