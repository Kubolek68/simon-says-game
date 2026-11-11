# Simon Says

Prosta gra typu Simon Says napisana w Pythonie z użyciem `tkinter`.
Nie trzeba instalować dodatkowych bibliotek.

## Co jest w środku

- plansza od 2x2 do 6x6,
- dwa tryby gry: klasyczny i losowa sekwencja,
- wybór prędkości,
- białe kafelki, które podczas pokazu robią się czerwone,
- wynik i komunikat o przegranej w głównym oknie,
- możliwość zmiany rozmiaru okna,
- skrót na pulpicie z własną ikoną w Windows.

## Uruchomienie

W PowerShellu przejdź do folderu projektu i wpisz:

```powershell
python simon_says.py
```

Jeśli chcesz utworzyć skrót na pulpicie:

```powershell
powershell -ExecutionPolicy Bypass -File .\install_shortcut.ps1
```

W trybie klasycznym kolejny poziom zachowuje poprzednią sekwencję i dodaje
jeden kafelek. W trybie losowym cała sekwencja jest układana od nowa, ale
również zwiększa się o jeden element.
