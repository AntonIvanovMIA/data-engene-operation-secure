# IDS Implementation - Week 3-4
## Author: Anton Ivanov - Data Operations Team
## Date: April 2026

## Overview
Added Snort-format IDS alerts as the second security log source, satisfying
the coursework requirement for minimum 3 security sources:
1. Firewall/System logs (Week 1-2) - via Filebeat -> Logstash -> ES
2. IDS alerts (Week 3-4) - via Python -> ES REST API
3. Authentication logs (Week 1-2) - via Filebeat -> Logstash -> ES

## Architecture Decision
The original plan was to use Filebeat to ship IDS logs from Gateway to
Logstash for parsing. However, Snort IDS alerts are multi-line (3 lines
per alert), and Filebeat sends each line as a separate event. After
5 troubleshooting iterations, the architecture was changed to direct
Python-to-Elasticsearch REST API indexing.

### Why This Approach Is Better
- Bypasses the Filebeat multi-line limitation completely
- Documents have all fields pre-structured correctly
- Demonstrates Python + Elasticsearch API integration skills
- Uses same index pattern (logstash-firewall-*) so Kibana works seamlessly
- 500 alerts indexed with 0 failures

## Components

### 1. IDS Log Generator (scripts/generate_ids_logs.py)
- **Location:** Gateway VM (192.168.100.1)
- **Purpose:** Generates 800 realistic Snort-format IDS alerts
- **Output:** /var/log/snort/alert.log
- **Alert Types:** 14 signatures across 5 categories
- **Command:** sudo python3 ~/generate_ids_logs.py

### 2. Python IDS-to-ES Indexer (scripts/ids_to_elasticsearch.py)
- **Location:** ElasticStackServer VM (192.168.100.30)
- **Purpose:** Generates IDS alerts and sends directly to Elasticsearch
- **Method:** HTTP POST to Elasticsearch REST API with TLS + authentication
- **Result:** 500 alerts indexed, 0 failures
- **Command:** python3 ~/catnip-soc/scripts/ids_to_elasticsearch.py

### 3. Python IDS Preprocessor (scripts/preprocess_ids.py)
- **Location:** ElasticStackServer VM (192.168.100.30)
- **Purpose:** Offline batch analysis of IDS alert log files
- **Output:** Enriched JSON + classification/severity/IP statistics
- **Result:** 800 alerts parsed successfully
- **Command:** python3 ~/catnip-soc/scripts/preprocess_ids.py <input> <output>

### 4. Logstash IDS Detection (configs/firewall_week3.conf)
- **Location:** ElasticStackServer VM (192.168.100.30)
- **Purpose:** Detects IDS events via "Classification:" keyword in pipeline
- **Note:** IDS events are primarily indexed via Python, but the Logstash
  pipeline also has IDS detection capability for any events that pass through

### 5. Filebeat IDS Input (configs/filebeat_gateway_week3.yml)
- **Location:** Gateway VM (192.168.100.1)
- **Purpose:** Configured to read /var/log/snort/alert.log
- **Note:** Filebeat reads the file but multi-line grouping was not reliable

### 6. Kibana IDS Visualisations
- **IDS Alerts by Classification** - Bar chart showing alert type distribution
- **IDS Severity Distribution** - Pie chart (CRITICAL 49.6%, HIGH 32.6%, MEDIUM 17.8%)
- **IDS Alerts Timeline** - Line chart showing alert volume over time
- All 3 added to "Catnip SOC - Security Overview" dashboard

## Alert Categories Generated
| Category | Example Signatures | Priority | Severity | Count |
|---|---|---|---|---|
| Reconnaissance | SSH Scan, Nmap, FTP Brute Force | 2 | HIGH | ~166 |
| Exploits | SQL Injection, Struts RCE, PHP RFI | 1 | CRITICAL | ~179 |
| Trojans/Malware | Emotet C2, CobaltStrike, Malicious UA | 1 | CRITICAL | ~187 |
| Denial of Service | SYN Flood, NTP Amplification | 2 | HIGH | ~111 |
| Policy Violations | Non-Standard SSH, BitTorrent | 3 | MEDIUM | ~101 |
| Successful Admin | Root access gained | 1 | CRITICAL | ~56 |

## Preprocessor Results (800 alerts)
- **Severity:** CRITICAL 422, HIGH 277, MEDIUM 101
- **Top Attacker IP:** 203.0.113.138 (27 alerts)
- **Top Target IP:** 192.168.100.20 / Zabbix (173 alerts)
- **Top Target Port:** 8443 (99 alerts)

## Troubleshooting Log (5 issues resolved)
| # | Problem | Root Cause | Resolution |
|---|---|---|---|
| 1 | Filebeat not reading IDS file | Registry tracked old state | Deleted registry |
| 2 | IDS not parsed as intrusion_detection | Multi-line split by Filebeat | Changed to Python indexing |
| 3 | Logstash syntax error | Duplicated if-condition | Rewrote pipeline |
| 4 | event_category.keyword returns 0 | Text mapping, not keyword | Deleted index, re-indexed |
| 5 | Architecture incompatibility | Snort multi-line vs Filebeat | Python REST API solution |

## Key Learning
Snort IDS alerts are fundamentally multi-line, making them incompatible
with Filebeat's line-by-line shipping model. The solution was to use
Python to generate properly structured documents and send them directly
to Elasticsearch via the REST API. This demonstrates professional
flexibility in choosing the right ingestion method for each data source.
```
