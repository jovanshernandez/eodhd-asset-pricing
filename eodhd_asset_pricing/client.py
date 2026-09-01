from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import requests

SUPPORTED_ASSETS = {"stock", "etf", "fund", "bonds", "index", "commodity", "crypto"}


@dataclass(frozen=True)
class SearchResult:
    symbol: str
    name: str
    exchange: str | None = None
    country: str | None = None
    currency: str | None = None
    asset_type: str | None = None


class EodhdClient:
    def __init__(self, api_key: str, base_url: str = "https://eodhistoricaldata.com/api", timeout: float = 10.0):
        if not api_key:
            raise ValueError("api_key is required")
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def search(self, asset_type: str, query: str) -> list[SearchResult]:
        normalized_asset = asset_type.lower()
        if normalized_asset not in SUPPORTED_ASSETS:
            allowed = ", ".join(sorted(SUPPORTED_ASSETS))
            raise ValueError(f"asset_type must be one of: {allowed}")
        if not query.strip():
            raise ValueError("query is required")

        response = requests.get(
            f"{self.base_url}/search/{query}",
            params={"api_token": self.api_key, "type": normalized_asset},
            timeout=self.timeout,
        )
        response.raise_for_status()
        payload = response.json()
        if not isinstance(payload, list):
            raise ValueError("unexpected EODHD response format")

        return [_parse_result(item, normalized_asset) for item in payload]


def _parse_result(item: dict[str, Any], asset_type: str) -> SearchResult:
    return SearchResult(
        symbol=str(item.get("Code") or item.get("Symbol") or "").upper(),
        name=str(item.get("Name") or ""),
        exchange=item.get("Exchange"),
        country=item.get("Country"),
        currency=item.get("Currency"),
        asset_type=asset_type,
    )
