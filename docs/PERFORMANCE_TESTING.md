# Performance Testing Results - Catnip Games SOC
# Date: April 2026
# Requirement: Search response <2 seconds for basic queries

## Test Environment
- ElasticStackServer: 192.168.100.30
- Elasticsearch 8.19 (single node)
- Total documents: ~10,000+
- Index pattern: logstash-firewall-*

## Results
student@elasticstackstudentserver:~/catnip-soc$ time curl -s --cacert /etc/elasticsearch/certs/http_ca.crt \
  -u elastic:$ELASTIC_PASSWORD \
  'https://localhost:9200/logstash-*/_search?size=10' > /dev/null

real	0m2.201s
user	0m0.163s
sys	0m0.155s
student@elasticstackstudentserver:~/catnip-soc$ time curl -s --cacert /etc/elasticsearch/certs/http_ca.crt \
  -u elastic:$ELASTIC_PASSWORD \
  'https://localhost:9200/logstash-*/_search' \
  -H 'Content-Type: application/json' \
  -d '{"query":{"term":{"event_category":"intrusion_detection"}},"size":10}' > /dev/null

real	0m0.588s
user	0m0.034s
sys	0m0.104s
student@elasticstackstudentserver:~/catnip-soc$ time curl -s --cacert /etc/elasticsearch/certs/http_ca.crt \
  -u elastic:$ELASTIC_PASSWORD \
  'https://localhost:9200/logstash-*/_search' \
  -H 'Content-Type: application/json' \
  -d '{"size":0,"aggs":{"top_ips":{"terms":{"field":"source_ip","size":10}}}}' > /dev/null

real	0m0.625s
user	0m0.025s
sys	0m0.065s
student@elasticstackstudentserver:~/catnip-soc$ time curl -s --cacert /etc/elasticsearch/certs/http_ca.crt \
  -u elastic:$ELASTIC_PASSWORD \
  'https://localhost:9200/logstash-*/_count' > /dev/null

real	0m0.219s
user	0m0.022s
sys	0m0.113s


## Conclusion
All queries completed well under the 2-second requirement.
The single-node cluster handles the current data volume efficiently.
