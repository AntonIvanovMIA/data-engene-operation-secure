# Week 1 - Evidence Summary

## Kibana Verification
- Data view created: firewall-logs (pattern: logstash-firewall-*)
- Timestamp field: @timestamp
- Documents verified in Discover: 292 events
- Agents detected: gateway, webserver
- Fields observed: agent.name, source_vm, log_type, @timestamp, event.original

## Filebeat Agents
- Gateway (192.168.100.1): shipping /var/log/syslog, /var/log/auth.log, /var/log/ufw.log
- Webserver (192.168.100.10): shipping /var/log/syslog, /var/log/auth.log, /var/log/nginx/*.log

## Services Running
| Service | VM | Port | Status |
|---|---|---|---|
| Elasticsearch | ElasticStackServer | 9200 (HTTPS) | Active |
| Kibana | ElasticStackServer | 5601 | Active |
| Logstash | ElasticStackServer | 5044 | Active |
| Filebeat | Gateway | N/A (client) | Active |
| Filebeat | Webserver | N/A (client) | Active |

## Security Measures
- Elasticsearch: TLS enabled, user authentication required
- Logstash: Credentials in keystore (ES_PWD), not plaintext
- Kibana: Uses kibana_system account, CA cert in /etc/kibana/certs/x
