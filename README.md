# Hello Rasa — Session 1

A minimal Rasa assistant: say "hello world" and it replies. Everything here
is rule-based (no LLM calls yet), so it works whether or not your Rasa Pro
license has arrived.

## 1. Set up Python with `uv`

This project targets Python 3.10 or 3.11. Rasa Pro itself supports up to 3.13,
but the classic NLU pipeline used here (`config.yml`) relies on TensorFlow,
which doesn't yet support Python 3.12+. `uv` installs 3.10 for you without
touching your system Python:

```bash
uv python install 3.10
uv venv --python 3.10
```

Activate the environment:

```bash
source .venv/bin/activate        # macOS/Linux
.venv\Scripts\activate           # Windows (cmd/PowerShell)
```

## 2. Install Rasa

**Option A — Rasa Pro Developer Edition** (free; what the course uses from
Session 2 onward). Request a key at
[rasa.com/rasa-pro-developer-edition-license-key-request](https://rasa.com/rasa-pro-developer-edition-license-key-request)
— it's a plain public-PyPI install, no special index needed:

```bash
uv remove rasa
uv add rasa-pro
```

Then set your license key for this shell session:

```bash
export RASA_LICENSE="<your license key>"     # macOS/Linux
$env:RASA_LICENSE="<your license key>"        # Windows PowerShell
```

Rasa reads this from `RASA_LICENSE` specifically — `RASA_PRO_LICENSE` is a
common typo and is silently ignored.

(Or put it in a `.env` file — copy `.env.example` to `.env` and fill it in —
and load it with `export $(cat .env | xargs)` or a tool like `direnv`.)

**Option B — Rasa open source** (no signup required, fine for this exercise;
this is what's in `pyproject.toml` by default — a frozen/legacy release
last updated Jan 2025, so plan to move to Pro once your key arrives):

```bash
uv add rasa
```

## 3. Train and talk to it

```bash
rasa train
rasa shell
```

Try typing `hello world`, `hi`, and `bye`.

## 4. (Optional) Run the tests

```bash
rasa test
```

## Known issue: Apple Silicon + Rasa open source

On at least one Apple Silicon Mac, `rasa train` on Option B failed natively
with a TensorFlow/macOS error (`TypeError: Unable to convert function return
value...` or `SystemError: initialization of _pywrap_checkpoint_reader...`).
This is a native TensorFlow build issue, not a mistake in these project
files (they validate fine as plain YAML). It runs cleanly in a Linux
environment instead — use GitHub Codespaces (see `.devcontainer/`), or
Docker/Colima locally.

## Project layout

| File | Purpose |
|---|---|
| `domain.yml` | What the assistant can say and understand (intents, responses) |
| `data/nlu.yml` | Example phrasings for each intent, used to train the NLU model |
| `data/rules.yml` | Fixed intent → response mappings |
| `config.yml` | The NLU pipeline and dialogue policies used for training |
| `endpoints.yml` / `credentials.yml` | Where to run custom actions / which channels are enabled |
| `actions/actions.py` | Optional custom Python action (not wired up by default — see file) |
| `tests/test_stories.yml` | A couple of end-to-end conversation tests for `rasa test` |
