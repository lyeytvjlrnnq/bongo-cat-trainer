# Bongo Cat Trainer — Memory Offsets (2026)

Reference offsets used by `bongo_cat_trainer` handlers. These are for the
current Bongo Cat build shipping on Steam as of early 2026. Update after
each game patch; the `scripts/pattern_dump.py` helper writes a fresh
`offsets.json` from the current constants.

| Module           | Symbol               | Offset       |
|------------------|----------------------|--------------|
| aim_assist       | target.x             | 0x00B4C8A0   |
| speed_modifier   | base_speed           | 0x00A13F20   |
| unlock_all       | unlock_flag          | 0x00C2F110   |
| unlock_all       | cosmetic_table[42]   | 0x00C2F200   |

## Notes

- Offsets shift on every minor patch — re-scan with `bongo_memscan.dll`.
- Speed patches are reverted automatically on `disable()`.
- `unlock_all` writes are non-persistent; they reset on restart.