# 🛡️ Système Intelligent de Détection et Prédiction des Cybermenaces

> Projet de fin d'études — Licence Statistique et Sciences des Données

---

## 📌 Vue d'ensemble

Système automatisé combinant méthodes statistiques, Machine Learning et LLM
pour détecter, analyser et prédire les cybermenaces à partir de données réelles
collectées depuis des sources ouvertes (Firehol, spear.cx).

---

## 🚀 Lancement

```bash
# Activer l'environnement virtuel
.\venv\Scripts\activate

# Lancer le pipeline complet
python main.py
```

---

## 🧩 Modules

| Fichier | Description |
|---|---|
| `collecte.py` | Collecte données réelles (Firehol + spear.cx) |
| `extraction_iocs.py` | Extraction des IOCs (IPs, domaines, hashs) |
| `detection_anomalies.py` | Détection anomalies par Z-score (N-sigma) |
| `detection_anomalies_mobile.py` | Détection N-sigma avec moyenne mobile glissante |
| `isolation_forest.py` | Isolation Forest + Extended Isolation Forest |
| `ml_supervise.py` | Classification ML supervisée (LR, Random Forest, SVM) |
| `prediction_temporelle.py` | Prédiction temporelle sur 30 jours |
| `clustering.py` | Clustering K-Means — 4 familles de menaces |
| `graph_menaces.py` | Modélisation par graphes (NetworkX) |
| `lstm_sktime.py` | Prédiction séquentielle LSTM (via sktime) |
| `vrai_llm_qwen.py` | Analyse contextuelle LLM (Qwen 1.8B local) |
| `stockage_sqlite.py` | Stockage structuré en base SQLite |

---

## 📊 Données collectées

| Source | Type | Quantité |
|---|---|---|
| Firehol level1 | IPs / Plages CIDR blacklistées | 4 385 |
| spear.cx | Domaines suspects | 89 |
| spear.cx | Hashs MD5 malveillants | 9 |
| **Total IOCs** | | **4 483** |

---

## 📈 Résultats obtenus

| Méthode | Résultat |
|---|---|
| Z-score | 62 anomalies détectées (1.4%) |
| Moyenne mobile | 106 anomalies détectées (2.4%) |
| Isolation Forest | 223 anomalies détectées (5.0%) |
| Extended IF | 217 anomalies détectées (4.8%) |
| ML supervisé (meilleur) | Logistic Regression — 97.73% accuracy |
| Clustering K-Means | 4 familles : DDoS, Phishing, Reconnaissance, Malware |

---

## ⚙️ Installation

```bash
pip install -r requirements.txt
```

**Prérequis LLM :**
```bash
# Installer Ollama puis télécharger le modèle
ollama pull qwen:1.8b
```

---

## 🛠️ Technologies

`Python 3.14` · `scikit-learn` · `NetworkX` · `sktime` · `Ollama` ·
`SQLite` · `matplotlib` · `pandas` · `numpy` · `BeautifulSoup`