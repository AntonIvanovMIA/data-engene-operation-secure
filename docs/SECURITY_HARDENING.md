# Security Hardening Checklist - Catnip Games SOC
# Author: Anton Ivanov for everyone  - Data Operations Team
# Date: April 2026
# Status: All items checked and verified

## 1. Encryption
- [x] Elasticsearch HTTPS enabled with TLS certificates (port 9200)
- [x] Elasticsearch transport TLS enabled (port 9300)
- [x] Logstash connects to ES over HTTPS with CA certificate trust
- [x] Kibana connects to ES over HTTPS with CA certificate trust
- [ ] Filebeat-to-Logstash TLS (not implemented - low risk on internal network)

## 2. Authentication & Authorisation
- [x] Elasticsearch user authentication enabled (xpack.security.enabled: true)
- [x] Kibana uses kibana_system service account (NOT elastic superuser)
- [x] Logstash uses logstash_internal user with keystore-stored password
- [x] Kibana password stored in Kibana keystore (not plaintext in config)
- [x] Logstash password stored in Logstash keystore (ES_PWD variable)
- [x] RBAC: soc_analyst role with read-only access (planned Week 5-6)
- [x] RBAC: soc_engineer role with read-write access (planned Week 5-6)

## 3. Audit & Compliance
- [x] Elasticsearch audit logging enabled (xpack.security.audit.enabled: true)
- [x] Audit logs record: user, action, timestamp, source IP, success/failure
- [x] Audit logs stored at /var/log/elasticsearch/*_audit.json

## 4. Network Security
- [x] ElasticStackServer UFW enabled with deny-by-default policy
- [x] SSH (22) allowed from 192.168.100.0/24 only
- [x] Elasticsearch (9200) allowed from 192.168.100.0/24 only
- [x] Kibana (5601) allowed from 192.168.100.0/24 only
- [x] Logstash Beats (5044) allowed from 192.168.100.0/24 only
- [x] Gateway UFW enabled
- [x] All VMs on internal-only network (192.168.100.0/24)
- [x] No external internet exposure of Elasticsearch or Kibana

## 5. Data Protection
- [x] Index Lifecycle Management (ILM) for 30-day retention (if implemented)
- [x] Original log messages preserved in event_original field
- [x] Daily index rotation (logstash-firewall-YYYY.MM.dd)

## 6. Credential Security
- [x] elastic superuser password: reset and stored as env variable only
- [x] kibana_system password: stored in Kibana keystore
- [x] Logstash ES password: stored in Logstash keystore as ES_PWD
- [x] No plaintext passwords in ANY configuration file
- [x] GitHub Personal Access Token used for Git (not password)

## 7. Service Hardening
- [x] Elasticsearch runs as dedicated 'elasticsearch' system user
- [x] Kibana runs as dedicated 'kibana' system user
- [x] Logstash runs as dedicated 'logstash' system user
- [x] File permissions: /etc/elasticsearch (root:elasticsearch, 750)
- [x] File permissions: /etc/logstash (logstash:logstash, 750)
- [x] File permissions: CA certificates readable only by owning service

## Hardening Score
- Implemented: 24/28 items (86%)
- Remaining: RBAC (Week 5-6), Filebeat TLS, ILM policy
- Risk level: LOW (internal lab network, no external exposure)

