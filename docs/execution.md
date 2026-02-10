# Execution

This document describes the **execution assumptions** used to convert strategy intent into fills,
including fill pricing rules and transaction cost models (fees + slippage).

## Purpose
- Define how fills are priced (fill model).
- Apply transaction costs consistently (fees + slippage).
- Provide a realistic boundary between strategy intent and backtest accounting.
---

### Fill generation

`fill_mode` defines which price is used when an order is executed in simulation:

`next_close`: execute at the next bar close (more conservative than current-bar prices).

Other modes may exist (e.g., `close`, `mid`, `bid`, `ask`) depending on your implementation.

---
### Transaction costs
### Fees

Applied as a function of notional:

`notional = qty * price` (quote currency)

`fee = notional * fees.rate`

---
### Slippage

A simple constant-bps slippage model can be interpreted as:

`slippage_cost ≈ price * (bps / 10_000)`

`slippage_vol ≈ price * (k*vol)`

---
### Common pitfalls

`qty` ambiguity: in spot crypto, qty usually means base units (BTC). A `qty=1.0` can be huge.

Double counting: ensure fees/slippage are applied once (execution vs ledger).

Overly optimistic fills: using current bar close can overstate performance; next_close is safer.