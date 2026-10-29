import logging
import math
from typing import Optional, Tuple

from bongo_cat_trainer.core.process_attach import ProcessAttacher
from bongo_cat_trainer.utils.memory_reader import read_float


class AimAssist:
    def __init__(self, attacher: ProcessAttacher, smoothing: float = 0.35) -> None:
        self.log = logging.getLogger(__name__)
        self.attacher = attacher
        self.smoothing = smoothing
        self.enabled = False
        self.target_offset = 0x00B4C8A0

    def enable(self) -> None:
        self.enabled = True
        self.log.info("Aim assist enabled (smoothing=%.2f)", self.smoothing)

    def disable(self) -> None:
        self.enabled = False

    def start(self) -> None:
        self.enable()

    def compute_delta(self, cursor: Tuple[float, float], target: Tuple[float, float]) -> Tuple[float, float]:
        dx = target[0] - cursor[0]
        dy = target[1] - cursor[1]
        return dx * self.smoothing, dy * self.smoothing

    def read_target(self) -> Optional[Tuple[float, float]]:
        if not self.enabled or not self.attacher.handle:
            return None
        x = read_float(self.attacher.handle, self.target_offset)
        y = read_float(self.attacher.handle, self.target_offset + 0x4)
        if x is None or y is None:
            return None
        if math.isnan(x) or math.isnan(y):
            return None
        return x, y