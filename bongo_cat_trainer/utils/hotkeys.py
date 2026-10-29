import ctypes
import logging
from typing import Callable, Dict

user32 = ctypes.WinDLL("user32", use_last_error=True)
MOD_NOREPEAT = 0x4000
WM_HOTKEY = 0x0312


class HotkeyManager:
    def __init__(self) -> None:
        self.log = logging.getLogger(__name__)
        self._bindings: Dict[int, Callable[[], None]] = {}
        self._next_id = 1

    def register(self, vk: int, callback: Callable[[], None]) -> int:
        hk_id = self._next_id
        self._next_id += 1
        if not user32.RegisterHotKey(None, hk_id, MOD_NOREPEAT, vk):
            self.log.warning("RegisterHotKey failed for vk=%d", vk)
            return -1
        self._bindings[hk_id] = callback
        return hk_id

    def dispatch(self, hk_id: int) -> None:
        cb = self._bindings.get(hk_id)
        if cb:
            try:
                cb()
            except Exception as exc:
                self.log.error("Hotkey handler error: %s", exc)