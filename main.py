import subprocess
import sys

print("=== SYSTEME INTELLIGENT DE DETECTION DES CYBERMENACES ===\n")

scripts = [
    ("src/collecte.py", "[1/12] Collecte des donnees..."),
    ("src/extraction_iocs.py", "[2/12] Extraction des IOCs..."),
    ("src/vrai_llm_qwen.py", "[3/12] Analyse LLM..."),
    ("src/detection_anomalies.py", "[4/12] Detection Z-score..."),
    ("src/detection_anomalies_mobile.py", "[4b/12] Detection moyenne mobile..."),
    ("src/isolation_forest.py", "[4c/12] Isolation Forest + EIF..."),
    ("src/ml_supervise.py", "[5/12] ML supervise..."),
    ("src/clustering.py", "[6/12] Clustering K-Means..."),
    ("src/graph_menaces.py", "[7/12] Graphes NetworkX..."),
    ("src/prediction_temporelle.py", "[8/12] Prediction temporelle..."),
    ("src/lstm_sktime.py", "[9/12] LSTM..."),
    ("src/stockage_sqlite.py", "[10/12] Stockage SQLite..."),
    ("src/analyse_normalite.py", "[11/12] Analyse normalite..."),
    ("src/validation_ml.py", "[12/12] Validation ML..."),
]

for script, message in scripts:
    print(message)
    subprocess.run([sys.executable, script])

print("\n=== SYSTEME EXECUTE AVEC SUCCES ===")
print("Lancez l'interface : streamlit run app.py")