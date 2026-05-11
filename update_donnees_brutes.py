import json

with open("scraped_one_thread_full.json", "r") as f:
    data = json.load(f)

with open("donnees_brutes.txt", "w") as f:
    f.write("=== ADRESSES IP ===\n")
    f.write("\n=== DOMAINES ===\n")
    for d in data["domaines"]:
        f.write(d + "\n")
    f.write("\n=== HASH MD5 ===\n")
    for h in data["hashs"]:
        f.write(h + "\n")

print(f"donnees_brutes.txt mis a jour avec {len(data['domaines'])} domaines et {len(data['hashs'])} hashs")