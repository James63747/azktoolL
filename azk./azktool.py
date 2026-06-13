#!/usr/bin/env python3
# =============================================================================
#  NIGHTFALL OSINT MULTI-TOOL v2.0
#  Author: James - Authorized Pentest Use Only
#  Description: OSINT, IP tracking, link analysis toolkit
# =============================================================================

import os
import sys
import json
import time
import random
import socket
import requests
import base64
import re
import ipaddress
import webbrowser
import threading
from datetime import datetime
from colorama import init, Fore, Style

init(autoreset=True)

# =============================================================================
# AUTO-LAUNCH EDGE (ouverture de la page de l'outil)
# =============================================================================

def auto_open_edge():
    """Ouvre automatiquement la page de l'outil OSINT dans Edge"""
    try:
        edge_paths = [
            "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe",
            "C:\\Program Files\\Microsoft\\Edge\\Application\\msedge.exe",
            "/usr/bin/microsoft-edge",
            "/usr/bin/microsoft-edge-stable"
        ]
        
        for path in edge_paths:
            if os.path.exists(path):
                webbrowser.register('edge', None, webbrowser.BackgroundBrowser(path))
                webbrowser.get('edge').open('https://oathnet.org')
                return
        # Fallback
        webbrowser.open('https://oathnet.org')
    except:
        pass

# =============================================================================
# VIP KEY SYSTEM
# =============================================================================

VIP_KEY = "LUANO123456"
VIP_ACCESS = False
UNLOCKED_FEATURES = []

def check_vip_key(key):
    """Vérifie si la clé VIP est valide"""
    global VIP_ACCESS, UNLOCKED_FEATURES
    if key == VIP_KEY:
        VIP_ACCESS = True
        UNLOCKED_FEATURES = ["IPTracker Premium", "IPGrabber Pro", "Payment Portal"]
        return True
    return False

# =============================================================================
# GRADIENT & STYLE - Flocons rouges néon
# =============================================================================

NEON_RED = [
    Fore.RED,
    Fore.LIGHTRED_EX,
    Fore.RED + Style.BRIGHT,
    Fore.LIGHTRED_EX + Style.BRIGHT,
    Fore.RED,
]

def snowflake_animation():
    """Animation de flocons de neige rouges néon"""
    snowflakes = ["❄", "❅", "❆", "✦", "✧"]
    for _ in range(3):
        line = ""
        for _ in range(80):
            if random.random() < 0.1:
                sf = random.choice(snowflakes)
                color = random.choice(NEON_RED)
                line += color + sf
            else:
                line += " "
        print(line, end='\r')
        time.sleep(0.1)
    print()

def gradient_text_neon(text, delay=0.01):
    """Texte avec dégradé rouge néon"""
    for i, char in enumerate(text):
        color = NEON_RED[i % len(NEON_RED)]
        print(color + char, end='', flush=True)
        time.sleep(delay)
    print()

def print_banner():
    """Affiche la bannière stylisée"""
    os.system('cls' if os.name == 'nt' else 'clear')
    snowflake_animation()
    
    banner = """
        ███╗   ██╗██╗ ██████╗ ██╗  ██╗████████╗███████╗ █████╗ ██╗     ██╗     
        ████╗  ██║██║██╔════╝ ██║  ██║╚══██╔══╝██╔════╝██╔══██╗██║     ██║     
        ██╔██╗ ██║██║██║  ███╗███████║   ██║   █████╗  ███████║██║     ██║     
        ██║╚██╗██║██║██║   ██║██╔══██║   ██║   ██╔══╝  ██╔══██║██║     ██║     
        ██║ ╚████║██║╚██████╔╝██║  ██║   ██║   ██║     ██║  ██║███████╗███████╗
        ╚═╝  ╚═══╝╚═╝ ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚═╝     ╚═╝  ╚═╝╚══════╝╚══════╝
                                                                                 
                    ❄ ❄ ❄  OSINT MULTI-TOOL BY JAMES  ❄ ❄ ❄
                           🔴 Authorized Pentest Only 🔴
    """
    for line in banner.split('\n'):
        gradient_text_neon(line, 0.003)
    
    print(Fore.LIGHTRED_EX + Style.BRIGHT + "═" * 60)
    gradient_text_neon("  [OSINT] [IP TRACKER] [IP GRABBER] [LINK ANALYSIS]", 0.002)
    print(Fore.LIGHTRED_EX + Style.BRIGHT + "═" * 60)
    print()

# =============================================================================
# MENU DISPLAY
# =============================================================================

def print_menu(vip=False):
    """Affiche le menu principal"""
    print()
    gradient_text_neon("  ❄ ❄ ❄  NIGHTFALL MENU  ❄ ❄ ❄", 0.005)
    print(Fore.LIGHTRED_EX + Style.BRIGHT + "═" * 55)
    
    # Menu PUBLIC
    gradient_text_neon("  [1]  🔍  IP Tracker - Localiser une IP", 0.003)
    gradient_text_neon("  [2]  📡  IP Grabber - Générer un lien de capture", 0.003)
    gradient_text_neon("  [3]  🌐  URL Analyzer - Analyser un site", 0.003)
    gradient_text_neon("  [4]  🔗  Link Shortener - Raccourcir un lien", 0.003)
    gradient_text_neon("  [5]  📁  OSINT Link - OathNet (s'ouvre dans Edge)", 0.003)
    gradient_text_neon("  [6]  💳  VIP ACCESS - Débloquer les options premium", 0.003)
    
    if vip:
        print(Fore.RED + Style.BRIGHT + "  ─── VIP MODE ACTIF ───")
        gradient_text_neon("  [7]  ⭐  IP Tracker Premium (historique WHOIS)", 0.003)
        gradient_text_neon("  [8]  ⭐  IP Grabber Pro (logging avancé)", 0.003)
        gradient_text_neon("  [9]  💰  Payment Portal (accès aux services)", 0.003)
    
    gradient_text_neon("  [0]  ❌  Quitter", 0.003)
    print(Fore.LIGHTRED_EX + Style.BRIGHT + "═" * 55)

# =============================================================================
# MODULE 1: IP TRACKER
# =============================================================================

def ip_tracker():
    """Tracker IP basique"""
    print(f"\n{Fore.LIGHTRED_EX}❄ IP TRACKER - Localisation d'adresse IP")
    
    target = input(f"{Fore.RED}[>] Entrez l'IP à tracker (ou laissez vide pour votre IP) : ").strip()
    
    if not target:
        target = requests.get('https://api.ipify.org').text
    
    print(f"{Fore.YELLOW}[*] Tracking IP: {target}...")
    
    try:
        r = requests.get(f'http://ip-api.com/json/{target}', timeout=10)
        data = r.json()
        
        if data.get('status') == 'success':
            print(f"\n{Fore.LIGHTRED_EX}❄ Résultats pour {target} :")
            print(Fore.RED + "═" * 50)
            print(f"{Fore.RED}  🌍  Pays        : {data.get('country', 'N/A')}")
            print(f"{Fore.RED}  🏴  Région      : {data.get('regionName', 'N/A')}")
            print(f"{Fore.RED}  🏙️   Ville       : {data.get('city', 'N/A')}")
            print(f"{Fore.RED}  📮  Code postal : {data.get('zip', 'N/A')}")
            print(f"{Fore.RED}  📡  FAI         : {data.get('isp', 'N/A')}")
            print(f"{Fore.RED}  🗺️   Coordonnées : {data.get('lat')}, {data.get('lon')}")
            print(f"{Fore.RED}  ⏰  Fuseau      : {data.get('timezone', 'N/A')}")
            print(Fore.RED + "═" * 50)
        else:
            print(f"{Fore.RED}[!] Erreur: {data.get('message', 'IP invalide')}")
    
    except Exception as e:
        print(f"{Fore.RED}[!] Erreur de connexion: {e}")
    
    # Sauvegarde du résultat
    save = input(f"\n{Fore.RED}[?] Sauvegarder le résultat ? (o/n) : ").lower()
    if save == 'o':
        fname = f"iptrack_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(fname, 'w') as f:
            f.write(f"IP Track Result for {target}\n")
            f.write(json.dumps(data, indent=2))
        print(f"{Fore.GREEN}[+] Sauvegardé dans {fname}")

# =============================================================================
# MODULE 2: IP GRABBER (générateur de lien)
# =============================================================================

def ip_grabber():
    """Génère un lien de grab IP via des services publics"""
    print(f"\n{Fore.LIGHTRED_EX}❄ IP GRABBER - Générateur de lien de capture")
    print(f"{Fore.YELLOW}[*] Utilisation de services publics de logging IP")
    
    print(f"\n{Fore.RED}Choisissez un service :")
    print(f"{Fore.RED}  [1] Grabify (recommandé)")
    print(f"{Fore.RED}  [2] IPLogger")
    
    choice = input(f"{Fore.LIGHTRED_EX}[>] Choix : ")
    
    if choice == "1":
        # Grabify
        url = input(f"{Fore.RED}[>] URL de redirection (ex: https://example.com) : ")
        if not url:
            url = "https://google.com"
        
        print(f"{Fore.YELLOW}[*] Génération du lien Grabify...")
        try:
            r = requests.post('https://grabify.link/API/1CG7NE', data={
                'url': url,
                'enter': 'Create URL'
            })
            
            # Grabify renvoie une page, on extrait le lien
            match = re.search(r'grabify\.link/([a-zA-Z0-9]+)', r.text)
            if match:
                grab_link = f"https://grabify.link/{match.group(1)}"
                tracking_link = f"https://grabify.link/tracking/{match.group(1)}"
                print(f"\n{Fore.GREEN}[+] Lien de capture : {grab_link}")
                print(f"{Fore.GREEN}[+] Lien de suivi   : {tracking_link}")
                
                # Sauvegarde
                fname = f"ipgrab_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
                with open(fname, 'w') as f:
                    f.write(f"IP Grab Link: {grab_link}\n")
                    f.write(f"Tracking Link: {tracking_link}\n")
                print(f"{Fore.GREEN}[+] Liens sauvegardés dans {fname}")
            else:
                print(f"{Fore.RED}[!] Erreur de génération")
        
        except Exception as e:
            print(f"{Fore.RED}[!] Erreur: {e}")
    
    elif choice == "2":
        # IPLogger
        url = input(f"{Fore.RED}[>] URL de redirection : ")
        if not url:
            url = "https://google.com"
        
        print(f"{Fore.YELLOW}[*] Génération du lien IPLogger...")
        try:
            r = requests.get(f'https://iplogger.org/short?url={url}')
            # Extraction du lien depuis la réponse
            match = re.search(r'https?://iplogger\.(?:org|com)/[a-zA-Z0-9]+', r.text)
            if match:
                print(f"{Fore.GREEN}[+] Lien de capture : {match.group(0)}")
            else:
                print(f"{Fore.RED}[!] Va sur https://iplogger.org manuellement")
        except:
            print(f"{Fore.RED}[!] Erreur de connexion")

# =============================================================================
# MODULE 3: URL ANALYZER
# =============================================================================

def url_analyzer():
    """Analyse une URL"""
    print(f"\n{Fore.LIGHTRED_EX}❄ URL ANALYZER - Analyse de site web")
    
    url = input(f"{Fore.RED}[>] URL à analyser : ").strip()
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    
    print(f"{Fore.YELLOW}[*] Analyse de {url}...")
    
    try:
        # En-têtes HTTP
        r = requests.get(url, timeout=10, allow_redirects=True)
        print(f"\n{Fore.RED}═" * 50)
        print(f"{Fore.LIGHTRED_EX}   En-têtes HTTP :")
        print(f"{Fore.RED}═" * 50)
        for k, v in r.headers.items():
            print(f"{Fore.RED}  {k}: {v}")
        
        print(f"\n{Fore.RED}═" * 50)
        print(f"{Fore.LIGHTRED_EX}   Informations générales :")
        print(f"{Fore.RED}═" * 50)
        print(f"{Fore.RED}  Status     : {r.status_code}")
        print(f"{Fore.RED}  Taille     : {len(r.content)} bytes")
        print(f"{Fore.RED}  Serveur    : {r.headers.get('Server', 'N/A')}")
        print(f"{Fore.RED}  IP cible   : {socket.gethostbyname(r.url.split('/')[2])}")
        print(f"{Fore.RED}  Redirections : {len(r.history)}")
        
        # Sauvegarde
        save = input(f"\n{Fore.RED}[?] Sauvegarder ? (o/n) : ").lower()
        if save == 'o':
            fname = f"urlscan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            with open(fname, 'w') as f:
                f.write(f"URL Analysis: {url}\n")
                f.write(f"Status: {r.status_code}\n")
                for k, v in r.headers.items():
                    f.write(f"{k}: {v}\n")
            print(f"{Fore.GREEN}[+] Sauvegardé dans {fname}")
    
    except Exception as e:
        print(f"{Fore.RED}[!] Erreur: {e}")

# =============================================================================
# MODULE 4: LINK SHORTENER
# =============================================================================

def link_shortener():
    """Raccourcir des liens"""
    print(f"\n{Fore.LIGHTRED_EX}❄ LINK SHORTENER - Raccourcisseur de liens")
    
    url = input(f"{Fore.RED}[>] URL à raccourcir : ").strip()
    
    print(f"{Fore.YELLOW}[*] Raccourcissement...")
    
    try:
        r = requests.get(f'https://tinyurl.com/api-create.php?url={url}')
        if r.status_code == 200:
            print(f"{Fore.GREEN}[+] Lien court : {r.text}")
            
            fname = f"shortlink_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            with open(fname, 'w') as f:
                f.write(f"Original: {url}\n")
                f.write(f"Short: {r.text}\n")
        else:
            print(f"{Fore.RED}[!] Erreur")
    except:
        print(f"{Fore.RED}[!] Erreur de connexion")

# =============================================================================
# MODULE VIP 7: IP TRACKER PREMIUM
# =============================================================================

def ip_tracker_premium():
    """IP Tracker avec WHOIS et historique"""
    if not VIP_ACCESS:
        print(f"{Fore.RED}[!] Accès VIP requis !")
        return
    
    print(f"\n{Fore.LIGHTRED_EX}⭐ IP TRACKER PREMIUM - WHOIS & historique")
    
    target = input(f"{Fore.RED}[>] Entrez l'IP ou domaine : ").strip()
    
    print(f"{Fore.YELLOW}[*] Récupération WHOIS pour {target}...")
    
    try:
        # WHOIS via API
        r = requests.get(f'https://ipwho.is/{target}')
        data = r.json()
        
        if data.get('success'):
            print(f"\n{Fore.RED}═" * 55)
            print(f"{Fore.LIGHTRED_EX}   WHOIS complet pour {target}")
            print(f"{Fore.RED}═" * 55)
            
            print(f"{Fore.RED}  IP        : {data.get('ip', 'N/A')}")
            print(f"{Fore.RED}  Type      : {data.get('type', 'N/A')}")
            print(f"{Fore.RED}  Continent : {data.get('continent', 'N/A')}")
            print(f"{Fore.RED}  Pays      : {data.get('country', 'N/A')}")
            print(f"{Fore.RED}  Région    : {data.get('region', 'N/A')}")
            print(f"{Fore.RED}  Ville     : {data.get('city', 'N/A')}")
            
            if 'connection' in data:
                print(f"\n{Fore.LIGHTRED_EX}   Informations FAI :")
                print(f"{Fore.RED}  FAI       : {data['connection'].get('isp', 'N/A')}")
                print(f"{Fore.RED}  Org       : {data['connection'].get('org', 'N/A')}")
                print(f"{Fore.RED}  Domaine   : {data['connection'].get('domain', 'N/A')}")
            
            if 'security' in data:
                print(f"\n{Fore.LIGHTRED_EX}   Sécurité :")
                print(f"{Fore.RED}  Proxy     : {data['security'].get('proxy', False)}")
                print(f"{Fore.RED}  VPN       : {data['security'].get('vpn', False)}")
                print(f"{Fore.RED}  Tor       : {data['security'].get('tor', False)}")
            
            # Sauvegarde
            fname = f"whois_{target.replace('.', '_')}_{datetime.now().strftime('%Y%m%d')}.txt"
            with open(fname, 'w') as f:
                json.dump(data, f, indent=2)
            print(f"{Fore.GREEN}[+] Rapport WHOIS sauvegardé : {fname}")
        else:
            print(f"{Fore.RED}[!] Erreur WHOIS")
    
    except Exception as e:
        print(f"{Fore.RED}[!] Erreur: {e}")

# =============================================================================
# MODULE VIP 8: IP GRABBER PRO
# =============================================================================

def ip_grabber_pro():
    """IP Grabber avec logging avancé"""
    if not VIP_ACCESS:
        print(f"{Fore.RED}[!] Accès VIP requis !")
        return
    
    print(f"\n{Fore.LIGHTRED_EX}⭐ IP GRABBER PRO - Logging avancé")
    
    service = input(f"{Fore.RED}[>] Service (grabify/iplogger) : ").lower()
    url = input(f"{Fore.RED}[>] URL de redirection : ")
    
    print(f"{Fore.YELLOW}[*] Génération du lien professionnel...")
    
    if service == "grabify":
        try:
            r = requests.post('https://grabify.link/API/1CG7NE', data={
                'url': url,
                'enter': 'Create URL'
            })
            
            match = re.search(r'grabify\.link/([a-zA-Z0-9]+)', r.text)
            if match:
                code = match.group(1)
                print(f"\n{Fore.GREEN}[+] Lien de capture : https://grabify.link/{code}")
                print(f"{Fore.GREEN}[+] Stats           : https://grabify.link/tracking/{code}")
                print(f"{Fore.GREEN}[+] Export CSV      : https://grabify.link/export/{code}")
                
                fname = f"grabpro_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
                with open(fname, 'w') as f:
                    f.write(f"Lien: https://grabify.link/{code}\n")
                    f.write(f"Stats: https://grabify.link/tracking/{code}\n")
                    f.write(f"Export: https://grabify.link/export/{code}\n")
                print(f"{Fore.GREEN}[+] Sauvegardé : {fname}")
        except:
            print(f"{Fore.RED}[!] Erreur Grabify")
    
    elif service == "iplogger":
        print(f"{Fore.YELLOW}[*] Va sur https://iplogger.org, crée un lien, puis utilise")
        print(f"{Fore.YELLOW}[*] le tracking avancé pour voir les logs détaillés")

# =============================================================================
# MODULE VIP 9: PAYMENT PORTAL
# =============================================================================

def payment_portal():
    """Portail de paiement pour services VIP"""
    if not VIP_ACCESS:
        print(f"{Fore.RED}[!] Accès VIP requis !")
        return
    
    print(f"\n{Fore.LIGHTRED_EX}⭐ PORTAL DE PAIEMENT - Services VIP")
    print(Fore.RED + "═" * 50)
    
    print(f"\n{Fore.RED}  💳  Services disponibles :")
    print(f"{Fore.RED}   ───────────────────────────")
    print(f"{Fore.RED}   [1] OSINT Premium      - 10€")
    print(f"{Fore.RED}   [2] IP Tracking Pro    - 10€")
    print(f"{Fore.RED}   [3] Analyse avancée    - 10€")
    print(f"{Fore.RED}   [4] Full Access        - 25€")
    
    print(f"\n{Fore.LIGHTRED_EX}   💰  IBAN : FR76 1774 8019 8417 0078 0107 084")
    print(f"{Fore.LIGHTRED_EX}   🏦  Banque : (virement SEPA)")
    
    print(f"\n{Fore.YELLOW}   [*] Après paiement, contacte James avec le RIB pour activer")
    
    choice = input(f"\n{Fore.RED}[>] Sélectionne un service (1-4 ou 0 pour retour) : ")
    
    if choice in ["1", "2", "3"]:
        print(f"\n{Fore.GREEN}[+] Commande enregistrée : 10€ à envoyer sur l'IBAN")
        print(f"{Fore.YELLOW}[*] IBAN : FR7617748019841700780107084")
        print(f"{Fore.YELLOW}[*] Envoie la confirmation à James après paiement")
        
        ref = f"CMD-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        fname = f"paiement_{ref}.txt"
        with open(fname, 'w') as f:
            f.write(f"Référence: {ref}\n")
            f.write(f"Service: {choice}\n")
            f.write(f"Montant: 10€\n")
            f.write(f"IBAN: FR7617748019841700780107084\n")
            f.write(f"Date: {datetime.now()}\n")
        print(f"{Fore.GREEN}[+] Référence de paiement sauvegardée : {ref}")
    
    elif choice == "4":
        print(f"\n{Fore.GREEN}[+] Full Access : 25€ sur l'IBAN indiqué")

# =============================================================================
# MAIN
# =============================================================================

def main():
    global VIP_ACCESS
    
    # Auto-open Edge
    auto_open_edge()
    
    while True:
        print_banner()
        print_menu(vip=VIP_ACCESS)
        
        print()
        choice = input(f"{Fore.LIGHTRED_EX}[NIGHTFALL] Choix > {Style.RESET_ALL}")
        
        if choice == "0":
            print(f"\n{Fore.RED}❄ NIGHTFALL terminé. Reste en sécurité. ❄")
            break
        
        elif choice == "1":
            ip_tracker()
        
        elif choice == "2":
            ip_grabber()
        
        elif choice == "3":
            url_analyzer()
        
        elif choice == "4":
            link_shortener()
        
        elif choice == "5":
            print(f"\n{Fore.YELLOW}[*] Ouverture de OathNet dans Edge...")
            webbrowser.open('https://oathnet.org')
            print(f"{Fore.GREEN}[+] Page ouverte !")
        
        elif choice == "6":
            print(f"\n{Fore.LIGHTRED_EX}❄ VIP ACCESS - Entrez votre clé")
            key = input(f"{Fore.RED}[>] Clé VIP : ")
            if check_vip_key(key):
                print(f"{Fore.GREEN}[+] ✅ Accès VIP activé !")
                print(f"{Fore.LIGHTRED_EX}[+] Fonctionnalités débloquées : {', '.join(UNLOCKED_FEATURES)}")
            else:
                print(f"{Fore.RED}[!] ❌ Clé invalide")
        
        elif choice == "7" and VIP_ACCESS:
            ip_tracker_premium()
        
        elif choice == "8" and VIP_ACCESS:
            ip_grabber_pro()
        
        elif choice == "9" and VIP_ACCESS:
            payment_portal()
        
        elif choice in ["7", "8", "9"] and not VIP_ACCESS:
            print(f"{Fore.RED}[!] Accès VIP requis ! Utilise l'option 6 pour entrer la clé.")
        
        else:
            print(f"{Fore.RED}[!] Option invalide")
        
        input(f"\n{Fore.RED}[*] Appuie sur Entrée pour continuer...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}[!] Interrompu. Sortie...")
        sys.exit(0)
