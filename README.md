# EODHD Asset Pricing Search

CLI utility for searching EOD Historical Data instruments by asset class. The original script has been refactored into a small package with API-key handling, validation, test coverage, and optional CSV output.

## What It Shows

- Environment-based credential handling with `EODHD_API_KEY`
- Validated asset-class search for stocks, ETFs, funds, bonds, indices, commodities, and crypto
- Request timeout and HTTP error handling
- Typed result model for downstream workflows
- Optional CSV export for repeatable reports
- Unit tests using mocked API responses
- GitHub Actions workflow for pull-request validation

## Run Locally

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
pytest -q
EODHD_API_KEY=your_token eodhd-search apple --asset-type stock --output reports/apple.csv
```

The legacy entry point still works:

```bash
EODHD_API_KEY=your_token python eod-data.py apple --asset-type stock
```

## Repository Layout

```text
eodhd_asset_pricing/
  client.py   EODHD API client and result parsing
  cli.py      Console entry point and CSV export
tests/
  test_client.py
```

## Resume Positioning

This is best used as a supporting data-ingestion utility, not the headline project. It complements a platform or SRE story when paired with CI, validation, and operational documentation.
