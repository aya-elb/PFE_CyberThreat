print("=== SYSTEME INTELLIGENT DE DETECTION DES CYBERMENACES ===\n")

print("[1/10] Lancement de la collecte...")
exec(open("collecte.py", encoding="utf-8").read())

print("\n[2/10] Extraction des IOCs...")
exec(open("extraction_iocs.py", encoding="utf-8").read())

print("\n[3/10] Analyse par LLM (simulation)...")
exec(open("vrai_llm_qwen.py", encoding="utf-8").read())

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