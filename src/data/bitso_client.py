from __future__ import annotations

from typing import Any
from dataclasses import dataclass
from datetime import datetime, timezone
from decimal import Decimal
from src.models.types import paramsLike, payloadLike
from src.types import PathLike
import requests
from tenacity import (retry,
                      wait_exponential,
                      stop_after_attempt,
                      retry_if_exception_type
                      )

@dataclass(frozen = True)
class BitsoConfig:
    base_url:str = "https://api.bitso.com/v3"
    timeout_s: float = 10.0
    
class BitsoError(RuntimeError):
    pass

def _parse_dt_utc(dt_str:str)->datetime:
    s = dt_str.replace("Z", "+00:00")
    dt = datetime.fromisoformat(s)
    
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)

class BitsoClient:
    def __init__(self, cfg: BitsoConfig|None = None):
        self.cfg = cfg or BitsoConfig()
        self._session = requests.Session()
        
    @retry(
        wait = wait_exponential(multiplier=0.5, min=0.5, max=8),
        stop = stop_after_attempt(5),
        retry = retry_if_exception_type((requests.RequestException, BitsoError)),
        reraise = True
    )
    def _get(self, path: PathLike, params: paramsLike = None,)->dict[str, Any]:
        url = f"{self.cfg.base_url}{path}"
        r = self._session.get(url, params = params, timeout=self.cfg.timeout_s)
        r.raise_for_status
        data = r.json()
        if not data.get("success", False):
            raise BitsoError(f"Bitso API returned success = false: {data}")
        
        return data
    
    def list_available_books(self)->list[dict[str,Any]]:
        data = self._get("/available_books/")
        return data["payload"]
    
    def get_ticker(self, book:str)->payloadLike:
        data = self._get("/ticker/", params = {"book":book})
        return data["payload"]
    
    def get_best_bid_ask_from_ticker(self, book: str)->tuple[datetime, Decimal, Decimal]:
        p = self.get_ticker(book)
        ts = _parse_dt_utc(p["created_at"])
        bid = Decimal(str(p["bid"]))
        ask = Decimal(str(p["ask"]))
        return ts, bid, ask