# AGENTS.md

Root-scoped instructions for agents working in this repository. Keep guidance concrete, repository-specific, and updated when structure, commands, compatibility constraints, or release workflow changes.

## Project Overview

`mobilus-client` is a typed Python package and CLI for controlling a Mobilus Cosmo GTW gateway over its local MQTT broker. It must connect only to a user-provided local gateway; do not add cloud-service, public-internet, or vendor-hosted runtime dependencies.

Core responsibilities:

- MQTT login/session handling, request publishing, response matching, protobuf serialization, and CLI JSON output.
- Compatibility with Mobilus Cosmo GTW protocol details: protobuf field names, category IDs, encryption framing, default port `8884`, and default protocol `websockets`.

## Non-Negotiables

- Tests and CI must be fully mocked/local: no real gateway, real MQTT broker, cloud service, or internet access.
- Never commit or log real gateway hosts, credentials, keys, derived `user_key`, session keys, gateway IPs, or captured payloads.
- Documentation examples must use synthetic placeholders such as `GATEWAY_HOST`, `USER_LOGIN`, and `USER_PASSWORD`.
- CLI stdout is reserved for JSON command results; use logging for diagnostics.
- Do not create commits or tags unless explicitly asked.

## Worktree Safety

Before editing, inspect `git status --short`. Preserve unrelated tracked and untracked changes. Do not run `git clean`, `git reset --hard`, delete files, or reformat unrelated files unless explicitly asked. Keep changes focused and mention pre-existing modified or untracked files in the handoff.

## Environment And Checks

- Runtime Python is `>=3.9`; CI tests Python `3.9` through `3.14`.
- Runtime dependencies are `paho-mqtt`, `cryptography`, and `protobuf`; prefer the standard library and existing dependencies.
- Install development dependencies with `python -m pip install -e ".[test]"`.

Run the narrowest relevant checks while iterating. Before handoff, run the full local gate unless the change is docs-only, user-limited, or tools are unavailable:

```bash
python -m ruff check --output-format=github .
python -m mypy .
python -m coverage run -m unittest -v
python -m coverage report --fail-under=100
```

Coverage is expected to remain at 100% for non-generated code. For release, dependency, or packaging changes, also run:

```bash
python -m pip install build
python -m build
```

If checks are skipped or fail for environment reasons, report the exact command, reason, and remaining risk.

## Repository Map

- `mobilus_client/__main__.py`, `app.py`, `client.py`, `config.py`: CLI parsing, orchestration, MQTT lifecycle, and runtime configuration.
- `mobilus_client/messages/`: message factory, validation, encryption/decryption, serialization, and status handling.
- `mobilus_client/registries/`: encryption key and request/response tracking.
- `mobilus_client/proto/`: tracked `.proto` files plus generated `_pb2.py` and `_pb2.pyi` files.
- `mobilus_client/utils/`: shared encryption helpers and protobuf type aliases.
- `tests/`: `unittest` suite using mocked MQTT/orchestration seams.
- `scripts/`: Docker Compose/protoc helper for protobuf regeneration.

## Code And Tests

- Follow `pyproject.toml` for Ruff, mypy, and coverage configuration; do not duplicate or weaken those settings.
- Use module loggers via `logging.getLogger(__name__)`; avoid stray `print()` in package logic.
- Keep imports type-safe. Use annotation-only imports under `if TYPE_CHECKING:` when needed.
- Use targeted `# noqa: RULE` and `# type: ignore[...]` only when necessary and clear.
- Use `unittest.TestCase`; do not introduce pytest-only patterns unless the project intentionally migrates.
- Use `unittest.mock.patch` for MQTT, sockets, time, logging, and orchestration seams.
- Use `tests/factories.py` for protobuf objects and `tests/helpers.py` for encrypted-message helpers.
- Patch `time.time` for byte-level encryption assertions so encrypted payloads are deterministic.
- Keep tests credential-free; inert placeholder passwords/keys are acceptable fixtures.

## MQTT, Commands, And Protocol Boundaries

- Keep MQTT lifecycle and callbacks in `Client`; keep high-level command orchestration in `App`.
- Preserve public CLI behavior unless intentionally changing it:
  - required flags: `--host`, `--login`, `--password`;
  - optional flag: `--verbose`;
  - command syntax such as `current_state`, `devices_list`, and `call_events:device_id=DEVICE_ID,value=VALUE`;
  - command results written to stdout as JSON.
- When adding commands or protobuf message types, update the relevant `MessageFactory` builder, `MessageRegistry` mapping, `MessageEncryptor` category maps, message unions in `mobilus_client/utils/types.py`, `mobilus_client/proto/__init__.py` exports if needed, tests, and README usage.

## Protobuf Workflow

Do not hand-edit generated `_pb2.py` or `_pb2.pyi` files. Edit `.proto` files, then regenerate with:

```bash
docker compose -f scripts/docker-compose.yml up --build
```

The helper must generate both runtime `_pb2.py` modules and `_pb2.pyi` stubs. If it does not, fix the helper or report incomplete regeneration. Review generated diffs carefully and include generated files with the `.proto` change.

## Documentation, Packaging, And Handoff

- Update `README.md` for user-visible behavior changes: installation, dependencies, CLI flags, command syntax, JSON output shape, supported `call_events` values, protobuf/protocol assumptions, or gateway compatibility notes.
- Packaging uses `hatchling` with `hatch-vcs`; builds exclude dotfiles, `scripts/`, and `tests/`.
- The package is typed via `mobilus_client/py.typed`; keep public type information accurate.
- Publish workflow runs only for tags matching `v*` and uses trusted publishing to PyPI.
- In reviews, flag cloud/public-internet dependencies, real gateway/MQTT test requirements, protocol changes without tests/docs, or secret leakage.
- In handoff notes, call out changes to CLI flags, commands, protobuf files, MQTT behavior, dependencies, packaging, CI, or release behavior.

## Generated And Local Files

Do not stage tool caches, coverage reports, build artifacts, or scratch files. Keep common local outputs ignored or remove them before handoff, including `.mypy_cache/`, `.ruff_cache/`, `.pytest_cache/`, `htmlcov/`, `build/`, `dist/`, `.coverage`, and `tmp/`. Do not rely on untracked local state.
