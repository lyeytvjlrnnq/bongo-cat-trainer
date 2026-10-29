import logging

from bongo_cat_trainer.core.process_attach import ProcessAttacher
from bongo_cat_trainer.utils.memory_reader import write_byte


UNLOCK_FLAG_OFFSET = 0x00C2F110
COSMETIC_TABLE_OFFSET = 0x00C2F200
COSMETIC_COUNT = 42


class UnlockAll:
    def __init__(self, attacher: ProcessAttacher) -> None:
        self.log = logging.getLogger(__name__)
        self.attacher = attacher
        self.enabled = False

    def enable(self) -> None:
        if not self.attacher.handle:
            self.log.error("No process handle, cannot unlock cosmetics")
            return
        write_byte(self.attacher.handle, UNLOCK_FLAG_OFFSET, 1)
        for i in range(COSMETIC_COUNT):
            write_byte(self.attacher.handle, COSMETIC_TABLE_OFFSET + i, 1)
        self.enabled = True
        self.log.info("Unlocked %d cosmetic slots for Bongo Cat", COSMETIC_COUNT)

    def disable(self) -> None:
        self.enabled = False

    def start(self) -> None:
        self.enable()