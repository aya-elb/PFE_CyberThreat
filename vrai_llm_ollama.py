import requests
import json

print("=== VRAI LLM AVEC OLLAMA ===\n")

with open("iocs_extraits.txt", "r") as f:
    iocs = f.read()

prompt = f"Analyse ces indicateurs de menace cyber : {iocs}. Donne le niveau de risque, une explication courte, une recommandation."

try:
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": "tinyllama", "prompt": prompt, "stream": False},
        timeout=60
    )
    result = response.json()
    print("\n=== REPONSE DU LLM ===\n")
    print(result["response"])
except Exception as e:
    print(f"Erreur : {e}")