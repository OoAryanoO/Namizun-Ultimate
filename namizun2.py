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
from collections import deque

CONFIG_FILE = "/etc/namizun2_conf.json"
SERVICE_PATH = "/etc/systemd/system/namizun2.service"
HISTORY_LEN = 50
history = deque([0] * HISTORY_LEN, maxlen=HISTORY_LEN)

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
    "ratio_min": 1,
    "ratio_max": 1,
    "interface": get_best_interface(),
    "total_real_sent": 0,
    "total_fake_sent": 0,
    "active_target": "None",
    "targets": ["1.1.1.1", "8.8.8.8", "filimo.com", "arvancloud.ir", "snapp.ir", "varzesh3.com"]
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

def perform_upload(amount, protocol, host):
    try:
        port = random.choice([80, 443])
        if protocol == "TCP":
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(1); s.connect((host, port))
                s.sendall(random.randbytes(min(amount, 1024*512)))
        else:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                s.sendto(random.randbytes(min(amount, 60000)), (host, port))
    except: pass

def fake_uploader():
    while True:
        config = load_config()
        if config["status"] != "running":
            time.sleep(2); continue
            
        iface = config.get("interface", "eth0")
        try:
            io_before = psutil.net_io_counters(pernic=True).get(iface)
            recv_before = io_before.bytes_recv
            sent_before = io_before.bytes_sent
            
            time.sleep(1)
            
            io_after = psutil.net_io_counters(pernic=True).get(iface)
            recv_after = io_after.bytes_recv
            sent_after = io_after.bytes_sent
            
            real_download_speed = recv_after - recv_before
            real_upload_speed = sent_after - sent_before
        except: time.sleep(1); continue

        if real_download_speed > 1024 * 10: 
            target_ratio = random.uniform(config["ratio_min"], config["ratio_max"])
            target_upload = real_download_speed * target_ratio
            
            needed_fake = target_upload - real_upload_speed
            
            if needed_fake > 0:
                target = random.choice(config["targets"])
                config["active_target"] = target
                config["total_fake_sent"] += needed_fake
                save_config(config)
                
                chunk_size = int(needed_fake / 10) + 1
                threads = []
                for _ in range(10):
                    t = threading.Thread(target=perform_upload, args=(chunk_size, config["protocol"], target))
                    t.start(); threads.append(t)
                for t in threads: t.join(timeout=0.5)
            else:
                config["active_target"] = "Waiting (Balanced)"
                save_config(config)

def get_size(bytes, suffix="B"):
    factor = 1024
    for unit in ["", "K", "M", "G", "T"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor
    return f"{bytes:.2f}P{suffix}"

def draw_box(title, lines, width=60):
    box = f"\033[1;34m╔{'═' * (width-2)}╗\033[0m\n"
    box += f"\033[1;34m║\033[0m {title:^{width-4}} \033[1;34m║\033[0m\n"
    box += f"\033[1;34m╠{'═' * (width-2)}╣\033[0m\n"
    for line in lines:
        clean_line = line.replace('\033[32m', '').replace('\033[31m', '').replace('\033[1;33m', '').replace('\033[0m', '')
        padding = width - 4 - len(clean_line)
        padding = max(0, padding)
        box += f"\033[1;34m║\033[0m {line}{' ' * padding} \033[1;34m║\033[0m\n"
    box += f"\033[1;34m╚{'═' * (width-2)}╝\033[0m"
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

        status_color = "\033[32mRUNNING" if config['status'] == 'running' else "\033[31mSTOPPED"
        status_line = f"Status: {status_color}\033[0m   Protocol: \033[1;33m{config['protocol']}\033[0m"
        
        target_display = config.get('active_target', 'None')[:20]
        info_line = f"Target: {target_display}"
        ratio_line = f"Mode: \033[1;33mDownload Matching\033[0m (Ratio: {config['ratio_min']}x)"
        
        stats_line = f"Real: {get_size(config['total_real_sent'])} | Fake: {get_size(config['total_fake_sent'])}"
        
        chart_lines = draw_chart(list(history))
        
        content = [
            status_line,
            ratio_line,
            info_line,
            stats_line,
            "-" * 54
        ] + chart_lines + [
            "-" * 54,
            "1. Start/Stop       2. TCP/UDP",
            "3. Set Ratio        4. Manage Targets",
            "5. Install Service  6. Uninstall",
            "7. Exit"
        ]

        print(draw_box(f"NAMIZUN 2 PRO - {iface}", content))
        print(f"\nCommand > {user_input}", end="\033[K", flush=True)

        i, _, _ = select.select([sys.stdin], [], [], 0.5)
        
        if i:
            char = sys.stdin.read(1)
            if char == '\n':
                choice = user_input.strip()
                user_input = ""
                
                if choice == '1':
                    config['status'] = 'running' if config['status'] == 'stopped' else 'stopped'
                    save_config(config)
                elif choice == '2':
                    config['protocol'] = 'UDP' if config['protocol'] == 'TCP' else 'TCP'
                    save_config(config)
                elif choice == '3':
                    restore_terminal(old_settings)
                    os.system('clear')
                    print(draw_box("SETTINGS", ["Enter Traffic Ratio", "1 = Equal Upload/Download", "0.5 = Half Upload", "2 = Double Upload"]))
                    try:
                        print("\n(Current Ratio: " + str(config['ratio_min']) + ")")
                        new_r = float(input("Enter new ratio: "))
                        config['ratio_min'] = new_r
                        config['ratio_max'] = new_r
                        save_config(config)
                    except: pass
                    set_raw_mode()
                    os.system('clear')
                elif choice == '4':
                    restore_terminal(old_settings)
                    manage_targets_static()
                    set_raw_mode()
                    os.system('clear')
                elif choice == '5':
                    install_service()
                elif choice == '6':
                    uninstall(); break
                elif choice == '7':
                    break
            elif ord(char) == 127: # Backspace handle
                user_input = user_input[:-1]
            else:
                user_input += char

def manage_targets_static():
    os.system('clear')
    config = load_config()
    print("==== 🎯 Manage Targets ====")
    for i, t in enumerate(config["targets"]): print(f"{i+1}. {t}")
    print("-" * 25 + "\nA. Add | R. Remove | Enter to Back")
    c = input("\nAction: ").lower()
    if c == 'a':
        t = input("Enter Target (Domain/IP): ")
        if t: config["targets"].append(t); save_config(config)
    elif c == 'r':
        try: idx = int(input("Remove ID: ")) - 1; config["targets"].pop(idx); save_config(config)
        except: pass

def install_service():
    script_path = os.path.abspath(__file__)
    content = f"[Unit]\nDescription=Namizun2\nAfter=network.target\n\n[Service]\nType=simple\nExecStart=/usr/bin/python3 {script_path} run\nRestart=always\n\n[Install]\nWantedBy=multi-user.target"
    with open(SERVICE_PATH, 'w') as f: f.write(content)
    os.system("systemctl daemon-reload && systemctl enable namizun2 && systemctl restart namizun2")
    print("\n\033[32m✓ Service Updated Successfully.\033[0m"); time.sleep(1.5)

def uninstall():
    os.system("systemctl stop namizun2 && systemctl disable namizun2 && rm " + SERVICE_PATH)
    if os.path.exists(CONFIG_FILE): os.remove(CONFIG_FILE)
    os.system("rm /usr/local/bin/namizun2")
    print("\n✓ Uninstalled."); time.sleep(1)

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
        except KeyboardInterrupt:
            pass
        finally:
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)

            os.system('clear')
