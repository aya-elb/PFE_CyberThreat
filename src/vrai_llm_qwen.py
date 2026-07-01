import requests
import json
from datetime import datetime

print("=== ANALYSE LLM (Qwen 1.8B local via Ollama) ===\n")

try:
    with open("iocs_extraits.txt", "r", encoding="utf-8") as f:
        iocs = f.read()
except FileNotFoundError:
    print("[LLM] Fichier iocs_extraits.txt introuvable.")
    iocs = "Aucun IOC disponible."

prompt = (
    f"Tu es un expert en cybersecurite. Analyse ces indicateurs de compromission (IOCs) "
    f"et fournis : 1) le niveau de risque global (faible/moyen/eleve/critique), "
    f"2) une explication courte, 3) une recommandation concrete.\n\nIOCs :\n{iocs[:500]}"
)

try:
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": "qwen:1.8b", "prompt": prompt, "stream": False},
        timeout=180
    )
    resultat = response.json().get("response", "Aucune reponse.")
    print("[LLM] Analyse terminee avec succes.\n")
    print(resultat)

    with open("analyse_llm_resultats.json", "w", encoding="utf-8") as f:
        json.dump({
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "modele": "qwen:1.8b",
            "reponse": resultat
        }, f, indent=2, ensure_ascii=False)

except requests.exceptions.Timeout:
    print("[LLM] Delai depasse (180s). Modele trop lent sur CPU.")
    print("[LLM] Solution en production : deployer sur GPU ou utiliser une API cloud.")
except requests.exceptions.ConnectionError:
    print("[LLM] Ollama non demarre. Lancez 'ollama serve' avant d'executer le systeme.")
except Exception as e:
    print(f"[LLM] Erreur inattendue : {e}")

print("\n=== FIN ANALYSE LLM ===")