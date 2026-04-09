#!/usr/bin/env python3
import json
import ssl
import base64
import os
import sys
import re
import urllib.request
import urllib.error
from datetime import datetime, timezone
from collections import defaultdict

ES_USER = "elastic"
ES_PASS = "Anton@"
ES_HOST = "https://localhost:9200"
ES_INDEX = "logstash-firewall-*"
CA_CERT = "/etc/elasticsearch/certs/http_ca.crt"
THRESHOLD = 5
CRITICAL_LIMIT = 20
TIME_WINDOW_MIN = 999999
REPORT_DIR = os.path.expanduser("~/catnip-soc/data/processed")


def es_request(path, body=None):
    url = f"{ES_HOST}/{path}"
    creds = base64.b64encode(f"{ES_USER}:{ES_PASS}".encode()).decode()
    headers = {
        "Authorization": f"Basic {creds}",
        "Content-Type": "application/json"
    }
    data = json.dumps(body).encode() if body else None
    req = urllib.request.Request(
        url, data=data, headers=headers,
        method="POST" if body else "GET"
    )
    if os.path.exists(CA_CERT):
        ctx = ssl.create_default_context(cafile=CA_CERT)
    else:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=30) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        print(f"[ERROR] HTTP {e.code}: {e.read().decode()}")
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"[ERROR] Cannot reach Elasticsearch: {e.reason}")
        sys.exit(1)


def classify(count):
    if count >= CRITICAL_LIMIT:
        return "CRITICAL - Active Brute Force Attack"
    elif count >= THRESHOLD:
        return "HIGH - Suspected Brute Force"
    elif count >= 3:
        return "MEDIUM - Multiple Failures"
    return "LOW - Isolated Failure"


def extract_ip(msg):
    pattern = r"Failed password for (?:invalid user )?\S+ from (\d+\.\d+\.\d+\.\d+)"
    m = re.search(pattern, msg)
    return m.group(1) if m else None


def extract_user(msg):
    pattern = r"Failed password for (?:invalid user )?(\S+) from"
    m = re.search(pattern, msg)
    return m.group(1) if m else "unknown"


def run():
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    print("")
    print("=" * 60)
    print("  BRUTE-FORCE DETECTION REPORT")
    print(f"  Author  : Mohammad Ali - Week 5-6")
    print(f"  Time    : {now}")
    print(f"  Index   : {ES_INDEX}")
    print(f"  Window  : last {TIME_WINDOW_MIN} minutes")
    print(f"  Threshold: {THRESHOLD} failed attempts")
    print("=" * 60)
    print("")

    query = {
        "size": 1000,
        "query": {
            "bool": {
                "must": [
                    {
                        "match_phrase": {
                            "message": "Failed password"
                        }
                    },
                    {
                        "range": {
                            "@timestamp": {
                                "gte": f"now-{TIME_WINDOW_MIN}m",
                                "lte": "now"
                            }
                        }
                    }
                ]
            }
        },
        "_source": ["message", "@timestamp"]
    }

    result = es_request(f"{ES_INDEX}/_search", query)
    hits = result.get("hits", {}).get("hits", [])
    total = result.get("hits", {}).get("total", {}).get("value", 0)

    print(f"  Total Failed password events found: {total}")
    print("")

    if not hits:
        print("  [OK] No failed SSH login activity found.")
        print("")
        return

    ip_data = defaultdict(lambda: {
        "count": 0,
        "users": set(),
        "first": None,
        "last": None
    })

    for hit in hits:
        msg = hit["_source"].get("message", "")
        ts = hit["_source"].get("@timestamp", "")
        ip = extract_ip(msg)
        usr = extract_user(msg)
        if ip:
            ip_data[ip]["count"] += 1
            ip_data[ip]["users"].add(usr)
            if ip_data[ip]["first"] is None or ts < ip_data[ip]["first"]:
                ip_data[ip]["first"] = ts
            if ip_data[ip]["last"] is None or ts > ip_data[ip]["last"]:
                ip_data[ip]["last"] = ts

    sorted_ips = sorted(
        ip_data.items(),
        key=lambda x: x[1]["count"],
        reverse=True
    )

    alerts = []
    for ip, d in sorted_ips:
        if d["count"] >= THRESHOLD:
            alerts.append({
                "ip": ip,
                "count": d["count"],
                "threat": classify(d["count"]),
                "users": list(d["users"]),
                "first_seen": d["first"],
                "last_seen": d["last"]
            })

    if not alerts:
        print(f"  [OK] No IPs exceeded threshold of {THRESHOLD}.")
        print("")
        print("  All IPs with failed attempts:")
        for ip, d in sorted_ips:
            print(f"    {ip}  attempts={d['count']}  level={classify(d['count'])}")
    else:
        print(f"  [ALERT] {len(alerts)} IP(s) flagged:")
        print("")
        for a in alerts:
            print("  " + "-" * 55)
            print(f"  Source IP  : {a['ip']}")
            print(f"  Threat     : {a['threat']}")
            print(f"  Attempts   : {a['count']}")
            print(f"  Targets    : {', '.join(a['users'])}")
            print(f"  First seen : {a['first_seen']}")
            print(f"  Last seen  : {a['last_seen']}")
        print("")

    os.makedirs(REPORT_DIR, exist_ok=True)
    ts_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    fname = f"{REPORT_DIR}/bruteforce_{ts_str}.json"
    report = {
        "generated_at": now,
        "author": "Mohammad Ali - Week 5-6",
        "project": "Catnip Games International",
        "total_events_searched": total,
        "threshold": THRESHOLD,
        "alerts": alerts
    }
    with open(fname, "w") as f:
        json.dump(report, f, indent=2)
    print(f"  [SAVED] Report: {fname}")
    print("")


if __name__ == "__main__":
    run()
