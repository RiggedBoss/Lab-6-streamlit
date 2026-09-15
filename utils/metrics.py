from __future__ import annotations

from typing import Any, Dict

import pandas as pd


def get_metric(df: pd.DataFrame) -> Dict[str, Any]:
    """Return summary metrics used by the dashboard."""
    total_students = int(len(df))
    average_cgpa = round(float(df["CGPA"].mean()), 2) if total_students else 0.0
    placement_rate = round(float(df["Placement Status"].eq("Placed").mean() * 100), 2) if total_students else 0.0

    return {
        "total_students": total_students,
        "average_cgpa": f"{average_cgpa:.2f}",
        "placement_status": f"{placement_rate:.2f}%",
    }
