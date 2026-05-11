import json

# 1. Charger les domaines et hashs depuis spear.cx
with open("scraped_one_thread_full.json", "r") as f:
    spear_data = json.load(f)

# 2. Charger les IPs depuis Firehol (fichier texte)
ips = []
with open("firehol_ips.txt", "r") as f:
    for line in f:
        if line.strip():
            ips.append(line.strip())

# 3. Sauvegarder dans scraped_all.json
with open("scraped_all.json", "w") as f:
    json.dump({
        "ips": ips,
        "domaines": spear_data["domaines"],
        "hashs_md5": spear_data["hashs"]
    }, f, indent=2)

print(f"Sauvegarde terminee : {len(ips)} IPs, {len(spear_data['domaines'])} domaines, {len(spear_data['hashs'])} hashs")