import requests
import re

print("=== AJOUT D'IPS DEPUIS GITHUB (FIREHOL) ===\n")

url = "https://raw.githubusercontent.com/firehol/blocklist-ipsets/master/firehol_level1.netset"
r = requests.get(url)
ips = []
for line in r.text.splitlines():
    if re.match(r"\d+\.\d+\.\d+\.\d+", line):
        ips.append(line)

# Lire l'ancien fichier (contenu actuel)
with open("donnees_brutes.txt", "r") as f:
    ancien = f.read()

# Écrire avec les IPs en premier
with open("donnees_brutes.txt", "w") as f:
    f.write("=== ADRESSES IP ===\n")
    for ip in set(ips):
        f.write(ip + "\n")
    f.write("\n" + ancien)

print(f"Ajout de {len(set(ips))} IPs dans donnees_brutes.txt")