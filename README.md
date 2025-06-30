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
