import json

with open("spear_indicators.json", "r") as f:
    data = json.load(f)

with open("donnees_brutes.txt", "w") as f:
    f.write("=== ADRESSES IP ===\n")
    for ip in data["ips"]:
        f.write(ip + "\n")
    f.write("\n=== DOMAINES ===\n")
    for domaine in data["domains"]:
        f.write(domaine + "\n")
    f.write("\n=== HASH MD5 ===\n")
    for hash_md5 in data["md5"]:
        f.write(hash_md5 + "\n")

print("donnees_brutes.txt mis a jour avec des IOCs reels")