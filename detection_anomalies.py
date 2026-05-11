import numpy as np
import pandas as pd
import json
from datetime import datetime

print("\n=== DETECTION D'ANOMALIES (Z-SCORE) ===\n")
print("Methode demandee par le PDF: Z-score (deviation statistique)")

# 1. SIMULATION DE DONNEES
print("[1/3] Generation des donnees de trafic...")

np.random.seed(42)
n_normales = 900
n_anomalies = 100

# Donnees normales (debit entre 50 et 150 Mbps)
debits_normaux = np.random.normal(100, 30, n_normales)

# Donnees anomalies (debit anormalement eleve > 300 Mbps)
debits_anormaux = np.random.normal(500, 150, n_anomalies)

# Fusion
debits = np.concatenate([debits_normaux, debits_anormaux])
df = pd.DataFrame({'debit_mbps': debits})

print(f"   Total echantillons: {len(df)}")
print(f"   Moyenne des debits: {df['debit_mbps'].mean():.1f} Mbps")
print(f"   Ecart-type: {df['debit_mbps'].std():.1f}")

# 2. DETECTION PAR Z-SCORE (methode demandee par le PDF)
print("\n[2/3] Detection des anomalies par Z-score...")

# Calcul du Z-score pour chaque valeur
moyenne = df['debit_mbps'].mean()
ecart_type = df['debit_mbps'].std()
df['z_score'] = (df['debit_mbps'] - moyenne) / ecart_type

# Un Z-score > 3 signifie une anomalie (deviation de 3 ecarts-types)
SEUIL = 3
df['anomalie'] = df['z_score'].abs() > SEUIL

n_anomalies_detectees = df['anomalie'].sum()

print(f"   Seuil utilise: Z-score > {SEUIL}")
print(f"   Anomalies detectees: {n_anomalies_detectees}")
print(f"   Pourcentage: {n_anomalies_detectees/len(df)*100:.1f}%")

# 3. AFFICHAGE DES ANOMALIES
print("\n[3/3] Exemples d'anomalies detectees:")

anomalies_trouvees = df[df['anomalie'] == True]
for idx, row in anomalies_trouvees.head(5).iterrows():
    print(f"   - Debit: {row['debit_mbps']:.0f} Mbps | Z-score: {row['z_score']:.2f}")

# 4. SAUVEGARDE DES RESULTATS
rapport = {
    "date_analyse": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "methode": "Z-score (deviation statistique)",
    "seuil": SEUIL,
    "total_echantillons": len(df),
    "moyenne_mbps": round(moyenne, 2),
    "ecart_type_mbps": round(ecart_type, 2),
    "anomalies_detectees": int(n_anomalies_detectees),
    "pourcentage_anomalies": round(n_anomalies_detectees / len(df) * 100, 2)
}

with open("detection_anomalies_resultats.json", "w", encoding="utf-8") as f:
    json.dump(rapport, f, indent=2, ensure_ascii=False)

print("\nRESUME DE LA DETECTION D'ANOMALIES (Z-SCORE)")
print("="*50)
print(f"Total echantillons: {len(df)}")
print(f"Moyenne: {moyenne:.1f} Mbps")
print(f"Ecart-type: {ecart_type:.1f}")
print(f"Anomalies detectees: {n_anomalies_detectees}")
print(f"Pourcentage: {n_anomalies_detectees/len(df)*100:.1f}%")
print("\nResultats sauvegardes dans 'detection_anomalies_resultats.json'")

print("\n=== FIN DETECTION ANOMALIES (Z-SCORE) ===")