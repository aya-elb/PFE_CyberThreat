import requests
import re
import json
import time

url_base = "https://spear.cx/showthread.php?tid=682"
headers = {"User-Agent": "Mozilla/5.0"}

tous_domaines = []
tous_hashs = []

for page in range(1, 10):
    url = f"{url_base}&page={page}"
    print(f"Scraping page {page}...")
    try:
        r = requests.get(url, headers=headers, timeout=10)
        if r.status_code != 200:
            print(f"Arret (code {r.status_code})")
            break
        html = r.text
        domaines = re.findall(r"\b[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b", html)
        hashs = re.findall(r"\b[a-fA-F0-9]{32}\b", html)
        tous_domaines.extend(domaines)
        tous_hashs.extend(hashs)
        print(f"  -> {len(domaines)} domaines, {len(hashs)} hashs")
        time.sleep(2)
    except Exception as e:
        print(f"Erreur : {e}")
        break

with open("scraped_one_thread_full.json", "w") as f:
    json.dump({
        "domaines": list(set(tous_domaines)),
        "hashs": list(set(tous_hashs))
    }, f, indent=2)

print(f"\nTermine : {len(set(tous_domaines))} domaines, {len(set(tous_hashs))} hashs")