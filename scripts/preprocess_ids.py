#!/usr/bin/env python3
"""
Catnip Games International - IDS Alert Preprocessor
====================================================
Parses Snort-format IDS alert logs into structured JSON.
Extracts signatures, classifications, priorities, network data.

Usage: python3 preprocess_ids.py <input_alert_log> <output_json>
Example: python3 preprocess_ids.py ./ids_alerts.log ./ids_enriched.json

Author: Anton Ivanov - Data Operations Team
Date: April 2026
"""

import re
import json
import sys
import os
from datetime import datetime, timezone
from collections import Counter

# Map Snort priority numbers to severity labels
SEVERITY_MAP = {
    "1": "CRITICAL",
    "2": "HIGH",
    "3": "MEDIUM",
    "4": "LOW",
}


def parse_snort_alert(block):
    """
    Parse a multi-line Snort alert block into structured data.

    Snort alert format (3 lines):
      [**] [1:100001:3] ET SCAN Potential SSH Scan [**]
      [Classification: attempted-recon] [Priority: 2]
      04/01/2026-14:30:01.123456 10.1.2.3:54321 -> 192.168.100.1:22 TCP
    """
    # Extract signature ID and message
    sig = re.search(r"\[\*\*\]\s*\[([^\]]+)\]\s*(.+?)\s*\[\*\*\]", block)
    # Extract classification
    cls = re.search(r"\[Classification:\s*(.+?)\]", block)
    # Extract priority
    pri = re.search(r"\[Priority:\s*(\d+)\]", block)
    # Extract network metadata (src:port -> dst:port proto)
    net = re.search(
        r"(\d+\.\d+\.\d+\.\d+):(\d+)\s*->\s*(\d+\.\d+\.\d+\.\d+):(\d+)\s*(\w+)",
        block
    )
    # Extract timestamp
    ts = re.search(r"(\d{2}/\d{2}/\d{4}-\d{2}:\d{2}:\d{2}\.\d+)", block)

    if not sig:
        return None

    result = {
        "timestamp_original": ts.group(1) if ts else None,
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "ids_sid": sig.group(1).strip(),
        "ids_signature": sig.group(2).strip(),
        "ids_classification": cls.group(1) if cls else "unclassified",
        "ids_priority": pri.group(1) if pri else "4",
        "severity": SEVERITY_MAP.get(pri.group(1), "LOW") if pri else "LOW",
        "event_category": "intrusion_detection",
    }

    if net:
        result["source_ip"] = net.group(1)
        result["source_port"] = int(net.group(2))
        result["destination_ip"] = net.group(3)
        result["destination_port"] = int(net.group(4))
        result["network_protocol"] = net.group(5)

    return result


def process_ids_file(input_path, output_path):
    """Process a Snort alert log file and output enriched JSON."""
    stats = Counter()
    sev_stats = Counter()
    target_ips = Counter()
    target_ports = Counter()
    source_ips = Counter()
    results = []

    print(f"[*] Catnip Games - IDS Preprocessor v1.0")
    print(f"[*] Input: {input_path}")
    print(f"[*] Output: {output_path}")
    print(f"{'=' * 55}")

    with open(input_path, "r") as f:
        content = f.read()

    # Split by double newline (Snort alerts are separated by blank lines)
    blocks = content.split("\n")

    for block in blocks:
        if not block.strip():
            continue
        parsed = parse_snort_alert(block)
        if parsed:
            results.append(parsed)
            stats[parsed["ids_classification"]] += 1
            sev_stats[parsed["severity"]] += 1
            if "source_ip" in parsed:
                source_ips[parsed["source_ip"]] += 1
            if "destination_ip" in parsed:
                target_ips[parsed["destination_ip"]] += 1
            if "destination_port" in parsed:
                target_ports[parsed["destination_port"]] += 1

    with open(output_path, "w") as f:
        json.dump(results, f, indent=2)

    print(f"")
    print(f"[+] PROCESSING COMPLETE")
    print(f"    Total alerts parsed: {len(results)}")
    print(f"")
    print(f"[+] CLASSIFICATION BREAKDOWN:")
    for cls, count in stats.most_common():
        print(f"    {cls:35s} {count:5d}")
    print(f"")
    print(f"[+] SEVERITY DISTRIBUTION:")
    for sev, count in sev_stats.most_common():
        print(f"    {sev:10s} {count:5d}")
    print(f"")
    print(f"[+] TOP 10 SOURCE IPs (Attackers):")
    for ip, count in source_ips.most_common(10):
        print(f"    {ip:20s} {count:5d} alerts")
    print(f"")
    print(f"[+] TOP 10 TARGET IPs (Victims):")
    for ip, count in target_ips.most_common(10):
        print(f"    {ip:20s} {count:5d} alerts")
    print(f"")
    print(f"[+] TOP 10 TARGET PORTS:")
    for port, count in target_ports.most_common(10):
        print(f"    Port {port:<6d}          {count:5d} alerts")
    print(f"")
    print(f"[+] Output: {output_path}")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 preprocess_ids.py <input_alert_log> <output_json>")
        sys.exit(1)
    if not os.path.exists(sys.argv[1]):
        print(f"[!] Error: File not found: {sys.argv[1]}")
        sys.exit(1)
    process_ids_file(sys.argv[1], sys.argv[2])
