chmod +x ~/catnip-soc/scripts/backup.sh
Run it again

cache sudo:

sudo -v

 run:

~/catnip-soc/scripts/backup.sh
Verify it worked

Run:

ls -lh ~/backups

Then inspect contents:

tar -tzf "$(ls -t ~/backups/catnip-soc-backup-*.tar.gz | head -1)" | head -50
output 
catnip-soc-backup-20260421_042959/
catnip-soc-backup-20260421_042959/docs/
catnip-soc-backup-20260421_042959/docs/.gitkeep
catnip-soc-backup-20260421_042959/docs/WEEK1_EVIDENCE.md
catnip-soc-backup-20260421_042959/docs/TROUBLESHOOTING.md
catnip-soc-backup-20260421_042959/docs/SECURITY_HARDENING.md
catnip-soc-backup-20260421_042959/docs/PERFORMANCE_TESTING.md
catnip-soc-backup-20260421_042959/docs/KIBANA_DASHBOARDS.md
catnip-soc-backup-20260421_042959/docs/field_naming_convention.md
catnip-soc-backup-20260421_042959/docs/week2-report.md
catnip-soc-backup-20260421_042959/docs/IDS_IMPLEMENTATION.md
catnip-soc-backup-20260421_042959/docs/WEEK9_10_SECURITY_ENHANCEMENTS.md
catnip-soc-backup-20260421_042959/configs/
catnip-soc-backup-20260421_042959/configs/kibana.yml
catnip-soc-backup-20260421_042959/configs/firewall.conf
catnip-soc-backup-20260421_042959/configs/filebeat_gateway_week3.yml
catnip-soc-backup-20260421_042959/configs/firewall_week3.conf
catnip-soc-backup-20260421_042959/configs/elasticsearch.yml
catnip-soc-backup-20260421_042959/configs/filebeat_gateway.yml
catnip-soc-backup-20260421_042959/configs/filebeat_webserver.yml
catnip-soc-backup-20260421_042959/configs/firewall_week2.conf
catnip-soc-backup-20260421_042959/ufw-rules.txt
catnip-soc-backup-20260421_042959/disk-usage.txt
catnip-soc-backup-20260421_042959/scripts/
catnip-soc-backup-20260421_042959/scripts/.gitkeep
catnip-soc-backup-20260421_042959/scripts/preprocess_ids.py
catnip-soc-backup-20260421_042959/scripts/health_check.py
catnip-soc-backup-20260421_042959/scripts/preprocess_logs.py
catnip-soc-backup-20260421_042959/scripts/generate_ids_logs.py
catnip-soc-backup-20260421_042959/scripts/demo_verify.py
catnip-soc-backup-20260421_042959/scripts/ids_to_elasticsearch.py
catnip-soc-backup-20260421_042959/scripts/backup.sh
catnip-soc-backup-20260421_042959/scripts/alert_monitor.py
catnip-soc-backup-20260421_042959/elk-live-configs/
catnip-soc-backup-20260421_042959/elk-live-configs/kibana.yml
catnip-soc-backup-20260421_042959/elk-live-configs/firewall.conf
catnip-soc-backup-20260421_042959/elk-live-configs/elasticsearch.yml
catnip-soc-backup-20260421_042959/README.md
catnip-soc-backup-20260421_042959/listening-ports.txt
catnip-soc-backup-20260421_042959/memory-usage.txt
catnip-soc-backup-20260421_042959/running-services.txt

run  comands 
student@elasticstackstudentserver:~/catnip-soc$ nano ~/catnip-soc/scripts/backup.sh
student@elasticstackstudentserver:~/catnip-soc$ chmod +x ~/catnip-soc/scripts/backup.sh
student@elasticstackstudentserver:~/catnip-soc$ sudo -v
student@elasticstackstudentserver:~/catnip-soc$ ~/catnip-soc/scripts/backup.sh
==========================================
  CATNIP GAMES SOC - BACKUP SYSTEM
  Tue Apr 21 04:29:59 AM UTC 2026
==========================================

[1/5] Backing up project files...
    Done: scripts, configs, docs
[2/5] Backing up ELK configurations...
    Done: elasticsearch.yml, kibana.yml, firewall.conf
[3/5] Backing up firewall rules...
    Done: ufw-rules.txt
[4/5] Capturing system state...
    Done: services, ports, disk, memory
[5/5] Creating compressed archive...

==========================================
  BACKUP COMPLETE
  File: /home/student/backups/catnip-soc-backup-20260421_042959.tar.gz
  Size: 53K
==========================================
