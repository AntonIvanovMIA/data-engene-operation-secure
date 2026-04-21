Real-Time SOC Alert Monitor (WOW Factor)

▶ VM: ElasticStackServer
▶ IP: 192.168.100.30
▶ Role: ELK Stack Core

WHY

A real Security Operations Center (SOC) requires continuous monitoring of incoming security events. Analysts do not manually run queries — they rely on live alert feeds to identify threats as they occur.

This component implements a real-time alert monitoring system that queries Elasticsearch every 30 seconds and displays HIGH and CRITICAL severity events in a live terminal interface.

This demonstrates that the ELK stack is not only storing logs, but actively supporting operational security monitoring.

Step 1 — Create the alert monitoring script
nano ~/catnip-soc/scripts/alert_monitor.py

Paste the full script (see scripts directory).

Make executable:

chmod +x ~/catnip-soc/scripts/alert_monitor.py
Step 2 — Run the alert monitor
export ELASTIC_PASSWORD='Anton@'
python3 ~/catnip-soc/scripts/alert_monitor.py
Expected Behaviour
The script connects to Elasticsearch over HTTPS
Queries indices logstash-*
Refreshes every 30 seconds
Displays:
total event count
severity breakdown (CRITICAL, HIGH, MEDIUM)
recent HIGH/CRITICAL alerts (last 60 minutes)
Output is colour-coded:
CRITICAL → red
HIGH → yellow
normal → green
Runs continuously until stopped (Ctrl+C)
Example Output
CATNIP GAMES SOC - REAL-TIME ALERT MONITOR
2026-04-21 03:52:22 UTC

Total events: 9169
Severity: CRITICAL: 917 | HIGH: 606 | MEDIUM: 277

No HIGH/CRITICAL alerts in last 60 minutes.

Next refresh in 30s...
Integration with Kibana

At the same time, events displayed in the terminal are also visible in Kibana:

Open browser:
http://192.168.100.30:5601
Navigate to:
Discover
Select index:
logstash-*
Set time range:
Last 15 minutes or Last 1 hour
Add fields:
@timestamp
severity
event_category
source_ip
destination_ip

This allows direct correlation between:

live terminal alerts
indexed events in Kibana
Verification

The following checks confirm correct operation:

Script runs without errors
Output refreshes every 30 seconds
Severity counts are displayed
Kibana shows matching events
Filtering in Kibana (e.g. severity: "CRITICAL") returns same alerts
EVIDENCE

Capture the following:

Screenshot of terminal running alert_monitor.py
Screenshot of Kibana Discover showing same events
Screenshot showing severity filtering (e.g. CRITICAL only)

Optional:

Save sample output:
python3 ~/catnip-soc/scripts/alert_monitor.py > ~/catnip-soc/evidence/alert-monitor-sample.log
WHAT THIS IMPLEMENTS

This feature demonstrates:

real-time querying of Elasticsearch
automated alert detection
severity-based prioritisation
SOC-style monitoring workflow
integration between backend (Elasticsearch) and frontend (Kibana)

This is representative of real-world SOC operations where analysts monitor live alert streams continuously.


An additional improvement I implemented was a real-time SOC alert monitor.
This script queries Elasticsearch every 30 seconds and displays HIGH and CRITICAL events in a live terminal feed.
It simulates how analysts monitor alerts in a real SOC environment.
At the same time, these events are indexed and searchable in Kibana, allowing deeper investigation.
This demonstrates both real-time detection and analytical capabilities of the platform.
