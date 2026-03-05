from __future__ import annotations
from typing import Any, TypeAlias, Sequence
from dataclasses import dataclass
from enum import Enum
from src.types import SeriesLike, IntArray


class OrderSide(str, Enum):
    BUY = "buy"
    SELL = "sell"

@dataclass(frozen=True)
class Fill:
    timestamp: object
    side: OrderSide
    qty: float
    price: float
    fee: float
    
PositionLike: TypeAlias = IntArray | SeriesLike
FillVectorLike: TypeAlias = Sequence[Fill]

@dataclass(frozen=True)
class ShadowExecutionResult:
    step: RealtimeSimulationStepResult
    fills_count: int
    has_position_change: bool
    artifact_dir: str | None

@dataclass(frozen=True)
class RealtimeSimulationStepResult:
    timestamp: str
    bid: float
    ask: float
    mid: float
    predicted_return: float
    target_position: int
    action: str

@dataclass(frozen=True)
class PaperTradingResult:
    step: RealtimeSimulationStepResult
    previous_position: int
    target_position: int
    fills_count: int
    blotter_path: str
    state_path: str
    
class BitsoBrokerError(RuntimeError):
    """Raised when an authenticated bitso broker request fails."""

@dataclass(frozen = True)
class BitsoOrderResponse:
    oid: str | None
    status: str
    raw: dict[str, Any]