from __future__ import annotations

import json

from src.execution import BitsoBrokerClient


def test_build_auth_headers_has_expected_shape(monkeypatch) -> None:
    monkeypatch.setattr("src.execution.brokers.bitso_brokers.time.time", lambda: 123456.123456)

    client = BitsoBrokerClient(
        {
            "live_broker":{
                "base_url": "https://api.bitso.com/v3",
                "timeout_s": 5.0,
            },
            "local_live_broker":{
                "api_key": "api-key",
                "api_secret": "secret",
            }  
        }
    )
    payload = json.dumps({"book": "btc_mxn", "major": "0.001"}, separators=(",", ":"), sort_keys=True)
    headers = client._build_auth_headers(method="POST", request_path="/orders/", payload_str=payload)

    assert "Authorization" in headers
    assert headers["Authorization"].startswith("Bitso api-key:")
    assert headers["Authorization"].count(":") == 2