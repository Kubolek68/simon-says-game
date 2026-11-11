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

## How GitHub commits and Contributions work

- A commit is one saved change in Git history. It can contain one line or many
  files; the number of changed lines does not determine the number of commits.
- The commit must use an email address connected to the author's GitHub account.
- Commits usually appear on the contribution graph when they are pushed to the
  repository's default branch or included in a merged pull request.
- A private repository's activity is only shown on the profile when private
  contributions are enabled in GitHub profile settings.
- Creating many empty or meaningless commits is not a useful way to measure
  progress. Separate commits are best used for separate, understandable
  changes, such as a code fix followed by its documentation.

## GitHub profile names

GitHub supports a unique **username** such as `mlpawelcodes` and a separate
public **Name** field. You can use `Kaszub` as the Name, or put it in your
profile bio, while keeping your legal first and last name private. The
username is used in profile and repository URLs; the Name is only a display
label and does not have to match it.
