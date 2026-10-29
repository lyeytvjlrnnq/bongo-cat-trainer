import subprocess
import sys
from pathlib import Path


def build() -> int:
    src = Path(__file__).resolve().parent.parent / "bongo_cat_trainer" / "native" / "bongo_memscan.cpp"
    out = src.parent / "bongo_memscan.dll"
    cmd = ["cl", "/LD", "/O2", str(src), f"/Fe:{out}"]
    print("Building native helper:", " ".join(cmd))
    return subprocess.call(cmd)


if __name__ == "__main__":
    sys.exit(build())