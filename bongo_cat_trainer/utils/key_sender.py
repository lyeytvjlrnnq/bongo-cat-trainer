import ctypes
from ctypes import wintypes

user32 = ctypes.WinDLL("user32", use_last_error=True)
KEYEVENTF_KEYUP = 0x0002


def send_key(vk_code: int, hold_ms: int = 15) -> None:
    user32.keybd_event(vk_code, 0, 0, 0)
    ctypes.windll.kernel32.Sleep(hold_ms)
    user32.keybd_event(vk_code, 0, KEYEVENTF_KEYUP, 0)


def send_mouse_move(dx: int, dy: int) -> None:
    user32.mouse_event(0x0001, dx, dy, 0, 0)