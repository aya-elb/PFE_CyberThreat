import json
import requests

print("=== COLLECTE DES VRAIES DONNEES ===\n")

# 1. Charger tes vraies données (scrapées + Firehol)
with open("scraped_all.json", "r") as f:
    data = json.load(f)

# 2. (Optionnel) Ajouter une source supplémentaire si tu veux
try:
    r = requests.get("https://raw.githubusercontent.com/fabrimagic72/malware-samples/master/README.md")
    text = r.text
    # Tu pourrais extraire des domaines ou IPs supplémentaires ici
except:
    pass

# 3. Écrire dans donnees_brutes.txt
with open("donnees_brutes.txt", "w") as f:
    f.write("=== ADRESSES IP ===\n")
    for ip in data.get("ips", []):
        f.write(ip + "\n")
    f.write("\n=== DOMAINES ===\n")
    for dom in data.get("domaines", []):
        f.write(dom + "\n")
    f.write("\n=== HASH MD5 ===\n")
    for h in data.get("hashs_md5", []):
        f.write(h + "\n")

print(f"Donnees reelles chargees : {len(data.get('ips', []))} IPs, {len(data.get('domaines', []))} domaines, {len(data.get('hashs_md5', []))} hashs")