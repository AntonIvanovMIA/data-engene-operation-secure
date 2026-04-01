# Catnip Games International - Field Naming Convention
# Version: 1.0 | Date: March 2026 | Author: Data Operations Team

## Naming Rules
1. All field names use snake_case (lowercase with underscores)
2. All timestamps normalised to UTC (ISO 8601 format)
3. IP fields use Elasticsearch 'ip' type for CIDR and geo lookups
4. Category values are lowercase keywords for exact matching
5. No spaces or special characters in field names
6. Fields follow Elastic Common Schema (ECS) principles where possible

## Core Fields (present in ALL log sources)

| Field Name | ES Type | Description | Example |
|---|---|---|---|
| @timestamp | date | UTC normalised event time | 2026-03-12T14:30:01.000Z |
| event_original | text | Complete unmodified log line | Mar 12 14:30:01 gw sshd... |
| event_category | keyword | Event type classification | firewall / authentication / system / intrusion_detection |
| event_outcome | keyword | Result of the event | success / failure / denied / allowed / info |
| severity | keyword | Threat severity level | LOW / MEDIUM / HIGH / CRITICAL |
| source_vm | keyword | VM that generated the log | gateway / webserver |
| log_type | keyword | Source log category | system / firewall / web / ids |
| host_name | keyword | Hostname of logging machine | gateway / webserver |
| process_name | keyword | Process that generated log | sshd / ufw / nginx / kernel |
| process_pid | integer | Process ID number | 1234 |
| log_message | text | Parsed message content | Failed password for root from 10.0.0.5 |

## Network Fields (firewall and IDS events)

| Field Name | ES Type | Description | Example |
|---|---|---|---|
| source_ip | ip | Source IP address | 10.0.0.5 |
| destination_ip | ip | Destination IP address | 192.168.100.1 |
| source_port | integer | Source port number | 54321 |
| destination_port | integer | Destination port number | 22 |
| network_protocol | keyword | Network protocol | TCP / UDP / ICMP |

## Firewall-Specific Fields

| Field Name | ES Type | Description | Example |
|---|---|---|---|
| ufw_action | keyword | Firewall decision | BLOCK / ALLOW |
| ufw_interface_in | keyword | Incoming network interface | eth0 |
| ufw_interface_out | keyword | Outgoing network interface | eth1 |

## Authentication Fields

| Field Name | ES Type | Description | Example |
|---|---|---|---|
| auth_user | keyword | Username in auth event | root / admin / student |
| auth_method | keyword | Authentication method | password / publickey |

## IDS Fields (intrusion detection events - Week 3-4)

| Field Name | ES Type | Description | Example |
|---|---|---|---|
| ids_sid | keyword | IDS signature ID | 1:100001:3 |
| ids_signature | keyword | IDS alert name | ET SCAN Potential SSH Scan |
| ids_classification | keyword | IDS classification type | attempted-recon |
| ids_priority | integer | IDS alert priority (1=highest) | 2 |

## Why This Convention Matters
- Consistent names allow cross-source queries (search all sources for source_ip)
- Correct ES types enable features (ip type allows CIDR range queries and geo lookups)
- keyword type enables exact-match filtering in Kibana (faster than text search)
- integer type enables range queries on ports (e.g. destination_port > 1024)
