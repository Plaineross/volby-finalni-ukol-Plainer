# Volební scraper 2017

Scraper výsledků parlamentních voleb z roku 2017. Zadáš odkaz na okres z volby.cz a on ti stáhne výsledky všech obcí do CSV souboru.

## Instalace

```
pip install -r requirements.txt
```

## Spuštění

```
python Finalniukol_prog_Plainer.py <odkaz> <nazev_souboru.csv>
```

## Ukázka

```
python Finalniukol_prog_Plainer.py "https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103" vysledky_prostejov.csv
```

Program postupně stahuje data z každé obce a na konci uloží všechno do CSV. Každý řádek = jedna obec, sloupce jsou kód obce, název, počet voličů, vydané obálky, platné hlasy a pak hlasy pro každou stranu zvlášť.
