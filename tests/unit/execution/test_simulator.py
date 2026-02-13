from __future__ import annotations

import pandas as pd
import pytest
from src.types import ConfigLike, FrameLike
from src.execution import Fill, OrderSide, simulate_fills_from_target_position

@pytest.fixture
def cfg()->ConfigLike:
    return {
        "execution": {
            "fill_mode": "next_close",
            "qty": 2.0,
            "fees": {
                "rate": 0.001
                },
            "slippage": {
                "bps": 10.0, 
                "vol_k": 0.5
                },
        }
    }
@pytest.fixture
def market_frame()->FrameLike:
    return pd.DataFrame({
            "Close": [100.0, 101.0, 102.0, 103.0],
            "mid": [99.5, 100.5, 101.5, 102.5],
            "bid": [99.0, 100.0, 101.0, 102.0],
            "ask": [100.0, 101.0, 102.0, 103.0],
    })
    

def test_simulator_for_position_changes(
    cfg: ConfigLike,
    market_frame: FrameLike
)->None:
    target_position = pd.Series([0, 1, 1, -1])
    volatility = pd.Series([0.01, 0.02, 0.03, 0.04])

    fills = simulate_fills_from_target_position(cfg = cfg,
                                                target_position=target_position,
                                                price_frame=market_frame,
                                                volatility=volatility)

    assert len(fills) == 2
    assert all(isinstance(fill, Fill) for fill in fills)
    
    first = fills[0]
    assert first.timestamp == 1
    assert first.side == OrderSide.BUY
    assert first.qty == 2.0
    assert first.price == pytest.approx(102.111) # base = 101, bps = 0.101, vol = 1.01 ==> price = 102.111
    assert first.fee == pytest.approx(0.204222)#price = 102.111, qty = 2, fee_rate = 0.001  ==> fee = 0.204222
    
    second = fills[1]
    assert second.timestamp == 3
    assert second.side == OrderSide.SELL
    assert second.qty == 2.0
    assert second.price == pytest.approx(100.837) # base = 103, bps = 0.103, vol = 2.06 ==> price = 100.837
    assert second.fee == pytest.approx(0.201674) # price = 100.837, qty = 2, fee_rate = 0.001
    
@pytest.mark.parametrize(("fill_mode, expected_side, expected_price"),
                         [
                             ("next_close", OrderSide.BUY, 101),
                             ("mid", OrderSide.BUY, 100.5),
                             ("bid_ask",OrderSide.BUY, 101.0)
                         ],
                         )
def test_simulator_uses_configured_fill_mode(
    fill_mode:str,
    expected_side: OrderSide,
    expected_price: float,
    cfg: ConfigLike,
    market_frame:FrameLike
)->None:
    cfg = {
        "execution":{
            **cfg["execution"],
            "fill_mode": fill_mode,
            "slippage":{
                "bps":0.0,
                "vol_k": 0.0
            }
        }
    }
    target_position = pd.Series([0,1])
    fills = simulate_fills_from_target_position(cfg = cfg, 
                                                target_position=target_position,
                                                price_frame=market_frame.iloc[:2],
                                                volatility=None)
    
    assert len(fills) == 1
    assert fills[0].side == expected_side
    assert fills[0].price == expected_price
    
def test_simulator_unknown_fill_mode(cfg:ConfigLike,
                                     market_frame:FrameLike
                                     )->None:
    target_position = pd.Series([0,1])
    cfg = {
        "execution":{
            **cfg["execution"],
            "fill_mode": "unknown"
            }
    }
    
    with pytest.raises(ValueError,match="Unknown fill_mode"):
        simulate_fills_from_target_position(
                cfg=cfg,
                target_position=target_position,
                price_frame=market_frame.iloc[:2],
                volatility=None
            )
    