# Troubleshooting Log - Week 1

## Error 1: APT 404 / NO_PUBKEY
- **Problem:** apt update failed with 404 or missing key
- **Cause:** Wrong repository URL or GPG key not imported
- **Fix:** Import key with gpg --dearmor, use correct packages/8.x/apt URL

## Error 2: Elasticsearch Duplicate Config Keys
- **Problem:** ES failed to start with "Duplicate field xpack.security"
- **Cause:** Auto-generated and manual security settings conflicted
- **Fix:** Cleaned elasticsearch.yml to remove all duplicates

## Error 3: Elasticsearch Exit Status 78
- **Problem:** ES could not write to log directory
- **Cause:** elasticsearch user lacked permissions on /var/log/elasticsearch
- **Fix:** sudo chown -R elasticsearch:elasticsearch /var/log/elasticsearch

## Error 4: Empty ELASTIC_PASSWORD Variable
- **Problem:** curl to ES failed because $ELASTIC_PASSWORD was empty
- **Cause:** export command not run in current shell session
- **Fix:** sudo elasticsearch-reset-password -u elastic -i, then export

## Error 5: Kibana "elastic" User Forbidden
- **Problem:** Kibana refused to start with elastic superuser
- **Cause:** ES 8.x blocks superuser for Kibana system config
- **Fix:** Switched to kibana_system user with separate password

## Error 6: Kibana EACCES on CA Certificate
- **Problem:** Kibana could not read /etc/elasticsearch/certs/http_ca.crt
- **Cause:** kibana user has no access to elasticsearch certs directory
- **Fix:** Copied CA cert to /etc/kibana/certs/ with kibana ownership

## Error 7: Kibana NOT LISTENING on Port 5601
- **Problem:** systemctl showed "running" but port 5601 not open
- **Cause:** Kibana takes 30-90 seconds to fully boot
- **Fix:** Used timeout watch loop to wait for port to bind

## Error 8: logstash Command Not Found
- **Problem:** typing "logstash" returned command not found
- **Cause:** Binary at /usr/share/logstash/bin/ not in system PATH
- **Fix:** Used full path: /usr/share/logstash/bin/logstash

## Error 9: Logstash Keystore AccessDeniedException
- **Problem:** Could not create keystore file
- **Cause:** logstash user had no write permission on /etc/logstash/
- **Fix:** sudo chown -R logstash:logstash /etc/logstash && sudo chmod 750 /etc/logstash
