# Algorithmic Momentum & Mean-Reversion Strategy Backtester

Datheon internship project. (GitHub does not allow `&` in repository names, so it is written as `and` in the repo name.)

## Status

| Task | Description | Status |
|------|-------------|--------|
| 1 | Historical Market Tick Ingestion & Data Sanitation | Done |
| 2 | Momentum & Bollinger Band Mean-Reversion Rules | In progress |
| 3 | Institutional Execution Simulator & Risk Analytics | Planned |

## Task 1: Data Ingestion & Sanitation

**Script:** `task1_data_ingestion.py`

**Stocks:** AAPL, MSFT, TSLA, NVDA, AMZN

**What it does**
1. Downloads 10 years of daily prices and about 2 years of hourly prices from Yahoo Finance (`yfinance`).
2. Sanitises the data: removes duplicate timestamps, sorts by time, drops rows with missing or non-positive prices.
3. Uses `Adj Close`, which Yahoo has already adjusted for stock splits and dividends, so there are no fake crashes on split dates.
4. Computes simple returns (`pct_change`) and log returns (`ln(P_t / P_t-1)`).
5. Flags moves above 10% in one period and checks they are real events, not unadjusted splits.
6. Saves cleaned files to `data/`.

**Validation (AAPL daily example)**
- 2,512 rows from 2016-11-11 to 2026-11-10, no duplicates, no missing price values.
- The 4-for-1 split on 2020-08-31 shows no -75% drop; the return that day is about +3.4%.
- The only moves above 10% were on 2020-03-13, 2020-03-16, 2020-03-24, 2020-07-31 and 2025-04-09, consistent with known market events (COVID-19 crash, earnings, tariff news).

**Known limitation:** Yahoo Finance provides only about the last 730 days of hourly data, so the hourly files cover about 2 years, not 10.

**Data files:** `data/<TICKER>_daily_cleaned.csv` and `data/<TICKER>_hourly_cleaned.csv`. (The first row of each return column is empty because there is no prior period.)

## How to run

```bash
pip install -r requirements.txt
python task1_data_ingestion.py
```
