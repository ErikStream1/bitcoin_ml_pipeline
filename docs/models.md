# Models

This document describes the **model layer**: the common model interface, supported model types,
how models are built via a factory, and how they are persisted/loaded for inference.

## Purpose
- Provide a consistent API for training and inference across model implementations.
- Support reproducible persistence (model artifact + metadata).

## Scope

### In scope
- `BaseModel` interface (`fit`, `predict`, `save`, `load`, `from_payload`, `_get_serializable_model`)
- Model implementations (e.g., Ridge, XGBoost)
- Model factory (`build_model`) to construct models from config
- Model artifacts: how models and metadata are serialized

### Out of scope
- Feature engineering (`src/features`)
- Training/validation orchestration (`src/pipelines`, `src/validation`)
- Backtest strategy logic (`src/strategy`, `src/backtest`)


## Core concepts

### Model interface (`BaseModel`)
All models implement a shared interface to ensure the pipelines can:
- train a model: `fit(X, y) -> Self`
- produce predictions: `predict(X) -> Prediction`
- persist artifacts: `save(path) -> None`

This keeps pipelines agnostic to the specific estimator (linear vs XGBoost).

### Model metadata (`info`)
Each model carries an `info` object/dict that stores descriptive metadata such as:
- model type / name
- any identifiers needed for reproducibility

### Model payload
The persisted artifact typically includes:
- the fitted estimator object (e.g., sklearn model, xgboost booster)
- the model `info` metadata

## Model artifacts (payload contract)

Trained models are persisted as a single artifact (joblib) containing:
- `info`: model metadata (serializable dict)
- `model`: the trained estimator in a serializable form

### `_get_serializable_model()`
Each model implementation must provide a serializable representation of the trained estimator.
This is used by `BaseModel.save()`.

Typical returns:
- sklearn models: return the fitted estimator instance
- xgboost: return the fitted XGBRegressor/XGBClassifier instance (or Booster if used)

### `from_payload(payload)`
Reconstructs a model instance from a persisted payload (model + metadata). This enables:
- loading models for inference
- consistent restoration across model types

## Supported models

### Linear (Ridge)
A regularized linear regression model (L2). Configured via `alpha`, etc.

### XGBoost
Non-linear gradient boosted trees. Configured via typical xgboost hyperparameters
(e.g., `n_estimators`, `max_depth`, `learning_rate`, etc.).

> Note: The exact set of supported models depends on what is implemented in `src/models/`.

