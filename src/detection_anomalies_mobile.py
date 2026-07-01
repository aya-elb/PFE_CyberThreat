import json
import numpy as np
import matplotlib.pyplot as plt
import re
from datetime import datetime

print("\n=== DETECTION D'ANOMALIES (N-SIGMA MOYENNE MOBILE) ===\n")
print("Methode demandee par le PDF section IV.2.2 : N-sigma base sur la moyenne mobile")

# ------------------------------------------------------------------
# 1. CHARGEMENT DES DONNEES REELLES
# ------------------------------------------------------------------
print("\n[1/3] Chargement des IOCs reels...")

with open("scraped_all.json", "r", encoding="utf-8") as f:
    data = json.load(f)

ips_raw  = data.get("ips", [])
domaines = data.get("domaines", [])
hashs    = data.get("hashs_md5", [])

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

# ------------------------------------------------------------------
# 2. N-SIGMA AVEC MOYENNE MOBILE
# ------------------------------------------------------------------
print("\n[2/3] Application du N-sigma avec moyenne mobile...")

fenetre = 50   # taille de la fenetre glissante
seuil_n = 2.5  # nombre de sigmas

anomalies_idx = []
moyennes_mobiles = []
seuils_sup = []
seuils_inf = []

for i in range(len(valeurs)):
    # Fenetre glissante : on prend les 'fenetre' valeurs precedentes
    debut = max(0, i - fenetre)
    fenetre_vals = valeurs[debut:i+1]

    mu    = np.mean(fenetre_vals)
    sigma = np.std(fenetre_vals)

    seuil_superieur = mu + seuil_n * sigma
    seuil_inferieur = mu - seuil_n * sigma

    moyennes_mobiles.append(mu)
    seuils_sup.append(seuil_superieur)
    seuils_inf.append(seuil_inferieur)

    if valeurs[i] > seuil_superieur or valeurs[i] < seuil_inferieur:
        anomalies_idx.append(i)

print(f"    Fenetre glissante : {fenetre} IOCs")
print(f"    Seuil N-sigma     : {seuil_n}")
print(f"    Anomalies detectees : {len(anomalies_idx)}")
print(f"    Pourcentage         : {len(anomalies_idx)/len(valeurs)*100:.1f}%")

print("\n    Exemples d'anomalies detectees :")
for idx in anomalies_idx[:8]:
    print(f"    - {labels[idx]:<45} | longueur: {int(valeurs[idx])} | seuil: {seuils_sup[idx]:.2f}")

# ------------------------------------------------------------------
# 3. GRAPHIQUE + SAUVEGARDE
# ------------------------------------------------------------------
print("\n[3/3] Generation du graphique et sauvegarde...")

plt.figure(figsize=(14, 5))
plt.plot(valeurs, color='#3498db', alpha=0.6, label='Longueur IOC', linewidth=0.8)
plt.plot(moyennes_mobiles, color='#2ecc71', label='Moyenne mobile', linewidth=1.5)
plt.plot(seuils_sup, color='#e74c3c', linestyle='--', label=f'Seuil +{seuil_n}σ', linewidth=1.2)
plt.plot(seuils_inf, color='#e74c3c', linestyle='--', label=f'Seuil -{seuil_n}σ', linewidth=1.2)

if anomalies_idx:
    plt.scatter(anomalies_idx,
                [valeurs[i] for i in anomalies_idx],
                color='#e74c3c', zorder=5, s=30, label='Anomalie')

plt.xlabel("Index IOC")
plt.ylabel("Longueur (caracteres)")
plt.title("Detection d'anomalies par N-sigma avec moyenne mobile (donnees reelles)")
plt.legend(fontsize=8)
plt.tight_layout()
plt.savefig("detection_mobile.png", dpi=150)
plt.close()
print("    Graphique sauvegarde : detection_mobile.png")

rapport = {
    "date_analyse"      : datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "source_donnees"    : "scraped_all.json (donnees reelles)",
    "methode"           : "N-sigma avec moyenne mobile glissante",
    "fenetre"           : fenetre,
    "seuil_n_sigma"     : seuil_n,
    "total_iocs"        : len(valeurs),
    "nb_anomalies"      : len(anomalies_idx),
    "pourcentage"       : round(len(anomalies_idx)/len(valeurs)*100, 2),
    "anomalies"         : [{"ioc": labels[i], "longueur": int(valeurs[i])} for i in anomalies_idx[:20]]
}

with open("detection_mobile_resultats.json", "w", encoding="utf-8") as f:
    json.dump(rapport, f, indent=2, ensure_ascii=False)

print("\nRESUME N-SIGMA MOYENNE MOBILE")
print("=" * 50)
print(f"Source      : scraped_all.json (donnees reelles)")
print(f"Fenetre     : {fenetre} IOCs")
print(f"Seuil       : {seuil_n} sigmas")
print(f"Anomalies   : {len(anomalies_idx)} ({len(anomalies_idx)/len(valeurs)*100:.1f}%)")
print("Resultats sauvegardes dans detection_mobile_resultats.json")
print("\n=== FIN N-SIGMA MOYENNE MOBILE ===")