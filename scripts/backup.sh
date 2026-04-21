#!/bin/bash
# Catnip Games SOC - Automated Backup Script
# Backs up: project files, live ELK configs, UFW rules, and system state
# Output: timestamped tar.gz archive
# Author: Anton Ivanov

set -euo pipefail

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="$HOME/backups"
BACKUP_NAME="catnip-soc-backup-${TIMESTAMP}"
TEMP_DIR="/tmp/${BACKUP_NAME}"

echo "=========================================="
echo "  CATNIP GAMES SOC - BACKUP SYSTEM"
echo "  $(date)"
echo "=========================================="
echo ""

mkdir -p "${BACKUP_DIR}"
mkdir -p "${TEMP_DIR}"

# 1. Backup project files
echo "[1/5] Backing up project files..."
cp -r ~/catnip-soc/scripts "${TEMP_DIR}/"
cp -r ~/catnip-soc/configs "${TEMP_DIR}/"
cp -r ~/catnip-soc/docs "${TEMP_DIR}/"
cp ~/catnip-soc/README.md "${TEMP_DIR}/" 2>/dev/null || true
echo "    Done: scripts, configs, docs"

# 2. Backup live ELK configurations
echo "[2/5] Backing up ELK configurations..."
mkdir -p "${TEMP_DIR}/elk-live-configs"

if sudo -n true 2>/dev/null; then
    sudo cp /etc/elasticsearch/elasticsearch.yml "${TEMP_DIR}/elk-live-configs/" 2>/dev/null || true
    sudo cp /etc/kibana/kibana.yml "${TEMP_DIR}/elk-live-configs/" 2>/dev/null || true
    sudo cp /etc/logstash/conf.d/firewall.conf "${TEMP_DIR}/elk-live-configs/" 2>/dev/null || true
    sudo chown -R "$USER:$USER" "${TEMP_DIR}/elk-live-configs" 2>/dev/null || true
    echo "    Done: elasticsearch.yml, kibana.yml, firewall.conf"
else
    echo "    Skipped live ELK config backup: sudo password required"
fi

# 3. Backup firewall rules
echo "[3/5] Backing up firewall rules..."
if sudo -n true 2>/dev/null; then
    sudo ufw status verbose > "${TEMP_DIR}/ufw-rules.txt" 2>/dev/null || echo "UFW not active" > "${TEMP_DIR}/ufw-rules.txt"
else
    echo "sudo not available without password" > "${TEMP_DIR}/ufw-rules.txt"
fi
echo "    Done: ufw-rules.txt"

# 4. Capture system state
echo "[4/5] Capturing system state..."
systemctl list-units --type=service --state=running > "${TEMP_DIR}/running-services.txt" 2>/dev/null || true
ss -lntp > "${TEMP_DIR}/listening-ports.txt" 2>/dev/null || true
df -h > "${TEMP_DIR}/disk-usage.txt" 2>/dev/null || true
free -h > "${TEMP_DIR}/memory-usage.txt" 2>/dev/null || true
echo "    Done: services, ports, disk, memory"

# 5. Create compressed archive
echo "[5/5] Creating compressed archive..."
tar -czf "${BACKUP_DIR}/${BACKUP_NAME}.tar.gz" -C /tmp "${BACKUP_NAME}"
rm -rf "${TEMP_DIR}"

SIZE=$(ls -lh "${BACKUP_DIR}/${BACKUP_NAME}.tar.gz" | awk '{print $5}')

echo ""
echo "=========================================="
echo "  BACKUP COMPLETE"
echo "  File: ${BACKUP_DIR}/${BACKUP_NAME}.tar.gz"
echo "  Size: ${SIZE}"
echo "=========================================="
