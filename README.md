# Hello Rasa — Session 1

A minimal Rasa assistant: say "hello world" and it replies. Everything here
is rule-based (no LLM calls yet), so it works whether or not your Rasa Pro
license has arrived.

## Quick start — GitHub Codespaces (no install needed)

If the local setup below gives you trouble — especially on Apple Silicon, see the
"Known issue" note near the bottom — skip it entirely and run this in the browser:

1. Click **Use this template ▸ Create a new repository**. Name it `hello_rasa`.
   This is *your* copy, so you're not editing the course repo.
2. In **your** new repo, click **Code ▸ Codespaces ▸ Create codespace on main**.
3. **Wait for setup to finish before typing anything — this takes about 5
   minutes, and VS Code hands you a terminal well before it's done.** The
   container itself builds in about a minute; installing Rasa (which pulls in
   TensorFlow) takes several more. You'll know it's finished when a `.venv`
   folder appears in the file list on the left, and the **GitHub Codespaces**
   tab in the terminal panel stops printing.
4. Once setup is done, in the Codespace terminal:

   ```bash
   source .venv/bin/activate
   rasa train
   rasa shell
   ```

5. Type `hello world`, `hi`, or `bye`. Press Ctrl-C to exit.

   > **If you see `AttributeError: module 'numpy' has no attribute
   > 'VisibleDeprecationWarning'`** — you started too early and setup was
   > still running. Nothing is broken. Wait for `.venv` to appear, then run
   > the commands again.

6. **Stop your codespace when you're done**, at
   [github.com/codespaces](https://github.com/codespaces) (**⋯ ▸ Stop codespace**).
   An idle codespace keeps consuming your free monthly hours until it times out.

Everything below is the local install, if you'd rather work on your own machine.

---

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
