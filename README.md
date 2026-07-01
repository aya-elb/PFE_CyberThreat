# 🛡️ Système Intelligent de Détection et Prédiction des Cybermenaces

> Projet de Fin d'Études — Licence Statistique et Sciences des Données  
> FST Tanger — Université Abdelmalek Essaâdi — 2025/2026  
> **Auteure :** Aya EL BAKRAOUI  
> **Encadrant universitaire :** Pr. Halimi Rachid  
> **Encadrant entreprise :** Mr. Youssef Cheikhi (NearSecure, Rabat)

---

## 📌 Vue d'ensemble

Système automatisé combinant méthodes statistiques, Machine Learning et LLM
pour détecter, analyser et prédire les cybermenaces à partir de **9 383 IOCs réels**
collectés depuis trois sources ouvertes reconnues.

---

## 🚀 Lancement

### Pipeline complet
```bash
.\venv\Scripts\activate
python main.py
```

### Interface web
```bash
streamlit run app.py
```

---

## 🧩 Structure du projet
PFE_CyberThreat/

├── src/                    → 14 modules Python

├── outputs/                → Graphiques générés automatiquement

├── main.py                 → Orchestrateur principal

├── app.py                  → Interface web Streamlit

├── requirements.txt        → Dépendances Python

└── .env                    → Clés API (non pushé sur GitHub)

---

## 🧩 Modules

| Fichier | Description |
|---|---|
| `src/collecte.py` | Collecte depuis Firehol + spear.cx + AlienVault OTX |
| `src/extraction_iocs.py` | Extraction des IOCs (IPs, domaines, hashs) |
| `src/detection_anomalies.py` | Détection anomalies par Z-score |
| `src/detection_anomalies_mobile.py` | Détection N-sigma avec moyenne mobile |
| `src/isolation_forest.py` | Isolation Forest + Extended Isolation Forest |
| `src/ml_supervise.py` | Classification ML supervisée (LR, RF, SVM) |
| `src/clustering.py` | Clustering K-Means — 4 familles de menaces |
| `src/graph_menaces.py` | Modélisation par graphes (NetworkX) |
| `src/prediction_temporelle.py` | Prédiction temporelle — régression linéaire |
| `src/lstm_sktime.py` | Prédiction séquentielle LSTM (via sktime) |
| `src/vrai_llm_qwen.py` | Analyse contextuelle LLM (Qwen 1.8B local) |
| `src/stockage_sqlite.py` | Stockage structuré en base SQLite |
| `src/analyse_normalite.py` | Tests de normalité (Shapiro-Wilk, KS) |
| `src/validation_ml.py` | Validation croisée k-fold + ROC-AUC |

---

## 📊 Données collectées

| Source | Type | Quantité |
|---|---|---|
| Firehol Level 1 | IPs / Plages CIDR malveillantes | 4 729 |
| spear.cx + AlienVault OTX | Domaines suspects | 4 668 |
| spear.cx | Hashs MD5 malveillants | 10 |
| **Total IOCs** | | **9 383** |

---

## 📈 Résultats obtenus

| Méthode | Type | Résultat |
|---|---|---|
| Z-score | Statistique | 245 anomalies (2,6%) |
| Moyenne mobile N-sigma | Statistique adaptative | 254 anomalies (2,7%) |
| Isolation Forest | ML non-supervisé | 470 anomalies (5,0%) |
| Extended Isolation Forest | ML non-supervisé | 470 + 89 supplémentaires |
| Random Forest | ML supervisé | **93,73% accuracy — AUC 0,9654** |
| Logistic Regression | ML supervisé | 92,19% accuracy |
| SVM | ML supervisé | 92,29% accuracy |
| K-Means | Clustering | 4 familles de menaces |
| LSTM (sktime) | ML séquentiel | ~27 menaces/pas |
| LLM Qwen 1.8B | IA générative | Analyse contextuelle |

---

## ✅ Validation scientifique

| Test | Statistique | p-value | Conclusion |
|---|---|---|---|
| Shapiro-Wilk | W = 0,7282 | < 0,001 | Normalité rejetée |
| Kolmogorov-Smirnov | D = 0,2852 | < 0,001 | Normalité rejetée |

Validation croisée k-fold (k=5) — Random Forest : **93,88% ± 0,31% — IC95% [93,61 ; 94,15]**

---

## ⚙️ Installation

```bash
pip install -r requirements.txt
```

Créez un fichier `.env` à la racine :
OTX_API_KEY=votre_clé_ici

**Prérequis LLM :**
```bash
ollama pull qwen:1.8b
```

---

## 🛠️ Technologies

`Python 3.14` · `scikit-learn` · `NetworkX` · `sktime` · `Streamlit` ·
`Ollama` · `SQLite` · `matplotlib` · `pandas` · `numpy` · `BeautifulSoup`