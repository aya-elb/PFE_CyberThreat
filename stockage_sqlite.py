import sqlite3
import json
from datetime import datetime

print("\n=== STOCKAGE SQLITE ===\n")

# Connexion à la base (elle sera créée automatiquement)
conn = sqlite3.connect("cyber_threat.db")
cursor = conn.cursor()

# Création de la table (si elle n'existe pas)
cursor.execute("""
CREATE TABLE IF NOT EXISTS detection_anomalies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    methode TEXT,
    anomalies_detectees INTEGER,
    total_echantillons INTEGER,
    pourcentage REAL
)
""")

# Lecture du fichier JSON existant (détection anomalies Z-score)
try:
    with open("detection_anomalies_resultats.json", "r") as f:
        data = json.load(f)

    cursor.execute("""
    INSERT INTO detection_anomalies (date, methode, anomalies_detectees, total_echantillons, pourcentage)
    VALUES (?, ?, ?, ?, ?)
    """, (
        data.get("date_analyse", str(datetime.now())),
        data.get("methode", "Z-score"),
        data.get("anomalies_detectees", 0),
        data.get("total_echantillons", 0),
        data.get("pourcentage_anomalies", 0.0)
    ))

    print(" Insertion réussie depuis detection_anomalies_resultats.json")

except FileNotFoundError:
    print(" Fichier detection_anomalies_resultats.json introuvable. Insertion manuelle.")
    cursor.execute("""
    INSERT INTO detection_anomalies (date, methode, anomalies_detectees, total_echantillons, pourcentage)
    VALUES (?, ?, ?, ?, ?)
    """, (str(datetime.now()), "Z-score (simulation)", 39, 1000, 3.9))

# Valider et fermer
conn.commit()
conn.close()

print(" Base SQLite mise à jour : cyber_threat.db")