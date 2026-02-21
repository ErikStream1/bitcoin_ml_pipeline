from __future__ import annotations
from src.types import ConfigLike
from src.models import ModelLike, LinearModel, XGBoostModel

from pathlib import Path

def _load_model(model_path: Path) -> LinearModel | XGBoostModel:
    model_path_str = str(model_path)

    if "linear" in model_path_str:
        return LinearModel.load(model_path)
    if "xgboost" in model_path_str:
        return XGBoostModel.load(model_path)

    raise ValueError(f"Model not found for path: {model_path_str}")


def build_model(cfg : ConfigLike) -> ModelLike:
    model_cfg = cfg["models"]
    active_model = cfg["training"]["model_run"].get("active_model", "xgboost_v1")

    act_model = model_cfg[active_model]
    model_type = act_model["type"]
    params = act_model.get("params", {})
    model = ""
    if model_type == "linear_regression":
        model = LinearModel(**params)
    
    elif model_type == "xgboost":
        model = XGBoostModel(params = params)
    
    else:
        raise ValueError(f"Model {model_type} not found.")
    
    return model