import requests
import re

print("=== AJOUT D'IPS DEPUIS FEODO TRACKER ===\n")

url = "https://feodotracker.abuse.ch/downloads/ipblocklist.csv"
r = requests.get(url)
ips = []
for line in r.text.splitlines()[1:100]:
    parts = line.split(",")
    if len(parts) >= 2:
        ip = parts[0].strip()
        if re.match(r"\d+\.\d+\.\d+\.\d+", ip):
            ips.append(ip)

# Lire l'ancien fichier
with open("donnees_brutes.txt", "r") as f:
    ancien = f.read()

# Écrire avec les IPs
with open("donnees_brutes.txt", "w") as f:
    f.write("=== ADRESSES IP ===\n")
    for ip in set(ips):
        f.write(ip + "\n")
    f.write("\n" + ancien)

print(f"Ajout de {len(set(ips))} IPs dans donnees_brutes.txt")