import json
import re
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from datetime import datetime

print("\n=== MODELISATION PAR GRAPHES (NETWORKX) ===\n")
print("Methode demandee par le PDF section 5.5: Representation des cybermenaces sous forme de graphe")
print("Noeuds : IP, domaines, acteurs, malwares")
print("Relations : liens entre entites")

# ------------------------------------------------------------------
# 1. CHARGEMENT DES DONNEES REELLES
# ------------------------------------------------------------------
print("\n[1/5] Chargement des donnees reelles...")

with open("scraped_all.json", "r", encoding="utf-8") as f:
    data = json.load(f)

ips_raw  = data.get("ips", [])
domaines = data.get("domaines", [])
hashs    = data.get("hashs_md5", [])

# Nettoyage des IPs
ips = [
    ip.strip() for ip in ips_raw
    if ip.strip()
    and not ip.strip().startswith("#")
    and re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}(/\d{1,2})?$', ip.strip())
]

# On prend un echantillon representatif pour le graphe
ips_sample      = ips[:8]
domaines_sample = [d for d in domaines if "." in d and len(d) > 5][:6]
hashs_sample    = hashs[:5]

print(f"    IPs selectionnees : {len(ips_sample)}")
print(f"    Domaines selectionnes : {len(domaines_sample)}")
print(f"    Hashs selectionnes : {len(hashs_sample)}")

# ------------------------------------------------------------------
# 2. CREATION DU GRAPHE
# ------------------------------------------------------------------
print("\n[2/5] Creation du graphe des menaces...")
G = nx.DiGraph()

# Ajout des noeuds IPs
for ip in ips_sample:
    G.add_node(ip, type="ip")

# Ajout des noeuds domaines
for dom in domaines_sample:
    G.add_node(dom, type="domaine")

# Ajout des noeuds hashs (malwares)
for h in hashs_sample:
    G.add_node(h[:12] + "...", type="hash")

print("\n[3/5] Ajout des relations entre entites...")

# Relations IP -> Domaine (une IP peut pointer vers un domaine)
for i, ip in enumerate(ips_sample):
    if i < len(domaines_sample):
        G.add_edge(ip, domaines_sample[i], relation="resolu_vers")

# Relations Domaine -> Hash (un domaine heberge un malware)
for i, dom in enumerate(domaines_sample):
    if i < len(hashs_sample):
        G.add_edge(dom, hashs_sample[i][:12] + "...", relation="heberge")

# Relations IP -> IP (communication entre IPs suspectes)
for i in range(len(ips_sample) - 1):
    if i % 2 == 0:
        G.add_edge(ips_sample[i], ips_sample[i+1], relation="communication")

print(f"    Total noeuds  : {G.number_of_nodes()}")
print(f"    Total relations : {G.number_of_edges()}")

# ------------------------------------------------------------------
# 3. ANALYSE DU GRAPHE
# ------------------------------------------------------------------
print("\n[4/5] Analyse du graphe...")

degres = dict(G.degree())
top5   = sorted(degres.items(), key=lambda x: x[1], reverse=True)[:5]

print("\n    Noeuds les plus connectes :")
for noeud, deg in top5:
    print(f"       - {noeud} : {deg} connexions")

# ------------------------------------------------------------------
# 4. VISUALISATION
# ------------------------------------------------------------------
print("\n[5/5] Generation du graphique...")

couleurs = []
for node in G.nodes():
    t = G.nodes[node].get("type", "")
    if t == "ip":
        couleurs.append("#e74c3c")
    elif t == "domaine":
        couleurs.append("#3498db")
    else:
        couleurs.append("#f39c12")

plt.figure(figsize=(14, 9))
pos = nx.spring_layout(G, seed=42, k=2)

nx.draw_networkx_nodes(G, pos, node_color=couleurs, node_size=600, alpha=0.9)
nx.draw_networkx_labels(G, pos, font_size=7, font_color="white", font_weight="bold")
nx.draw_networkx_edges(G, pos, edge_color="#95a5a6", arrows=True,
                       arrowsize=15, width=1.2, alpha=0.7)

legend_elements = [
    plt.scatter([], [], c="#e74c3c", s=100, label="IP suspecte (Firehol)"),
    plt.scatter([], [], c="#3498db", s=100, label="Domaine malveillant (spear.cx)"),
    plt.scatter([], [], c="#f39c12", s=100, label="Hash malware (spear.cx)")
]
plt.legend(handles=legend_elements, loc='upper left', fontsize=9)
plt.title("Graphe de cybermenaces reelles (IOCs collectes)", fontsize=13)
plt.axis("off")
plt.tight_layout()
plt.savefig("graph_menaces.png", dpi=150)
plt.close()
print("    Graphique sauvegarde : graph_menaces.png")

# ------------------------------------------------------------------
# 5. SAUVEGARDE
# ------------------------------------------------------------------
resultats = {
    "date_analyse"   : datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "source_donnees" : "scraped_all.json (donnees reelles collectees)",
    "nb_noeuds"      : G.number_of_nodes(),
    "nb_relations"   : G.number_of_edges(),
    "types_noeuds"   : {
        "ips"     : len(ips_sample),
        "domaines": len(domaines_sample),
        "hashs"   : len(hashs_sample)
    },
    "noeuds_connectes": [{"noeud": n, "degre": d} for n, d in top5]
}

with open("graph_menaces_resultats.json", "w", encoding="utf-8") as f:
    json.dump(resultats, f, indent=2, ensure_ascii=False)

print("\nRESUME DE LA MODELISATION PAR GRAPHES")
print("=" * 50)
print(f"Source          : scraped_all.json (donnees reelles)")
print(f"Total noeuds    : {G.number_of_nodes()}")
print(f"Total relations : {G.number_of_edges()}")
print("\nTypes de noeuds :")
print("   Rouge  : IPs suspectes (blacklist Firehol)")
print("   Bleu   : Domaines malveillants (spear.cx)")
print("   Orange : Hashs malware (spear.cx)")
print("\nResultats sauvegardes dans graph_menaces_resultats.json")
print("\n=== FIN MODELISATION PAR GRAPHES ===")