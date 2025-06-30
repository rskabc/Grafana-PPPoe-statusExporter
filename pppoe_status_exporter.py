# pppoe_status_exporter.py
# Author: Reski Abuchaer (@rskabc)
# License: MIT
import os
import re
import json
import requests
from librouteros import connect
from pathlib import Path

MT_HOST = os.getenv('MT_HOST')
MT_USERNAME = os.getenv('MT_USERNAME')
MT_PASSWORD = os.getenv('MT_PASSWORD')
PUSH_URL = os.getenv('PUSH_URL', 'http://pushgateway:9091/metrics/job/mikrotik_pppoe_users')

if not MT_USERNAME or not MT_PASSWORD or not MT_HOST:
    raise ValueError("Environment variables MT_HOST, MT_USERNAME, and MT_PASSWORD must be set")

def parse_uptime_to_seconds(uptime_str):
    total = 0
    units = {'d': 86400, 'h': 3600, 'm': 60, 's': 1}
    matches = re.findall(r'(\d+)([dhms])', uptime_str)
    for value, unit in matches:
        total += int(value) * units[unit]
    return total

def fetch_active_users():
    try:
        api = connect(
            host=MT_HOST,
            username=MT_USERNAME,
            password=MT_PASSWORD
        )
        return list(api('/ppp/active/print'))
    except Exception as e:
        print(f"Gagal koneksi ke MikroTik: {e}")
        return []

def push_to_prometheus(active_users):
    lines = []

    for user in active_users:
        name = user.get('name')
        address = user.get('address', '0.0.0.0')
        caller_id = user.get('caller-id', 'unknown')
        uptime_str = user.get('uptime', '0s')
        uptime = parse_uptime_to_seconds(uptime_str)

        lines.append(f'mikrotik_pppoe_user_status{{user="{name}", instance="{address}"}} 1')
        lines.append(f'mikrotik_pppoe_user_callerid{{user="{name}", caller_id="{caller_id}"}} 1')
        lines.append(f'mikrotik_pppoe_user_uptime_seconds{{user="{name}"}} {uptime}')

    payload = "\n".join(lines) + "\n"

    try:
        response = requests.post(PUSH_URL, data=payload)
        if response.status_code == 200:
            print("Metrics pushed successfully")
        else:
            print(f"Failed to push metrics: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Error saat mengirim ke Pushgateway: {e}")

if __name__ == "__main__":
    users = fetch_active_users()
    if users:
        push_to_prometheus(users)
    else:
        print("Tidak ada data untuk dikirim.")
