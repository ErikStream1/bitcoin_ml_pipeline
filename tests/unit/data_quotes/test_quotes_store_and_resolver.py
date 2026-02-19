from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
import pytest

from src.data import QuoteSnapshot, QuoteStore, to_utc,load_quotes


def test_to_utc_normalizes_naive_and_aware_datetimes() -> None:
    naive = datetime(2024, 1, 1, 0, 0, 0)
    aware = datetime(2024, 1, 1, 0, 0, 0, tzinfo=timezone.utc)

    assert to_utc(naive).tzinfo == timezone.utc
    assert to_utc(aware) == aware


def test_quote_store_write_chunk_writes_parquet(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    recorded = {}

    def fake_to_parquet(self, out_path, index=False):
        recorded["path"] = Path(out_path)
        recorded["columns"] = list(self.columns)
        recorded["index"] = index

    monkeypatch.setattr(pd.DataFrame, "to_parquet", fake_to_parquet)

    rows = [
        QuoteSnapshot(
            ts_exchange=datetime(2024, 1, 1, 0, 0, 0),
            book="btc_mxn",
            ask=10.0,
            bid=8.0,
            source="test",
        )
    ]

    out_path = QuoteStore(tmp_path).write_chunk(rows)

    assert out_path.suffix == ".parquet"
    assert "book=btc_mxn" in str(out_path)
    assert recorded["path"] == out_path
    assert recorded["index"] is False
    assert recorded["columns"] == ["ts_exchange", "book", "ask", "bid", "mid", "source"]


def test_load_quotes_sorts_data_by_timestamp(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    base = tmp_path / "book=btc_mxn"
    base.mkdir(parents=True)
    first = base / "part1.parquet"
    second = base / "part2.parquet"
    first.touch()
    second.touch()

    frames = {
        str(first): pd.DataFrame(
            {
                "ts_exchange": ["2024-01-01T02:00:00Z"],
                "bid": [9.0],
                "ask": [11.0],
                "mid":[10.0]
            }
        ),
        str(second): pd.DataFrame(
            {
                "ts_exchange": ["2024-01-01T01:00:00Z"],
                "bid": [8.0],
                "ask": [10.0],
                "mid": [9.0]
            }
        ),
    }

    monkeypatch.setattr(pd, "read_parquet", lambda path: frames[str(path)])

    result = load_quotes(tmp_path, "btc_mxn")

    assert result.df["bid"].tolist() == [8.0, 9.0]


def test_load_quotes_raises_if_book_folder_missing(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        load_quotes(tmp_path, "btc_mxn")