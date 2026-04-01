### 3.1 Enhanced Logstash Pipeline

The existing pipeline was extended to include:

- UFW firewall parsing (IP, ports, protocol)
- SSH authentication parsing (success/failure detection)
- Event classification:
  - firewall
  - authentication
  - system
- Severity assignment (LOW, MEDIUM, HIGH)
- Timestamp normalisation (UTC)

Validation:

```bash
sudo /usr/share/logstash/bin/logstash --path.settings /etc/logstash -t
sudo systemctl restart logstash
sudo ss -lntp | grep 5044

Result:

Logstash running successfully
Port 5044 listening for Filebeat
## 3.2 Python Log Preprocessing

A custom Python script was developed to process syslog files independently of ELK.

Key features:

Parses syslog format logs
Classifies events using regex threat patterns
Extracts:
IP addresses
usernames
Assigns severity levels
Outputs structured JSON

Execution:

python3 ~/catnip-soc/scripts/preprocess_logs.py /var/log/auth.log ~/catnip-soc/data/processed/auth_enriched.json

Result:

184 logs parsed successfully
2 brute-force events detected (HIGH severity)

This demonstrates the ability to detect security threats programmatically.

## 3.3 Field Naming Convention

A consistent schema was defined based on Elastic Common Schema (ECS):

snake_case naming
standardised timestamp format (UTC)
correct Elasticsearch data types:
keyword
integer
ip

This enables efficient querying and aggregation in Kibana.

## 3.4 Elasticsearch Index Template

An index template was created to enforce mappings:

PUT _index_template/catnip-logs

Result:

Structured indexing
Improved query performance
Correct field typing across all data
## 3.5 Kibana Visualisations

Three visualisations were created using Kibana Lens:

Log Events by Source VM (Area Chart)
Field: source_vm.keyword
Purpose: compare activity across Gateway and Webserver
Events by Log Type (Horizontal Bar)
Field: log_type.keyword
Purpose: distribution of system/firewall/web logs
Events by Process (Donut Chart)
Field: program.keyword
Purpose: identify most active processes
### 3.6 Security Dashboard

Dashboard created:

Name: Catnip SOC - Security Overview

Includes:

Timeline of events
Log type distribution
Process distribution

This provides a high-level SOC monitoring view.

## 4. Problems Encountered
Problem	Cause	Solution
Python parser failed (0 logs parsed)	syslog format mismatch	Updated regex patterns
Git push rejected (100MB file)	Large JSON file	Implemented .gitignore
Permission denied (Filebeat config)	root ownership	copied to /tmp with sudo
## 5. Learning Outcomes
Advanced log parsing using Grok and regex
Data normalisation and schema design
Python-based security log analysis
Git version control and troubleshooting
Building SOC-style dashboards
### 6. Contribution to Project

This work directly supports:

Centralised log ingestion
Security event detection
Real-time monitoring capability

It forms the foundation for multi-source integration in later weeks.

### 7. Conclusion

Week 2 successfully transformed raw logs into structured, enriched, and visualised data. The system now supports meaningful security analysis and provides a strong base for IDS integration in Week 3.
