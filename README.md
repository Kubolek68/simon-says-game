# Simon Says

A standalone Simon Says memory game built with Python's standard-library
`tkinter` module. No third-party packages are required.

## Features

- Dark-mode desktop interface
- Configurable grid sizes from 2x2 through 6x6
- Slow, Normal, and Fast playback speeds
- The sequence starts with one random button
- Every successful level appends exactly one new random button
- Playback gets slightly faster as the score increases
- Wrong input ends the game and shows the final score

## Run

```powershell
python simon_says.py
```

On Windows, run `install_shortcut.ps1` once to create a desktop shortcut with
the included Simon Says icon:

```powershell
powershell -ExecutionPolicy Bypass -File .\install_shortcut.ps1
```
