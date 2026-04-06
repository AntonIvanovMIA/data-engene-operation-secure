# Kibana Dashboards - Catnip Games SOC
## Last Updated: April 2026

## Dashboard: Catnip SOC - Security Overview
URL: http://192.168.100.30:5601
Login: elastic / [password]
Data View: firewall (logstash-firewall-*)

### Visualisation 1: Events by Process (Pie Chart) - Week 2
- Chart type: Pie/Donut
- Metric: Count
- Slice by: program.keyword (Top 10)
- Shows: filebeat 74%, systemd 14%, CRON, sshd, etc.

### Visualisation 2: Log Events by Source VM (Area Chart) - Week 2
- Chart type: Area (stacked)
- X-axis: @timestamp (Date Histogram, 12 hours)
- Y-axis: Count
- Breakdown: source_vm.keyword
- Shows: gateway vs webserver event volume over time

### Visualisation 3: Events by Log Type (Bar Chart) - Week 2
- Chart type: Bar
- Metric: Count
- Breakdown: log_type.keyword (Top 5)
- Shows: system events dominating

### Visualisation 4: IDS Alerts by Classification (Bar Chart) - Week 3-4
- Chart type: Bar (stacked)
- Filter: event_category = intrusion_detection
- Horizontal axis: event_category + ids_classification
- Metric: Count
- Shows: web-application-attack, trojan-activity, attempted-recon, etc.

### Visualisation 5: IDS Severity Distribution (Pie Chart) - Week 3-4
- Chart type: Pie
- Filter: event_category = intrusion_detection
- Slice by: event_category (Top 5) + severity (Top 5)
- Shows: CRITICAL 49.6%, HIGH 32.6%, MEDIUM 17.8%

### Visualisation 6: IDS Alerts Timeline (Line Chart) - Week 3-4
- Chart type: Line
- Filter: event_category = intrusion_detection
- X-axis: @timestamp (12 hour intervals)
- Breakdown: ids_classification (Top 5)
- Shows: web-application, trojan, recon, policy, DoS trends over time

## Important Notes
- Use event_category (NOT event_category.keyword) in filters
- Index template maps fields as keyword type directly
- "Problem with 1 cluster" warning is normal for single-node lab
- Time range: Last 15-30 days to see all data
```<img width="2559" height="1559" alt="Screenshot 2026-04-06 204109" src="https://github.com/user-attachments/assets/28a6aeae-918d-4781-b1fc-5bffb4b8082f" />

