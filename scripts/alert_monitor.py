#!/usr/bin/env python3
"""
Catnip Games - Real-Time Security Alert Monitor
Queries ES every 30 seconds for HIGH/CRITICAL alerts.
Displays colour-coded live feed in terminal.
Usage: python3 alert_monitor.py
Press Ctrl+C to stop.
Author: Anton Ivanov
"""
import subprocess, json, os, time, sys
from datetime import datetime, timezone, timedelta
# Configuration
CA = "/etc/elasticsearch/certs/http_ca.crt"
URL = "https://localhost:9200"
USER = "elastic"
PWD = os.environ.get('ELASTIC_PASSWORD', 'Anton@')
INTERVAL = 30
# Seconds between each refresh cycle
# Terminal colour codes
RED = '\033[91m'
# Red colour for CRITICAL alerts
YEL = '\033[93m'
# Yellow for HIGH alerts
GRN = '\033[92m'
# Green for normal/MEDIUM
CYN = '\033[96m'
# Cyan for headers
BLD = '\033[1m'
# Bold text
RST = '\033[0m'
# Reset to normal
def query_es(body):
# Sends a JSON query to Elasticsearch and returns parsed response
    result = subprocess.run([
        'curl', '-s', '--cacert', CA, '-u', f'{USER}:{PWD}',
        f'{URL}/logstash-*/_search',
        '-H', 'Content-Type: application/json',
        '-d', json.dumps(body)
    ], capture_output=True, text=True, timeout=15)
    try:
        return json.loads(result.stdout)
    except Exception:
        return None
def get_recent_alerts(minutes=60):
# Gets HIGH/CRITICAL events from the last N minutes
    return query_es({
        'size': 15,
        'sort': [{'@timestamp': 'desc'}],
        'query': {
            'bool': {
                'must': [
                    {'terms': {'severity': ['HIGH', 'CRITICAL']}},
                    {'range': {'@timestamp': {'gte': f'now-{minutes}m'}}}
                ]
            }
        }
    })
def get_stats():
# Gets category and severity counts for the status line
    return query_es({
        'size': 0,
        'aggs': {
            'cats': {'terms': {'field': 'event_category', 'size': 5}},
            'sevs': {'terms': {'field': 'severity', 'size': 5}}
        }
    })
def format_alert(hit):
# Formats one alert line with colour coding based on severity
    s = hit.get('_source', {})
    sev = s.get('severity', '?')
    cat = s.get('event_category', '?')
    msg = s.get('ids_signature', s.get('message', '?'))[:70]
    sip = s.get('source_ip', '?')
    dip = s.get('destination_ip', '?')
    ts = s.get('@timestamp', '?')[:19]
    clr = RED if sev == 'CRITICAL' else YEL if sev == 'HIGH' else GRN
    return f'  {clr}{BLD}[{sev:8s}]{RST} {ts} {cat:20s} {sip:>15s} -> {dip:<15s} {msg}'
def main():
    print(f'\n{BLD}[*] Catnip SOC Alert Monitor starting...{RST}')
    print(f'[*] Target: {URL}')
    print(f'[*] Refresh: every {INTERVAL}s')
    print(f'[*] Press Ctrl+C to stop\n')
    time.sleep(2)
    cycle = 0
    try:
        while True:
            cycle += 1
            ts = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')
            # Clear screen
            print('\033[2J\033[H', end='')
            print(f'{CYN}{BLD}' + '=' * 88 + f'{RST}')
            print(f'{CYN}{BLD}  CATNIP GAMES SOC - REAL-TIME ALERT MONITOR{RST}')
            print(f'{CYN}  {ts}  |  Cycle {cycle}  |  Ctrl+C to stop{RST}')
            print(f'{CYN}{BLD}' + '=' * 88 + f'{RST}')
            # Show stats
            stats = get_stats()
            if stats:
                total = stats.get('hits', {}).get('total', {}).get('value', 0)
                print(f'\n  {BLD}Total events:{RST} {total}')
                sevs = stats.get('aggregations', {}).get('sevs', {}).get('buckets', [])
                if sevs:
                    parts = []
                    for b in sevs:
                        k = b['key']
                        cl = RED if k == 'CRITICAL' else YEL if k == 'HIGH' else GRN
                        parts.append(f'{cl}{k}: {b["doc_count"]}{RST}')
                    print(f'  Severity: ' + ' | '.join(parts))
            # Show recent alerts
            alerts = get_recent_alerts(60)
            if alerts and alerts.get('hits', {}).get('hits'):
                hits = alerts['hits']['hits']
                print(f'\n  {BLD}Recent HIGH/CRITICAL (last 60 min): {len(hits)}{RST}')
                print(f'  ' + '-' * 84)
                for hit in hits:
                    print(format_alert(hit))
            else:
                print(f'\n  {GRN}No HIGH/CRITICAL alerts in last 60 minutes.{RST}')
            print(f'\n  {CYN}Next refresh in {INTERVAL}s...{RST}')
            time.sleep(INTERVAL)
    except KeyboardInterrupt:
        print(f'\n\n{BLD}[*] Monitor stopped. Cycles: {cycle}{RST}\n')
if __name__ == '__main__':
    main()

