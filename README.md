<div align="center">

# 🌊 NAMIZUN 2 ULTIMATE
### Smart Traffic Obfuscator & Generator
### ابزار هوشمند متقارن‌سازی ترافیک

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python)](https://www.python.org/)
[![Systemd](https://img.shields.io/badge/Service-Systemd-green?style=for-the-badge)](https://www.freedesktop.org/wiki/Software/systemd/)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg?style=for-the-badge)](https://github.com/OoAryanoO/Namizun-2/graphs/commit-activity)
[![License](https://img.shields.io/badge/License-MIT-orange?style=for-the-badge)](LICENSE)


</div>

---

## English Description

**Namizun 2** is a stealthy, lightweight, and powerful script designed to make your server's traffic look completely natural. It monitors your real download usage and automatically generates fake upload traffic to match it (e.g., 1:1 or 1:10 or 1:15 ratio), preventing detection by data centers or firewalls due to asymmetric traffic.

### ✨ Key Features
* **⚖️ Smart Balance Mode:** Automatically adjusts fake upload based on real-time download usage.
* **🛡️ Stealth & Obfuscation:** injects fake HTTP/HTTPS headers to make traffic look like legitimate web activity.
* **📉 Traffic Jitter:** Simulates human behavior by varying packet sending speed (prevents flat-line patterns).
* **🌐 Fake Web Server:** Runs a lightweight "Cloud Node" status page on port 80/8080 to satisfy IP probes.
* **🖥️ Beautiful UI:** A modern, flicker-free ASCII dashboard to monitor and control everything.
* **🚀 Background Service:** Runs automatically using `systemd` (survives reboots).

### 📥 Quick Installation
Run the following command on your Linux server. **Ubuntu 22+** :

```bash
bash <(curl -sL [https://raw.githubusercontent.com/OoAryanoO/Namizun-Ultimate/main/install.sh](https://raw.githubusercontent.com/OoAryanoO/Namizun-Ultimate/main/install.sh) | tr -d '\r')
```

### ⚙️ Usage
After installation, type the following command to open the menu:

```bash
namizun
```
### ❤ Give Me a Coffee
<a href="https://www.coffeebede.com/darkmine"><img class="img-fluid" src="https://coffeebede.ir/DashboardTemplateV2/app-assets/images/banner/default-yellow.svg" /></a>
