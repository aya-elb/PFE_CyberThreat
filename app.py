import streamlit as st
import json
import os
import pandas as pd
from PIL import Image

st.set_page_config(
    page_title="Système de Détection des Cybermenaces",
    page_icon="🛡️",
    layout="wide"
)

st.title("🛡️ Système Intelligent de Détection des Cybermenaces")
st.markdown("**Projet de Fin d'Études — Aya EL BAKRAOUI — FST Tanger 2025/2026**")
st.markdown("---")

st.sidebar.title("Navigation")
page = st.sidebar.radio("Choisir une section", [
    "📊 Vue d'ensemble",
    "📈 Détection statistique",
    "🌲 Isolation Forest",
    "🤖 ML Supervisé",
    "🔵 Clustering K-Means",
    "🕸️ Graphes de menaces",
    "📅 Prédiction temporelle",
    "✅ Validation scientifique"
])

def load_json(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return None

def show_image(path, caption=""):
    full_path = os.path.join("outputs", path)
    if os.path.exists(full_path):
        img = Image.open(full_path)
        st.image(img, caption=caption, use_column_width=True)
    else:
        st.info(f"Image non disponible : {path}")

if page == "📊 Vue d'ensemble":
    st.header("Vue d'ensemble du système")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("IOCs collectés", "9 383")
    col2.metric("Méthodes implémentées", "8")
    col3.metric("Meilleure accuracy", "93,73%")
    col4.metric("Familles de menaces", "4")
    st.markdown("---")
    st.subheader("Résumé des résultats")
    data = {
        "Méthode": ["Z-score", "Moy. mobile", "Isolation Forest", "Extended IF", "Random Forest", "K-Means"],
        "Type": ["Statistique", "Statistique", "ML non-supervisé", "ML non-supervisé", "ML supervisé", "Clustering"],
        "Résultat": ["245 anomalies (2,6%)", "254 anomalies (2,7%)", "470 anomalies (5,0%)", "+89 supplémentaires", "93,73% accuracy", "4 familles"]
    }
    st.dataframe(pd.DataFrame(data), use_container_width=True)

elif page == "📈 Détection statistique":
    st.header("Détection d'anomalies statistiques")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Z-score")
        st.metric("Anomalies détectées", "245")
        st.metric("Pourcentage", "2,6%")
        st.metric("Seuil utilisé", "2,5σ")
    with col2:
        st.subheader("Moyenne mobile")
        st.metric("Anomalies détectées", "254")
        st.metric("Pourcentage", "2,7%")
        st.metric("Fenêtre glissante", "50 IOCs")
    st.markdown("---")
    show_image("detection_mobile.png", "Détection par N-sigma avec moyenne mobile")

elif page == "🌲 Isolation Forest":
    st.header("Isolation Forest & Extended Isolation Forest")
    col1, col2, col3 = st.columns(3)
    col1.metric("IF — Anomalies", "470 (5,0%)")
    col2.metric("EIF — Anomalies", "470 (5,0%)")
    col3.metric("Gain EIF", "+89 IOCs supplémentaires")
    st.markdown("---")
    show_image("isolation_forest_comparaison.png", "IF standard vs Extended IF")

elif page == "🤖 ML Supervisé":
    st.header("Classification supervisée")
    col1, col2, col3 = st.columns(3)
    col1.metric("Logistic Regression", "92,19%")
    col2.metric("🏆 Random Forest", "93,73%")
    col3.metric("SVM", "92,29%")
    st.markdown("---")
    st.subheader("Performances détaillées")
    perf = {
        "Modèle": ["Logistic Regression", "Random Forest", "SVM"],
        "Accuracy": ["92,19%", "93,73%", "92,29%"],
        "Précision": ["95,76%", "95,76%", "96,08%"],
        "Rappel": ["89,53%", "92,52%", "89,39%"],
        "F1-score": ["92,54%", "94,11%", "92,62%"],
        "AUC": ["0,9419", "0,9654", "0,9284"]
    }
    st.dataframe(pd.DataFrame(perf), use_container_width=True)
    col1, col2 = st.columns(2)
    with col1:
        show_image("matrices_confusion.png", "Matrices de confusion")
    with col2:
        show_image("courbes_roc.png", "Courbes ROC")

elif page == "🔵 Clustering K-Means":
    st.header("Clustering K-Means — 4 familles de menaces")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("DDoS / Plage réseau", "4 707 IOCs", "50,2%")
    col2.metric("Reconnaissance", "2 785 IOCs", "29,7%")
    col3.metric("Phishing", "1 863 IOCs", "19,9%")
    col4.metric("Malware DGA", "28 IOCs", "0,3%")
    st.markdown("---")
    show_image("clustering_menaces.png", "Visualisation des clusters K-Means")

elif page == "🕸️ Graphes de menaces":
    st.header("Modélisation par graphes (NetworkX)")
    col1, col2, col3 = st.columns(3)
    col1.metric("Nœuds", "19")
    col2.metric("Relations", "15")
    col3.metric("Types", "IP / Domaines / Hashs")
    st.markdown("---")
    show_image("graph_menaces.png", "Graphe de relations entre IOCs")
    st.info("🔴 Rouge = IPs suspectes   |   🔵 Bleu = Domaines malveillants   |   🟠 Orange = Hashs malware")

elif page == "📅 Prédiction temporelle":
    st.header("Prédiction temporelle des cybermenaces")
    col1, col2, col3 = st.columns(3)
    col1.metric("MAE", "4,08 menaces/jour")
    col2.metric("Prévision 30j", "30,8 à 32,8 / jour")
    col3.metric("Pic prévu", "30 janvier 2026")
    st.markdown("---")
    show_image("prediction_menaces.png", "Prédiction temporelle — Régression linéaire")
    st.caption("Complété par LSTM (sktime) — prédictions stables à 27-28 menaces/pas")

elif page == "✅ Validation scientifique":
    st.header("Validation scientifique")
    st.subheader("Tests de normalité")
    norm = {
        "Test": ["Shapiro-Wilk", "Kolmogorov-Smirnov"],
        "Statistique": ["W = 0,7282", "D = 0,2852"],
        "p-value": ["< 0,001", "< 0,001"],
        "Conclusion": ["Normalité rejetée", "Normalité rejetée"]
    }
    st.dataframe(pd.DataFrame(norm), use_container_width=True)
    col1, col2 = st.columns(2)
    with col1:
        show_image("histogramme_normalite.png", "Histogramme")
    with col2:
        show_image("qqplot_normalite.png", "QQ-plot")
    st.markdown("---")
    st.subheader("Validation croisée k-fold (k=5)")
    cv = {
        "Modèle": ["Logistic Regression", "Random Forest", "SVM"],
        "CV moyenne": ["92,50%", "93,88%", "92,41%"],
        "Écart-type": ["±0,33%", "±0,31%", "±0,33%"],
        "IC à 95%": ["[92,21 ; 92,78]", "[93,61 ; 94,15]", "[92,12 ; 92,70]"]
    }
    st.dataframe(pd.DataFrame(cv), use_container_width=True)
    col1, col2 = st.columns(2)
    with col1:
        show_image("courbes_roc.png", "Courbes ROC")
    with col2:
        show_image("qqplot_normalite.png", "QQ-plot normalité")