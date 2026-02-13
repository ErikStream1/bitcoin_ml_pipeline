from __future__ import annotations
from src.types import SeriesLike

def fill_price_next_close(close: SeriesLike, t: int)->float:
    
    value = close.loc[t]
    return float(value)

def fill_price_mid(mid: SeriesLike, t: int)->float:
    return float(mid.loc[t])

def fill_price_bid_ask(bid: SeriesLike, ask: SeriesLike, side: str, t:int)->float:      
    side_ = side.upper()
    
    if side_ == "BUY":
        return float(ask.loc[t])
    
    elif side_ == "SELL":
        return float(bid.loc[t])
    else:
        raise ValueError("Invalid side")