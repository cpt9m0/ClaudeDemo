"""Load and clean the Financial_Sample dataset."""

from pathlib import Path

import pandas as pd
import streamlit as st

DATA_PATH = Path(__file__).resolve().parent.parent / "Financial_Sample.xlsx"

MEASURES = {
    "Gross Sales": "Gross Sales",
    "Net Sales": "Sales",
    "Discounts": "Discounts",
    "COGS": "COGS",
    "Profit": "Profit",
    "Units Sold": "Units Sold",
}

DIMENSIONS = ["Segment", "Country", "Product", "Discount Band"]


@st.cache_data
def load_data() -> pd.DataFrame:
    df = pd.read_excel(DATA_PATH)
    df.columns = [c.strip() for c in df.columns]
    df["Discount Band"] = df["Discount Band"].fillna("None")
    df["Profit Margin"] = df["Profit"] / df["Sales"]
    df["Discount Rate"] = df["Discounts"] / df["Gross Sales"]
    df["Date"] = pd.to_datetime(df["Date"])
    return df
