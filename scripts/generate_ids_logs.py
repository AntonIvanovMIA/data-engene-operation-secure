#!/usr/bin/env python3
"""
Catnip Games International - Simulated IDS Log Generator
=========================================================
Generates Snort-format IDS alerts for lab testing.

Snort alert format:
  [**] [generator:sid:rev] Alert Message [**]
  [Classification: type] [Priority: level]
  MM/DD/YYYY-HH:MM:SS.ffffff src_ip:src_port -> dst_ip:dst_port PROTO

This script generates 800 realistic alerts covering:
  - Reconnaissance (SSH scans, Nmap detection)
  - Exploits (SQL injection, Apache Struts RCE)
  - Trojans (malware C2, CobaltStrike)
  - Denial of Service (SYN flood, NTP amplification)
  - Policy violations (SSH on non-standard port, BitTorrent)

Usage: sudo python3 generate_ids_logs.py
Output: /var/log/snort/alert.log

Author: Anton Ivanov  - Data Operations Team
Date: April 2026
"""

import random
import os
from datetime import datetime, timedelta

# ================================================================
# IDS ALERT DEFINITIONS
# ================================================================
# Each tuple: (generator_id, signature_id, message, classification, priority)
# Priority 1 = highest severity, 4 = lowest
# Classifications follow Snort standard naming
# ================================================================

ALERTS = [
    # --- Reconnaissance ---
    (1, 100001, "ET SCAN Potential SSH Scan", "attempted-recon", 2),
# Detects multiple SSH connection attempts from one source = someone scanning for SSH servers
    (1, 100002, "ET SCAN Nmap Scripting Engine Detected", "attempted-recon", 2),
# Detects Nmap's NSE scripts which are used for vulnerability scanning
    (1, 100003, "ET SCAN Potential FTP Brute Force", "attempted-recon", 2),
# Multiple FTP login attempts from one source

    # --- Exploits ---
    (1, 200001, "ET EXPLOIT Possible SQL Injection Attempt", "web-application-attack", 1),
# Priority 1 (critical) - SQL injection can lead to data theft
    (1, 200002, "ET EXPLOIT Apache Struts Remote Code Execution", "web-application-attack", 1),
# Critical - allows attacker to execute commands on the web server
    (1, 200003, "ET EXPLOIT PHP Remote File Include Attempt", "web-application-attack", 1),
# Attacker trying to include malicious PHP code

    # --- Trojans / Malware ---
    (1, 300001, "GPL ATTACK_RESPONSE id check returned root", "successful-admin", 1),
# Critical - someone successfully gained root access
    (1, 300002, "ET MALWARE Known Malicious User-Agent String", "trojan-activity", 1),
# HTTP request using a user-agent associated with known malware
    (1, 300003, "ET MALWARE Win32/Emotet Command and Control", "trojan-activity", 1),
# Emotet malware communicating with its control server
    (1, 300004, "ET MALWARE CobaltStrike Beacon Activity Detected", "trojan-activity", 1),
# CobaltStrike is a penetration testing tool often used by attackers

    # --- Denial of Service ---
    (1, 400001, "ET DOS Possible TCP SYN Flood Attack", "attempted-dos", 2),
# SYN flood overwhelms a server by opening thousands of half-connections
    (1, 400002, "ET DOS Possible NTP Amplification DDoS", "attempted-dos", 2),
# Uses NTP servers to amplify traffic towards the victim

    # --- Policy Violations ---
    (1, 500001, "ET POLICY Outbound SSH on Non-Standard Port", "policy-violation", 3),
# SSH normally uses port 22 - using other ports may indicate tunnelling
    (1, 500002, "ET P2P BitTorrent DHT Ping Request", "policy-violation", 3),
# BitTorrent traffic on corporate network = policy violation
]

# ================================================================
# NETWORK ADDRESSES
# ============================================

# Internal IPs = your lab VMs (targets of attacks)
INTERNAL_IPS = [
    "192.168.100.1",   # Gateway
    "192.168.100.10",  # Webserver
    "192.168.100.20",  # Zabbix
    "192.168.100.30",  # ElasticStackServer
    "192.168.100.40",  # Workstation
]

# External IPs = simulated attackers (random public-looking IPs)
EXTERNAL_IPS = [
    f"10.{random.randint(1,254)}.{random.randint(1,254)}.{random.randint(1,254)}"
    for _ in range(30)
]
# Add some recognisable attack IPs
EXTERNAL_IPS += [
    f"203.0.113.{random.randint(1,254)}" for _ in range(10)
]

# Common target ports
PORTS_DST = [22, 80, 443, 8080, 8443, 3306, 5432, 53, 25, 3389]
# 22=SSH, 80=HTTP, 443=HTTPS, 3306=MySQL, 3389=RDP, etc.

# ================================================================
# GENERATE ALERTS
# ================================================================

OUTPUT = "/var/log/snort/alert.log"
os.makedirs("/var/log/snort", exist_ok=True)

NUM_ALERTS = 800
from datetime import datetime, timedelta, UTC

now = datetime.now(UTC)

print(f"[*] Catnip Games - IDS Alert Generator")
print(f"[*] Output: {OUTPUT}")
print(f"[*] Generating {NUM_ALERTS} alerts...")

with open(OUTPUT, "a") as f:
    for i in range(NUM_ALERTS):
        gen_rev, sid, msg, classtype, priority = random.choice(ALERTS)
        src = random.choice(EXTERNAL_IPS)
        dst = random.choice(INTERNAL_IPS)
        sport = random.randint(1024, 65535)
        dport = random.choice(PORTS_DST)
        proto = random.choice(["TCP", "UDP"])
        # Random timestamp within last 7 days
        ts = (now - timedelta(minutes=random.randint(0, 10080))).strftime("%m/%d/%Y-%H:%M:%S.%f")
        rev = random.randint(1, 5)

        alert = (
            f"[**] [{gen_rev}:{sid}:{rev}] {msg} [**]\n"
            f"[Classification: {classtype}] [Priority: {priority}]\n"
            f"{ts} {src}:{sport} -> {dst}:{dport} {proto}\n"
        )
        f.write(alert + "\n")

        if (i + 1) % 200 == 0:
            print(f"    Generated {i + 1}/{NUM_ALERTS} alerts...")

print(f"[+] Done! {NUM_ALERTS} alerts written to {OUTPUT}")
print(f"[+] Alert types: recon, exploit, trojan, DoS, policy violation")

