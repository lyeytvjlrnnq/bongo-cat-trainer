import ctypes
import logging
from ctypes import wintypes
from typing import Optional

kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
PROCESS_ALL_ACCESS = 0x1F0FFF


class ProcessAttacher:
    def __init__(self, process_name: str = "BongoCat.exe") -> None:
        self.log = logging.getLogger(__name__)
        self.process_name = process_name
        self.pid: Optional[int] = None
        self.handle: Optional[int] = None

    def _find_pid(self) -> Optional[int]:
        import subprocess
        try:
            out = subprocess.check_output(
                ["tasklist", "/FI", f"IMAGENAME eq {self.process_name}", "/FO", "CSV", "/NH"],
                text=True,
                creationflags=0x08000000,
            )
        except Exception as exc:
            self.log.error("tasklist failed: %s", exc)
            return None
        for line in out.splitlines():
            parts = [p.strip('"') for p in line.split(",")]
            if len(parts) >= 2 and parts[0].lower() == self.process_name.lower():
                try:
                    return int(parts[1])
                except ValueError:
                    continue
        return None

    def attach(self) -> bool:
        pid = self._find_pid()
        if pid is None:
            self.log.warning("Process %s not running", self.process_name)
            return False
        handle = kernel32.OpenProcess(PROCESS_ALL_ACCESS, False, pid)
        if not handle:
            self.log.error("OpenProcess failed, err=%s", ctypes.get_last_error())
            return False
        self.pid = pid
        self.handle = handle
        self.log.info("Attached to %s (pid=%d)", self.process_name, pid)
        return True

    def detach(self) -> None:
        if self.handle:
            kernel32.CloseHandle(self.handle)
            self.handle = None
            self.pid = None
            self.log.info("Detached from Bongo Cat")