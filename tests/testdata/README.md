# Test Fixtures

Cross-language test fixtures for verifying Go and Python SDK compatibility
against the same SQLite database.

## Python-format (Pydantic JSON)

Written by the Python SDK. Uses snake_case enum values.

- `python_unit.json` — Local tier, one stale flag.
- `python_flagged_unit.json` — Local tier, two flags (stale + incorrect), multiple languages.
- `python_real_unit.json` — Real production unit from team API, team tier.
- `python_team_confirmed.json` — Team tier, confirmed twice, no flags.

## Go-format (protojson)

Written by the Go SDK. Uses proto-canonical enum names.

- `go_unit.json` — Local tier, no flags.
- `go_flagged_unit.json` — Local tier, one duplicate flag.

Both formats must be readable by both SDKs.
