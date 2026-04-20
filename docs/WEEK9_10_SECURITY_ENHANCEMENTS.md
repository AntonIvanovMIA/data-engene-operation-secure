# Week 9–10: Security Enhancements and Advanced Monitoring

## Author
Anton Ivanov  
Data Engineering – Security Operations Coursework  

---

# 1. Objective

The goal of Week 9–10 was to enhance the security posture of the ELK stack by implementing:

- Elasticsearch audit logging
- License upgrade (trial activation)
- Security event validation
- Verification of audit trail generation

This extends the system from monitoring → **security-grade logging and compliance readiness**.

---

# 2. Elasticsearch Audit Logging Enablement

## Machine
ElasticStackServer (192.168.100.30)

## Configuration File
 /etc/elasticsearch/elasticsearch.yml`

## Change Applied

yaml
xpack.security.audit.enabled: true
Command Used
sudo nano /etc/elasticsearch/elasticsearch.yml
Service Restart
sudo systemctl restart elasticsearch
sudo systemctl status elasticsearch --no-pager
Result
Elasticsearch restarted successfully
No configuration errors detected
# 3. License Limitation Identified

After enabling audit logging, no logs were generated.

Investigation Command
sudo grep -i audit /var/log/elasticsearch/*.log
Output
Auditing logging is DISABLED because the currently active license [BASIC] does not permit it
Analysis
Audit logging requires a higher-tier license
Basic license does NOT support audit logging
This demonstrates understanding of real-world licensing constraints
# 4. Trial License Activation
Step 1 — Check Eligibility
curl --cacert /etc/elasticsearch/certs/http_ca.crt \
-u elastic:$ELASTIC_PASSWORD \
https://localhost:9200/_license/trial_status?pretty
Result
"eligible_to_start_trial": true
Step 2 — Activate Trial License
curl --cacert /etc/elasticsearch/certs/http_ca.crt \
-u elastic:$ELASTIC_PASSWORD \
-X POST "https://localhost:9200/_license/start_trial?acknowledge=true&pretty"
Result
"trial_was_started": true
"type": "trial"
Step 3 — Verify License
curl --cacert /etc/elasticsearch/certs/http_ca.crt \
-u elastic:$ELASTIC_PASSWORD \
https://localhost:9200/_license?pretty
Result
License type: trial
Status: active
Expiry: 30 days
# 5. Audit Logging Verification
Generate Security Event
curl --cacert /etc/elasticsearch/certs/http_ca.crt \
-u elastic:$ELASTIC_PASSWORD \
https://localhost:9200/_security/_authenticate?pretty
Check Audit Log File
ls -lh /var/log/elasticsearch/*audit*
Result
catnip-elk-cluster_audit.json (2.6 MB)
View Audit Logs
sudo tail -20 /var/log/elasticsearch/*audit*
Example Audit Events Observed
{
  "event.type": "transport",
  "event.action": "access_granted",
  "user.name": "kibana_system",
  "authentication.type": "REALM",
  "indices": [".kibana_8.19.12"]
}
# 6. Security Value

Audit logging provides:

Full trace of user activity
Authentication tracking
Access monitoring (who accessed what)
Forensic investigation capability
Compliance support (SOC, ISO27001)
# 7. Key Learnings
Security features depend on licensing tiers
Proper validation requires log inspection
Real SOC systems require audit trails for accountability
Elasticsearch provides deep visibility into system access
# 8. Evidence Collected
Elasticsearch configuration file
License activation output
Audit log file presence
Audit log entries (JSON format)
# 9. Current Status
Feature	Status
Audit logging enabled	✅
Trial license active	✅
Audit events generated	✅
Logs verified	
