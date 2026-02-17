import pandas as pd
from src.evaluation import directional_accuracy, mae, rmse
from pytest import approx

def test_rmse_matches_expected_value() -> None:
    y_true = pd.Series([1.0, 3.0, 2.0])
    y_pred = pd.Series([1.0, 1.0, 4.0])

    result = rmse(y_true, y_pred)
    assert result == approx(pow(8/3, 0.5)) 


def test_mae_matches_expected_value() -> None:
    result = mae([1.0, 2.0], [2.0, -1.0])

    assert result == approx(2.0)


def test_directional_accuracy_returns_fraction() -> None:
    result = directional_accuracy([1.0, -1.0, 0.0], [0.5, 3.0, 0.0])

    assert result == approx(2 / 3)