import json
import numpy as np
import matplotlib.pyplot as plt
import requests
from collections import Counter
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, roc_curve, auc, ConfusionMatrixDisplay
)
import re

print("\n=== VALIDATION COMPLETE DES MODELES ML SUPERVISES ===\n")

# ------------------------------------------------------------------
# 1. CHARGEMENT ET PREPARATION DES DONNEES (identique a ml_supervise.py)
# ------------------------------------------------------------------
print("[1/6] Chargement des donnees reelles...")

with open("scraped_all.json", "r", encoding="utf-8") as f:
    data = json.load(f)

ips_raw  = data.get("ips", [])
domaines = data.get("domaines", [])
hashs    = data.get("hashs_md5", [])

ips = [
    ip.strip() for ip in ips_raw
    if ip.strip() and not ip.strip().startswith("#")
    and re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}(/\d{1,2})?$', ip.strip())
]

try:
    r = requests.get(
        "https://raw.githubusercontent.com/firehol/blocklist-ipsets/master/firehol_level1.netset",
        timeout=30
    )
    blacklist_ips = set(l.strip() for l in r.text.splitlines() if l.strip() and not l.strip().startswith("#"))
except Exception:
    blacklist_ips = set()
    try:
        with open("firehol_ips.txt", "r") as f:
            blacklist_ips = set(l.strip() for l in f if l.strip() and not l.strip().startswith("#"))
    except:
        pass

def extraire_features(ioc, type_ioc):
    longueur    = len(ioc)
    nb_chiffres = sum(c.isdigit() for c in ioc)
    nb_points   = ioc.count(".")
    nb_tirets   = ioc.count("-")
    nb_lettres  = sum(c.isalpha() for c in ioc)
    est_ip      = 1 if type_ioc == "ip" else 0
    est_domaine = 1 if type_ioc == "domaine" else 0
    est_hash    = 1 if type_ioc == "hash" else 0
    entropie = 0.0
    if longueur > 0:
        freqs = Counter(ioc)
        for c in freqs:
            p = freqs[c] / longueur
            entropie -= p * np.log2(p)
    return [longueur, nb_chiffres, nb_points, nb_tirets, nb_lettres, est_ip, est_domaine, est_hash, round(entropie, 4)]

def est_malveillant(ioc, type_ioc, blacklist):
    if type_ioc == "ip":
        return 1 if ioc in blacklist else 0
    if type_ioc == "domaine":
        suspects = [".tk", ".ml", ".ga", ".cf", ".gq", "onion", "bit.ly", ".xyz", ".top"]
        return 1 if any(s in ioc for s in suspects) else 0
    if type_ioc == "hash":
        return 1
    return 0

X, y = [], []
for ip in ips:
    X.append(extraire_features(ip, "ip"))
    y.append(est_malveillant(ip, "ip", blacklist_ips))
for dom in domaines:
    X.append(extraire_features(dom, "domaine"))
    y.append(est_malveillant(dom, "domaine", blacklist_ips))
for h in hashs:
    X.append(extraire_features(h, "hash"))
    y.append(est_malveillant(h, "hash", blacklist_ips))

ips_benines = ["192.168.1.1","8.8.8.8","8.8.4.4","1.1.1.1","1.0.0.1","9.9.9.9",
    "208.67.222.222","185.228.168.9","76.76.19.19","94.140.14.14","172.217.16.142",
    "142.250.185.78","93.184.216.34","151.101.1.69","104.244.42.65","31.13.72.36",
    "157.240.214.35","52.84.12.1","13.107.42.14","40.112.72.205"]
domaines_benins = ["google.com","github.com","microsoft.com","apple.com","amazon.com",
    "cloudflare.com","wikipedia.org","youtube.com","stackoverflow.com","mozilla.org",
    "python.org","linux.org","ubuntu.com","debian.org","openssl.org","apache.org",
    "nginx.org","nodejs.org","pytorch.org","tensorflow.org"]

for ip in ips_benines:
    X.append(extraire_features(ip, "ip")); y.append(0)
for dom in domaines_benins:
    X.append(extraire_features(dom, "domaine")); y.append(0)

X = np.array(X, dtype=float)
y = np.array(y)
print(f"    Total IOCs : {len(y)} | Menaces : {y.sum()} | Benins : {(y==0).sum()}")

# ------------------------------------------------------------------
# 2. TRAIN/TEST SPLIT DOCUMENTE
# ------------------------------------------------------------------
print("\n[2/6] Division Train/Test (stratifiee)...")

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.30, random_state=42, stratify=y
)
print(f"    Train : {len(X_train)} echantillons ({len(X_train)/len(X)*100:.1f}%)")
print(f"    Test  : {len(X_test)} echantillons ({len(X_test)/len(X)*100:.1f}%)")
print(f"    Stratification : preserve le ratio menaces/benins dans train et test")

# ------------------------------------------------------------------
# 3. ENTRAINEMENT DES 3 MODELES
# ------------------------------------------------------------------
print("\n[3/6] Entrainement des modeles...")

models = {
    "Logistic_Regression": LogisticRegression(random_state=42, max_iter=1000),
    "Random_Forest": RandomForestClassifier(n_estimators=100, random_state=42),
    "SVM": SVC(kernel='rbf', random_state=42, probability=True)
}

resultats_complets = {}

for nom, model in models.items():
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    resultats_complets[nom] = {
        "accuracy": round(accuracy_score(y_test, y_pred) * 100, 2),
        "precision": round(precision_score(y_test, y_pred, zero_division=0) * 100, 2),
        "recall": round(recall_score(y_test, y_pred, zero_division=0) * 100, 2),
        "f1_score": round(f1_score(y_test, y_pred, zero_division=0) * 100, 2),
    }
    print(f"    {nom} : Accuracy = {resultats_complets[nom]['accuracy']}%")

# ------------------------------------------------------------------
# 4. VALIDATION CROISEE K-FOLD (k=5)
# ------------------------------------------------------------------
print("\n[4/6] Validation croisee K-Fold (k=5)...")

skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

for nom, model in models.items():
    scores = cross_val_score(model, X, y, cv=skf, scoring='accuracy')
    resultats_complets[nom]["cv_scores"] = [round(s*100, 2) for s in scores]
    resultats_complets[nom]["cv_mean"] = round(scores.mean()*100, 2)
    resultats_complets[nom]["cv_std"] = round(scores.std()*100, 2)
    # Intervalle de confiance a 95% (approx normale)
    ic95 = 1.96 * scores.std() / np.sqrt(len(scores))
    resultats_complets[nom]["ic95_low"] = round((scores.mean() - ic95)*100, 2)
    resultats_complets[nom]["ic95_high"] = round((scores.mean() + ic95)*100, 2)
    print(f"    {nom} : {resultats_complets[nom]['cv_mean']}% (+/- {resultats_complets[nom]['cv_std']}%) "
          f"| IC95% = [{resultats_complets[nom]['ic95_low']}%, {resultats_complets[nom]['ic95_high']}%]")

# ------------------------------------------------------------------
# 5. MATRICES DE CONFUSION
# ------------------------------------------------------------------
print("\n[5/6] Generation des matrices de confusion...")

fig, axes = plt.subplots(1, 3, figsize=(16, 5))
for ax, (nom, model) in zip(axes, models.items()):
    y_pred = model.predict(X_test)
    cm = confusion_matrix(y_test, y_pred)
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=["Benin", "Menace"])
    disp.plot(ax=ax, cmap="Blues", colorbar=False)
    ax.set_title(nom.replace("_", " "))
    resultats_complets[nom]["confusion_matrix"] = cm.tolist()

plt.tight_layout()
plt.savefig("matrices_confusion.png", dpi=150)
plt.close()
print("    Graphique sauvegarde : matrices_confusion.png")

# ------------------------------------------------------------------
# 6. COURBES ROC-AUC
# ------------------------------------------------------------------
print("\n[6/6] Generation des courbes ROC-AUC...")

plt.figure(figsize=(8, 7))
colors = {"Logistic_Regression": "#00C2D1", "Random_Forest": "#0A1F3D", "SVM": "#FF6B5B"}

for nom, model in models.items():
    y_proba = model.predict_proba(X_test)[:, 1]
    fpr, tpr, _ = roc_curve(y_test, y_proba)
    roc_auc = auc(fpr, tpr)
    resultats_complets[nom]["roc_auc"] = round(roc_auc, 4)
    plt.plot(fpr, tpr, label=f"{nom.replace('_',' ')} (AUC = {roc_auc:.3f})",
              color=colors[nom], linewidth=2)

plt.plot([0, 1], [0, 1], linestyle="--", color="gray", label="Aleatoire (AUC = 0.5)")
plt.xlabel("Taux de faux positifs (1 - Specificite)")
plt.ylabel("Taux de vrais positifs (Sensibilite)")
plt.title("Courbes ROC - Comparaison des modeles")
plt.legend(loc="lower right")
plt.tight_layout()
plt.savefig("courbes_roc.png", dpi=150)
plt.close()
print("    Graphique sauvegarde : courbes_roc.png")

for nom in models:
    print(f"    {nom} : AUC = {resultats_complets[nom]['roc_auc']}")

# ------------------------------------------------------------------
# SAUVEGARDE FINALE
# ------------------------------------------------------------------
with open("validation_ml_resultats.json", "w", encoding="utf-8") as f:
    json.dump(resultats_complets, f, indent=2, ensure_ascii=False)

print("\nResultats complets sauvegardes dans validation_ml_resultats.json")
print("\n=== FIN VALIDATION ML ===")