# Architecture

```
bongo_cat_trainer/
  main.py                 bootstrap entry (attach, engine, overlay)
  core/
    process_attach.py     OpenProcess + tasklist discovery
    trainer_engine.py     module registry + toggle dispatch
  handlers/               one module per cheat/trainer feature
    auto_tapper.py        spacebar autoclicker (CPS configurable)
    aim_assist.py         target read + smoothed delta
    speed_modifier.py     base speed patch with revert
    unlock_all.py         cosmetic flag writer
  ui/
    overlay_window.py     tkinter overlay, topmost
  config/
    settings.py           JSON settings in ~/.bongo-cat-trainer
  utils/
    memory_reader.py      ReadProcessMemory / WriteProcessMemory wrappers
    key_sender.py         keybd_event helper
    hotkeys.py            RegisterHotKey manager
  native/
    bongo_memscan.cpp     pattern scan DLL (optional)
```

## Module contract

Every handler exposes `enable()`, `disable()`, `start()` and an `enabled`
attribute. `TrainerEngine.toggle_module(name, on)` is the only entry
point the UI is allowed to call.

## Process model

The bootstrap attaches once at startup. If Bongo Cat is not running the
trainer enters a wait loop and the overlay shows "not attached". Panic
key (F9) disables every module and detaches.