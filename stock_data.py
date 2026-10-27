
import os
import requests
import pandas as pd
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

API_URL = "https://www.alphavantage.co/query"


def get_api_key():
    # First, check the local .env environment variable
    api_key = os.getenv("ALPHA_VANTAGE_API_KEY")

    if api_key:
        return api_key

    # If deployed, try Streamlit Cloud Secrets
    try:
        return st.secrets["ALPHA_VANTAGE_API_KEY"]
    except Exception:
        return None


@st.cache_data(ttl=300)
def get_stock_data(symbol):
    api_key = get_api_key()

    if not api_key:
        raise ValueError(
            "API key missing. Configure .env or Streamlit Secrets."
        )

    params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": symbol,
        "outputsize": "compact",
        "apikey": api_key
    }

    response = requests.get(
        API_URL,
        params=params,
        timeout=20
    )
    response.raise_for_status()

    data = response.json()

    if "Error Message" in data:
        raise ValueError(data["Error Message"])

    if "Note" in data or "Information" in data:
        raise ValueError(
            data.get("Note", data.get("Information"))
        )

    series = data.get("Time Series (Daily)")

    if not series:
        raise ValueError(
            "Stock data unavailable. Check the symbol or API limit."
        )

    df = pd.DataFrame.from_dict(series, orient="index")

    df.index = pd.to_datetime(df.index)
    df = df.sort_index()

    df = df.rename(columns={
        "1. open": "Open",
        "2. high": "High",
        "3. low": "Low",
        "4. close": "Close",
        "5. volume": "Volume"
    })

    df = df.apply(pd.to_numeric)
    df.index.name = "Date"

    return df
