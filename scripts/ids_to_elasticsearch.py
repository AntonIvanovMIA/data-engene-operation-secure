#!/usr/bin/env python3
"""
Catnip Games - IDS Alert Indexer
Parses Snort alerts and sends them DIRECTLY to Elasticsearch.
Bypasses Filebeat/Logstash for IDS data.
This demonstrates Python + Elasticsearch API integration.
"""
import re
import json
import random
import subprocess
import os
from datetime import datetime, timezone, timedelta

# ── Elasticsearch connection settings ──
ES_URL = "https://localhost:9200"
CA_CERT = "/etc/elasticsearch/certs/http_ca.crt"
ES_USER = "elastic"
ES_PASS = os.environ.get("ELASTIC_PASSWORD", "Anton@")
INDEX = f"logstash-firewall-{datetime.now(timezone.utc).strftime('%Y.%m.%d')}"

# ── IDS alert definitions ──
ALERTS = [
    (1,100001,"ET SCAN Potential SSH Scan","attempted-recon",2),
    (1,100002,"ET SCAN Nmap Scripting Engine Detected","attempted-recon",2),
    (1,100003,"ET SCAN Potential FTP Brute Force","attempted-recon",2),
    (1,200001,"ET EXPLOIT Possible SQL Injection Attempt","web-application-attack",1),
    (1,200002,"ET EXPLOIT Apache Struts Remote Code Execution","web-application-attack",1),
    (1,200003,"ET EXPLOIT PHP Remote File Include Attempt","web-application-attack",1),
    (1,300001,"GPL ATTACK_RESPONSE id check returned root","successful-admin",1),
    (1,300002,"ET MALWARE Known Malicious User-Agent String","trojan-activity",1),
    (1,300003,"ET MALWARE Win32 Emotet Command and Control","trojan-activity",1),
    (1,300004,"ET MALWARE CobaltStrike Beacon Activity Detected","trojan-activity",1),
    (1,400001,"ET DOS Possible TCP SYN Flood Attack","attempted-dos",2),
    (1,400002,"ET DOS Possible NTP Amplification DDoS","attempted-dos",2),
    (1,500001,"ET POLICY Outbound SSH on Non-Standard Port","policy-violation",3),
    (1,500002,"ET P2P BitTorrent DHT Ping Request","policy-violation",3),
]

SEVERITY_MAP = {"1": "CRITICAL", "2": "HIGH", "3": "MEDIUM", "4": "LOW"}

INTERNAL = ["192.168.100.1","192.168.100.10","192.168.100.20","192.168.100.30","192.168.100.40"]
EXTERNAL = [f"10.{random.randint(1,254)}.{random.randint(1,254)}.{random.randint(1,254)}" for _ in range(30)]
EXTERNAL += [f"203.0.113.{random.randint(1,254)}" for _ in range(10)]
PORTS = [22, 80, 443, 8080, 8443, 3306, 5432, 53, 25, 3389]


def send_to_elasticsearch(doc):
    """Send a single document to Elasticsearch."""
    body = json.dumps(doc)
    result = subprocess.run([
        "curl", "-s",
        "--cacert", CA_CERT,
        "-u", f"{ES_USER}:{ES_PASS}",
        "-X", "POST",
        f"{ES_URL}/{INDEX}/_doc",
        "-H", "Content-Type: application/json",
        "-d", body
    ], capture_output=True, text=True, timeout=10)
    return '"result":"created"' in result.stdout


def generate_and_index(count=500):
    """Generate IDS alerts and send directly to Elasticsearch."""
    now = datetime.now(timezone.utc)
    success = 0
    fail = 0

    print(f"[*] Catnip Games - IDS Alert Indexer v1.0")
    print(f"[*] Target: {ES_URL}/{INDEX}")
    print(f"[*] Generating and indexing {count} IDS alerts...")
    print(f"{'=' * 55}")

    for i in range(count):
        g, sid, msg, cls, pri = random.choice(ALERTS)
        src = random.choice(EXTERNAL)
        dst = random.choice(INTERNAL)
        sp = random.randint(1024, 65535)
        dp = random.choice(PORTS)
        proto = random.choice(["TCP", "UDP"])
        rev = random.randint(1, 5)
        ts = now - timedelta(minutes=random.randint(0, 10080))

        doc = {
            "@timestamp": ts.strftime("%Y-%m-%dT%H:%M:%S.000Z"),
            "event_category": "intrusion_detection",
            "event_outcome": "alert",
            "severity": SEVERITY_MAP.get(str(pri), "MEDIUM"),
            "source_vm": "gateway",
            "log_type": "ids",
            "ids_sid": f"{g}:{sid}:{rev}",
            "ids_signature": msg,
            "ids_classification": cls,
            "ids_priority": pri,
            "source_ip": src,
            "source_port": sp,
            "destination_ip": dst,
            "destination_port": dp,
            "network_protocol": proto,
            "host_name": "gateway",
            "process_name": "snort",
            "message": f"[**] [{g}:{sid}:{rev}] {msg} [**] [Classification: {cls}] [Priority: {pri}] {src}:{sp} -> {dst}:{dp} {proto}",
            "event_original": f"[**] [{g}:{sid}:{rev}] {msg} [**] [Classification: {cls}] [Priority: {pri}] {src}:{sp} -> {dst}:{dp} {proto}",
        }

        if send_to_elasticsearch(doc):
            success += 1
        else:
            fail += 1

        if (i + 1) % 100 == 0:
            print(f"    Indexed {i+1}/{count} (success: {success}, fail: {fail})")

    print(f"")
    print(f"[+] INDEXING COMPLETE")
    print(f"    Total: {count}")
    print(f"    Success: {success}")
    print(f"    Failed: {fail}")
    print(f"    Index: {INDEX}")
    print(f"")
    print(f"[+] Verify with:")
    print(f'    curl --cacert {CA_CERT} -u {ES_USER}:$ELASTIC_PASSWORD \\')
    print(f'      -s "{ES_URL}/logstash-firewall-*/_search" \\')
    print(f'      -H "Content-Type: application/json" \\')
    print(f"      -d '{{\"query\":{{\"term\":{{\"event_category.keyword\":\"intrusion_detection\"}}}},\"size\":0}}'")


if __name__ == "__main__":
    generate_and_index(500)

###Save: Ctrl+O, Enter, Ctrl+X

##**Run it:**

##export ELASTIC_PASSWORD='Anton@'
#python3 ~/catnip-soc/scripts/ids_to_elasticsearch.py`

#This will take 2-3 minutes (500 individual curl calls). Wait for it to finish.

#**Then verify:**
#```
#curl --cacert /etc/elasticsearch/certs/http_ca.crt \
 # -u elastic:$ELASTIC_PASSWORD \
  #-s "https://localhost:9200/logstash-firewall-*/_search" \
 # -H "Content-Type: application/json" \
 # -d '{"query":{"term":{"event_category.keyword":"intrusion_detection"}},"size":0}' 2>/dev/null###
