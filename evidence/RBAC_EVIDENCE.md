# RBAC Evidence — Role-Based Access Control

## Environment
VM: ElasticStackServer  
IP: 192.168.100.30  
Stack: Elasticsearch, Logstash, Kibana  

---

## Objective
Implement Role-Based Access Control (RBAC) to enforce the principle of least privilege.

Two roles were created:
- soc_analyst → read-only access
- soc_engineer → full access

Two users were created:
- analyst_user (SOC Analyst)
- engineer_user (SOC Engineer)

---

## 1. Role Verification

### soc_analyst Role
- Index access: logstash-*
- Privileges: read, view_index_metadata
- Kibana: read-only (Discover, Dashboard, Visualize)

### soc_engineer Role
- Index access: logstash-*
- Privileges: read, write, create_index, manage
- Kibana: full access

---

## 2. User Verification

Command used:

curl --cacert /etc/elasticsearch/certs/http_ca.crt
-u elastic:$ELASTIC_PASSWORD
https://localhost:9200/_security/user/analyst_user?pretty


Result:
- Username: analyst_user
- Role: soc_analyst
- Full name: Anton Ivanov

This confirms identity customization and role assignment.

---

## 3. Analyst Read Access Test

Command:

curl --cacert /etc/elasticsearch/certs/http_ca.crt
-u analyst_user:Analyst2026@
https://localhost:9200/logstash-*/_search?size=1&pretty


Result:
- Successful response
- Log data returned

This proves:
- Analyst can read and search logs

---

## 4. Analyst Restriction Test (CRITICAL)

Command:

curl --cacert /etc/elasticsearch/certs/http_ca.crt
-u analyst_user:Analyst2026@
-X DELETE https://localhost:9200/logstash-test-delete?pretty


Result:
- HTTP 403 security_exception
- Operation denied

Meaning:
- Analyst cannot delete or manage indices
- Least privilege enforced

---

## 5. Kibana RBAC Verification

Login used:
- Username: analyst_user
- Password: Analyst2026@

Observed behavior:
- Discover page accessible
- Logs visible
- Dashboards visible

Restrictions observed:
- No option to create dashboards
- No option to edit dashboards
- No access to Stack Management
- No ability to modify index patterns

---

## 6. Conclusion

RBAC is correctly implemented.

The system enforces:
- Separation of duties
- Least privilege access
- Protection against accidental or malicious changes

Analysts can monitor and investigate data but cannot alter system configuration.

This reflects real-world SOC operational security practices.
