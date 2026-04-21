#!/usr/bin/env python3
"""
Catnip Games - Live Demo Log Simulator
Generates security events in real-time during demos.
Events appear immediately in Kibana and Alert Monitor.
Usage: python3 demo_simulator.py
Author: Anton Ivanov
"""

import subprocess
import json
import os
import time
import random
from datetime import datetime, timezone

CA = "/etc/elasticsearch/certs/http_ca.crt"
URL = "https://localhost:9200"
USER = "elastic"
PWD = os.environ.get("ELASTIC_PASSWORD", "Anton@")

SCENARIOS = [
    {
        "sig": "ET SCAN Potential SSH Scan",
        "cls": "attempted-recon",
        "sev": "HIGH",
        "pri": 2,
        "dp": 22,
    },
    {
        "sig": "ET EXPLOIT SQL Injection Attempt",
        "cls": "web-application-attack",
        "sev": "CRITICAL",
        "pri": 1,
        "dp": 80,
    },
    {
        "sig": "ET MALWARE CobaltStrike Beacon",
        "cls": "trojan-activity",
        "sev": "CRITICAL",
        "pri": 1,
        "dp": 443,
    },
    {
        "sig": "ET DOS TCP SYN Flood",
        "cls": "attempted-dos",
        "sev": "HIGH",
        "pri": 2,
        "dp": 8080,
    },
    {
        "sig": "ET POLICY BitTorrent Traffic",
        "cls": "policy-violation",
        "sev": "MEDIUM",
        "pri": 3,
        "dp": 6881,
    },
    {
        "sig": "ET EXPLOIT Apache Struts RCE",
        "cls": "web-application-attack",
        "sev": "CRITICAL",
        "pri": 1,
        "dp": 8443,
    },
]

TARGETS = [
    "192.168.100.1",
    "192.168.100.10",
    "192.168.100.30",
    "192.168.100.40",
]

RED = "\033[91m"
YEL = "\033[93m"
GRN = "\033[92m"
RST = "\033[0m"


def send_event(doc: dict) -> None:
    """Send one event document to Elasticsearch."""
    idx = f"logstash-firewall-{datetime.now(timezone.utc).strftime('%Y.%m.%d')}"
    subprocess.run(
        [
            "curl",
            "-s",
            "--cacert",
            CA,
            "-u",
            f"{USER}:{PWD}",
            "-X",
            "POST",
            f"{URL}/{idx}/_doc",
            "-H",
            "Content-Type: application/json",
            "-d",
            json.dumps(doc),
        ],
        capture_output=True,
        text=True,
        timeout=10,
        check=False,
    )


def main() -> None:
    print("\n[*] CATNIP SOC - LIVE DEMO SIMULATOR")
    print("[*] Generating security events in real-time...")
    print("[*] Events appear in Kibana and Alert Monitor")
    print("[*] Press Ctrl+C to stop\n")

    count = 0

    try:
        while True:
            sc = random.choice(SCENARIOS)
            attacker = (
                f"10.{random.randint(1,254)}."
                f"{random.randint(1,254)}."
                f"{random.randint(1,254)}"
            )
            target = random.choice(TARGETS)
            now = datetime.now(timezone.utc)

            doc = {
                "@timestamp": now.strftime("%Y-%m-%dT%H:%M:%S.000Z"),
                "event_category": "intrusion_detection",
                "event_outcome": "alert",
                "severity": sc["sev"],
                "ids_signature": sc["sig"],
                "ids_classification": sc["cls"],
                "ids_priority": sc["pri"],
                "source_ip": attacker,
                "source_port": random.randint(1024, 65535),
                "destination_ip": target,
                "destination_port": sc["dp"],
                "network_protocol": random.choice(["TCP", "UDP"]),
                "source_vm": "gateway",
                "log_type": "ids",
                "host_name": "gateway",
                "process_name": "snort",
                "message": f'[LIVE] {sc["sig"]} from {attacker} to {target}:{sc["dp"]}',
            }

            send_event(doc)
            count += 1

            clr = RED if sc["sev"] == "CRITICAL" else YEL if sc["sev"] == "HIGH" else GRN
            print(
                f'  [{now.strftime("%H:%M:%S")}] '
                f'{clr}{sc["sev"]:8s}{RST} '
                f'{sc["sig"]:45s} '
                f'{attacker} -> {target}'
            )

            time.sleep(random.uniform(2, 5))

    except KeyboardInterrupt:
        print(f"\n[*] Simulator stopped. Generated {count} events.")
        print("[*] Check Kibana - new events should be visible!\n")


if __name__ == "__main__":
    main()
