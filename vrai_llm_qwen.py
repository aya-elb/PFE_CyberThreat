import requests
import json

print("=== VRAI LLM AVEC QWEN 1.8B ===\n")

with open("iocs_extraits.txt", "r") as f:
    iocs = f.read()

prompt = f"Analyse ces indicateurs de menace : {iocs}. Donne le niveau de risque, une explication courte, une recommandation."

try:
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": "qwen:1.8b", "prompt": prompt, "stream": False},
        timeout=180
    )
    print("\n=== REPONSE DU LLM ===\n")
    print(response.json()["response"])
except Exception as e:
    print(f"Erreur : {e}")