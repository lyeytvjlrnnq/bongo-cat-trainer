import logging
import threading
from typing import Optional

from bongo_cat_trainer.core.process_attach import ProcessAttacher
from bongo_cat_trainer.handlers.auto_tapper import AutoTapper
from bongo_cat_trainer.handlers.aim_assist import AimAssist
from bongo_cat_trainer.handlers.speed_modifier import SpeedModifier
from bongo_cat_trainer.handlers.unlock_all import UnlockAll


class TrainerEngine:
    def __init__(self, attacher: ProcessAttacher, settings) -> None:
        self.log = logging.getLogger(__name__)
        self.attacher = attacher
        self.settings = settings
        self._lock = threading.RLock()
        self._running = False
        self.modules = {
            "auto_tapper": AutoTapper(attacher),
            "aim_assist": AimAssist(attacher),
            "speed_modifier": SpeedModifier(attacher),
            "unlock_all": UnlockAll(attacher),
        }
        self.log.info("Trainer engine initialized with %d modules", len(self.modules))

    def toggle_module(self, name: str, enabled: bool) -> bool:
        with self._lock:
            module = self.modules.get(name)
            if module is None:
                self.log.error("Unknown module: %s", name)
                return False
            if enabled:
                module.enable()
            else:
                module.disable()
            self.log.info("Module %s -> %s", name, enabled)
            return True

    def start(self) -> None:
        if self._running:
            return
        self._running = True
        for module in self.modules.values():
            if module.enabled:
                module.start()

    def shutdown(self) -> None:
        self.log.info("Shutting down trainer engine")
        self._running = False
        for module in self.modules.values():
            try:
                module.disable()
            except Exception as exc:
                self.log.warning("Module shutdown error: %s", exc)