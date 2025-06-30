from librouteros import connect
import requests

# -----------------------------
# Konfigurasi
# -----------------------------

ROUTER_IP = '10.0.0.1'           # Ganti dengan IP MikroTik kamu
USERNAME = 'admin'               # Username login MikroTik
PASSWORD = 'yourpassword'        # Password MikroTik
PUSH_URL = 'http://localhost:9091/metrics/job/mikrotik_pppoe_users'  # Ubah jika Pushgateway di server lain

# -----------------------------
# Ambil data dari MikroTik
# -----------------------------

def get_pppoe_status():
    try:
        api = connect(
            host=ROUTER_IP,
            username=USERNAME,
            password=PASSWORD,
            port=8728
        )

        # Semua user dari /ppp secret
        all_users = {u['name']: 0 for u in api.path('ppp', 'secret')}

        # User yang sedang aktif dari /ppp active
        active_users = [u['name'] for u in api.path('ppp', 'active')]

        # Tandai user yang aktif
        for user in active_users:
            if user in all_users:
                all_users[user] = 1

        return all_users

    except Exception as e:
        print(f'Gagal koneksi ke MikroTik: {e}')
        return {}

# -----------------------------
# Push ke Pushgateway
# -----------------------------

def push_to_prometheus(user_status_dict):
    if not user_status_dict:
        print("Tidak ada data untuk dikirim.")
        return

    lines = [
        '# HELP mikrotik_pppoe_user_status 1=aktif, 0=tidak aktif',
        '# TYPE mikrotik_pppoe_user_status gauge'
    ]

    for user, status in user_status_dict.items():
        lines.append(f'mikrotik_pppoe_user_status{{user="{user}"}} {status}')

    payload = '\n'.join(lines) + '\n'

    try:
        response = requests.post(PUSH_URL, data=payload)

        if response.status_code in (200, 202):
            print('Metrics pushed successfully')
        else:
            print(f'Failed to push metrics: {response.status_code} - {response.text}')

    except requests.exceptions.RequestException as e:
        print(f'Error saat mengirim ke Pushgateway: {e}')

# -----------------------------
# Main
# -----------------------------

if __name__ == "__main__":
    status = get_pppoe_status()
    push_to_prometheus(status)
