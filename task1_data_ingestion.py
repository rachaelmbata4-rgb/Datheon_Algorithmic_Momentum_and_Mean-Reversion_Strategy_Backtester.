"""
Task 1: Historical Market Tick Ingestion & Data Sanitation

What this script does:
1. Downloads 10 years of DAILY and ~2 years of HOURLY equity prices (Yahoo Finance).
2. Sanitises the data: removes duplicate timestamps, sorts by time, checks missing values.
3. Uses Adj Close (already adjusted for stock splits and dividends) for all returns.
4. Computes simple returns and log returns.
5. Flags unusually large moves (> 10% daily) so unadjusted splits can be ruled out.
6. Saves cleaned data to the data/ folder as CSV files.

Run:  python task1_data_ingestion.py
"""
import os

import numpy as np
import pandas as pd
import yfinance as yf

TICKERS = ["AAPL", "MSFT", "TSLA", "NVDA", "AMZN"]
OUTPUT_DIR = "data"
BIG_MOVE_THRESHOLD = 0.10  # 10% in one period


def download(ticker: str, period: str, interval: str) -> pd.DataFrame:
    """Download raw prices and flatten the column names."""
    df = yf.download(ticker, period=period, interval=interval, auto_adjust=False, progress=False)
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    return df


def sanitise(df: pd.DataFrame) -> pd.DataFrame:
    """Remove duplicate timestamps, sort by time, drop rows with invalid prices."""
    df = df[~df.index.duplicated(keep="first")].sort_index()
    price_cols = ["Open", "High", "Low", "Close", "Adj Close"]
    df = df.dropna(subset=price_cols)
    df = df[(df[price_cols] > 0).all(axis=1)]  # no zero or negative prices
    return df


def add_returns(df: pd.DataFrame) -> pd.DataFrame:
    """Add simple and log returns computed from the split-adjusted close."""
    df = df.copy()
    df["return"] = df["Adj Close"].pct_change()
    df["log_return"] = np.log(df["Adj Close"] / df["Adj Close"].shift(1))
    return df


def report(name: str, df: pd.DataFrame) -> None:
    big = df[df["return"].abs() > BIG_MOVE_THRESHOLD]
    print(f"{name}: rows={len(df)}, start={df.index.min()}, end={df.index.max()}, "
          f"missing={int(df.isna().sum().sum())}, moves>{BIG_MOVE_THRESHOLD:.0%}={len(big)}")


def main() -> None:
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    for ticker in TICKERS:
        # Daily: 10 years
        daily = add_returns(sanitise(download(ticker, "10y", "1d")))
        report(f"{ticker} daily", daily)
        daily.to_csv(f"{OUTPUT_DIR}/{ticker}_daily_cleaned.csv")

        # Hourly: Yahoo only provides about the last 730 days
        hourly = add_returns(sanitise(download(ticker, "2y", "1h")))
        report(f"{ticker} hourly", hourly)
        hourly.to_csv(f"{OUTPUT_DIR}/{ticker}_hourly_cleaned.csv")


if __name__ == "__main__":
    main()
