#!/usr/bin/env python3
"""
Catnip Games International - Security Log Preprocessor
========================================================
Purpose:
  Parse raw syslog-format log files, classify events into
  security threat categories, assign severity levels, extract
  IP addresses and usernames, and output enriched JSON.

Usage:
  python3 preprocess_logs.py <input_log_file> <output_json_file>

Examples:
  python3 preprocess_logs.py /var/log/auth.log ./auth_enriched.json
  python3 preprocess_logs.py /var/log/syslog ./syslog_enriched.json

Author:  Anton Ivanov - Data Operations Team
Date:    March 2026
Version: 1.0
"""

import re
import json
import sys
import os
from datetime import datetime, timezone
from collections import Counter


# ================================================================
# THREAT CLASSIFICATION RULES
# ================================================================
# Each category contains regex patterns that identify specific
# types of security events. When a log message matches a pattern,
# it is classified into that threat category.
# The first matching category wins.
# ================================================================

THREAT_PATTERNS = {
    "brute_force": [
        r"Failed password for",
        r"Failed publickey for",
        r"authentication failure",
        r"Invalid user .* from",
        r"maximum authentication attempts",
        r"Too many authentication failures",
    ],
    "port_scan": [
        r"UFW BLOCK.*DPT=",
        r"refused connect from",
        r"Connection refused",
    ],
    "privilege_escalation": [
        r"sudo:.*COMMAND=",
        r"su\[.*\]: .*session opened",
        r"FAILED su for",
        r"pkexec",
    ],
    "service_anomaly": [
        r"segfault at",
        r"Out of memory",
        r"service .* failed",
        r"oom-killer",
        r"kernel:.*error",
    ],
    "reconnaissance": [
        r"nmap",
        r"nikto",
        r"masscan",
        r"Connection closed by.*\[preauth\]",
    ],
}

# Severity assigned to each threat category
SEVERITY_MAP = {
    "brute_force":          "HIGH",
    "port_scan":            "MEDIUM",
    "privilege_escalation": "HIGH",
    "service_anomaly":      "MEDIUM",
    "reconnaissance":       "MEDIUM",
    "normal":               "LOW",
}


# ================================================================
# PARSING FUNCTIONS
# ================================================================

def parse_syslog_line(line):
    """
    Parse a standard syslog-format line into structured fields.

    Syslog format: MMM dd HH:mm:ss hostname process[pid]: message
    Example: Mar 12 14:30:01 gateway sshd[1234]: Failed password for root

    Returns:
        dict with keys: timestamp, hostname, process, pid, message
        None if the line cannot be parsed
    """
    # Try multiple syslog formats
    patterns = [
        # Traditional: Mar 12 14:30:01 hostname process[pid]: message
        (r"^(?P<timestamp>\w{3}\s+\d{1,2}\s\d{2}:\d{2}:\d{2})\s+"
         r"(?P<hostname>[\w.-]+)\s+"
         r"(?P<process>[\w/.-]+)(?:\[(?P<pid>\d+)\])?:\s+"
         r"(?P<message>.+)$"),
        # ISO format: 2026-03-12T14:30:01.123456+00:00 hostname process[pid]: message
        (r"^(?P<timestamp>\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d+[+-]\d{2}:\d{2})\s+"
         r"(?P<hostname>[\w.-]+)\s+"
         r"(?P<process>[\w/.-]+)(?:\[(?P<pid>\d+)\])?:\s+"
         r"(?P<message>.+)$"),
        # Systemd journal: hostname process[pid]: message (no timestamp at start)
        (r"^(?P<hostname>[\w.-]+)\s+"
         r"(?P<process>[\w/.-]+)(?:\[(?P<pid>\d+)\])?:\s+"
         r"(?P<message>.+)$"),
    ]
    for pattern in patterns:
        match = re.match(pattern, line.strip())
        if match:
            result = match.groupdict()
            if "timestamp" not in result:
                result["timestamp"] = "unknown"
            return result
    return None

def classify_event(message):
    """
    Classify a log message into a threat category.

    Checks the message against all threat patterns defined
    in THREAT_PATTERNS. Returns the first matching category,
    or "normal" if no patterns match.
    """
    for category, patterns in THREAT_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, message, re.IGNORECASE):
                return category
    return "normal"


def extract_ip_addresses(message):
    """Extract all IPv4 addresses from a log message."""
    return re.findall(r"\b(?:\d{1,3}\.){3}\d{1,3}\b", message)


def extract_username(message):
    """Extract username from authentication-related messages."""
    patterns = [
        r"for (?:invalid user )?([\w.-]+) from",
        r"user=([\w.-]+)",
        r"session opened for user ([\w.-]+)",
        r"sudo:\s+([\w.-]+)",
    ]
    for pattern in patterns:
        match = re.search(pattern, message)
        if match:
            return match.group(1)
    return None


def enrich_event(parsed):
    """
    Enrich a parsed syslog event with security classification,
    severity, extracted IOCs, and UTC normalised timestamp.

    Takes a parsed dict from parse_syslog_line() and adds:
    - event_category: which threat type this event belongs to
    - severity: LOW, MEDIUM, or HIGH
    - source_ips: list of all IP addresses found in the message
    - username: extracted username if present
    - is_security_event: True if not "normal" category
    """
    if parsed is None:
        return None

    message = parsed.get("message", "")
    category = classify_event(message)
    ips = extract_ip_addresses(message)
    username = extract_username(message)

    enriched = {
        "timestamp_original": parsed["timestamp"],
        "timestamp_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
        "hostname": parsed["hostname"],
        "process": parsed["process"],
        "pid": parsed.get("pid"),
        "message": message,
        "event_category": category,
        "severity": SEVERITY_MAP.get(category, "LOW"),
        "source_ips": ips,
        "ip_count": len(ips),
        "username": username,
        "message_length": len(message),
        "is_security_event": category != "normal",
    }
    return enriched


# ================================================================
# MAIN PROCESSING FUNCTION
# ================================================================

def process_log_file(input_path, output_path):
    """
    Process an entire log file:
      1. Read each line
      2. Parse syslog format
      3. Classify and enrich each event
      4. Write enriched JSON output
      5. Print summary statistics
    """
    stats = Counter()
    severity_stats = Counter()
    ip_stats = Counter()
    user_stats = Counter()
    results = []
    unparsed = 0

    print(f"[*] Catnip Games - Log Preprocessor v1.0")
    print(f"[*] Input:  {input_path}")
    print(f"[*] Output: {output_path}")
    print(f"[*] Processing started at {datetime.now(timezone.utc).isoformat()}Z")
    print(f"{'=' * 55}")

    with open(input_path, "r", errors="replace") as f:
        for line_num, line in enumerate(f, 1):
            if not line.strip():
                continue

            parsed = parse_syslog_line(line)
            enriched = enrich_event(parsed)

            if enriched:
                results.append(enriched)
                stats[enriched["event_category"]] += 1
                severity_stats[enriched["severity"]] += 1
                for ip in enriched["source_ips"]:
                    ip_stats[ip] += 1
                if enriched["username"]:
                    user_stats[enriched["username"]] += 1
            else:
                unparsed += 1

    # Write enriched output
    with open(output_path, "w") as f:
        json.dump(results, f, indent=2, default=str)

    # Print comprehensive summary
    total = sum(stats.values())
    security = total - stats.get("normal", 0)

    print(f"")
    print(f"[+] PROCESSING COMPLETE")
    print(f"    Total lines processed:  {total + unparsed}")
    print(f"    Successfully parsed:    {total}")
    print(f"    Unparsed lines:         {unparsed}")
    print(f"    Security events found:  {security}")
    print(f"")
    print(f"[+] EVENT CATEGORY BREAKDOWN:")
    for cat, count in stats.most_common():
        pct = (count / total * 100) if total > 0 else 0
        sev = SEVERITY_MAP.get(cat, "N/A")
        print(f"    {cat:25s} {count:6d} ({pct:5.1f}%)  Severity: {sev}")
    print(f"")
    print(f"[+] SEVERITY DISTRIBUTION:")
    for sev, count in severity_stats.most_common():
        print(f"    {sev:10s} {count:6d}")
    print(f"")
    if ip_stats:
        print(f"[+] TOP 10 SOURCE IPs:")
        for ip, count in ip_stats.most_common(10):
            print(f"    {ip:20s} {count:6d} events")
    if user_stats:
        print(f"")
        print(f"[+] TOP 10 USERNAMES:")
        for user, count in user_stats.most_common(10):
            print(f"    {user:20s} {count:6d} events")
    print(f"")
    print(f"[+] Output written to: {output_path}")

    return stats


# ================================================================
# ENTRY POINT
# ================================================================

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 preprocess_logs.py <input_log> <output_json>")
        print("")
        print("Examples:")
        print("  python3 preprocess_logs.py /var/log/auth.log ./auth_enriched.json")
        print("  python3 preprocess_logs.py /var/log/syslog  ./syslog_enriched.json")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    if not os.path.exists(input_file):
        print(f"[!] Error: File not found: {input_file}")
        sys.exit(1)
    process_log_file(input_file, output_file)
