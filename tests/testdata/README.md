# Test Fixtures

Cross-language test fixtures for verifying Go and Python SDK compatibility
against the same SQLite database.

## Legacy Python format

Written by pre-proto Python code. Uses snake_case field names with
short enum values (`"local"`, `"team"`, `"stale"`). The SDK normalizes
these to proto-canonical values on deserialization.

- `python_unit.json` — Local tier, one stale flag.
- `python_flagged_unit.json` — Local tier, two flags (stale + incorrect), multiple languages.
- `python_real_unit.json` — Real production unit from team API, team tier.
- `python_team_confirmed.json` — Team tier, confirmed twice, no flags.
- `ku_*.json` — Real KU backups from production, all team tier.

## Go format (proto-canonical)

Written by the Go SDK. Uses snake_case field names with proto-canonical
enum values (`"TIER_LOCAL"`, `"FLAG_REASON_STALE"`).

- `go_unit.json` — Local tier, no flags.
- `go_flagged_unit.json` — Local tier, one duplicate flag.

Both formats must be readable by both SDKs.
