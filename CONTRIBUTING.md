# Contributing to bongo-cat-trainer

Thanks for wanting to help build Bongo Cat cheats & trainers for PC.

## Scope

- New trainer modules go in `bongo_cat_trainer/handlers/`.
- Every handler must implement `enable()`, `disable()`, `start()` and
  expose an `enabled: bool`.
- Register new handlers in `TrainerEngine.modules` and add a matching
  entry to `docs/offsets.md`.

## Offsets

Offsets are version-specific. If you update offsets after a Bongo Cat
patch, bump `bongo_cat_trainer.__version__` and note the game build
in your PR description.

## Native helpers

`bongo_memscan.cpp` is built with `scripts/build_native.py` (MSVC `cl`).
Only add native code when a pure-Python ReadProcessMemory loop is too
slow for the pattern.

## Testing

```
python -m pytest tests/
```

Tests must not require an actual running Bongo Cat process — mock the
attacher (`MagicMock(handle=1)`).

## Legal

This project is for educational and single-player modding use only.
Do not submit PRs that target multiplayer/anti-cheat bypasses.