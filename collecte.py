import requests
import json
import re
from bs4 import BeautifulSoup
from datetime import datetime

print("=== COLLECTE DES VRAIES DONNEES ===\n")

# ------------------------------------------------------------------
# CHARGEMENT DES DONNEES EXISTANTES
# ------------------------------------------------------------------
try:
    with open("scraped_all.json", "r", encoding="utf-8") as f:
        donnees = json.load(f)
    ips_existantes      = set(donnees.get("ips", []))
    domaines_existants  = set(donnees.get("domaines", []))
    hashs_existants     = set(donnees.get("hashs_md5", []))
except FileNotFoundError:
    ips_existantes     = set()
    domaines_existants = set()
    hashs_existants    = set()

print(f"Donnees existantes : {len(ips_existantes)} IPs | "
      f"{len(domaines_existants)} domaines | {len(hashs_existants)} hashs")

# ------------------------------------------------------------------
# SOURCE 1 : FIREHOL LEVEL 1 (IPs malveillantes)
# ------------------------------------------------------------------
print("\n[SOURCE 1] Firehol Level 1 - Blacklist IPs...")
try:
    r = requests.get(
        "https://raw.githubusercontent.com/firehol/blocklist-ipsets/"
        "master/firehol_level1.netset",
        timeout=30
    )
    nouvelles_ips = set()
    for line in r.text.splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            nouvelles_ips.add(line)
    ips_existantes.update(nouvelles_ips)
    print(f"    {len(nouvelles_ips)} IPs/plages chargees depuis Firehol")
except Exception as e:
    print(f"    Firehol non disponible : {e}")
    try:
        with open("firehol_ips.txt", "r") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    ips_existantes.add(line)
        print(f"    Fallback local : {len(ips_existantes)} IPs")
    except:
        print("    Aucune source Firehol disponible.")

# ------------------------------------------------------------------
# SOURCE 2 : ALIENVAULT OTX - Domaines et hashs (pulse encadrant)
# ------------------------------------------------------------------
print("\n[SOURCE 2] AlienVault OTX - Domaines et hashs...")

OTX_API_KEY = "21a8850e84465bbba616b03abee8dddef9f1a8fe53bcce866ccac528162f1359"
PULSE_ID    = "5ee7247cdb3820b358b37a71"
headers_otx = {"X-OTX-API-KEY": OTX_API_KEY}

nb_dom_otx  = 0
nb_hash_otx = 0

try:
    page = 1
    while True:
        url  = f"https://otx.alienvault.com/api/v1/pulses/{PULSE_ID}/indicators/"
        resp = requests.get(
            url,
            params={"limit": 100, "page": page},
            headers=headers_otx,
            timeout=30
        )

        if resp.status_code != 200:
            print(f"    OTX erreur : code {resp.status_code}")
            break

        data    = resp.json()
        results = data.get("results", [])

        if not results:
            break

        for item in results:
            ioc_type  = item.get("type", "")
            ioc_value = item.get("indicator", "").strip()

            if not ioc_value:
                continue

            if ioc_type in ("domain", "hostname"):
                domaines_existants.add(ioc_value.lower())
                nb_dom_otx += 1

            elif ioc_type == "URL":
                domaine = re.sub(r'^https?://', '', ioc_value)
                domaine = domaine.split('/')[0].strip().lower()
                if domaine and len(domaine) > 3:
                    domaines_existants.add(domaine)
                    nb_dom_otx += 1

            elif ioc_type in ("FileHash-MD5", "FileHash-SHA1",
                              "FileHash-SHA256", "hash"):
                hashs_existants.add(ioc_value.lower())
                nb_hash_otx += 1

        if data.get("next"):
            page += 1
        else:
            break

    print(f"    {nb_dom_otx} domaines ajoutes depuis AlienVault OTX")
    print(f"    {nb_hash_otx} hashs ajoutes depuis AlienVault OTX")

except Exception as e:
    print(f"    AlienVault OTX non disponible : {e}")
# ------------------------------------------------------------------
# SOURCE 3 : SPEAR.CX (domaines et hashs supplementaires)
# ------------------------------------------------------------------
print("\n[SOURCE 3] Spear.cx - IOCs supplementaires...")
try:
    r = requests.get(
        "https://spear.cx/",
        timeout=30,
        headers={"User-Agent": "Mozilla/5.0"}
    )
    soup = BeautifulSoup(r.text, "html.parser")

    # Extraction des hashs MD5 (32 caracteres hexadecimaux)
    texte    = soup.get_text()
    md5_list = re.findall(r'\b[a-fA-F0-9]{32}\b', texte)
    for h in md5_list:
        hashs_existants.add(h.lower())

    # Extraction de domaines supplementaires
    liens = soup.find_all("a", href=True)
    for lien in liens:
        href = lien["href"]
        if href.startswith("http"):
            domaine = re.sub(r'^https?://', '', href).split('/')[0]
            if domaine and "." in domaine and len(domaine) > 4:
                if "spear.cx" not in domaine:
                    domaines_existants.add(domaine)

    print(f"    Scraping spear.cx termine")
except Exception as e:
    print(f"    Spear.cx non disponible : {e}")

# ------------------------------------------------------------------
# SAUVEGARDE
# ------------------------------------------------------------------
print("\n[SAUVEGARDE] Consolidation des donnees...")

# Conversion en listes triees
ips_list      = sorted(list(ips_existantes))
domaines_list = sorted(list(domaines_existants))
hashs_list    = sorted(list(hashs_existants))

donnees_finales = {
    "date_collecte" : datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "sources"       : ["Firehol Level 1", "AlienVault OTX", "spear.cx"],
    "ips"           : ips_list,
    "domaines"      : domaines_list,
    "hashs_md5"     : hashs_list
}

with open("scraped_all.json", "w", encoding="utf-8") as f:
    json.dump(donnees_finales, f, indent=2, ensure_ascii=False)

# Ecriture donnees_brutes.txt
with open("donnees_brutes.txt", "w", encoding="utf-8") as f:
    f.write(f"# Date de collecte : {donnees_finales['date_collecte']}\n")
    f.write(f"# Sources : {', '.join(donnees_finales['sources'])}\n\n")
    f.write("# === ADRESSES IP ET PLAGES RESEAU ===\n")
    for ip in ips_list:
        f.write(ip + "\n")
    f.write("\n# === DOMAINES SUSPECTS ===\n")
    for dom in domaines_list:
        f.write(dom + "\n")
    f.write("\n# === HASHS MD5 MALVEILLANTS ===\n")
    for h in hashs_list:
        f.write(h + "\n")

print(f"\nDonnees reelles chargees : "
      f"{len(ips_list)} IPs | "
      f"{len(domaines_list)} domaines | "
      f"{len(hashs_list)} hashs")
print("Fichiers sauvegardes : scraped_all.json + donnees_brutes.txt")
print("\n=== FIN COLLECTE ===")