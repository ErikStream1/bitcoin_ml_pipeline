from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen = True)
class BitsoConfig:
    base_url:str = "https://api.bitso.com/v3"
    timeout_s: float = 10.0
    
class BitsoError(RuntimeError):
    pass

@dataclass(frozen = True)
class QuoteSnapshot:
    ts_exchange: datetime
    ts_local: datetime
    book: str
    ask: float
    bid: float
    source: str
    