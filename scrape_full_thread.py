import requests
import re
import json

url = "https://spear.cx/showthread.php?tid=682"
headers = {"User-Agent": "Mozilla/5.0"}

r = requests.get(url, headers=headers, timeout=10)
html = r.text

# Expressions régulières
ip_pattern = r"\b(?:\d{1,3}\.){3}\d{1,3}\b"
domain_pattern = r"\b[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b"
md5_pattern = r"\b[a-fA-F0-9]{32}\b"
sha1_pattern = r"\b[a-fA-F0-9]{40}\b"

ips = list(set(re.findall(ip_pattern, html)))
domains = list(set(re.findall(domain_pattern, html)))
md5s = list(set(re.findall(md5_pattern, html)))
sha1s = list(set(re.findall(sha1_pattern, html)))

data = {
    "ips": ips,
    "domains": domains,
    "md5": md5s,
    "sha1": sha1s
}

with open("spear_indicators.json", "w") as f:
    json.dump(data, f, indent=2)

print(f"IPs  : {len(ips)}")
print(f"Domaines : {len(domains)}")
print(f"MD5  : {len(md5s)}")
print(f"SHA1 : {len(sha1s)}")