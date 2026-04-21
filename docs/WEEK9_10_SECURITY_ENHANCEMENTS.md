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
`/etc/elasticsearch/elasticsearch.yml`

## Change Applied

```yaml
xpack.security.audit.enabled: true
Command Used
sudo nano /etc/elasticsearch/elasticsearch.yml
Service Restart
sudo systemctl restart elasticsearch
sudo systemctl status elasticsearch --no-pager
Result
Elasticsearch restarted successfully
No configuration errors detected
3. License Limitation Identified

After enabling audit logging, no logs were generated.

Investigation Command
sudo grep -i audit /var/log/elasticsearch/*.log
Output
Auditing logging is DISABLED because the currently active license [BASIC] does not permit it
Analysis
Audit logging requires a higher-tier license
Basic license does NOT support audit logging
This demonstrates understanding of real-world licensing constraints
4. Trial License Activation
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
```
## 5. Audit Logging Verification
```
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
```
## 6. Security Value
```
Audit logging provides:

Full trace of user activity
Authentication tracking
Access monitoring (who accessed what)
Forensic investigation capability
Compliance support (SOC, ISO27001)
```
###  7. Key Learnings
```
Security features depend on licensing tiers
Proper validation requires log inspection
Real SOC systems require audit trails for accountability
Elasticsearch provides deep visibility into system access
```
##  8. Evidence Collected
Elasticsearch configuration file
License activation output
Audit log file presence
Audit log entries (JSON format)
## 9. Current Status
Feature	Status
Audit logging enabled	
Trial license active
Audit events generated	
Logs verified	
---

# 11. UFW Firewall Implementation

## Machine
ElasticStackServer (192.168.100.30)

## Configuration

Default policies:

```bash
sudo ufw default deny incoming
sudo ufw default allow outgoing

Allowed services (internal network only):

sudo ufw allow from 192.168.100.0/24 to any port 22 proto tcp
sudo ufw allow from 192.168.100.0/24 to any port 9200 proto tcp
sudo ufw allow from 192.168.100.0/24 to any port 5601 proto tcp
sudo ufw allow from 192.168.100.0/24 to any port 5044 proto tcp
sudo ufw allow from 127.0.0.1

Firewall enabled:

sudo ufw enable

Verification:

sudo ufw status verbose
```
## Security Benefit
Restricts access to ELK services to internal network only
Prevents external unauthorized access
Implements network-level security layer
Result

Firewall successfully configured and verified without disrupting ELK services.
---

# 12. Firewall Validation and Testing

## Connectivity Test

From Workstation (192.168.100.40):

- Accessed Kibana:
  http://192.168.100.30:5601

Result:
- Access successful
- No service disruption after firewall activation

## Internal Service Validation

Verified Elasticsearch access locally:

```bash
curl --cacert /etc/elasticsearch/certs/http_ca.crt \
-u elastic:$ELASTIC_PASSWORD \
https://localhost:9200

Result:

Successful response
Localhost rule working correctly
Security Validation
External networks cannot access ports
Only internal subnet (192.168.100.0/24) allowed
Firewall blocks all other incoming traffic
```
## 13. Security Architecture Summary
```
The system now implements multiple layers of security:

Layer	Technology	Purpose
Network	UFW Firewall	Restrict access to services
Transport	TLS (HTTPS)	Encrypt communication
Authentication	Elasticsearch Security	User-based access control
Logging	Audit Logs	Track user activity
Monitoring	ELK Stack	Centralised visibility
```
## 14. Professional Reflection

## This implementation demonstrates:

Understanding of layered security architecture
Ability to apply real-world SOC hardening techniques
Awareness of licensing constraints and feature availability
Practical DevOps workflow (configuration, validation, documentation)
---

# 17. Gateway Firewall Implementation

## Machine
Gateway (192.168.100.1)

## Installation

UFW was not pre-installed on the Gateway system.

```bash
sudo apt update
sudo apt install ufw -y
Configuration

Default policies:

sudo ufw default deny incoming
sudo ufw default allow outgoing

##Allowed services:

sudo ufw allow from 192.168.100.0/24 to any port 22 proto tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

Firewall enabled:

sudo ufw enable

##Verification:

sudo ufw status verbose
Result
Firewall successfully enabled
SSH restricted to internal network
Web traffic (HTTP/HTTPS) allowed
System protected against unauthorized access
Security Role

The Gateway acts as the network edge firewall, controlling incoming traffic before it reaches internal systems.

This implements:

First line of defense
Traffic filtering at network boundary
Reduced attack surface
##  Week 9–10: Security Enhancements & Operational Validation (Anton)

---

#  Objective

Enhance security posture of the ELK stack by:

* Enabling firewall restrictions (UFW)
* Validating Elasticsearch security features (audit + TLS)
* Ensuring Logstash ingestion pipeline reliability
* Implementing and testing system health monitoring
* Troubleshooting real-world pipeline failure

---

#  Environment

* **ElasticStackServer**: ELK stack (Elasticsearch, Logstash, Kibana)
* **Gateway**: Log source + firewall logs
* Network: `192.168.100.0/24`

---

#  1. Firewall Hardening (UFW)

##  ElasticStackServer Configuration

### Commands executed:

```bash
sudo ufw status

sudo ufw default deny incoming
sudo ufw default allow outgoing

sudo ufw allow from 192.168.100.0/24 to any port 22 proto tcp
sudo ufw allow from 192.168.100.0/24 to any port 9200 proto tcp
sudo ufw allow from 192.168.100.0/24 to any port 5601 proto tcp
sudo ufw allow from 192.168.100.0/24 to any port 5044 proto tcp

sudo ufw enable
sudo ufw status verbose
```

##  Result

* Incoming traffic restricted
* Only lab network allowed access to:

  * SSH (22)
  * Elasticsearch (9200)
  * Kibana (5601)
  * Logstash Beats (5044)

---

##  Gateway Configuration

### Issue encountered

```bash
sudo: ufw: command not found
```

### Fix applied:

```bash
sudo apt update
sudo apt install ufw -y
```

### Firewall setup:

```bash
sudo ufw default deny incoming
sudo ufw default allow outgoing

sudo ufw allow from 192.168.100.0/24 to any port 22 proto tcp
sudo ufw allow from any to any port 80 proto tcp
sudo ufw allow from any to any port 443 proto tcp

sudo ufw enable
sudo ufw status verbose
```

##  Result

* Gateway secured
* SSH restricted to lab network
* Optional web ports exposed

---

#  2. Elasticsearch Security Validation

##  Objective

Ensure security features are active:

* TLS
* Authentication
* Audit logging
* License (trial)

---

##  Enable trial license

```bash
export ELASTIC_PASSWORD='Anton@'

curl --cacert /etc/elasticsearch/certs/http_ca.crt \
-u elastic:$ELASTIC_PASSWORD \
https://localhost:9200/_license/trial_status?pretty

curl --cacert /etc/elasticsearch/certs/http_ca.crt \
-u elastic:$ELASTIC_PASSWORD \
-X POST "https://localhost:9200/_license/start_trial?acknowledge=true&pretty"
```

---

##  Verify license

```bash
curl --cacert /etc/elasticsearch/certs/http_ca.crt \
-u elastic:$ELASTIC_PASSWORD \
https://localhost:9200/_license?pretty
```

 Result:

* Trial license activated
* Security features enabled

---

##  Audit log verification

```bash
ls -lh /var/log/elasticsearch/*audit*
sudo tail -20 /var/log/elasticsearch/*audit*
```

### Observed:

* Authentication events
* Kibana system access
* Index operations

 Audit logging working correctly

---

#  3. Logstash Pipeline Failure (Critical Incident)

## ❌ Problem

Health check showed:

```text
[ FAIL ] Logstash port 5044
STATUS: DEGRADED
```

---

##  Investigation

### Check port:

```bash
sudo ss -lntp | grep 5044
```

➡ No output → port not listening

---

### Check service:

```bash
sudo systemctl status logstash
```

Observed:

* Restart loop
* Exit code failure

---

### Validate config:

```bash
sudo /usr/share/logstash/bin/logstash --path.settings /etc/logstash -t
```

Error:

```
Expected one of [input, filter, output]
```

---

##  Root Cause

Inside `firewall.conf`:

* `filter {}` block was **closed too early**
* Remaining filters were outside pipeline
* Logstash could not compile pipeline

---

## 🛠 Fix Applied

### Edited:

```bash
sudo nano /etc/logstash/conf.d/firewall.conf
```

### Correct structure:

```ruby
filter {

  if "[**]" in [message] {
    mutate {
      replace => {
        "log_type" => "ids"
        "event_category" => "intrusion_detection"
      }
    }
  } else {
    mutate {
      replace => {
        "log_type" => "system"
        "event_category" => "system"
      }
    }
  }

  # CONTINUE OTHER FILTERS HERE (DO NOT CLOSE BLOCK)
```

---

##  Validation

```bash
sudo /usr/share/logstash/bin/logstash --path.settings /etc/logstash -t
```

Result:

```
Configuration OK
```

---

## Restart & Verification

```bash
sudo systemctl restart logstash
sleep 30

sudo ss -lntp | grep 5044
```

Port now listening

---

# ⚠ Important Operational Insight

Logstash requires time to initialize pipelines.

### Observation:

* Service = active
* Port = not yet listening (initially)

### Lesson:

> Service status ≠ pipeline readiness

---

#  4. Health Monitoring Script

##  Execution

```bash
export ELASTIC_PASSWORD='Anton@'
python3 ~/catnip-soc/scripts/health_check.py
```

---

##  Initial Result

```text
RESULT: 7/8 checks passed
STATUS: DEGRADED
```

Cause:

* Logstash port not ready

---

##  Final Result

```text
RESULT: 8/8 checks passed
STATUS: HEALTHY
```

---

#  5. Final System State

## Services

* Elasticsearch 
* Kibana 
* Logstah 

## Ports

* 9200 (Elasticsearch) 
* 5601 (Kibana) 
* 5044 (Logstash) 

## Cluster

* Status: YELLOW (single node expected)

## Logs

* Firewall logs ingested
* Indices growing correctly

---

#  Key Lessons Learned

### 1. Pipeline structure is critical

One misplaced `}` breaks entire ingestion

### 2. Always validate config before restart

```bash
logstash -t
```

### 3. Service status can be misleading

* "active" ≠ working pipeline

### 4. Timing matters in distributed systems

* Allow startup delay

### 5. Observability is essential

* Health script detected issue early

---

#  Conclusion

The ELK stack security and ingestion pipeline is now:

*  Hardened (firewall + TLS + auth)
*  Observable (health monitoring)
* ⚙ Stable (validated pipeline)
*  Operationally understood (real incident resolved)

---

#  Next Steps (Future Work)

* Add alerting (ElastAlert / Kibana alerts)
* Integrate IDS alerts into dashboard
* Automate health check via cron
* Expand threat detection rules

---
## Automated Health Check Scheduling

A cron job was configured to execute the health monitoring script every 15 minutes.  
The output was redirected to a project evidence log file:

`/home/student/catnip-soc/evidence/catnip-health.log`

This allowed repeatable verification of system health without requiring manual execution each time.

Verification was performed using:

- `crontab -l`
- manual execution of the same command
- `tail -20` on the generated log output

The test confirmed successful execution and a final system state of `HEALTHY` with 8/8 checks passed.
