import logging

from bongo_cat_trainer.core.process_attach import ProcessAttacher
from bongo_cat_trainer.utils.memory_reader import read_float, write_float


BASE_SPEED_OFFSET = 0x00A13F20
DEFAULT_SPEED = 1.0


class SpeedModifier:
    def __init__(self, attacher: ProcessAttacher, multiplier: float = 3.0) -> None:
        self.log = logging.getLogger(__name__)
        self.attacher = attacher
        self.multiplier = multiplier
        self.enabled = False
        self._original: float | None = None

    def enable(self) -> None:
        if not self.attacher.handle:
            self.log.error("Cannot enable speed modifier without process handle")
            return
        self._original = read_float(self.attacher.handle, BASE_SPEED_OFFSET) or DEFAULT_SPEED
        write_float(self.attacher.handle, BASE_SPEED_OFFSET, self._original * self.multiplier)
        self.enabled = True
        self.log.info("Speed x%.2f applied (was %.2f)", self.multiplier, self._original)

    def disable(self) -> None:
        if not self.enabled or not self.attacher.handle:
            return
        if self._original is not None:
            write_float(self.attacher.handle, BASE_SPEED_OFFSET, self._original)
        self.enabled = False
        self.log.info("Speed modifier reverted")

    def start(self) -> None:
        self.enable()