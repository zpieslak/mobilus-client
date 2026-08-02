# AGENTS.md

Project-specific rules for agents working in `mobilus-client`.

## Core Constraints

- Control only a user-provided local Mobilus Cosmo GTW gateway; do not add cloud, public-internet, or vendor-hosted runtime behavior.
- Preserve protocol compatibility: default port `8884`, transport `websockets`, protobuf fields, category IDs, and encryption framing.
- Keep CLI stdout as stable JSON command output; diagnostics/logging go to stderr.
- Maintain 100% coverage for non-generated code.

## Architecture

```text
CLI (__main__.py) parses arguments into Config
  -> App orchestrates commands and serializes responses
  -> Client manages MQTT lifecycle, authentication, publishing, and callbacks
       -> messages/, registries/, proto/, and utils/ support protocol handling
  <-> local MQTT gateway
```

Keep orchestration/serialization in `App`, MQTT lifecycle in `Client`, and protocol construction/validation/encryption in `messages/`.

## Hard Boundaries

- Never expose or commit real gateway hosts, credentials, keys, derived `user_key` values, session keys, gateway IPs, or captured payloads.
- Keep tests fully mocked/local; do not contact a real gateway, MQTT broker, cloud service, public internet, or vendor-hosted runtime.
- Use synthetic placeholders in docs/tests: `GATEWAY_HOST`, `USER_LOGIN`, `USER_PASSWORD`.
- Do not broaden public CLI, protocol, dependency, CI, release, or cloud behavior unless the task requires it.
- Do not hand-edit generated `_pb2.py` or `_pb2.pyi` files.

## Checks

Runtime Python is `>=3.9`; CI tests Python `3.9` through `3.14`. Install dev deps if needed:

```bash
python -m pip install -e ".[test]"
```

Use narrow checks while iterating:

```bash
python -m unittest tests.test_config.TestConfig.test_gateway_host
python -m ruff check mobilus_client/config.py tests/test_config.py
python -m mypy mobilus_client/config.py
```

Full local gate:

```bash
set -e
COVERAGE_FILE="$(mktemp -t mobilus-client-coverage.XXXXXX)"
export COVERAGE_FILE
trap 'rm -f "$COVERAGE_FILE"' EXIT
python -m ruff check --output-format=github .
python -m mypy .
python -m coverage run -m unittest -v
python -m coverage report --fail-under=100
```

For dependency, packaging, release, or build metadata changes also run `python -m pip install build` and `python -m build`. For package contents/installability changes, inspect distributions and test wheel installation in a temp venv.

## Task Routes

- New/changed CLI command: inspect `__main__.py`, `app.py`, and nearest command; update `__main__.py` only for CLI interface changes and `config.py` only for runtime configuration; update protocol builders/validation/registries/category maps/type unions/protobuf exports only where required; add focused tests and README usage.
- MQTT/session behavior: start with `client.py`, then inspect `registries/`, `messages/`, and related tests.
- Encryption/protocol behavior: inspect `messages/`, `mobilus_client/utils/`, protobuf definitions, tests, and deterministic time patches.
- Protobuf message changes: edit `.proto` files, follow Protobuf Workflow, and review generated diffs.
- CLI output/logging behavior: add a CLI-level test that stdout contains only final JSON and `--verbose` diagnostics go to stderr.
- User-visible behavior: update `README.md` and tests together.

## Code And Tests

- Use `unittest.TestCase` and `unittest.mock.patch`; do not introduce pytest-only patterns.
- Mock MQTT, sockets, time, logging, orchestration, gateways, and brokers.
- Use `tests/factories.py` for populated protobuf fixtures and `tests/helpers.py` for encrypted-message helpers.
- Patch `time.time` for byte-level encryption assertions.
- Keep tests credential-free; avoid coverage-only assertions/branches.

## Protobuf Workflow

Edit `.proto` files only, then regenerate runtime modules and stubs:

```bash
docker compose -f scripts/docker-compose.yml run --build --rm --user "$(id -u):$(id -g)" protoc
```

If both `_pb2.py` and `_pb2.pyi` are not regenerated, fix/report the helper. Review generated diffs and update README Development if this command changes.

## Handoff

Call out validation and any user-visible, protocol, MQTT, protobuf, dependency, build, CI, or release impact.
