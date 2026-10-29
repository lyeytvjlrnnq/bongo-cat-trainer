"""Dump current Bongo Cat memory offsets used by the trainer modules."""
import json
import sys
from pathlib import Path

OFFSETS = {
    "aim_assist.target": 0x00B4C8A0,
    "speed.base": 0x00A13F20,
    "unlock.flag": 0x00C2F110,
    "unlock.cosmetics": 0x00C2F200,
}


def main() -> int:
    out = Path("docs") / "offsets.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(OFFSETS, indent=2))
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())