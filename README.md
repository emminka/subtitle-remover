# Bakalárska práca - Odmazávanie titulkov z videa

Spustiteľná aplikácia na stiahnutie je dostupná na https://drive.google.com/drive/folders/1WVaxNCP269B1vbV8axTeqS_w3hCQijUm?usp=sharing .

<b>Návod pre non-IT people:</b>

Aplikácia je vhodná pre Windows 10. Požaduje mať nainštalovaný Python vo verzii >=3.8 a <3.10. Stiahnuť a nainštalovať Python je možné po kliknutí na nasledujúci odkaz: https://www.python.org/ftp/python/3.9.2/python-3.9.2-amd64.exe. Po stiahnutí je potrebné otvoriť spomenutý súbor, na spodnej časti okna zakliknúť možnosť <i>Add python.exe to PATH</i> a následne kliknúť na <i>Install Now</i> vyššie v okne. Python sa nainštaluje, je potrebné povoliť vykonávať zmeny v zariadení. Po správe <i>Setup was successfull</i> je možné zatvoriť okno.

Teraz je pre lepšiu prehladnosť vhodné vytvoriť si nový priečinok na pracovnej ploche. Pravým tlačidlom myši je potrebné kliknúť na voľné miesto na pracovnej ploche, prejsť na <i>Nový</i> a kliknúť na <i>Priečinok</i>. Je možné ho pomenovať ľubovoľne, no odporúčam zvoliť názov 'virtual_env'. Stiahnutú a rozbalenú aplikáciu je potrebné presunúť do vytvoreného priečinka. Po stisknutí kláves `Win + R`, sa objaví okno, kde zadáte `cmd` a stisknete Enter. Po otvorení Príkazového riadku, je potrebné doň zadať príkaz `cd Desktop`, čím sa presunieme na pracovnú plochu. Následne je potrebné zadať `cd virtual_env`, čím sa presunieme do skôr vytvoreného priečinku. <b>Tip:</b> automatické dopĺňanie slov je možné po stisknutí klávesy <i>Tab</i>.

Teraz v priečinku cez Príkazový riadok nainštalujeme virtuálne prostredie. Napíšeme príkaz `python -m venv .`, počkáme kým sa vykoná a následne napíšeme príkaz `.\Scripts\activate.bat` . Týmto sme si aktivovali virtuálne prostredie, a vidíme, že na začiatku riadku je napísané (virtual_env).

Príkazom `python -m pip install --upgrade pip` overíme, či máme najnovšiu pip verziu. Ak nie, nainštaluje sa. Teraz prejdeme cez Príkazový riadok do priečinku aplikácie príkazom `cd <nazovapky>` a ďalej napíšeme príkaz `pip install -r .\resources\app\requirements.txt` čím sa nainštalujú potrebné balíčky pre funkčnosť aplikácie. Po nainštalovaní napíšeme do príkazoveho riadku `<nazovapky>.exe` a tým sa aplikácia spustí. Pre podrobnejšie informácie je možné otvoriť v aplikácii konzolu stlačením kláves `Ctrl + Shift + I`. Po vypnutí aplikácie deaktivujeme virtuálne prostredie príkazom `deactivate`.


<b>Návod pre IT people:</b>

Potrebný Windows 10 a Python >=3.8 no zároveň <3.10
Pre lepšiu prehľadnosť je odporúčané vytvoriť samostatný priečinok pre nainštalovanie virtuálneho prostredia.
Po navigácii do vytvoreného priečinka je potrebné nainštalovať spomenuté virtuálne prostredie príkazom `python -m venv .` a následne ho aktivovať príkazom `.\Scripts\activate.bat` . Je potrebné overiť či je nainštalovaná najnovšia verzia pip a poprípade ju aktualizovať príkazom `python -m pip install --upgrade pip`.  Stiahnutú aplikáciu je potrebné rozbaliť, a terminálom so zapnutým virtuálnym prostredím otvoriť súbor obsahujúci .exe aplikáciu. Ďalej je potrebné prejsť do priečinku 'resources' a následne do 'app' a príkazom `pip install -r requirements.txt` nainštalovať potrebné balíky. Po doinštalovaní je potrebné vrátiť sa späť do hlavného priečinku obsahujúceho .exe aplikáciu a spustiť ju. Po dokončení a vypnutí  aplikácie je potrebné vypnúť virtuálne prostredie príkazom `deactivate`.






poznamky:
otvor si prikazovy riadok 

python -m venv <path/to/venv> - na vytvorenie virtualneho prsoterdia
<path/to/venv>\Scripts\activate.bat

cd subtitleremover

vo virtual prostredi pip install pywin32 na otvorenie konzolky
python -m pip install --upgrade pip

pip install -r requiremetns

ked po vsetkom napis deactivate
