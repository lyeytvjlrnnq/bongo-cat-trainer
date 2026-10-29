import tkinter as tk
from tkinter import ttk
import logging

from bongo_cat_trainer.core.trainer_engine import TrainerEngine


class OverlayWindow:
    def __init__(self, engine: TrainerEngine, settings) -> None:
        self.log = logging.getLogger(__name__)
        self.engine = engine
        self.settings = settings
        self.root = tk.Tk()
        self.root.title("Bongo Cat Trainer 2026")
        self.root.geometry("420x360")
        self.root.attributes("-topmost", True)
        self._build()

    def _build(self) -> None:
        header = ttk.Label(self.root, text="Bongo Cat Cheats & Trainers for PC", font=("Segoe UI", 12, "bold"))
        header.pack(pady=8)

        self.vars = {}
        for name in self.engine.modules:
            var = tk.BooleanVar(value=False)
            cb = ttk.Checkbutton(
                self.root,
                text=name.replace("_", " ").title(),
                variable=var,
                command=lambda n=name, v=var: self.engine.toggle_module(n, v.get()),
            )
            cb.pack(anchor="w", padx=20, pady=2)
            self.vars[name] = var

        ttk.Separator(self.root).pack(fill="x", pady=8)
        ttk.Label(self.root, text="Hotkey: F8 toggle overlay | F9 panic").pack(anchor="w", padx=20)

    def run(self) -> None:
        self.log.info("Overlay window starting")
        self.root.mainloop()