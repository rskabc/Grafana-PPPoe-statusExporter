# PPPoE Status Exporter for MikroTik → Prometheus → Grafana

🔧 Export status aktif/tidak aktif user PPPoE dari MikroTik ke Prometheus Pushgateway secara otomatis setiap 15 detik, lalu visualisasikan di Grafana.

📍 **Repository Resmi:**  
https://github.com/rskabc/Grafana-PPPoe-statusExporter

---

## 📦 Fitur

- Mengambil data user dari `/ppp secret` MikroTik via API
- Mendeteksi user yang sedang aktif dari `/ppp active`
- Menandai status user sebagai metrik:
  - `1` → Aktif
  - `0` → Tidak Aktif
- Push ke **Prometheus Pushgateway**
- Monitoring real-time di **Grafana**
- Berjalan otomatis via `systemd` setiap 15 detik

---

## 🚀 Instalasi Cepat

### 1. Clone Repo

```bash
git clone https://github.com/rskabc/Grafana-PPPoe-statusExporter.git
cd Grafana-PPPoe-statusExporter
```

### 2. Edit Script Konfigurasi

Buka `pppoe_status_exporter.py` dan sesuaikan:

```python
ROUTER_IP = '10.0.0.1'
USERNAME = 'admin'
PASSWORD = 'yourpassword'
PUSH_URL = 'http://localhost:9091/metrics/job/mikrotik_pppoe_users'
```

### 3. Install Dependensi

```bash
pip install librouteros requests
```

---

## ⚙️ Setup Systemd Service (Per 15 Detik)

### 1. Jalankan `install.sh`

```bash
chmod +x install.sh
./install.sh
```

Script ini akan:
- Menyalin service ke `/etc/systemd/system/`
- Enable dan menjalankan otomatis setiap 15 detik

---

## 🔎 Verifikasi

```bash
systemctl status pppoe-status
journalctl -fu pppoe-status
```

Cek Prometheus di `http://localhost:9090`, lalu query:

```promql
mikrotik_pppoe_user_status
```

---

## 📊 Tampilkan di Grafana

1. Tambahkan **Prometheus** sebagai data source
2. Buat Panel Tabel
3. Query:
   ```promql
   mikrotik_pppoe_user_status
   ```
4. Gunakan Transform:
   - Organize fields → user, value
   - Value mapping: `0 = Tidak Aktif`, `1 = Aktif`

---

## 🗓 Interval Update

Script dijalankan otomatis setiap **15 detik** menggunakan:

```ini
Restart=always
RestartSec=15s
```

Ubah di file:
```
/etc/systemd/system/pppoe-status.service
```

---

## 📂 Struktur Proyek

```
Grafana-PPPoe-statusExporter/
├── pppoe_status_exporter.py
├── pppoe-status.service
├── install.sh
└── README.md
```

---

## ✨ Kontributor


- @rskabc – 
---

## 📄 Lisensi

MIT License
