import sys
import logging
from pathlib import Path

from bongo_cat_trainer.core.trainer_engine import TrainerEngine
from bongo_cat_trainer.core.process_attach import ProcessAttacher
from bongo_cat_trainer.ui.overlay_window import OverlayWindow
from bongo_cat_trainer.config.settings import load_settings


def setup_logging() -> None:
    log_dir = Path.home() / ".bongo-cat-trainer" / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[
            logging.FileHandler(log_dir / "trainer.log", encoding="utf-8"),
            logging.StreamHandler(sys.stdout),
        ],
    )


def main() -> int:
    setup_logging()
    log = logging.getLogger("bongo-cat-trainer")
    log.info("Bongo Cat Trainer 2026 booting")

    settings = load_settings()
    attacher = ProcessAttacher(process_name=settings.target_process)
    if not attacher.attach():
        log.warning("Bongo Cat process not found, waiting for attach")

    engine = TrainerEngine(attacher=attacher, settings=settings)
    overlay = OverlayWindow(engine=engine, settings=settings)
    try:
        overlay.run()
    except KeyboardInterrupt:
        log.info("Interrupted by user")
    finally:
        engine.shutdown()
        attacher.detach()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())