from __future__ import annotations

from pathlib import Path
from typing import Iterable, Tuple, Union

import pandas as pd


REQUIRED_COLUMNS = ["Department", "Semester", "CGPA", "Placement Status"]


def _ensure_sample_data() -> pd.DataFrame:
    data = {
        "Student ID": [101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120],
        "Department": ["CSE", "ECE", "ME", "CSE", "EEE", "IT", "CSE", "ECE", "ME", "IT", "CSE", "EEE", "IT", "CSE", "ECE", "ME", "IT", "CSE", "EEE", "ME"],
        "Semester": [1, 2, 3, 4, 5, 6, 7, 8, 1, 2, 3, 4, 5, 6, 7, 8, 1, 2, 3, 4],
        "CGPA": [8.2, 7.8, 7.4, 8.7, 6.9, 8.1, 9.1, 7.6, 8.4, 7.9, 8.8, 7.2, 8.0, 9.3, 7.5, 7.1, 8.5, 8.9, 6.8, 7.7],
        "Placement Status": ["Placed", "Placed", "Not Placed", "Placed", "Not Placed", "Placed", "Placed", "Not Placed", "Placed", "Placed", "Placed", "Not Placed", "Placed", "Placed", "Not Placed", "Not Placed", "Placed", "Placed", "Not Placed", "Placed"],
    }
    return pd.DataFrame(data)


def load_student_data(source: Union[str, Path, object]) -> pd.DataFrame:
    """Load student data from a CSV path or uploaded file-like object."""
    if hasattr(source, "read"):
        return pd.read_csv(source)

    path = Path(source)
    if path.exists():
        return pd.read_csv(path)

    fallback_file = Path("student_dashboard/data/students.csv")
    if fallback_file.exists():
        return pd.read_csv(fallback_file)

    return _ensure_sample_data()


def validate_columns(df: pd.DataFrame, required: Iterable[str] = REQUIRED_COLUMNS) -> Tuple[bool, list[str]]:
    missing = [col for col in required if col not in df.columns]
    return (len(missing) == 0, missing)
