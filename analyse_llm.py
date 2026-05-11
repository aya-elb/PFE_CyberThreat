import random
import json

print("=== ANALYSE PAR LLM (SIMULATION) ===\n")

# Lire les IOCs qu'on a extraits
try:
    with open("iocs_extraits.txt", "r", encoding="utf-8") as f:
        contenu = f.read()
except:
    print("Erreur: fichier iocs_extraits.txt introuvable")
    exit()

# Extraire les domaines manuellement
domaines = []
lignes = contenu.split("\n")
zone_domaines = False
for ligne in lignes:
    if "=== DOMAINES ===" in ligne:
        zone_domaines = True
        continue
    if zone_domaines and ligne.strip() and not ligne.startswith("==="):
        if "." in ligne:
            domaine = ligne.strip()
            if domaine not in domaines:
                domaines.append(domaine)

print(f"[INFO] Analyse de {len(domaines)} IOC(s) détecté(s)\n")

# Simulation d'une analyse par LLM
print("=== RAPPORT D'ANALYSE PAR LLM ===\n")

for ioc in domaines:
    # Simulation d'une analyse intelligente
    niveau_risque = random.choice(["FAIBLE", "MOYEN", "ÉLEVÉ", "CRITIQUE"])
    confiance = random.randint(60, 98)
    
    commentaires = [
        f"Le domaine {ioc} a été signalé dans des feeds de malwares récents.",
        f"Activité suspecte détectée sur {ioc} (connexions anormales).",
        f"{ioc} lié à une campagne de phishing observée la semaine dernière.",
        f"Aucune menace active connue pour {ioc} mais surveillance recommandée.",
        f"Corrélation positive avec des attaques ransomware récentes."
    ]
    commentaire = random.choice(commentaires)
    
    print(f" IOC: {ioc}")
    print(f"    Niveau de risque: {niveau_risque}")
    print(f"    Confiance: {confiance}%")
    print(f"    Insight: {commentaire}")
    print()

# Sauvegarder l'analyse dans un fichier JSON
resultats = {
    "date_analyse": "2026-04-13",
    "nb_iocs_analyses": len(domaines),
    "iocs": []
}

for ioc in domaines:
    resultats["iocs"].append({
        "ioc": ioc,
        "type": "domaine",
        "risque": random.choice(["FAIBLE", "MOYEN", "ÉLEVÉ", "CRITIQUE"]),
        "action_recommandee": random.choice(["Surveiller", "Bloquer", "Analyser", "Ignorer"])
    })

with open("analyse_llm_resultats.json", "w", encoding="utf-8") as f:
    json.dump(resultats, f, indent=2, ensure_ascii=False)

print(" Analyse sauvegardée dans 'analyse_llm_resultats.json'")
print("=== FIN ANALYSE LLM ===")