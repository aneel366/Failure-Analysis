from pathlib import Path

import pandas as pd


class FailureDataLoader:
    """Centralized helpers for loading and normalizing failure data."""

    @staticmethod
    def from_database(engine) -> pd.DataFrame:
        df = pd.read_sql("SELECT * FROM failures", con=engine)
        return FailureDataLoader.normalize(df)

    @staticmethod
    def from_csv(path: str | Path) -> pd.DataFrame:
        df = pd.read_csv(path)
        return FailureDataLoader.normalize(df)

    @staticmethod
    def normalize(df: pd.DataFrame) -> pd.DataFrame:
        output = df.copy()
        if "failure_on" in output.columns:
            output["failure_on"] = pd.to_datetime(output["failure_on"], errors="coerce")
        if "repaired_on" in output.columns:
            output["repaired_on"] = pd.to_datetime(output["repaired_on"], errors="coerce")

        if "duration" not in output.columns and {"failure_on", "repaired_on"}.issubset(output.columns):
            duration_hours = (output["repaired_on"] - output["failure_on"]).dt.total_seconds() / 3600
            output["duration"] = duration_hours.fillna(0)

        if "lightning_index" not in output.columns:
            output["lightning_index"] = 0.0

        return output
