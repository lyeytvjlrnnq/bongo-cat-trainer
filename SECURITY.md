# Security Policy

## Reporting

If you find a vulnerability in `bongo-cat-trainer` — e.g. an offset
write that can corrupt the host process, a DLL-loading flaw in
`bongo_memscan.cpp`, or a settings-file injection — please open a
private advisory via GitHub rather than a public issue.

## Threat model

- The trainer requires `PROCESS_ALL_ACCESS` on `BongoCat.exe`. It does
  not request admin elevation and does not install to `System32`.
- Settings are stored in `~/.bongo-cat-trainer/settings.json` and
  parsed as JSON only — no `eval`, no imports from config.
- Logs are written to `~/.bongo-cat-trainer/logs/trainer.log` and
  never include memory dumps.

## Out of scope

Bypassing anti-cheat, kernel drivers, and spoofer features are
explicitly out of scope for this repo.