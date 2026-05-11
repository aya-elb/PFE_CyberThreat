import json
import numpy as np
import re
from datetime import datetime

print("\n=== DETECTION D'ANOMALIES (Z-SCORE) ===\n")
print("Methode demandee par le PDF : Z-score (deviation statistique)")

# ------------------------------------------------------------------
# 1. CHARGEMENT DES DONNEES REELLES
# ------------------------------------------------------------------
print("\n[1/3] Chargement des IOCs reels...")

with open("scraped_all.json", "r", encoding="utf-8") as f:
    data = json.load(f)

ips_raw  = data.get("ips", [])
domaines = data.get("domaines", [])
hashs    = data.get("hashs_md5", [])

# Nettoyage : on garde IPs et plages CIDR valides, on enleve les commentaires
ips = [
    ip.strip() for ip in ips_raw
    if ip.strip()
    and not ip.strip().startswith("#")
    and re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}(/\d{1,2})?$', ip.strip())
]

valeurs = []
labels  = []

for ip in ips:
    valeurs.append(len(ip))
    labels.append(f"IP:{ip}")

for dom in domaines:
    valeurs.append(len(dom))
    labels.append(f"DOM:{dom}")

for h in hashs:
    valeurs.append(len(h))
    labels.append(f"HASH:{h}")

valeurs = np.array(valeurs, dtype=float)
print(f"    Total IOCs charges : {len(valeurs)}")
print(f"    IPs/plages : {len(ips)} | Domaines : {len(domaines)} | Hashs : {len(hashs)}")

# ------------------------------------------------------------------
# 2. CALCUL DU Z-SCORE
# ------------------------------------------------------------------
print("\n[2/3] Detection des anomalies par Z-score...")

moyenne    = np.mean(valeurs)
ecart_type = np.std(valeurs)
seuil      = 2.5

print(f"    Moyenne des longueurs : {moyenne:.2f} caracteres")
print(f"    Ecart-type            : {ecart_type:.2f}")
print(f"    Seuil Z-score utilise : > {seuil}")

z_scores      = np.abs((valeurs - moyenne) / ecart_type)
anomalies_idx = np.where(z_scores > seuil)[0]

print(f"    Anomalies detectees   : {len(anomalies_idx)}")
print(f"    Pourcentage           : {len(anomalies_idx)/len(valeurs)*100:.1f}%")

# ------------------------------------------------------------------
# 3. AFFICHAGE ET SAUVEGARDE
# ------------------------------------------------------------------
print("\n[3/3] Exemples d'anomalies detectees (IOCs suspects) :")
for idx in anomalies_idx[:8]:
    print(f"    - {labels[idx]:<50} | longueur: {int(valeurs[idx])} | Z-score: {z_scores[idx]:.2f}")

anomalies_liste = [
    {
        "ioc"      : labels[idx],
        "longueur" : int(valeurs[idx]),
        "z_score"  : round(float(z_scores[idx]), 4)
    }
    for idx in anomalies_idx
]

rapport = {
    "date_analyse"     : datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "source_donnees"   : "scraped_all.json (donnees reelles collectees)",
    "methode"          : "Z-score sur longueur des IOCs (IPs, plages CIDR, domaines, hashs)",
    "total_iocs"       : len(valeurs),
    "moyenne_longueur" : round(float(moyenne), 2),
    "ecart_type"       : round(float(ecart_type), 2),
    "seuil_zscore"     : seuil,
    "nb_anomalies"     : len(anomalies_idx),
    "pourcentage"      : round(len(anomalies_idx) / len(valeurs) * 100, 2),
    "anomalies"        : anomalies_liste
}

with open("detection_anomalies_resultats.json", "w", encoding="utf-8") as f:
    json.dump(rapport, f, indent=2, ensure_ascii=False)

print(f"\nRESUME DE LA DETECTION D'ANOMALIES (Z-SCORE)")
print("=" * 50)
print(f"Source          : scraped_all.json (donnees reelles)")
print(f"Total IOCs      : {len(valeurs)}")
print(f"Moyenne         : {moyenne:.2f} caracteres")
print(f"Ecart-type      : {ecart_type:.2f}")
print(f"Anomalies       : {len(anomalies_idx)} ({len(anomalies_idx)/len(valeurs)*100:.1f}%)")
print(f"\nResultats sauvegardes dans 'detection_anomalies_resultats.json'")
print("\n=== FIN DETECTION ANOMALIES (Z-SCORE) ===")