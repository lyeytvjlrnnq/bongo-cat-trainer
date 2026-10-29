from unittest.mock import MagicMock
from bongo_cat_trainer.core.trainer_engine import TrainerEngine


def test_toggle_unknown_module_returns_false():
    attacher = MagicMock(handle=1)
    settings = MagicMock()
    engine = TrainerEngine(attacher=attacher, settings=settings)
    assert engine.toggle_module("does_not_exist", True) is False


def test_toggle_known_module_calls_enable():
    attacher = MagicMock(handle=1)
    settings = MagicMock()
    engine = TrainerEngine(attacher=attacher, settings=settings)
    module = engine.modules["auto_tapper"]
    module.enable = MagicMock()
    module.disable = MagicMock()
    assert engine.toggle_module("auto_tapper", True) is True
    module.enable.assert_called_once()