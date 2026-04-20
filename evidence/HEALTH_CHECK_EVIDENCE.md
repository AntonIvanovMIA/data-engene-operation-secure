# Health Check Automation Evidence

## Machine
ElasticStackServer (192.168.100.30)

## Cron Schedule Configured

```bash
*/15 * * * * ELASTIC_PASSWORD=Anton@ /usr/bin/python3 /home/student/catnip-soc/scripts/health_check.py >> /home/student/catnip-soc/evidence/catnip-health.log 2>&1

# Health Check Automation Evidence

## Overview

This file records the full process used to configure, validate, troubleshoot, and document the automated ELK health monitoring task on ElasticStackServer.

Machine used:
- ElasticStackServer (`192.168.100.30`)

Project path:
- `/home/student/catnip-soc`

Purpose:
- Run the health monitoring script automatically every 15 minutes
- Save output to a persistent evidence log
- verify that the ELK environment remains healthy over time
- provide reproducible evidence for coursework assessment

---

## 1. Initial Cron Approach

The first cron method used was:

```bash
(crontab -l 2>/dev/null; echo '*/15 * * * * export ELASTIC_PASSWORD=Anton@ && python3 /home/student/catnip-soc/scripts/health_check.py >> /var/log/catnip-health.log 2>&1') | crontab -

Verification command:

crontab -l

Issue identified:

output was redirected to /var/log/catnip-health.log
the student user could not reliably create or write to that location
the file did not appear when checked with:
tail -20 /var/log/catnip-health.log

Observed result:

tail: cannot open '/var/log/catnip-health.log' for reading: No such file or directory

Analysis:

/var/log/ is not the best destination for a non-root coursework cron job
cron environments also behave differently from an interactive shell
using export and a non-absolute Python path is less reliable in cron
2. Corrected Cron Configuration

A corrected cron job was created using:

direct environment variable assignment
absolute Python interpreter path
output redirected to the project evidence directory

The corrected cron entry is:

*/15 * * * * ELASTIC_PASSWORD=Anton@ /usr/bin/python3 /home/student/catnip-soc/scripts/health_check.py >> /home/student/catnip-soc/evidence/catnip-health.log 2>&1

The cron editor was opened with:

crontab -e

Verification:

crontab -l

Verified result:

the correct cron line was present
the job now writes inside the project directory
3. Evidence Directory Preparation

The evidence directory was created with:

mkdir -p /home/student/catnip-soc/evidence

Purpose:

store health-monitoring output in a user-writable project location
keep evidence files together with scripts and documentation
simplify later Git tracking and screenshots
4. Manual Validation of the Cron Command

Before waiting for the 15-minute cron schedule, the exact command was tested manually.

Command used:

ELASTIC_PASSWORD=Anton@ /usr/bin/python3 /home/student/catnip-soc/scripts/health_check.py >> /home/student/catnip-soc/evidence/catnip-health.log 2>&1

Output check:

tail -20 /home/student/catnip-soc/evidence/catnip-health.log

Observed result:

the script executed successfully
output was appended to catnip-health.log
final status showed the system as healthy

Example final status observed:

RESULT: 8/8 checks passed
STATUS: HEALTHY

This confirmed:

the script runs correctly
the environment variable is passed correctly
the output redirection works
the file path is valid
the ELK system was healthy at execution time
5. Git Evidence Preparation

The live log file catnip-health.log is expected to grow over time, so a smaller sample file was created for version control evidence.

Sample creation command:

tail -20 evidence/catnip-health.log > evidence/catnip-health-sample.log

Purpose:

store a short, stable evidence artifact
avoid committing a continuously growing log file
make the repository cleaner and easier to assess
6. Git Ignore Update

To prevent the live log file from being committed repeatedly, .gitignore was updated.

File edited:

nano ~/catnip-soc/.gitignore

Entry added:

evidence/catnip-health.log

Purpose:

ignore the continuously updated live log
keep only the controlled sample output in GitHub
7. Files Selected for GitHub Evidence

The following files were prepared for commit:

scripts/health_check.py
docs/WEEK9_10_SECURITY_ENHANCEMENTS.md
evidence/HEALTH_CHECK_EVIDENCE.md
evidence/catnip-health-sample.log
.gitignore

Git commands used:

cd ~/catnip-soc
git add .gitignore scripts/health_check.py docs/WEEK9_10_SECURITY_ENHANCEMENTS.md evidence/HEALTH_CHECK_EVIDENCE.md evidence/catnip-health-sample.log
git status
git commit -m "Week 9-10: Add health check automation evidence and sample output"
git push origin main
8. Troubleshooting Summary
Issue 1: Log file not created in /var/log/

Cause:

insufficient permissions for normal user output redirection

Fix:

moved output to /home/student/catnip-soc/evidence/catnip-health.log
Issue 2: Cron reliability concerns

Cause:

interactive shell assumptions do not always apply in cron

Fix:

replaced export ... && python3 with:
direct variable assignment
absolute path /usr/bin/python3
Issue 3: Git add failed for sample file

Cause:

evidence/catnip-health-sample.log had not yet been created

Fix:

created it explicitly using:
tail -20 evidence/catnip-health.log > evidence/catnip-health-sample.log
9. Security and Operational Value

This automation improves the project in several ways:

provides scheduled system monitoring
detects service or pipeline failures without manual checking
creates repeatable operational evidence
supports professional SOC-style maintenance
demonstrates practical DevOps and operational engineering workflow

This goes beyond simple installation by showing:

automation
validation
troubleshooting
evidence handling
repository hygiene
10. Final Outcome

The health monitoring process is now fully operational.

Final state:

cron job configured correctly
health script executes successfully
output stored in project evidence folder
sample output prepared for GitHub
live log excluded from version control
final health result verified as:
RESULT: 8/8 checks passed
STATUS: HEALTHY
