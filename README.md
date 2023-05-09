# Bakalárska práca - Odmazávanie titulkov z videa

Autor: Emma Krompaščíková
Akademický rok: 2022/23

## Štruktúra repozitára
CD-ROM
|-app/
| |-resources/
| | |-app/     
| |   |-delete_subtitles.py
| |   |-index.html
| |   |-mais.js
| |   |-package.json
| |   |-renderer.js
| |   |-requirements.txt
| |-Subtitles_remover_8_5.exe
|-LaTeX/
|-README.md
|-videos/
| |-removed_subtitles/
| | |-video1_gauss.mp4
| | |-video1_median.mp4
| | |-video1_ns.mp4
| | |-video1_remove_all_median.mp4
| | |-video1_telea.mp4
| | |-video2_gaus.mp4
| | |-video2_median.mp4
| | |-video2_ns.mp4
| | |-video2_remove_all_median.mp4
| | |-video2_telea.mp4
| |-with_subtitles/
|   |-video1.mp4
|   |-video2.mp4
|   |-video3.mp4
|   |-video4.mp4
|-video.mp4

## Závislosti
- OS Windows 10
- Python >=3.8 a <3.10
- Node.js 14

## Spustenie aplikácie
Je odporúčané vytvoriť samostatný priečinok pre nainštalovanie virtuálneho prostredia.
Po navigácii do vytvoreného priečinka je potrebné vytvoriť spomenuté virtuálne prostredie príkazom `python -m venv .` a následne ho aktivovať príkazom `.\Scripts\activate.bat` . Je potrebné overiť či je nainštalovaná najnovšia verzia pip a poprípade ju aktualizovať príkazom `python -m pip install --upgrade pip`. Ďalej je potrebné prejsť do priečinku 'resources' a následne do 'app' a príkazom `pip install -r requirements.txt` nainštalovať potrebné balíky. Po doinštalovaní je potrebné vrátiť sa späť do hlavného priečinku obsahujúceho .exe aplikáciu a spustiť ju. Pre podrobnejšie informácie je možné otvoriť v aplikácii konzolu stlačením kláves `Ctrl + Shift + I`. Po dokončení a vypnutí  aplikácie je potrebné vypnúť virtuálne prostredie príkazom `deactivate`.

## Spustenie aplikácie zo zdrojového kódu vo vývojárskom režime
Zdrojový kód aplikácie sa nachádza v priečinku app/resources/app. Aplikácia je spustiteľná vo vývojárskom režime po inštalácií závislostí jazyka Python uložených v requirements.txt a závislostí Node.js uložených v súbore package.json.

`pip install -r requirements.txt`
`npm install`

Aplikácia sa následne dá spustiť pomocou príkazu `npm run start`.

## Použité knižnice
Okrem knižníc uvedených v package.json a requirements.txt bola použitá aj knižnica toastr na plávajúce notifikácie (https://github.com/codeseven/toastr).
