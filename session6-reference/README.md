# Session 6 Reference: Custom Actions, a Live API, and SQLite

This folder holds the exact, tested code from Session 6, for when you are stuck
and want to diff your own project against a known-working version rather than
retype something from the slides.

## What's in here

- `actions/actions.py` — the final `ActionTellJoke` and `ActionSearchTrains`.
- `domain/session6_additions.yml` — the `actions:`, `slots:`, and `responses:`
  entries these actions need. These are additions to merge into your existing
  domain file, not a replacement for it.
- `data/flows/search_trains.yml` — the complete, correct flow, including the
  branching syntax that only becomes obvious once you hit the training error.
- `seed_trains_db.sh` — one command to create and fill `trains.db` with the
  same four routes used in class.
- `tests/test_session6_e2e.yml` — a real, runnable end-to-end test. Run it with
  `uv run rasa test e2e tests/test_session6_e2e.yml` (action server running in
  its own terminal, as always) and you get a pass/fail against this exact
  behavior, not just a description of it.

## The single most common mistake: pasting instead of replacing

Almost every real error hit while building this session traced back to one
thing: pasting a new block into a file without deleting the old one. If your
domain file ends up with two `slots:` sections, or your flows file ends up
with two `flows:` sections, YAML will either silently keep only one of them
or refuse to load at all, and the error message rarely makes that obvious.

The fix is always the same: open the file, make sure each top-level key
(`slots:`, `flows:`, `responses:`, `actions:`) appears exactly once, and
replace that whole block rather than pasting above or below it.

## Other real mistakes from building this session

- **A branch with no `next: END`.** A step that only branches (an
  `if`/`then`/`else` with no `action` or `collect` of its own) is not valid by
  itself. The branching has to attach directly to the action step, and every
  terminal step inside every branch needs its own explicit `next: END`.
- **A `collect` step with no matching response.** `collect: origin` needs a
  `utter_ask_origin` response in the domain, or training fails outright.
- **Case-sensitive SQL matches.** `WHERE origin=?` is case-sensitive: typing
  `berlin` against a row stored as `Berlin` silently returns no row at all,
  not an error. The reference action uses `LOWER(origin)=LOWER(?)` on both
  columns for exactly this reason.
- **The action server isn't running.** `rasa inspect` alone is not enough,
  every custom action needs a second terminal running `rasa run actions` the
  whole time. If your action "does nothing," this is the first thing to check.
- **Reading the action server's own terminal, not just the bot's reply.** A
  traceback in that terminal is ground truth: it tells you exactly what broke
  and on which line, before you guess.

## If your code "looks right" but still won't run

The most useful thing you can install is not a package, it's an editor
setting. Make sure you have the official **Python extension (Microsoft)** in
VS Code, which bundles Pylance: it underlines indentation and syntax errors
in red before you ever run the file, which catches most "this looks fine to
me" bugs immediately.

Two settings worth matching across the whole class, so copy-pasted code never
silently mixes tabs and spaces:

```json
"editor.insertSpaces": true,
"editor.tabSize": 4,
"editor.renderWhitespace": "all"
```

If you want an extra, terminal-based check, `ruff` catches the same class of
problems from the command line:

```
uv add --dev ruff
uv run ruff check actions.py
```

Neither of these is required to finish the session's exercise. They exist so
that if your own file "looks right" and still refuses to run, you have a fast
way to find out why, rather than retyping it line by line.
