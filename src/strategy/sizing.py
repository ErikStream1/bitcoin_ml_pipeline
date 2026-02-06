from __future__ import annotations

from src.types import SeriesLike, ConfigLike


def target_qty_from_fixed_notional(
    cfg: ConfigLike,
    desired_positions:SeriesLike,
    mid:SeriesLike
)->SeriesLike:
    
    strategy_cfg = cfg["strategy"]
    sizing_cfg = strategy_cfg["sizing"]
    
    notional = float(sizing_cfg["target_notional"])
    min_qty = float(sizing_cfg["min_qty"])
    max_notional = sizing_cfg.get("max_notional", None)
    
    desired_position = desired_positions.astype(float)
    mid = mid.astype(float)
    
    desired_position = desired_position.reindex(mid.index).ffill().fillna(0.0)
    qty = (notional / mid) * desired_position
    qty = qty.replace([float("inf"), float("-inf")], 0.0).fillna(0.0)
    
    if max_notional is not None:
        max_notional = float(max_notional)
        cap_qty = max_notional/mid
        qty = qty.clip(lower=-cap_qty, upper=cap_qty)
        
    if min_qty > 0:
        qty = qty.where(qty.abs() >= min_qty, 0.0)
        
    return qty