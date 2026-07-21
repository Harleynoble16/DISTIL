# DISTIL

Keyboard-first personal assistant for macOS with accessibility-focused eye and gesture controls.

## Project structure

- `Main.py`: command-line entry point.
- `distil_gui.py`: PySide6 desktop interface.
- `distil_engine.py`: commands, automation and accessibility features.
- `assets/icons`: application icons and artwork.
- `assets/sounds`: interface sounds.
- `assets/vision`: computer-vision resources.
- `assets/models`: future local models.
- `user_data`: private calibration, face, note and capture data. This folder is excluded from Git.
- `build` and `dist`: generated packaging output. These folders are excluded from Git.

Personal data should remain local and must not be committed to source control.

## Setup

DISTIL currently targets macOS and Python 3.12 or later.

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
python3 Main.py
```

macOS may ask for Accessibility, Camera and Screen Recording permissions when
the related controls are first used.
