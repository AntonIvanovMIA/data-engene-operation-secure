#!/usr/bin/env python3
"""Demo day verification - checks everything before presentation."""
import subprocess, json, os
from datetime import datetime, timezone

CA = "/etc/elasticsearch/certs/http_ca.crt"
URL = "https://localhost:9200"
U = "elastic"
PW = os.environ.get("ELASTIC_PASSWORD", "Anton@")

checks = []
def chk(name, cmd, expect=None):
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=15)
    ok = r.returncode == 0
    if expect: ok = ok and expect in r.stdout
    status = "PASS" if ok else "FAIL"
    checks.append((name, status))
    print(f"  [{status}] {name}")
    return ok

print(f"\n{"=" * 55}")
print(f"  CATNIP SOC - DEMO VERIFICATION")
print(f"  {datetime.now(timezone.utc).isoformat()}Z")
print(f"{"=" * 55}\n")

print("[Services]")
chk("Elasticsearch", "systemctl is-active elasticsearch", "active")
chk("Kibana", "systemctl is-active kibana", "active")
chk("Logstash", "systemctl is-active logstash", "active")

print("\n[Ports]")
chk("ES port 9200", "ss -lntp | grep :9200")
chk("Kibana port 5601", "ss -lntp | grep :5601")
chk("Logstash port 5044", "ss -lntp | grep :5044")

print("\n[Elasticsearch]")
chk("Cluster health", f"curl -s --cacert {CA} -u {U}:{PW} {URL}/_cluster/health", "status")
chk("Log indices exist", f"curl -s --cacert {CA} -u {U}:{PW} {URL}/_cat/indices | grep logstash")
chk("IDS events exist", f"curl -s --cacert {CA} -u {U}:{PW} {URL}/logstash-*/_count -H \"Content-Type: application/json\" -d '{{\"query\":{{\"term\":{{\"event_category\":\"intrusion_detection\"}}}}}}'", "\"count\":")

print("\n[Security]")
chk("UFW active", "sudo -n ufw status | grep 'Status: active'", "Status: active")
chk("Audit logging", "ls /var/log/elasticsearch/*audit* 2>/dev/null")

print("\n[Scripts]")
chk("preprocess_logs.py", "test -f ~/catnip-soc/scripts/preprocess_logs.py")
chk("preprocess_ids.py", "test -f ~/catnip-soc/scripts/preprocess_ids.py")
chk("ids_to_elasticsearch.py", "test -f ~/catnip-soc/scripts/ids_to_elasticsearch.py")
chk("health_check.py", "test -f ~/catnip-soc/scripts/health_check.py")

print("\n[Git]")
chk("Git repo", "cd ~/catnip-soc && git log --oneline | head -1")

passed = sum(1 for _, s in checks if s == "PASS")
total = len(checks)
print(f"\n{"=" * 55}")
print(f"  RESULT: {passed}/{total} checks passed")
print(f"  STATUS: {"ALL SYSTEMS GO" if passed == total else "FIX ISSUES FIRST"}")
print(f"{"=" * 55}\n")
