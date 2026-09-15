from __future__ import annotations

import plotly.express as px
import pandas as pd


def department_distribution(df: pd.DataFrame):
    counts = df["Department"].value_counts().reset_index()
    counts.columns = ["Department", "Count"]
    return px.pie(counts, names="Department", values="Count", title="Students by Department")


def average_cgpa_by_department(df: pd.DataFrame):
    summary = df.groupby("Department", as_index=False)["CGPA"].mean()
    summary.columns = ["Department", "Average CGPA"]
    return px.bar(summary, x="Department", y="Average CGPA", color="Department", title="Average CGPA by Department")


def placement_distribution(df: pd.DataFrame):
    counts = df["Placement Status"].value_counts().reset_index()
    counts.columns = ["Placement Status", "Count"]
    return px.bar(counts, x="Placement Status", y="Count", color="Placement Status", title="Placement Status")
