# Catnip Games International - Centralised Logging Solution

## Project Overview
ELK Stack security log management system for Catnip Games International.

## Components
- Elasticsearch 8.19 (storage, search, TLS security)
- Logstash (log ingestion, grok parsing, enrichment)
- Kibana (visualisation, dashboards)
- Filebeat (log shipping from Gateway and Webserver)
- Python (data preprocessing, threat classification)

## Network
| VM | IP | Role |
|---|---|---|
| Gateway | 192.168.100.1 | Firewall, system logs |
| Webserver | 192.168.100.10 | Web and system logs |
| ElasticStackServer | 192.168.100.30 | ELK Stack |
| Workstation | 192.168.100.40 | Management |

## Author
Anton Ivanov - Data Operations Team
