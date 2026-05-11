import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import json
from datetime import datetime

print("\n=== CLUSTERING DES MENACES (K-MEANS) ===\n")
print("Methode demandee par le PDF section 5.4 : Regroupement automatique des menaces similaires")

# 1. SIMULATION DE DONNEES DE MENACES
print("[1/4] Generation des donnees de menaces...")

np.random.seed(42)
n_menaces = 200

# Caracteristiques des menaces :
# - nb_connexions : nombre de connexions suspectes
# - ports_differents : nombre de ports differents utilises
# - duree_heures : duree de l'attaque en heures
# - score_gravite : gravite de 0 a 100

nb_connexions = np.random.normal(50, 20, n_menaces)
ports_differents = np.random.normal(10, 5, n_menaces)
duree_heures = np.random.normal(2, 1, n_menaces)
score_gravite = np.random.normal(60, 20, n_menaces)

# Creer 4 types de menaces distincts (pour que le clustering ait du sens)
# Type 1 : Attaques DDoS (connexions massives)
for i in range(40):
    nb_connexions[i] = np.random.normal(200, 30)
    ports_differents[i] = np.random.normal(5, 2)
    duree_heures[i] = np.random.normal(4, 1)
    score_gravite[i] = np.random.normal(85, 10)

# Type 2 : Scan de ports (peu de connexions, beaucoup de ports)
for i in range(40, 80):
    nb_connexions[i] = np.random.normal(20, 10)
    ports_differents[i] = np.random.normal(50, 15)
    duree_heures[i] = np.random.normal(1, 0.5)
    score_gravite[i] = np.random.normal(40, 15)

# Type 3 : Malware lent (longue duree)
for i in range(80, 120):
    nb_connexions[i] = np.random.normal(30, 10)
    ports_differents[i] = np.random.normal(8, 3)
    duree_heures[i] = np.random.normal(10, 3)
    score_gravite[i] = np.random.normal(70, 15)

# Type 4 : Attaques variees (valeurs moyennes)
for i in range(120, 200):
    nb_connexions[i] = np.random.normal(60, 25)
    ports_differents[i] = np.random.normal(15, 8)
    duree_heures[i] = np.random.normal(3, 2)
    score_gravite[i] = np.random.normal(55, 20)

df = pd.DataFrame({
    'nb_connexions': nb_connexions,
    'ports_differents': ports_differents,
    'duree_heures': duree_heures,
    'score_gravite': score_gravite
})

print(f"   Total menaces generees: {n_menaces}")
print(f"   Caracteristiques: connexions, ports, duree, gravite")

# 2. NORMALISATION DES DONNEES
print("\n[2/4] Normalisation des donnees...")

scaler = StandardScaler()
features = df[['nb_connexions', 'ports_differents', 'duree_heures', 'score_gravite']].values
features_normalisees = scaler.fit_transform(features)
print("   Donnees normalisees (moyenne=0, ecart-type=1)")

# 3. CLUSTERING AVEC K-MEANS
print("\n[3/4] Execution du clustering K-Means...")

# Determiner le nombre optimal de clusters (methode du coude)
inerties = []
K_range = range(1, 11)
for k in K_range:
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    kmeans.fit(features_normalisees)
    inerties.append(kmeans.inertia_)

# Choisir k=4 (car on a 4 types de menaces)
k_optimal = 4
kmeans = KMeans(n_clusters=k_optimal, random_state=42, n_init=10)
df['cluster'] = kmeans.fit_predict(features_normalisees)

print(f"   Nombre de clusters: {k_optimal}")
print(f"   Repartition:")
for i in range(k_optimal):
    print(f"      Cluster {i}: {(df['cluster'] == i).sum()} menaces")

# 4. ANALYSE DES CLUSTERS
print("\n[4/4] Analyse des clusters trouves...")

clusters_analyse = []
for i in range(k_optimal):
    cluster_data = df[df['cluster'] == i]
    cluster_info = {
        "cluster_id": int(i),
        "nb_menaces": int(len(cluster_data)),
        "moyenne_connexions": round(cluster_data['nb_connexions'].mean(), 1),
        "moyenne_ports": round(cluster_data['ports_differents'].mean(), 1),
        "moyenne_duree_heures": round(cluster_data['duree_heures'].mean(), 1),
        "moyenne_gravite": round(cluster_data['score_gravite'].mean(), 1),
        "type_menace": ""
    }
    
    # Identifier le type de menace
    if cluster_info["moyenne_connexions"] > 150:
        cluster_info["type_menace"] = "🔴 DDoS / Attaque massive"
    elif cluster_info["moyenne_ports"] > 30:
        cluster_info["type_menace"] = "🟠 Scan de ports / Reconnaissance"
    elif cluster_info["moyenne_duree_heures"] > 7:
        cluster_info["type_menace"] = "🟡 Malware persistant / APT"
    else:
        cluster_info["type_menace"] = "🟢 Attaque variee / Multiple"
    
    clusters_analyse.append(cluster_info)
    
    print(f"\n   Cluster {i}: {cluster_info['type_menace']}")
    print(f"      - {cluster_info['nb_menaces']} menaces")
    print(f"      - Moyenne connexions: {cluster_info['moyenne_connexions']}")
    print(f"      - Moyenne duree: {cluster_info['moyenne_duree_heures']}h")
    print(f"      - Gravite moyenne: {cluster_info['moyenne_gravite']}/100")

# 5. SAUVEGARDE DES RESULTATS
print("\n[5/5] Sauvegarde des resultats...")

rapport = {
    "date_analyse": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "methode": "K-Means Clustering",
    "n_menaces": n_menaces,
    "n_clusters": k_optimal,
    "clusters": clusters_analyse
}

with open("clustering_resultats.json", "w", encoding="utf-8") as f:
    json.dump(rapport, f, indent=2, ensure_ascii=False)

# 6. GRAPHIQUE VISUALISATION
print("\n[6/6] Generation du graphique...")

plt.figure(figsize=(10, 6))
couleurs = ['red', 'blue', 'green', 'orange']
for i in range(k_optimal):
    cluster_data = df[df['cluster'] == i]
    plt.scatter(cluster_data['nb_connexions'], 
                cluster_data['duree_heures'], 
                c=couleurs[i], 
                label=f'Cluster {i}',
                alpha=0.7,
                s=50)

plt.xlabel('Nombre de connexions suspectes')
plt.ylabel('Duree de l\'attaque (heures)')
plt.title('Clustering des menaces (K-Means) - 4 types identifies')
plt.legend()
plt.grid(True, alpha=0.3)
plt.savefig('clustering_menaces.png', dpi=100, bbox_inches='tight')
print("   Graphique sauvegarde: 'clustering_menaces.png'")

# AFFICHAGE FINAL
print("\nRESUME DU CLUSTERING")
print("="*50)
print(f"Total menaces analysees: {n_menaces}")
print(f"Clusters identifies: {k_optimal}")
print("\nTypes de menaces identifies:")
for cluster in clusters_analyse:
    print(f"   {cluster['type_menace']}")

print("\nResultats sauvegardes dans 'clustering_resultats.json'")
print("Graphique sauvegarde dans 'clustering_menaces.png'")

print("\n=== FIN CLUSTERING ===")