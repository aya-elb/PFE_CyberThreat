import requests
import re
from bs4 import BeautifulSoup
import json
import time

base_url = "https://spear.cx/Forum-Databases"
headers = {"User-Agent": "Mozilla/5.0"}

r = requests.get(base_url, headers=headers)
soup = BeautifulSoup(r.text, 'html.parser')

threads_liens = []
for a in soup.find_all('a', href=True):
    href = a['href']
    if 'tid=' in href and 'whoposted' not in href:
        if href.startswith('/showthread.php?tid='):
            threads_liens.append("https://spear.cx" + href)

threads_liens = list(set(threads_liens))
print(f"Threads trouves : {len(threads_liens)}")
print("Exemples :", threads_liens[:3])

tous_domaines = []
tous_hashs = []

for i, url_thread in enumerate(threads_liens[:10]):
    print(f"Scraping {i+1}/{min(10,len(threads_liens))} : {url_thread}")
    try:
        r = requests.get(url_thread, headers=headers, timeout=10)
        if r.status_code != 200:
            print(f"  -> code {r.status_code}, ignore")
            continue
        html = r.text
        domaines = re.findall(r"\b[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b", html)
        hashs = re.findall(r"\b[a-fA-F0-9]{32}\b", html)
        tous_domaines.extend(domaines)
        tous_hashs.extend(hashs)
        print(f"  -> {len(domaines)} domaines, {len(hashs)} hashs")
        time.sleep(1)
    except Exception as e:
        print(f"  -> Erreur : {e}")

with open("scraped_all.json", "w") as f:
    json.dump({
        "domaines": list(set(tous_domaines)),
        "hashs_md5": list(set(tous_hashs))
    }, f, indent=2)

print(f"Fini. Domaines uniques : {len(set(tous_domaines))}, Hashs uniques : {len(set(tous_hashs))}")