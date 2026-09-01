from unittest.mock import Mock, patch

import pytest

from eodhd_asset_pricing.client import EodhdClient


def test_search_parses_results() -> None:
    response = Mock()
    response.json.return_value = [
        {"Code": "AAPL", "Name": "Apple Inc", "Exchange": "US", "Currency": "USD"},
    ]
    response.raise_for_status.return_value = None

    with patch("eodhd_asset_pricing.client.requests.get", return_value=response) as get:
        results = EodhdClient("token").search("stock", "apple")

    assert results[0].symbol == "AAPL"
    assert results[0].name == "Apple Inc"
    get.assert_called_once()


def test_rejects_unsupported_asset_type() -> None:
    with pytest.raises(ValueError, match="asset_type must be one of"):
        EodhdClient("token").search("currency", "eur")
