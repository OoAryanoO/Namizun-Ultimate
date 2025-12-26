<div align="center">

# 🌊 NAMIZUN 2 ULTIMATE
### Smart Traffic Obfuscator & Generator
### ابزار هوشمند متقارن‌سازی و تولید ترافیک

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python)](https://www.python.org/)
[![Systemd](https://img.shields.io/badge/Service-Systemd-green?style=for-the-badge)](https://www.freedesktop.org/wiki/Software/systemd/)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg?style=for-the-badge)](https://github.com/OoAryanoO/Namizun-2/graphs/commit-activity)
[![License](https://img.shields.io/badge/License-MIT-orange?style=for-the-badge)](LICENSE)

<p align="center">
  <a href="#english">English</a> •
  <a href="#persian">فارسی</a>
</p>

![Terminal Interface](https://via.placeholder.com/800x400.png?text=Please+Upload+Your+Screenshot+Here)

</div>

---

<a name="english"></a>
## English Description

**Namizun 2** is a stealthy, lightweight, and powerful script designed to make your server's traffic look completely natural. It monitors your real download usage and automatically generates fake upload traffic to match it (e.g., 1:1 ratio), preventing detection by data centers or firewalls due to asymmetric traffic.

### ✨ Key Features
* **⚖️ Smart Balance Mode:** Automatically adjusts fake upload based on real-time download usage.
* **🛡️ Stealth & Obfuscation:** injects fake HTTP/HTTPS headers to make traffic look like legitimate web activity.
* **📉 Traffic Jitter:** Simulates human behavior by varying packet sending speed (prevents flat-line patterns).
* **🌐 Fake Web Server:** Runs a lightweight "Cloud Node" status page on port 80/8080 to satisfy IP probes.
* **🖥️ Beautiful UI:** A modern, flicker-free ASCII dashboard to monitor and control everything.
* **🚀 Background Service:** Runs automatically using `systemd` (survives reboots).

### 📥 Quick Installation
Run the following command on your Linux server. **This command automatically fixes line-ending issues** and installs all dependencies:

```bash
bash <(curl -sL [https://raw.githubusercontent.com/OoAryanoO/Namizun-Ultimate/main/install.sh](https://raw.githubusercontent.com/OoAryanoO/Namizun-Ultimate/main/install.sh) | tr -d '\r')
```

### ⚙️ Usage
After installation, simply type the following command to open the menu:

```bash
namizun
```
=================================================
<a name="persian"></a>

<div dir="rtl" align="right">

## توضیحات
**نامیزون 2**  یک ابزار حرفه‌ای برای "طبیعی‌سازی" ترافیک سرور شماست. این اسکریپت با رصد لحظه‌ای میزان دانلود سرور، ترافیک آپلود و رمزنگاری شده تولید می‌کند تا حساسیت  نسبت به ترافیک نامتقارن (فقط دانلود) از بین برود.

### ✨قابلیت‌های کلیدی

⚖️ (Smart Balance): اگر سرور دانلود کند، نامیزون به همان اندازه (یا با ضریب دلخواه) آپلود می‌کند تا ترافیک ۱ به ۱ شود.

🛡️  (Obfuscation): ترافیک ارسالی دارای هدرهای واقعی HTTP است تا شبیه به بازدید سایت یا آپلود فایل به نظر برسد.

📉  (Jitter): سرعت ارسال ثابت نیست و نوسان دارد تا الگوی ماشینی و خط صاف ایجاد نشود.

🖥️ (Ui): منوی گرافیکی در محیط ترمینال برای مدیریت آسان.


📥 نصب آسان (دستور اصلاح شده)
برای نصب بدون خطا، دستور زیر را کپی کرده و در ترمینال اجرا کنید (این دستور مشکل خطاهای ویندوزی را خودکار حل می‌کند):

Bash
```
bash <(curl -sL [https://raw.githubusercontent.com/OoAryanoO/Namizun-Ultimate/main/install.sh](https://raw.githubusercontent.com/OoAryanoO/Namizun-Ultimate/main/install.sh) | tr -d '\r')
```
⚙️ نحوه استفاده
بعد از نصب، برای باز کردن پنل تنظیمات کافیست دستور زیر را بزنید:
```bash
namizun
```
</div>
