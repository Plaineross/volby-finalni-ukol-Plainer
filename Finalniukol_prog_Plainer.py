"""
projekt_3.py: třetí projekt
author: Jan Plainer
email: plain67529@mot.sps-dopravni.cz
discord: COGYsek
"""
 
import requests
from bs4 import BeautifulSoup
import csv
import sys
 
 
def get_obce_links(url):
    response = requests.get(url)
    response.encoding = "utf-8"
    soup = BeautifulSoup(response.text, "html.parser")
 
    obce = []
    tabulky = soup.find_all("table")
 
    for tabulka in tabulky:
        radky = tabulka.find_all("tr")
        for radek in radky:
            bunky = radek.find_all("td")
            if len(bunky) >= 2:
                odkaz_tag = bunky[0].find("a")
                if odkaz_tag:
                    kod = bunky[0].text.strip()
                    nazev = bunky[1].text.strip()
                    href = odkaz_tag["href"]
                    plny_odkaz = "https://volby.cz/pls/ps2017nss/" + href
                    obce.append((kod, nazev, plny_odkaz))
 
    return obce
 
 
def get_data_obce(url):
    response = requests.get(url)
    response.encoding = "utf-8"
    soup = BeautifulSoup(response.text, "html.parser")
 
    registrovani = soup.find("td", {"headers": "sa2"})
    obalky = soup.find("td", {"headers": "sa3"})
    platne = soup.find("td", {"headers": "sa6"})
 
    if not registrovani:
        return None, None, None, []
 
    registrovani = registrovani.text.strip().replace("\xa0", "")
    obalky = obalky.text.strip().replace("\xa0", "")
    platne = platne.text.strip().replace("\xa0", "")
 
    strany = []
    tabulky = soup.find_all("table")
    for tabulka in tabulky:
        radky = tabulka.find_all("tr")
        for radek in radky:
            nazev_td = radek.find("td", {"headers": "t1sa1 t1sb2"})
            if not nazev_td:
                nazev_td = radek.find("td", {"headers": "t2sa1 t2sb2"})
            hlasy_td = radek.find("td", {"headers": "t1sa2 t1sb3"})
            if not hlasy_td:
                hlasy_td = radek.find("td", {"headers": "t2sa2 t2sb3"})
 
            if nazev_td and hlasy_td:
                nazev_strany = nazev_td.text.strip()
                pocet_hlasu = hlasy_td.text.strip().replace("\xa0", "")
                strany.append((nazev_strany, pocet_hlasu))
 
    return registrovani, obalky, platne, strany
 
 
def validace_argumentu(url):
    if not url.startswith("https://volby.cz/pls/ps2017nss/ps32"):
        return False
    return True
 
 
def main():
    if len(sys.argv) != 3:
        print("Chyba: zadej přesně 2 argumenty.")
        print("Použití: python projekt_3.py <url> <vystupni_soubor.csv>")
        sys.exit(1)
 
    url = sys.argv[1]
    vystupni_soubor = sys.argv[2]
 
    if not validace_argumentu(url):
        print("Chyba: první argument musí být odkaz na volby.cz (ps32...).")
        sys.exit(1)
 
    if not vystupni_soubor.endswith(".csv"):
        print("Chyba: druhý argument musí být název .csv souboru.")
        sys.exit(1)
 
    print(f"ZÍSKÁVÁM DATA Z URL: {url}")
    obce = get_obce_links(url)
 
    if not obce:
        print("Chyba: nepodařilo se načíst seznam obcí. Zkontroluj odkaz.")
        sys.exit(1)
 
    vsechna_data = []
    vsechny_strany = []
 
    for kod, nazev, odkaz in obce:
        print(f"ZÍSKÁVÁM DATA Z URL: {odkaz}")
        registrovani, obalky, platne, strany = get_data_obce(odkaz)
 
        if registrovani is None:
            continue
 
        if not vsechny_strany:
            vsechny_strany = [s[0] for s in strany]
 
        radek = {
            "code": kod,
            "location": nazev,
            "registered": registrovani,
            "envelopes": obalky,
            "valid": platne,
        }
 
        for nazev_strany, pocet in strany:
            radek[nazev_strany] = pocet
 
        vsechna_data.append(radek)
 
    if not vsechna_data:
        print("Chyba: žádná data se nepodařilo získat.")
        sys.exit(1)
 
    zahlavi = ["code", "location", "registered", "envelopes", "valid"] + vsechny_strany
 
    print(f"UKLÁDÁM DATA DO SOUBORU: {vystupni_soubor}")
    with open(vystupni_soubor, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=zahlavi)
        writer.writeheader()
        for radek in vsechna_data:
            writer.writerow(radek)
 
    print(f"DOKONČUJI: projekt_3.py")
 
 
if __name__ == "__main__":
    main()