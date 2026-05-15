# Système Intelligent de Détection et Prédiction des Cybermenaces

Projet de fin d'études — Licence Statistique et Sciences des Données

## Lancement
```bash
python main.py
```

## Modules principaux
| Fichier | Description |
|---|---|
| collecte.py | Collecte données réelles (Firehol + spear.cx) |
| extraction_iocs.py | Extraction IOCs |
| detection_anomalies.py | Z-score + Moyenne mobile |
| isolation_forest.py | Isolation Forest + Extended IF |
| ml_supervise.py | Classification ML (LR, RF, SVM) |
| prediction_temporelle.py | Prédiction temporelle |
| clustering.py | Clustering K-Means |
| graph_menaces.py | Graphes NetworkX |
| lstm_sktime.py | Prédiction séquentielle |
| vrai_llm_qwen.py | Analyse LLM Qwen 1.8B |
| stockage_sqlite.py | Base SQLite |