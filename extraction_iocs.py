import re

print("=== EXTRACTION DES IOCS ===\n")

# Lire le fichier qu'on a collecté
with open("donnees_brutes.txt", "r", encoding="utf-8") as f:
    contenu = f.read()

# 1. Extraire les adresses IP
ip_pattern = r"\b(?:\d{1,3}\.){3}\d{1,3}\b"
ips_trouvees = re.findall(ip_pattern, contenu)
ips_uniques = list(set(ips_trouvees))

print(f"[1] Adresses IP trouvées : {len(ips_uniques)}")
for ip in ips_uniques[:5]:
    print(f"    - {ip}")

# 2. Extraire les domaines (simplifié)
domaine_pattern = r"\b[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b"
domaines_trouves = re.findall(domaine_pattern, contenu)
domaines_uniques = list(set(domaines_trouves))

print(f"\n[2] Domaines trouvés : {len(domaines_uniques)}")
for domaine in domaines_uniques[:5]:
    print(f"    - {domaine}")

# 3. Sauvegarder tous les IOCs
with open("iocs_extraits.txt", "w") as f:
    f.write("=== INDICATEURS DE COMPROMIS (IOCs) ===\n\n")
    f.write("=== ADRESSES IP ===\n")
    for ip in ips_uniques:
        f.write(ip + "\n")
    f.write("\n=== DOMAINES ===\n")
    for domaine in domaines_uniques:
        f.write(domaine + "\n")

print("\n[3] IOCs sauvegardés dans 'iocs_extraits.txt'")
print("=== FIN EXTRACTION ===")
