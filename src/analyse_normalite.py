import json
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import re

print("\n=== ANALYSE DE NORMALITE DES DONNEES (Z-SCORE) ===\n")

# ------------------------------------------------------------------
# 1. CHARGEMENT DES DONNEES REELLES
# ------------------------------------------------------------------
print("[1/4] Chargement des IOCs reels...")

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
for ip in ips:
    valeurs.append(len(ip))
for dom in domaines:
    valeurs.append(len(dom))
for h in hashs:
    valeurs.append(len(h))

valeurs = np.array(valeurs, dtype=float)
print(f"    Total IOCs analyses : {len(valeurs)}")

# ------------------------------------------------------------------
# 2. HISTOGRAMME
# ------------------------------------------------------------------
print("\n[2/4] Generation de l'histogramme...")

mu = np.mean(valeurs)
sigma = np.std(valeurs)

plt.figure(figsize=(10, 6))
plt.hist(valeurs, bins=40, color="#00C2D1", edgecolor="white", alpha=0.85)
plt.axvline(mu, color="#FF6B5B", linestyle="--", linewidth=2, label=f"Moyenne (μ={mu:.2f})")
plt.xlabel("Longueur des IOCs (caracteres)")
plt.ylabel("Frequence")
plt.title("Distribution de la longueur des IOCs (n={})".format(len(valeurs)))
plt.legend()
plt.tight_layout()
plt.savefig("histogramme_normalite.png", dpi=150)
plt.close()
print("    Graphique sauvegarde : histogramme_normalite.png")

# ------------------------------------------------------------------
# 3. QQ-PLOT
# ------------------------------------------------------------------
print("\n[3/4] Generation du QQ-plot...")

plt.figure(figsize=(8, 8))
stats.probplot(valeurs, dist="norm", plot=plt)
plt.title("QQ-Plot : comparaison a la distribution normale")
plt.gca().get_lines()[0].set_markerfacecolor("#00C2D1")
plt.gca().get_lines()[0].set_markeredgecolor("#0A1F3D")
plt.gca().get_lines()[1].set_color("#FF6B5B")
plt.tight_layout()
plt.savefig("qqplot_normalite.png", dpi=150)
plt.close()
print("    Graphique sauvegarde : qqplot_normalite.png")

# ------------------------------------------------------------------
# 4. TESTS STATISTIQUES DE NORMALITE
# ------------------------------------------------------------------
print("\n[4/4] Tests statistiques de normalite...")

# Shapiro-Wilk (recommande pour n < 5000, on echantillonne si plus grand)
if len(valeurs) > 5000:
    echantillon = np.random.choice(valeurs, 5000, replace=False)
else:
    echantillon = valeurs

shapiro_stat, shapiro_p = stats.shapiro(echantillon)

# Kolmogorov-Smirnov
ks_stat, ks_p = stats.kstest(valeurs, 'norm', args=(mu, sigma))

# Skewness et Kurtosis
skewness = stats.skew(valeurs)
kurtosis = stats.kurtosis(valeurs)

print(f"\n    Test de Shapiro-Wilk :")
print(f"       Statistique W = {shapiro_stat:.4f}")
print(f"       p-value       = {shapiro_p:.6f}")
print(f"       Conclusion    = {'Normalite REJETEE (p<0.05)' if shapiro_p < 0.05 else 'Normalite non rejetee'}")

print(f"\n    Test de Kolmogorov-Smirnov :")
print(f"       Statistique D = {ks_stat:.4f}")
print(f"       p-value       = {ks_p:.6f}")
print(f"       Conclusion    = {'Normalite REJETEE (p<0.05)' if ks_p < 0.05 else 'Normalite non rejetee'}")

print(f"\n    Asymetrie (Skewness)  = {skewness:.4f}")
print(f"    Aplatissement (Kurtosis) = {kurtosis:.4f}")

resultats = {
    "n_observations": len(valeurs),
    "moyenne": round(float(mu), 4),
    "ecart_type": round(float(sigma), 4),
    "shapiro_wilk": {"statistique": round(float(shapiro_stat), 4), "p_value": round(float(shapiro_p), 8)},
    "kolmogorov_smirnov": {"statistique": round(float(ks_stat), 4), "p_value": round(float(ks_p), 8)},
    "skewness": round(float(skewness), 4),
    "kurtosis": round(float(kurtosis), 4),
    "normalite_rejetee": bool(shapiro_p < 0.05 or ks_p < 0.05)
}

with open("analyse_normalite_resultats.json", "w", encoding="utf-8") as f:
    json.dump(resultats, f, indent=2, ensure_ascii=False)

print("\nResultats sauvegardes dans analyse_normalite_resultats.json")
print("\n=== FIN ANALYSE DE NORMALITE ===")