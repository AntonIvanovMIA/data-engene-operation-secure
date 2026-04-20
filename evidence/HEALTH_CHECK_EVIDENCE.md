# Health Check Automation Evidence

## Machine
ElasticStackServer (192.168.100.30)

## Cron Schedule Configured

```bash
*/15 * * * * ELASTIC_PASSWORD=Anton@ /usr/bin/python3 /home/student/catnip-soc/scripts/health_check.py >> /home/student/catnip-soc/evidence/catnip-health.log 2>&1
