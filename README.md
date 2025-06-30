# PPPoE User Status Exporter for MikroTik → Prometheus → Grafana

🔧 **Pantau status aktif/nonaktif user PPPoE dari MikroTik Router dan tampilkan di Grafana menggunakan Prometheus Pushgateway.**

---

## 🚀 Fitur

- Mengambil data user PPPoE dari `/ppp secret` dan `/ppp active` via MikroTik API
- Menandai status user:
  - `1` = aktif
  - `0` = tidak aktif
- Mengirim metrik ke **Prometheus Pushgateway**
- Visualisasi real-time di **Grafana** menggunakan panel tabel/stat

---

## 📦 Kebutuhan Sistem

- Python 3.x
- MikroTik Router dengan API diaktifkan (`/ip service enable api`)
- Docker (untuk Prometheus, Pushgateway, Grafana)
- Pip packages:
  - `librouteros`
  - `requests`

---

## 🛠 Instalasi

### 1. Clone & Install Dependency

```bash
git clone https://github.com/namaprojek/pppoe-prometheus-exporter.git
cd pppoe-prometheus-exporter
pip install -r requirements.txt
