#!/usr/bin/env python3
"""
Catnip Games International - ELK Stack Health Monitor
=====================================================
Checks all ELK components and reports system status.
Run manually or schedule with cron for continuous monitoring.

Usage: python3 health_check.py
Requires: export ELASTIC_PASSWORD=your_password

Author: Anton Ivanov - Data Operations Team
Date: April 2026
"""

import subprocess
import json
import os
from datetime import datetime, timezone

# ── Elasticsearch connection settings ──
CA = "/etc/elasticsearch/certs/http_ca.crt"
URL = "https://localhost:9200"
USER = "elastic"
PWD = os.environ.get("ELASTIC_PASSWORD", "Anton@")


def run_cmd(cmd_str):
    """Run a shell command and return stdout + return code."""
    try:
        r = subprocess.run(cmd_str, shell=True, capture_output=True,
                          text=True, timeout=15)
        return r.stdout.strip(), r.returncode
    except subprocess.TimeoutExpired:
        return "TIMEOUT", 1
    except Exception as e:
        return str(e), 1


def check_service(name):
    """Check if a systemd service is active."""
    out, rc = run_cmd(f"systemctl is-active {name}")
    ok = out == "active"
    icon = "[  OK  ]" if ok else "[ FAIL ]"
    print(f"  {icon} {name}: {out}")
    return ok


def check_port(port, service_name):
    """Check if a port is listening."""
    out, _ = run_cmd("ss -lntp")
    ok = f":{port}" in out
    icon = "[  OK  ]" if ok else "[ FAIL ]"
    print(f"  {icon} {service_name} port {port}")
    return ok


def check_cluster():
    """Check Elasticsearch cluster health."""
    out, _ = run_cmd(
        f'curl -s --cacert {CA} -u {USER}:{PWD} {URL}/_cluster/health'
    )
    try:
        h = json.loads(out)
        status = h.get("status", "unknown")
        icon = "[  OK  ]" if status in ("green", "yellow") else "[ FAIL ]"
        print(f"  {icon} Cluster: {h.get('cluster_name', '?')}")
        print(f"         Status: {status}")
        print(f"         Nodes: {h.get('number_of_nodes', 0)}")
        print(f"         Active shards: {h.get('active_shards', 0)}")
        return status in ("green", "yellow")
    except Exception:
        print("  [ FAIL ] Cannot parse cluster health")
        return False


def check_indices():
    """Show log index information."""
    out, _ = run_cmd(
        f'curl -s --cacert {CA} -u {USER}:{PWD}'
        f' "{URL}/_cat/indices/logstash-*?v&h=index,docs.count,store.size"'
    )
    if out:
        print(f"  Indices:")
        for line in out.split("\n")[:10]:
            print(f"    {line}")


def check_disk():
    """Check disk usage."""
    out, _ = run_cmd("df -h / | tail -1")
    parts = out.split()
    if len(parts) >= 5:
        usage = parts[4].replace("%", "")
        ok = int(usage) < 85
        icon = "[  OK  ]" if ok else "[ WARN ]"
        print(f"  {icon} Disk usage: {parts[4]} ({parts[3]} free)")
        return ok
    return True


def check_memory():
    """Check memory usage."""
    out, _ = run_cmd("free -h | grep Mem")
    parts = out.split()
    if len(parts) >= 4:
        print(f"  [ INFO ] Memory: {parts[2]} used / {parts[1]} total")
    return True


def main():
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    print("")
    print("=" * 58)
    print("  CATNIP GAMES SOC - SYSTEM HEALTH CHECK")
    print(f"  {ts}")
    print("=" * 58)

    results = []

    print(f"\n[1] SERVICES")
    results.append(check_service("elasticsearch"))
    results.append(check_service("kibana"))
    results.append(check_service("logstash"))

    print(f"\n[2] PORTS")
    results.append(check_port(9200, "Elasticsearch"))
    results.append(check_port(5601, "Kibana"))
    results.append(check_port(5044, "Logstash"))

    print(f"\n[3] ELASTICSEARCH CLUSTER")
    results.append(check_cluster())

    print(f"\n[4] LOG INDICES")
    check_indices()

    print(f"\n[5] SYSTEM RESOURCES")
    results.append(check_disk())
    check_memory()

    passed = sum(1 for r in results if r)
    total = len(results)
    overall = "HEALTHY" if passed == total else "DEGRADED"
    color = "\033[92m" if overall == "HEALTHY" else "\033[93m"

    print("")
    print("=" * 58)
    print(f"  RESULT: {passed}/{total} checks passed")
    print(f"  STATUS: {color}{overall}\033[0m")
    print("=" * 58)
    print("")


if __name__ == "__main__":
    main()

