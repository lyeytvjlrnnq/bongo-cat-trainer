import json
import logging
from dataclasses import dataclass, field, asdict
from pathlib import Path


CONFIG_PATH = Path.home() / ".bongo-cat-trainer" / "settings.json"


@dataclass
class Settings:
    target_process: str = "BongoCat.exe"
    auto_tapper_cps: int = 20
    aim_smoothing: float = 0.35
    speed_multiplier: float = 3.0
    enable_overlay: bool = True
    hotkey_toggle: str = "F8"
    hotkey_panic: str = "F9"
    modules: dict = field(default_factory=dict)


def load_settings() -> Settings:
    log = logging.getLogger(__name__)
    if not CONFIG_PATH.exists():
        CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
        defaults = Settings()
        CONFIG_PATH.write_text(json.dumps(asdict(defaults), indent=2), encoding="utf-8")
        return defaults
    try:
        data = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
        return Settings(**{k: v for k, v in data.items() if k in Settings.__dataclass_fields__})
    except Exception as exc:
        log.warning("Failed to load settings, using defaults: %s", exc)
        return Settings()


def save_settings(settings: Settings) -> None:
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    CONFIG_PATH.write_text(json.dumps(asdict(settings), indent=2), encoding="utf-8")