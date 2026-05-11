import json
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from collections import Counter
import re
from datetime import datetime

print("\n=== CLUSTERING DES MENACES (K-MEANS) ===\n")
print("Methode demandee par le PDF section 5.4 : Regroupement automatique des menaces similaires")

# ------------------------------------------------------------------
# 1. CHARGEMENT DES DONNEES REELLES
# ------------------------------------------------------------------
print("\n[1/4] Chargement des IOCs reels...")

with open("scraped_all.json", "r", encoding="utf-8") as f:
    data = json.load(f)

ips_raw  = data.get("ips", [])
domaines = data.get("domaines", [])
hashs    = data.get("hashs_md5", [])

# Nettoyage : plages CIDR valides uniquement
ips = [
    ip.strip() for ip in ips_raw
    if ip.strip()
    and not ip.strip().startswith("#")
    and re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}(/\d{1,2})?$', ip.strip())
]

print(f"    IPs/plages : {len(ips)} | Domaines : {len(domaines)} | Hashs : {len(hashs)}")

# ------------------------------------------------------------------
# 2. EXTRACTION DE FEATURES DEPUIS LES DONNEES REELLES
# ------------------------------------------------------------------
print("\n[2/4] Extraction des features par IOC...")

def features_ioc(ioc, type_ioc):
    longueur    = len(ioc)
    nb_chiffres = sum(c.isdigit() for c in ioc)
    nb_points   = ioc.count(".")
    nb_tirets   = ioc.count("-")
    entropie    = 0.0
    if longueur > 0:
        freqs = Counter(ioc)
        for c in freqs:
            p = freqs[c] / longueur
            entropie -= p * np.log2(p)
    type_code = 0 if type_ioc == "ip" else (1 if type_ioc == "domaine" else 2)
    return [longueur, nb_chiffres, nb_points, entropie, type_code]

X      = []
labels = []

for ip in ips:
    X.append(features_ioc(ip, "ip"))
    labels.append(f"IP:{ip}")

for dom in domaines:
    X.append(features_ioc(dom, "domaine"))
    labels.append(f"DOM:{dom}")

for h in hashs:
    X.append(features_ioc(h, "hash"))
    labels.append(f"HASH:{h}")

X = np.array(X, dtype=float)
print(f"    Total IOCs pour clustering : {len(X)}")

# ------------------------------------------------------------------
# 3. NORMALISATION + K-MEANS
# ------------------------------------------------------------------
print("\n[3/4] Execution du clustering K-Means (4 clusters)...")

scaler  = StandardScaler()
X_norm  = scaler.fit_transform(X)

kmeans   = KMeans(n_clusters=4, random_state=42, n_init=10)
clusters = kmeans.fit_predict(X_norm)

# Nommage des clusters selon leurs caracteristiques
noms_clusters = {}
for i in range(4):
    idx        = np.where(clusters == i)[0]
    moy_long   = np.mean(X[idx, 0])
    moy_entrop = np.mean(X[idx, 3])
    type_dom   = np.mean(X[idx, 4])

    if type_dom > 1.5:
        nom = "Hash malveillant / Malware"
    elif type_dom > 0.5:
        nom = "Domaine suspect / Phishing"
    elif moy_entrop > 3.0:
        nom = "IP aleatoire / Botnet C2"
    else:
        nom = "Plage reseau blacklistee / DDoS"

    noms_clusters[i] = {
        "nom"          : nom,
        "nb_iocs"      : len(idx),
        "moy_longueur" : round(float(moy_long), 2),
        "moy_entropie" : round(float(moy_entrop), 4),
        "exemples"     : [labels[j] for j in idx[:3]]
    }

# Renommage si deux clusters ont le meme nom
noms_vus = {}
for i in range(4):
    nom = noms_clusters[i]["nom"]
    if nom in noms_vus:
        noms_clusters[i]["nom"] = "Scan de ports / Reconnaissance"
    else:
        noms_vus[nom] = True

print(f"    Repartition des clusters :")
for i, info in noms_clusters.items():
    print(f"       Cluster {i} ({info['nom']}) : {info['nb_iocs']} IOCs")

# ------------------------------------------------------------------
# 4. VISUALISATION
# ------------------------------------------------------------------
print("\n[4/4] Generation du graphique...")

couleurs = ['#e74c3c', '#3498db', '#2ecc71', '#f39c12']
fig, ax  = plt.subplots(figsize=(10, 6))

for i in range(4):
    idx = np.where(clusters == i)[0]
    ax.scatter(
        X_norm[idx, 0],
        X_norm[idx, 3],
        c=couleurs[i],
        label=f"Cluster {i} : {noms_clusters[i]['nom']}",
        alpha=0.6,
        s=20
    )

ax.set_xlabel("Longueur (normalisee)")
ax.set_ylabel("Entropie (normalisee)")
ax.set_title("Clustering K-Means des IOCs reels (4 familles de menaces)")
ax.legend(loc='upper right', fontsize=8)
plt.tight_layout()
plt.savefig("clustering_menaces.png", dpi=150)
plt.close()
print("    Graphique sauvegarde : clustering_menaces.png")

# ------------------------------------------------------------------
# 5. SAUVEGARDE
# ------------------------------------------------------------------
rapport = {
    "date_analyse"   : datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "source_donnees" : "scraped_all.json (donnees reelles collectees)",
    "methode"        : "K-Means (k=4) sur features extraites des IOCs reels",
    "total_iocs"     : len(X),
    "clusters"       : noms_clusters
}

with open("clustering_resultats.json", "w", encoding="utf-8") as f:
    json.dump(rapport, f, indent=2, ensure_ascii=False)

print("\nRESUME DU CLUSTERING")
print("=" * 50)
print(f"Source         : scraped_all.json (donnees reelles)")
print(f"Total IOCs     : {len(X)}")
print(f"Clusters       : 4")
print()
for i, info in noms_clusters.items():
    print(f"   Cluster {i} : {info['nom']}")
    print(f"              {info['nb_iocs']} IOCs | entropie moy. {info['moy_entropie']}")
    print(f"              Exemples : {info['exemples'][0]}")

print("\nResultats sauvegardes dans clustering_resultats.json")
print("\n=== FIN CLUSTERING ===")