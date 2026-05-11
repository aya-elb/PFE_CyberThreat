import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import json
from datetime import datetime

print("\n=== ML SUPERVISES (Classification Menaces) ===\n")
print("Methodes demandees par le PDF: Logistic Regression, Random Forest, SVM")

# 1. SIMULATION DE DONNEES
print("[1/4] Generation des donnees simulees...")

np.random.seed(42)
n_echantillons = 2000

# Caracteristiques (features) : debit, duree, nombre de connexions, ports suspects
debit = np.random.normal(100, 50, n_echantillons)
duree = np.random.normal(10, 5, n_echantillons)
nb_connexions = np.random.normal(20, 10, n_echantillons)
ports_suspects = np.random.choice([0, 1], n_echantillons, p=[0.9, 0.1])

X = np.column_stack([debit, duree, nb_connexions, ports_suspects])

# Labels : 1 = menace, 0 = non-menace
# Une menace est simulee par : debit eleve OU duree longue OU port suspect
y = ((debit > 150) | (duree > 15) | (ports_suspects == 1)).astype(int)

print(f"   Total echantillons: {n_echantillons}")
print(f"   Menaces: {y.sum()} ({y.sum()/n_echantillons*100:.1f}%)")
print(f"   Non-menaces: {(y==0).sum()} ({(y==0).sum()/n_echantillons*100:.1f}%)")

# 2. DIVISION ENTRAINEMENT / TEST
print("\n[2/4] Division des donnees...")

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
print(f"   Entrainement: {len(X_train)} echantillons")
print(f"   Test: {len(X_test)} echantillons")

# 3. ENTRAINEMENT DES 3 MODELES
print("\n[3/4] Entrainement des modeles...")

resultats = {}

# Modele 1: Logistic Regression
print("\n   [A] Logistic Regression...")
lr = LogisticRegression(random_state=42)
lr.fit(X_train, y_train)
y_pred_lr = lr.predict(X_test)

resultats['Logistic_Regression'] = {
    'accuracy': round(accuracy_score(y_test, y_pred_lr) * 100, 2),
    'precision': round(precision_score(y_test, y_pred_lr) * 100, 2),
    'recall': round(recall_score(y_test, y_pred_lr) * 100, 2),
    'f1_score': round(f1_score(y_test, y_pred_lr) * 100, 2)
}
print(f"      Accuracy: {resultats['Logistic_Regression']['accuracy']}%")

# Modele 2: Random Forest
print("\n   [B] Random Forest...")
rf = RandomForestClassifier(random_state=42)
rf.fit(X_train, y_train)
y_pred_rf = rf.predict(X_test)

resultats['Random_Forest'] = {
    'accuracy': round(accuracy_score(y_test, y_pred_rf) * 100, 2),
    'precision': round(precision_score(y_test, y_pred_rf) * 100, 2),
    'recall': round(recall_score(y_test, y_pred_rf) * 100, 2),
    'f1_score': round(f1_score(y_test, y_pred_rf) * 100, 2)
}
print(f"      Accuracy: {resultats['Random_Forest']['accuracy']}%")

# Modele 3: SVM
print("\n   [C] Support Vector Machine (SVM)...")
svm = SVC(random_state=42)
svm.fit(X_train, y_train)
y_pred_svm = svm.predict(X_test)

resultats['SVM'] = {
    'accuracy': round(accuracy_score(y_test, y_pred_svm) * 100, 2),
    'precision': round(precision_score(y_test, y_pred_svm) * 100, 2),
    'recall': round(recall_score(y_test, y_pred_svm) * 100, 2),
    'f1_score': round(f1_score(y_test, y_pred_svm) * 100, 2)
}
print(f"      Accuracy: {resultats['SVM']['accuracy']}%")

# 4. SAUVEGARDE
print("\n[4/4] Sauvegarde des resultats...")

rapport = {
    "date_analyse": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "n_echantillons": n_echantillons,
    "modeles": resultats,
    "meilleur_modele": max(resultats, key=lambda x: resultats[x]['accuracy'])
}

with open("ml_supervise_resultats.json", "w", encoding="utf-8") as f:
    json.dump(rapport, f, indent=2, ensure_ascii=False)

# AFFICHAGE FINAL
print("\nRESUME DES PERFORMANCES")
print("="*50)
print("Modele               Accuracy  Precision  Recall     F1-Score")
print("-"*50)
for modele, metrics in resultats.items():
    print(f"{modele:<20} {metrics['accuracy']:<9} {metrics['precision']:<10} {metrics['recall']:<9} {metrics['f1_score']}")

print(f"\nMeilleur modele: {rapport['meilleur_modele']}")
print("\nResultats sauvegardes dans 'ml_supervise_resultats.json'")

print("\n=== FIN ML SUPERVISES ===")