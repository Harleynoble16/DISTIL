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
