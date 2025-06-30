#!/bin/bash
echo " Menginstall PPPoE Status Exporter Service..."

# Salin service ke systemd
cp pppoe-status.service /etc/systemd/system/pppoe-status.service

# Reload systemd
systemctl daemon-reexec
systemctl daemon-reload

# Enable dan start service
systemctl enable pppoe-status
systemctl start pppoe-status

# Tampilkan status
systemctl status pppoe-status --no-pager
