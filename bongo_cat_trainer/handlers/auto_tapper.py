import time
import threading
import logging

from bongo_cat_trainer.core.process_attach import ProcessAttacher
from bongo_cat_trainer.utils.key_sender import send_key


class AutoTapper:
    def __init__(self, attacher: ProcessAttacher, cps: int = 20) -> None:
        self.log = logging.getLogger(__name__)
        self.attacher = attacher
        self.cps = cps
        self.enabled = False
        self._thread: threading.Thread | None = None
        self._stop = threading.Event()

    def enable(self) -> None:
        if self.enabled:
            return
        self.enabled = True
        self._stop.clear()
        self._thread = threading.Thread(target=self._loop, daemon=True, name="auto-tapper")
        self._thread.start()

    def disable(self) -> None:
        self.enabled = False
        self._stop.set()
        if self._thread:
            self._thread.join(timeout=1.0)
            self._thread = None

    def start(self) -> None:
        self.enable()

    def _loop(self) -> None:
        interval = 1.0 / max(self.cps, 1)
        while not self._stop.is_set():
            if self.attacher.handle:
                send_key(0x20)  # SPACE — bongo tap
            time.sleep(interval)