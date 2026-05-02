# Stride

A structured command runner — a clean alternative to `make`.

Stride reads a `stride.yaml` config, groups your commands logically, and runs them with a simple `group:command` syntax. No more flat Makefiles. No more guessing what commands exist.

---

## Why not make?

| | `make` | Stride |
|---|---|---|
| Grouped commands | ✗ | ✓ |
| Built-in discovery | ✗ | ✓ |
| Per-command descriptions | ✗ | ✓ |
| Readable config | Makefiles | YAML |
| Typo suggestions | ✗ | ✓ |

---

## Installation

```bash
pip install stride
# or
pipx install stride
```

---

## Quick start

Create a `stride.yaml` at your project root:

```yaml
groups:
  dev:
    description: Local development
    commands:
      start:
        description: Start the API server
        run: "uvicorn app.main:app --reload"
      reset:
        description: Reset local database
        run: "python scripts/reset_db.py"

  test:
    description: Test suite
    commands:
      run:
        description: Run all tests
        run: "pytest"
      watch:
        description: Run tests in watch mode
        run: "pytest --watch"
```

Then:

```bash
stride list          # see all commands
stride run dev:start # run one
stride validate      # check your config
```

---

## CLI reference

```
stride list                     List all commands
stride list --verbose           Also show raw run strings
stride run <group:command>      Execute a command
stride validate                 Validate stride.yaml
stride --version                Print version
stride --help                   Print help
```

---

## stride.yaml reference

```yaml
groups:
  <group-name>:
    description: string        # optional — shown in stride list
    commands:
      <command-name>:
        description: string    # optional — shown in stride list
        run: string            # required — shell command to execute
```

**Naming rules:**
- Group and command names: lowercase letters, numbers, hyphens only
- No spaces
- Names must be unique within their scope

**All `run` strings execute via `sh -c`** — pipes, redirects, `&&`, and env vars all work as expected.

---

## Config discovery

Stride finds `stride.yaml` in this order:

1. `STRIDE_CONFIG` environment variable
2. `--config` CLI flag
3. `stride.yaml` in current directory
4. Walk up the directory tree until `.git` is found

You can run `stride` from any subdirectory in your repo — it will find the config.

---

## Error behaviour

- All errors exit with code 1
- Child process exit codes are forwarded exactly
- Typos get a fuzzy suggestion: `Did you mean: dev:start?`
- `Ctrl+C` cleanly stops the child process — no zombie processes

---

## License

MIT