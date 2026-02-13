from __future__ import annotations
from src.execution import fee_proportional

import pytest

@pytest.mark.parametrize("notional, fee_rate, result",
                         [(100.0, 0.001, 0.1),
                          (-250, 0.002,0.5),
                          (0.0, 0.1, 0.0)])

def test_fee_proportional(notional: float, 
                          fee_rate:float, 
                          result:float
                          )->None:
    fee = fee_proportional(notional = notional, fee_rate =fee_rate)
    assert fee == pytest.approx(result)    