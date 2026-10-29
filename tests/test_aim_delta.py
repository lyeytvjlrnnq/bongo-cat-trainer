from unittest.mock import MagicMock
from bongo_cat_trainer.handlers.aim_assist import AimAssist


def test_compute_delta_smooths():
    assist = AimAssist(attacher=MagicMock(), smoothing=0.5)
    dx, dy = assist.compute_delta((100.0, 100.0), (120.0, 80.0))
    assert dx == 10.0
    assert dy == -10.0