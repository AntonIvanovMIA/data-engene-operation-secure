#!/usr/bin/env python3
"""
generate_test_events.py
Author : Mohammad Ali - Week 5-6
Purpose: Insert simulated brute-force SSH events into Elasticsearch
         for testing bruteforce_detector.py
"""
import json, ssl, base64, os, urllib.request
from datetime import datetime, timezone

ES_USER = "elastic"
ES_PASS = "Anton@"
ES_HOST = "https://localhost:9200"
CA_CERT = "/etc/elasticsearch/certs/http_ca.crt"
INDEX   = f"logstash-firewall-{datetime.now().strftime('%Y.%m.%d')}"

TEST_ATTACKS = [
    {"ip": "10.10.10.99",  "user": "root",   "count": 15},
    {"ip": "10.20.30.40",  "user": "admin",  "count": 8},
    {"ip": "172.16.5.100", "user": "ubuntu", "count": 3},
]

def insert_doc(doc):
    url   = f"{ES_HOST}/{INDEX}/_doc"
    creds = base64.b64encode(f"{ES_USER}:{ES_PASS}".encode()).decode()
    headers = {"Authorization": f"Basic {creds}",
               "Content-Type": "application/json"}
    data = json.dumps(doc).encode()
    req  = urllib.request.Request(url, data=data,
                                   headers=headers, method="POST")
    if os.path.exists(CA_CERT):
        ctx = ssl.create_default_context(cafile=CA_CERT)
    else:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode    = ssl.CERT_NONE
    with urllib.request.urlopen(req, context=ctx, timeout=10) as r:
        return json.loads(r.read())

def main():
    print("\n  Inserting simulated brute-force events...\n")
    total = 0
    for attack in TEST_ATTACKS:
        for i in range(attack["count"]):
            doc = {
                "@timestamp": datetime.now(timezone.utc).isoformat(),
                "message": (
                    f"Apr 09 05:00:{i:02d} gateway sshd[100{i}]: "
                    f"Failed password for invalid user {attack['user']} "
                    f"from {attack['ip']} port 4400{i} ssh2"
                ),
                "event_category": "authentication",
                "event_outcome":  "failure",
                "source_ip":      attack["ip"],
                "auth_user":      attack["user"],
                "host_name":      "gateway",
                "severity":       "HIGH",
                "source_vm":      "gateway",
                "log_type":       "system"
            }
            insert_doc(doc)
            total += 1
        print(f"  Inserted {attack['count']} events from "
              f"{attack['ip']} targeting '{attack['user']}'")
    print(f"\n  Total inserted: {total} documents")
    print(f"  Index: {INDEX}\n")

if __name__ == "__main__":
    main()
