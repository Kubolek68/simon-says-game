# Simon Says

A standalone Simon Says memory game built with Python's standard-library
`tkinter` module. No third-party packages are required.

## Features

- Dark-mode desktop interface
- Resizable application window
- Configurable grid sizes from 2x2 through 6x6
- Slow, Normal, and Fast playback speeds
- White tiles with high-contrast bright-red sequence highlighting
- Classic mode: every level keeps the previous sequence and adds one tile
- Random sequence mode: every level creates a new random sequence one tile longer
- Playback gets slightly faster as the score increases
- Wrong input ends the game and shows the final score inside the app

## Run

```powershell
python simon_says.py
```

On Windows, run `install_shortcut.ps1` once to create a desktop shortcut with
the included Simon Says icon:

```powershell
powershell -ExecutionPolicy Bypass -File .\install_shortcut.ps1
```
