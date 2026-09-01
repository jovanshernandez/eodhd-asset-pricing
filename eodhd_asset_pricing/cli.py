from __future__ import annotations

import argparse
import csv
import os
from dataclasses import asdict
from pathlib import Path

from eodhd_asset_pricing.client import EodhdClient, SUPPORTED_ASSETS


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Search EODHD instruments by asset class.")
    parser.add_argument("query", help="Ticker, company, fund, index, commodity, or crypto search term.")
    parser.add_argument("--asset-type", default="stock", choices=sorted(SUPPORTED_ASSETS))
    parser.add_argument("--api-key", default=os.getenv("EODHD_API_KEY"), help="EODHD API key. Defaults to EODHD_API_KEY.")
    parser.add_argument("--output", type=Path, help="Optional CSV output path.")
    return parser


def run(query: str, asset_type: str, api_key: str, output: Path | None = None) -> list[dict[str, str | None]]:
    client = EodhdClient(api_key)
    rows = [asdict(result) for result in client.search(asset_type, query)]

    if output:
        output.parent.mkdir(parents=True, exist_ok=True)
        with output.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=["symbol", "name", "exchange", "country", "currency", "asset_type"])
            writer.writeheader()
            writer.writerows(rows)
    return rows


def main() -> None:
    args = _build_parser().parse_args()
    if not args.api_key:
        raise SystemExit("EODHD_API_KEY or --api-key is required")

    rows = run(args.query, args.asset_type, args.api_key, args.output)
    for row in rows:
        print(f"{row['symbol']:<12} {row['name']:<40} {row.get('exchange') or ''}")


if __name__ == "__main__":
    main()
