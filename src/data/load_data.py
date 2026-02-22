from __future__ import annotations

import yfinance as yf
import pandas as pd
from src.types import FrameLike

COL_NAMES = ["Date","Open", "High", "Low", "Close", "Volume"]

def load_btc_data_daily_candles(
    ticker:str,
    lookback_days: int = 1
    )->FrameLike:

    df = yf.download(
            tickers=ticker,
            period=f"{lookback_days}d",
            interval="1d",
            progress=False,
    )
    
    if df is None:
        return pd.DataFrame()
    
    df = df.reset_index()
    df.columns = COL_NAMES
    
    return df

def load_historic_btc_data(
    ticker: str = "BTC-USD",
    start: str = "2015-01-01",
    end: str|None = None,
    )->FrameLike:

    df = yf.download(ticker, start=start, end=end, progress=False)
    
    if df is None:
        return pd.DataFrame()
    
    df = df.reset_index()
    df.columns = COL_NAMES
    return df