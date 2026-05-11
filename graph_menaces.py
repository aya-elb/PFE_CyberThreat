import networkx as nx
import matplotlib.pyplot as plt
import random
from datetime import datetime
import json

print("\n=== MODELISATION PAR GRAPHES (NETWORKX) ===\n")
print("Methode demandee par le PDF section 5.5: Representation des cybermenaces sous forme de graphe")
print("Noeuds : IP, domaines, acteurs, malwares")
print("Relations : liens entre entites\n")

# 1. CREER LE GRAPHE
print("[1/5] Creation du graphe des menaces...")

G = nx.Graph()

# 2. AJOUTER LES NOEUDS (entites)
print("[2/5] Ajout des noeuds (IPs, domaines, acteurs, malwares)...")

# IPs suspectes
ips = [
    "185.130.5.253", "45.227.254.10", "103.112.215.56",
    "194.156.98.42", "81.17.30.45", "5.188.86.45"
]

# Domaines suspects
domaines = [
    "malware-c2.net", "phishing-site.org", "ransomware-ctrl.com",
    "botnet-cc.ru", "darkweb-market.onion", "evil-domain.xyz"
]

# Acteurs malveillants (groupes)
acteurs = [
    "APT28 (Fancy Bear)", "APT29 (Cozy Bear)", "Lazarus Group",
    "REvil (Ransomware)", "Conti Group", "DarkSide"
]

# Malwares
malwares = [
    "TrickBot", "Emotet", "Ryuk", "Dridex", "CobaltStrike", "Mirai"
]

# Ajouter tous les noeuds
for ip in ips:
    G.add_node(ip, type="IP")
for domaine in domaines:
    G.add_node(domaine, type="Domaine")
for acteur in acteurs:
    G.add_node(acteur, type="Acteur")
for malware in malwares:
    G.add_node(malware, type="Malware")

print(f"   Total noeuds: {G.number_of_nodes()}")
print(f"   - IPs: {len(ips)}")
print(f"   - Domaines: {len(domaines)}")
print(f"   - Acteurs: {len(acteurs)}")
print(f"   - Malwares: {len(malwares)}")

# 3. AJOUTER LES RELATIONS (aretes)
print("\n[3/5] Ajout des relations entre entites...")

# Relations IP -> Domaine
relations_ip_domaine = [
    ("185.130.5.253", "malware-c2.net"),
    ("45.227.254.10", "phishing-site.org"),
    ("103.112.215.56", "ransomware-ctrl.com"),
    ("194.156.98.42", "botnet-cc.ru"),
    ("81.17.30.45", "darkweb-market.onion"),
    ("5.188.86.45", "evil-domain.xyz"),
    ("185.130.5.253", "botnet-cc.ru"),
    ("45.227.254.10", "evil-domain.xyz"),
]

# Relations Domaine -> Malware
relations_domaine_malware = [
    ("malware-c2.net", "TrickBot"),
    ("malware-c2.net", "Emotet"),
    ("phishing-site.org", "Ryuk"),
    ("ransomware-ctrl.com", "Ryuk"),
    ("ransomware-ctrl.com", "CobaltStrike"),
    ("botnet-cc.ru", "Mirai"),
    ("darkweb-market.onion", "Dridex"),
    ("evil-domain.xyz", "Emotet"),
]

# Relations Acteur -> Malware
relations_acteur_malware = [
    ("APT28 (Fancy Bear)", "CobaltStrike"),
    ("APT28 (Fancy Bear)", "TrickBot"),
    ("APT29 (Cozy Bear)", "CobaltStrike"),
    ("Lazarus Group", "Ryuk"),
    ("REvil (Ransomware)", "Ryuk"),
    ("REvil (Ransomware)", "Dridex"),
    ("Conti Group", "Emotet"),
    ("DarkSide", "Mirai"),
]

# Relations Acteur -> IP
relations_acteur_ip = [
    ("APT28 (Fancy Bear)", "185.130.5.253"),
    ("APT29 (Cozy Bear)", "45.227.254.10"),
    ("Lazarus Group", "103.112.215.56"),
    ("REvil (Ransomware)", "81.17.30.45"),
    ("Conti Group", "194.156.98.42"),
]

# Ajouter toutes les relations
for source, cible in relations_ip_domaine:
    G.add_edge(source, cible, relation="resout vers")
for source, cible in relations_domaine_malware:
    G.add_edge(source, cible, relation="heberge")
for source, cible in relations_acteur_malware:
    G.add_edge(source, cible, relation="utilise")
for source, cible in relations_acteur_ip:
    G.add_edge(source, cible, relation="controle")

print(f"   Total relations (aretes): {G.number_of_edges()}")

# 4. ANALYSE DU GRAPHE
print("\n[4/5] Analyse du graphe...")

degres = dict(G.degree())
noeuds_importants = sorted(degres.items(), key=lambda x: x[1], reverse=True)[:5]

print(f"\n   Statistiques du graphe:")
print(f"   - Noeuds: {G.number_of_nodes()}")
print(f"   - Relations: {G.number_of_edges()}")
print(f"\n   Noeuds les plus connectes:")
for noeud, degre in noeuds_importants:
    print(f"      - {noeud}: {degre} connexions")

# 5. VISUALISATION
print("\n[5/5] Generation du graphique...")

plt.figure(figsize=(14, 10))

couleurs = []
for node in G.nodes():
    if G.nodes[node]['type'] == 'IP':
        couleurs.append('red')
    elif G.nodes[node]['type'] == 'Domaine':
        couleurs.append('blue')
    elif G.nodes[node]['type'] == 'Acteur':
        couleurs.append('green')
    else:
        couleurs.append('orange')

pos = nx.spring_layout(G, k=1.5, iterations=50, seed=42)

nx.draw(G, pos, 
        node_color=couleurs, 
        node_size=800,
        with_labels=True, 
        font_size=8,
        font_weight='bold',
        edge_color='gray',
        alpha=0.9)

plt.title('Graphe des Cybermenaces\n(IPs, Domaines, Acteurs, Malwares)', 
          fontsize=14, fontweight='bold')
plt.tight_layout()

plt.savefig('graph_menaces.png', dpi=150, bbox_inches='tight')
print("   Graphique sauvegarde: 'graph_menaces.png'")

# Sauvegarde des resultats
resultats = {
    "date_analyse": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "methode": "NetworkX - Graphe de menaces",
    "nb_noeuds": G.number_of_nodes(),
    "nb_relations": G.number_of_edges(),
    "noeuds_importants": [
        {"noeud": noeud, "connexions": degre} 
        for noeud, degre in noeuds_importants
    ]
}

with open("graph_menaces_resultats.json", "w", encoding="utf-8") as f:
    json.dump(resultats, f, indent=2, ensure_ascii=False)

print("   Resultats sauvegardes dans 'graph_menaces_resultats.json'")

# AFFICHAGE FINAL
print("\n" + "="*50)
print("RESUME DE LA MODELISATION PAR GRAPHES")
print("="*50)
print(f"Total noeuds: {G.number_of_nodes()}")
print(f"Total relations: {G.number_of_edges()}")
print("\nTypes de noeuds:")
print("   Rouge: IPs suspectes")
print("   Bleu: Domaines malveillants")
print("   Vert: Acteurs (groupes cybercriminels)")
print("   Orange: Malwares")
print("\nRelations identifiees:")
print("   - IP -> Domaine: resolution DNS")
print("   - Domaine -> Malware: hebergement")
print("   - Acteur -> Malware: utilisation")
print("   - Acteur -> IP: controle")

print("\n=== FIN MODELISATION PAR GRAPHES ===")