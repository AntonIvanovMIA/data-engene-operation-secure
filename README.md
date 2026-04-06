# Catnip Games International - Centralised Logging Solution

## Description
Builds, manages, and operationalises data pipelines for security log management using the ELK Stack (Elasticsearch, Logstash, Kibana). This project implements a centralised logging and monitoring system capable of real-time data ingestion, normalisation, and visualisation for Catnip Games International.

## Technology Stack
- **Elasticsearch 8.19** — Log storage, full-text search, TLS security
- **Logstash** — Log ingestion, grok parsing, data enrichment
- **Kibana** — Visualisation, dashboards, security monitoring
- **Filebeat** — Lightweight log shipping from Gateway and Webserver VMs
- **Python** — Data preprocessing, threat classification, automation scripts
- **Git** — Version control and collaborative development

## Lab Network Architecture
| VM | IP Address | Role |
|---|---|---|
| Gateway | 192.168.100.1 | Router, UFW firewall, IDS logs, Filebeat agent |
| Webserver | 192.168.100.10 | Nginx/Apache web server, Filebeat agent |
| Zabbix | 192.168.100.20 | Infrastructure monitoring (future) |
| ElasticStackServer | 192.168.100.30 | Elasticsearch, Logstash, Kibana |
| Workstation | 192.168.100.40 | SSH management, Kibana browser access |

## Data Flow
Gateway / Webserver --> Filebeat (port 5044) --> Logstash --> Elasticsearch (HTTPS 9200) --> Kibana (5601)

## Team Task Distribution

### Part 1 — Week 1–2: Foundation & Data Analytics (Anton)
- ELK Stack installation and secure configuration (TLS, keystore, authentication)
- Logstash pipeline with advanced grok parsing (UFW firewall + SSH authentication)
- Filebeat deployment on Gateway and Webserver
- Python syslog preprocessor with threat classification
- First Kibana visualisations and security dashboard
- Git repository setup and documentation structure

### Part 2 — Week 3–4: IDS Log Source (Anton)
- IDS (Snort-format) log generator and simulation
- Filebeat configuration for IDS log collection
- Logstash IDS parsing pipeline
- Python IDS preprocessor script
- IDS Kibana visualisations and combined dashboard

### Part 2 — Week 5–6: Authentication & Access Control (Mohammad Ali)
- Authentication log deep analysis with brute-force detection
- RBAC implementation (soc_analyst and soc_engineer roles)
- Multi-source security dashboard

### Part 3 — Week 7–8: Retention & Monitoring (Nihal)
- Index Lifecycle Management (ILM) 30-day retention policy
- System health monitoring script (Python)
- Performance testing and optimisation

### Part 3 — Week 9–10: Security Hardening & Documentation (Anton)
- Elasticsearch audit logging
- UFW firewall rules on ElasticStackServer
- Security hardening checklist
- Complete project documentation (README, ARCHITECTURE, TROUBLESHOOTING, INSTALLATION)

### Part 4 — Week 11–12: WOW Factor & Final Delivery (Anton & Clesus)
- Automated security alert monitoring system
- Log simulation framework
- Automated backup script
- System verification script
- STAR narrative, screencast, Q&A preparation, report, final demonstration

## Status
## Week 1 2,3,4 Deliverables (Anton - Individual Contribution)



## Status
🟢 Week 1 — Complete (ELK Stack foundation)
🔴 Week 2 — Complete (Enhanced parsing, Python preprocessor, first dashboard)
⭕ Week 3-4 — Complete (IDS log source, Python IDS indexer, IDS preprocessor, IDS visualisations)
⬜ Week 5-6 — Planned (Auth analysis, RBAC)
⬜ Week 7-8 — Planned (ILM retention, health monitor)
⬜ Week 9-10 — Planned (Security hardening, documentation)
⬜ Week 11-12 — Planned (WOW factor, STAR, demo

## Repository Structure
catnip-soc/
├── README.md
├── configs/          # ELK configuration files
├── scripts/          # Python preprocessing and automation
├── data/
│   ├── raw/          # Raw log files
│   └── processed/    # Enriched JSON output
├── docs/             # Project documentation (Markdown)
└── evidence/         # Screenshots and evidence for report
