import ctypes
from ctypes import wintypes
from typing import Optional

kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)


def _read(handle: int, address: int, buffer: ctypes.Array) -> bool:
    read = ctypes.c_size_t(0)
    ok = kernel32.ReadProcessMemory(
        wintypes.HANDLE(handle),
        ctypes.c_void_p(address),
        ctypes.byref(buffer),
        ctypes.sizeof(buffer),
        ctypes.byref(read),
    )
    return bool(ok)


def _write(handle: int, address: int, buffer: ctypes.Array) -> bool:
    written = ctypes.c_size_t(0)
    ok = kernel32.WriteProcessMemory(
        wintypes.HANDLE(handle),
        ctypes.c_void_p(address),
        ctypes.byref(buffer),
        ctypes.sizeof(buffer),
        ctypes.byref(written),
    )
    return bool(ok)


def read_float(handle: int, address: int) -> Optional[float]:
    buf = ctypes.c_float(0.0)
    return buf.value if _read(handle, address, buf) else None


def write_float(handle: int, address: int, value: float) -> bool:
    return _write(handle, address, ctypes.c_float(value))


def write_byte(handle: int, address: int, value: int) -> bool:
    return _write(handle, address, ctypes.c_ubyte(value))