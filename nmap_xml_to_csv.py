#!/usr/bin/env python3
import sys, csv, xml.etree.ElementTree as ET

if len(sys.argv) < 2:
    print("Kullanım: nmap_xml_to_csv.py <input.xml> [output.csv]")
    sys.exit(1)

xml_in = sys.argv[1]
csv_out = sys.argv[2] if len(sys.argv) > 2 else "nmap.csv"

try:
    root = ET.parse(xml_in).getroot()
except Exception as e:
    print(f"XML okunamadı: {e}")
    sys.exit(1)

rows = []
for host in root.findall("host"):
    addr = ""
    addr_el = host.find("address")
    if addr_el is not None:
        addr = addr_el.get("addr", "")

    for p in host.findall("./ports/port"):
        proto = p.get("protocol", "")
        portid = p.get("portid", "")
        state_el = p.find("state")
        state = state_el.get("state", "") if state_el is not None else ""
        svc = p.find("service")
        name = svc.get("name", "") if svc is not None else ""
        product = svc.get("product", "") if svc is not None else ""
        version = svc.get("version", "") if svc is not None else ""
        rows.append([addr, proto, portid, state, name, product, version])

with open(csv_out, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["host","proto","port","state","service","product","version"])
    w.writerows(rows)

print(f"Yazıldı: {csv_out}")
