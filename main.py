import subprocess
import sys

print("=== SYSTEME INTELLIGENT DE DETECTION DES CYBERMENACES ===\n")

print("[1/10] Lancement de la collecte...")
exec(open("collecte.py", encoding="utf-8").read())

print("\n[2/10] Extraction des IOCs...")
exec(open("extraction_iocs.py", encoding="utf-8").read())

print("\n[3/10] Analyse par LLM (Qwen 1.8B local)...")
try:
    result = subprocess.run(
        [sys.executable, "vrai_llm_qwen.py"],
        timeout=300,
        capture_output=True,
        text=True
    )
    if result.returncode == 0:
        print(result.stdout)
    else:
        print("[LLM] Le module LLM a rencontre une erreur.")
        print("[LLM] Cause probable : modele Ollama non demarre ou ressources insuffisantes.")
except subprocess.TimeoutExpired:
    print("[LLM] Delai depasse (300s). Analyse LLM ignoree pour cette execution.")
    print("[LLM] Note : le modele Qwen 1.8B necessite un GPU pour une execution rapide.")
except Exception as e:
    print(f"[LLM] Erreur inattendue : {e}")

print("\n[4/10] Detection d'anomalies (Z-score)...")
exec(open("detection_anomalies.py", encoding="utf-8").read())

print("\n[5/10] ML Supervises (Logistic Regression, Random Forest, SVM)...")
exec(open("ml_supervise.py", encoding="utf-8").read())

print("\n[6/10] Prediction temporelle...")
exec(open("prediction_temporelle.py", encoding="utf-8").read())

print("\n[7/10] Clustering des menaces (K-Means)...")
exec(open("clustering.py", encoding="utf-8").read())

print("\n[8/10] Modelisation par graphes (NetworkX)...")
exec(open("graph_menaces.py", encoding="utf-8").read())

print("\n[9/10] LSTM-like (prediction sequentielle)...")
exec(open("lstm_sktime.py", encoding="utf-8").read())

print("\n[10/10] Stockage SQLite...")
exec(open("stockage_sqlite.py", encoding="utf-8").read())

print("\n=== SYSTEME EXECUTE AVEC SUCCES ===")

print("\n[4b/10] N-sigma avec moyenne mobile...")
exec(open("detection_anomalies_mobile.py", encoding="utf-8").read())

print("\n[4c/10] Isolation Forest + Extended Isolation Forest...")
exec(open("isolation_forest.py", encoding="utf-8").read())