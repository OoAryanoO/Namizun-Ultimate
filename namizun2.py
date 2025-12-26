#!/usr/bin/env python3
import os
import sys
import time
import socket
import random
import threading
import psutil
import json
import tty
import termios
import select
import http.server
import socketserver
from collections import deque

CONFIG_FILE = "/etc/namizun2_conf.json"
SERVICE_PATH = "/etc/systemd/system/namizun2.service"
WEB_ROOT = "/tmp/namizun_web"
HISTORY_LEN = 50
history = deque([0] * HISTORY_LEN, maxlen=HISTORY_LEN)

FAKE_SITE_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>StreamHub - Watch Unlimited Movies & Series</title>
<style>
    :root { --primary: #e50914; --dark: #141414; --light: #ffffff; --gray: #aaa; }
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body { font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; background-color: var(--dark); color: var(--light); overflow-x: hidden; }
    a { text-decoration: none; color: var(--light); }
    /* Header */
    header { display: flex; justify-content: space-between; align-items: center; padding: 20px 4%; position: fixed; width: 100%; z-index: 100; background: linear-gradient(to bottom, rgba(0,0,0,0.9) 0%, rgba(0,0,0,0) 100%); transition: background 0.3s; }
    .logo { font-size: 2rem; font-weight: bold; color: var(--primary); letter-spacing: 2px; }
    nav ul { display: flex; list-style: none; }
    nav ul li { margin-left: 20px; }
    nav ul li a { font-size: 0.9rem; transition: color 0.3s; }
    nav ul li a:hover { color: var(--gray); }
    /* Hero Section */
    .hero { height: 85vh; background: linear-gradient(rgba(0,0,0,0.4), var(--dark)), url('https://source.unsplash.com/1600x900/?cinematic,movie,dark') no-repeat center center/cover; display: flex; align-items: center; padding: 0 4%; }
    .hero-content { max-width: 600px; margin-top: 60px; }
    .hero-title { font-size: 3.5rem; margin-bottom: 20px; font-weight: 800; }
    .hero-desc { font-size: 1.1rem; margin-bottom: 30px; line-height: 1.4; color: #ddd; }
    .btn { padding: 12px 30px; border: none; border-radius: 4px; font-size: 1rem; font-weight: bold; cursor: pointer; transition: all 0.3s; display: inline-flex; align-items: center; }
    .btn-primary { background-color: var(--primary); color: var(--light); }
    .btn-primary:hover { background-color: #bd0810; }
    .btn-secondary { background-color: rgba(109, 109, 110, 0.7); color: var(--light); margin-left: 15px; }
    .btn-secondary:hover { background-color: rgba(109, 109, 110, 0.4); }
    /* Movie Sections */
    .section { padding: 20px 4%; margin-bottom: 40px; }
    .section-title { font-size: 1.4rem; margin-bottom: 20px; font-weight: 600; }
    .movie-row { display: grid; grid-template-columns: repeat(auto-fill, minmax(180px, 1fr)); gap: 15px; }
    .movie-card { position: relative; border-radius: 6px; overflow: hidden; cursor: pointer; transition: transform 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94); aspect-ratio: 2/3; background-color: #222; }
    .movie-card:hover { transform: scale(1.05); z-index: 2; box-shadow: 0 10px 20px rgba(0,0,0,0.5); }
    .movie-card img { width: 100%; height: 100%; object-fit: cover; opacity: 0.85; transition: opacity 0.3s; }
    .movie-card:hover img { opacity: 1; }
    .movie-info { position: absolute; bottom: 0; left: 0; width: 100%; padding: 15px; background: linear-gradient(to top, rgba(0,0,0,0.9), transparent); opacity: 0; transition: opacity 0.3s; }
    .movie-card:hover .movie-info { opacity: 1; }
    .movie-title { font-size: 0.9rem; font-weight: bold; }
    /* Footer */
    footer { padding: 30px 4%; text-align: center; color: var(--gray); font-size: 0.8rem; margin-top: 50px; border-top: 1px solid #333; }
    @media (max-width: 768px) { .hero-title { font-size: 2.5rem; } nav ul { display: none; } .movie-row { grid-template-columns: repeat(auto-fill, minmax(120px, 1fr)); } }
</style>
</head>
<body>
    <header>
        <div class="logo">STREAMHUB</div>
        <nav>
            <ul>
                <li><a href="#">Home</a></li>
                <li><a href="#">TV Shows</a></li>
                <li><a href="#">Movies</a></li>
                <li><a href="#">New & Popular</a></li>
            </ul>
        </nav>
    </header>

    <section class="hero">
        <div class="hero-content">
            <h1 class="hero-title">The Cyber Nexus</h1>
            <p class="hero-desc">In a future governed by data, one rogue AI decides to rewrite the rules. Witness the beginning of the digital revolution.</p>
            <div>
                <button class="btn btn-primary">▶ Play Now</button>
                <button class="btn btn-secondary">ℹ More Info</button>
            </div>
        </div>
    </section>

    <section class="section">
        <h2 class="section-title">Trending Now</h2>
        <div class="movie-row">
            <div class="movie-card"><img src="https://source.unsplash.com/300x450/?scifi,movie,1" alt="Movie"><div class="movie-info"><div class="movie-title">Stellar Odyssey</div></div></div>
            <div class="movie-card"><img src="https://source.unsplash.com/300x450/?action,movie,2" alt="Movie"><div class="movie-info"><div class="movie-title">Protocol Zero</div></div></div>
            <div class="movie-card"><img src="https://source.unsplash.com/300x450/?drama,movie,3" alt="Movie"><div class="movie-info"><div class="movie-title">The Silent Echo</div></div></div>
            <div class="movie-card"><img src="https://source.unsplash.com/300x450/?thriller,movie,4" alt="Movie"><div class="movie-info"><div class="movie-title">Midnight Protocol</div></div></div>
            <div class="movie-card"><img src="https://source.unsplash.com/300x450/?adventure,movie,5" alt="Movie"><div class="movie-info"><div class="movie-title">Lost Horizons</div></div></div>
            <div class="movie-card"><img src="https://source.unsplash.com/300x450/?fantasy,movie,6" alt="Movie"><div class="movie-info"><div class="movie-title">Aether Realm</div></div></div>
        </div>
    </section>

    <section class="section">
        <h2 class="section-title">New Releases</h2>
        <div class="movie-row">
            <div class="movie-card"><img src="https://source.unsplash.com/300x450/?cyberpunk,movie,7" alt="Movie"><div class="movie-info"><div class="movie-title">Neon Shadows</div></div></div>
            <div class="movie-card"><img src="https://source.unsplash.com/300x450/?mystery,movie,8" alt="Movie"><div class="movie-info"><div class="movie-title">The Enigma Key</div></div></div>
            <div class="movie-card"><img src="https://source.unsplash.com/300x450/?crime,movie,9" alt="Movie"><div class="movie-info"><div class="movie-title">Underground City</div></div></div>
             <div class="movie-card"><img src="https://source.unsplash.com/300x450/?dark,movie,10" alt="Movie"><div class="movie-info"><div class="movie-title">Void Walker</div></div></div>
        </div>
    </section>

    <footer>
        <p>© 2024 StreamHub Inc. All rights reserved. <br> This is a demonstration site for network testing purposes.</p>
    </footer>
</body>
</html>
"""

def get_best_interface():
    try:
        stats = psutil.net_io_counters(pernic=True)
        for iface in stats:
            if iface != 'lo' and stats[iface].bytes_sent > 0:
                return iface
    except: pass
    return "eth0"

default_config = {
    "status": "stopped",
    "protocol": "TCP",
    "ratio_min": 1.0,
    "ratio_max": 1.2,
    "interface": get_best_interface(),
    "total_real_sent": 0,
    "total_fake_sent": 0,
    "active_target": "None",
    "targets": ["1.1.1.1", "8.8.8.8", "filimo.com", "arvancloud.ir", "snapp.ir"],
    "web_server": False,
    "web_port": 8080,
    "jitter": True, 
    "obfuscate": True
}

def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as f: return json.load(f)
        except: pass
    return default_config

def save_config(config):
    try:
        with open(CONFIG_FILE, 'w') as f: json.dump(config, f)
    except: pass

def run_web_server_thread():
    if not os.path.exists(WEB_ROOT):
        os.makedirs(WEB_ROOT)
    with open(os.path.join(WEB_ROOT, "index.html"), "w") as f:
        f.write(FAKE_SITE_HTML)
    
    os.chdir(WEB_ROOT)
    config = load_config()
    port = config.get("web_port", 8080)
    
    Handler = http.server.SimpleHTTPRequestHandler
    class QuietHandler(Handler):
        def log_message(self, format, *args):
            pass
            
    try:
        with socketserver.TCPServer(("", port), QuietHandler) as httpd:
            httpd.serve_forever()
    except:
        pass 

def perform_upload(amount, protocol, host, jitter, obfuscate):
    try:
        port = random.choice([80, 443])
        
        if obfuscate:
            header = f"POST /api/v2/sync HTTP/1.1\r\nHost: {host}\r\nUser-Agent: Mozilla/5.0\r\nContent-Type: application/octet-stream\r\n\r\n".encode()
            data = header + random.randbytes(min(amount, 1024*64))
        else:
            data = random.randbytes(min(amount, 1024*512))

        if protocol == "TCP":
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(2)
                s.connect((host, port))
                
                if jitter:
                    chunk_size = len(data) // 4
                    for i in range(0, len(data), chunk_size):
                        s.send(data[i:i+chunk_size])
                        time.sleep(random.uniform(0.01, 0.05)) 
                else:
                    s.sendall(data)
        else:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                s.sendto(data[:60000], (host, port))
    except: pass

def fake_uploader():
    web_thread = None
    
    while True:
        config = load_config()
        
        if config["web_server"] and (web_thread is None or not web_thread.is_alive()):
            web_thread = threading.Thread(target=run_web_server_thread, daemon=True)
            web_thread.start()
            
        if config["status"] != "running":
            time.sleep(2); continue
            
        iface = config.get("interface", "eth0")
        try:
            io_before = psutil.net_io_counters(pernic=True).get(iface)
            recv_before = io_before.bytes_recv
            sent_before = io_before.bytes_sent
            time.sleep(1)
            io_after = psutil.net_io_counters(pernic=True).get(iface)
            
            real_download = io_after.bytes_recv - recv_before
            real_upload = io_after.bytes_sent - sent_before
        except: time.sleep(1); continue

        if real_download > 1024 * 10: 
            target_ratio = random.uniform(config["ratio_min"], config["ratio_max"])
            target_upload = real_download * target_ratio
            needed_fake = target_upload - real_upload
            
            if needed_fake > 0:
                target = random.choice(config["targets"])
                config["active_target"] = target
                config["total_fake_sent"] += needed_fake
                save_config(config)
                
                threads = []
                num_threads = 5 if config["jitter"] else 10
                chunk_size = int(needed_fake / num_threads) + 1
                
                for _ in range(num_threads):
                    t = threading.Thread(target=perform_upload, args=(chunk_size, config["protocol"], target, config["jitter"], config["obfuscate"]))
                    t.start(); threads.append(t)
                for t in threads: t.join(timeout=0.8)
            else:
                config["active_target"] = "Balanced"
                save_config(config)

def get_size(bytes, suffix="B"):
    factor = 1024
    for unit in ["", "K", "M", "G", "T"]:
        if bytes < factor: return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor
    return f"{bytes:.2f}P{suffix}"

def draw_box(title, lines, width=64):
    box = f"\033[1;36m╔{'═' * (width-2)}╗\033[0m\n"
    box += f"\033[1;36m║\033[0m {title:^{width-4}} \033[1;36m║\033[0m\n"
    box += f"\033[1;36m╠{'═' * (width-2)}╣\033[0m\n"
    for line in lines:
        clean_line = line
        for color in ['\033[32m', '\033[31m', '\033[33m', '\033[35m', '\033[36m', '\033[1;33m', '\033[0m']:
            clean_line = clean_line.replace(color, '')
        padding = max(0, width - 4 - len(clean_line))
        box += f"\033[1;36m║\033[0m {line}{' ' * padding} \033[1;36m║\033[0m\n"
    box += f"\033[1;36m╚{'═' * (width-2)}╝\033[0m"
    return box

def draw_chart(data):
    height = 5
    max_val = max(data) if max(data) > 0 else 1
    rows = []
    for h in range(height, 0, -1):
        line = ""
        threshold = (max_val / height) * h
        for val in data:
            if val >= threshold: line += "█"
            elif val >= threshold * 0.5: line += "▄"
            else: line += " "
        rows.append(f"\033[32m{line}\033[0m")
    return rows

def restore_terminal(old_settings):
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)

def set_raw_mode():
    tty.setcbreak(sys.stdin.fileno())

def menu(old_settings):
    config = load_config()
    iface = config["interface"]
    os.system('clear')
    user_input = ""
    
    while True:
        config = load_config()
        sys.stdout.write("\033[H")
        
        try:
            io1 = psutil.net_io_counters(pernic=True).get(iface)
            time.sleep(0.2)
            io2 = psutil.net_io_counters(pernic=True).get(iface)
            speed = (io2.bytes_sent + io2.bytes_recv) - (io1.bytes_sent + io1.bytes_recv)
            history.append(speed * 5)
        except: pass

        status_c = "\033[32mRUNNING" if config['status'] == 'running' else "\033[31mSTOPPED"
        web_c = f"\033[32mON (:{config.get('web_port')})" if config.get('web_server') else "\033[31mOFF"
        jitter_c = "\033[32mON" if config.get('jitter') else "\033[31mOFF"
        
        l1 = f"Status: {status_c}\033[0m   Protocol: \033[1;33m{config['protocol']}\033[0m   WebSite: {web_c}\033[0m"
        l2 = f"Mode: \033[36mSmart Balance\033[0m (Ratio: {config['ratio_min']}x)"
        l3 = f"Target: {config.get('active_target', 'None')[:25]}"
        l4 = f"Fake Upload: {get_size(config['total_fake_sent'])} | Jitter: {jitter_c}\033[0m"
        
        chart = draw_chart(list(history))
        
        content = [l1, l2, l3, l4, "-" * 58] + chart + ["-" * 58,
            "1. Start/Stop       2. TCP/UDP",
            "3. Set Ratio        4. Manage Targets",
            "5. Fake WebSite     6. Toggle Jitter/Obf",
            "7. Install Service  8. Uninstall",
            "9. Exit"
        ]
        
        print(draw_box(f"NAMIZUN 3 ULTIMATE - {iface}", content))
        print(f"\nCommand > {user_input}", end="\033[K", flush=True)

        i, _, _ = select.select([sys.stdin], [], [], 0.5)
        if i:
            char = sys.stdin.read(1)
            if char == '\n':
                c = user_input.strip()
                user_input = ""
                if c == '1':
                    config['status'] = 'running' if config['status'] == 'stopped' else 'stopped'
                    save_config(config)
                elif c == '2':
                    config['protocol'] = 'UDP' if config['protocol'] == 'TCP' else 'TCP'
                    save_config(config)
                elif c == '3':
                    restore_terminal(old_settings)
                    os.system('clear')
                    print(draw_box("RATIO SETTINGS", ["Enter ratio (e.g. 1.0 for equal up/dl)", "Recommended: 1.0 - 1.5"]))
                    try: 
                        r = float(input("\nRatio: "))
                        config['ratio_min'] = r; config['ratio_max'] = r + 0.2
                        save_config(config)
                    except: pass
                    set_raw_mode(); os.system('clear')
                elif c == '4':
                    restore_terminal(old_settings)
                    os.system('clear')
                    print("Targets: " + ", ".join(config['targets']))
                    t = input("\nAdd Target (Empty to cancel): ")
                    if t: config['targets'].append(t); save_config(config)
                    set_raw_mode(); os.system('clear')
                elif c == '5':
                    current = config.get("web_server", False)
                    config["web_server"] = not current
                    if not current:
                        restore_terminal(old_settings)
                        try:
                            p = int(input("\nWeb Port (80 or 8080): "))
                            config["web_port"] = p
                        except: pass
                        set_raw_mode()
                    save_config(config)
                elif c == '6':
                    config["jitter"] = not config.get("jitter", True)
                    config["obfuscate"] = not config.get("obfuscate", True)
                    save_config(config)
                elif c == '7':
                    script_path = os.path.abspath(__file__)
                    cnt = f"[Unit]\nDescription=Namizun3\nAfter=network.target\n\n[Service]\nType=simple\nExecStart=/usr/bin/python3 {script_path} run\nRestart=always\n\n[Install]\nWantedBy=multi-user.target"
                    with open(SERVICE_PATH, 'w') as f: f.write(cnt)
                    os.system("systemctl daemon-reload && systemctl enable namizun2 && systemctl restart namizun2")
                    print("\nService Installed."); time.sleep(1)
                elif c == '8':
                    os.system(f"systemctl stop namizun2 && systemctl disable namizun2 && rm {SERVICE_PATH}")
                    if os.path.exists(CONFIG_FILE): os.remove(CONFIG_FILE)
                    os.system("rm /usr/local/bin/namizun2")
                    break
                elif c == '9': break
            elif ord(char) == 127: user_input = user_input[:-1]
            else: user_input += char

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "run":
        fake_uploader()
    else:
        old_settings = termios.tcgetattr(sys.stdin)
        try:
            os.system(f"ln -sf {os.path.abspath(__file__)} /usr/local/bin/namizun2")
            os.system(f"chmod +x {os.path.abspath(__file__)}")
            tty.setcbreak(sys.stdin.fileno())
            menu(old_settings)
        except KeyboardInterrupt: pass
        finally:
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
            os.system('clear')
