# DISTIL

An experimental macOS desktop assistant exploring keyboard, eye-tracking and
gesture controls as alternatives to voice-first interaction.

> **Project status:** active prototype. DISTIL is a personal learning project,
> not production-ready assistive software.

## Why I built it

Many digital assistants assume that speech is the easiest input method for every
user. DISTIL explores a different approach. It brings common desktop actions
into one keyboard-first interface while testing eye and gesture interactions
that may reduce repeated physical input.

The project does not assume that one interface fits everyone. Its long-term
direction is to evaluate features with users before making accessibility claims.

## Current features

- PySide6 desktop interface with live Mac status information.
- Keyboard commands for opening apps and websites, typing text and taking notes.
- Spotify search and media controls through macOS automation.
- OpenCV-based gesture detection, face detection and eye calibration experiments.
- Screenshot, focus and study utilities.
- Local storage for calibration and user data, excluded from Git.

## Technology

- Python 3.12+
- PySide6
- OpenCV
- PyAutoGUI
- psutil
- AppleScript and macOS command-line tools

## Setup

DISTIL currently targets macOS.

```bash
git clone https://github.com/Harleynoble16/DISTIL.git
cd DISTIL
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
python3 Main.py
```

macOS may ask for Accessibility, Camera and Screen Recording permissions when
the related controls are first used.

## Example commands

```text
open notes and type hello
google accessible interface design
search spotify linkin park
gesture
eye calibrate
eye
status
make note
```

## Privacy and safety

Calibration data, screenshots, notes and other personal information stay in
`user_data`, which is excluded from version control. Generated builds, virtual
environments and IDE settings are also excluded.

Camera-based features run locally. Review the code and macOS permissions before
using automation features. Do not rely on this prototype for safety-critical
tasks.

## Project structure

```text
DISTIL/
├── Main.py             # Application entry point
├── distil_gui.py       # PySide6 desktop interface
├── distil_engine.py    # Commands and accessibility experiments
├── assets/             # Icons, sounds and vision resources
├── user_data/          # Private local data, excluded from Git
└── requirements.txt    # Python dependencies
```

## Roadmap

- Separate commands into smaller, testable modules.
- Add automated tests for command parsing and non-GUI functions.
- Improve error handling and configuration.
- Measure eye and gesture interaction accuracy.
- Add user-controlled sensitivity and input settings.
- Document a small usability evaluation before making accessibility claims.

## What I am learning

DISTIL is helping me develop practical skills in Python application design,
computer vision, human-computer interaction, macOS automation and responsible
accessibility-focused development.
