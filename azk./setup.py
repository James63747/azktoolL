#!/usr/bin/env python3
# =============================================================================
# setup.py - Install all dependencies for JAMES MULTI-TOOL
# =============================================================================

import subprocess
import sys
import os
import platform

# Liste de tous les modules nécessaires
REQUIRED_PACKAGES = [
    "requests",
    "colorama",
    "psutil",
]

# Modules de la bibliothèque standard (déjà inclus avec Python)
STDLIB_MODULES = [
    "os", "sys", "json", "time", "random", "socket", "threading",
    "base64", "subprocess", "platform", "datetime", "sqlite3",
    "re", "shutil", "webbrowser"
]

# Couleurs pour l'affichage (sans colorama pour le setup)
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    CYAN = '\033[96m'
    MAGENTA = '\033[95m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def print_banner():
    """Affiche une bannière stylée"""
    os.system('cls' if os.name == 'nt' else 'clear')
    banner = f"""
{Colors.MAGENTA}{Colors.BOLD}
        ██╗ █████╗ ███╗   ███╗███████╗███████╗
        ██║██╔══██╗████╗ ████║██╔════╝██╔════╝
        ██║███████║██╔████╔██║███████╗███████╗
        ██║██╔══██║██║╚██╔╝██║╚════██║╚════██║
        ██║██║  ██║██║ ╚═╝ ██║███████║███████║
        ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝╚══════╝
{Colors.RESET}
{Colors.CYAN}╔══════════════════════════════════════════╗
║         DEPENDENCY INSTALLER v1.0         ║
║   Automatic setup for JAMES MULTI-TOOL    ║
╚══════════════════════════════════════════╝{Colors.RESET}
"""
    print(banner)

def check_python_version():
    """Vérifie que Python est en version 3.6+"""
    print(f"{Colors.YELLOW}[*] Checking Python version...{Colors.RESET}")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 6):
        print(f"{Colors.RED}[!] Python 3.6+ required. You have {version.major}.{version.minor}.{version.micro}{Colors.RESET}")
        print(f"{Colors.RED}[!] Please upgrade Python: https://www.python.org/downloads/{Colors.RESET}")
        return False
    print(f"{Colors.GREEN}[✓] Python {version.major}.{version.minor}.{version.micro} detected{Colors.RESET}")
    return True

def check_pip():
    """Vérifie si pip est installé"""
    print(f"{Colors.YELLOW}[*] Checking pip...{Colors.RESET}")
    try:
        subprocess.run([sys.executable, "-m", "pip", "--version"], 
                      capture_output=True, check=True)
        print(f"{Colors.GREEN}[✓] pip is installed{Colors.RESET}")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print(f"{Colors.RED}[!] pip is not installed{Colors.RESET}")
        print(f"{Colors.YELLOW}[*] Installing pip...{Colors.RESET}")
        try:
            subprocess.run([sys.executable, "-m", "ensurepip", "--upgrade"], check=True)
            print(f"{Colors.GREEN}[✓] pip installed successfully{Colors.RESET}")
            return True
        except:
            print(f"{Colors.RED}[!] Failed to install pip manually{Colors.RESET}")
            print(f"{Colors.YELLOW}[*] Please install pip: https://pip.pypa.io/en/stable/installation/{Colors.RESET}")
            return False

def install_package(package):
    """Installe un package pip"""
    try:
        print(f"{Colors.YELLOW}  → Installing {package}...{Colors.RESET}", end=" ")
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", package, "--quiet"],
            capture_output=True,
            text=True,
            timeout=60
        )
        if result.returncode == 0:
            print(f"{Colors.GREEN}[✓]{Colors.RESET}")
            return True
        else:
            print(f"{Colors.RED}[✗]{Colors.RESET}")
            print(f"    Error: {result.stderr.strip()}")
            return False
    except subprocess.TimeoutExpired:
        print(f"{Colors.RED}[✗] Timeout{Colors.RESET}")
        return False
    except Exception as e:
        print(f"{Colors.RED}[✗] {str(e)}{Colors.RESET}")
        return False

def update_pip():
    """Met à jour pip"""
    print(f"{Colors.YELLOW}[*] Updating pip to latest version...{Colors.RESET}")
    try:
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "--upgrade", "pip", "--quiet"],
            capture_output=True,
            timeout=30
        )
        print(f"{Colors.GREEN}[✓] pip updated{Colors.RESET}")
    except:
        print(f"{Colors.YELLOW}[!] Could not update pip (non-critical){Colors.RESET}")

def install_all():
    """Installe tous les packages requis"""
    print(f"\n{Colors.CYAN}{Colors.BOLD}[*] Installing required packages...{Colors.RESET}\n")
    
    success_count = 0
    fail_count = 0
    
    for package in REQUIRED_PACKAGES:
        if install_package(package):
            success_count += 1
        else:
            fail_count += 1
    
    print(f"\n{Colors.CYAN}{'='*50}{Colors.RESET}")
    if fail_count == 0:
        print(f"{Colors.GREEN}{Colors.BOLD}[✓] All {success_count} packages installed successfully!{Colors.RESET}")
    else:
        print(f"{Colors.YELLOW}[!] {success_count} installed, {fail_count} failed{Colors.RESET}")
        print(f"{Colors.YELLOW}[!] You can install them manually with:{Colors.RESET}")
        print(f"{Colors.CYAN}    pip install {' '.join(REQUIRED_PACKAGES)}{Colors.RESET}")
    print(f"{Colors.CYAN}{'='*50}{Colors.RESET}")

def verify_installation():
    """Vérifie que tous les modules importent correctement"""
    print(f"\n{Colors.CYAN}{Colors.BOLD}[*] Verifying installation...{Colors.RESET}\n")
    
    all_modules = STDLIB_MODULES + [pkg.replace("-", "_") for pkg in REQUIRED_PACKAGES]
    all_ok = True
    
    for module_name in all_modules:
        try:
            if module_name == "sqlite3":
                import sqlite3
            elif module_name == "shutil":
                import shutil
            else:
                __import__(module_name)
            print(f"{Colors.GREEN}  [✓] {module_name}{Colors.RESET}")
        except ImportError:
            print(f"{Colors.RED}  [✗] {module_name} - MISSING{Colors.RESET}")
            all_ok = False
    
    print()
    if all_ok:
        print(f"{Colors.GREEN}{Colors.BOLD}[✓] All dependencies verified! You can now run James Multi-Tool.{Colors.RESET}")
        return True
    else:
        print(f"{Colors.RED}{Colors.BOLD}[!] Some modules are missing. Check the errors above.{Colors.RESET}")
        return False

def create_run_script():
    """Crée un script de lancement pratique"""
    script_name = "run_james.bat" if platform.system() == "Windows" else "run_james.sh"
    script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), script_name)
    
    if platform.system() == "Windows":
        content = """@echo off
echo [*] Checking if setup was already done...
python -c "import requests, colorama, psutil" 2>nul
if %errorlevel% neq 0 (
    echo [*] Running setup first...
    python setup.py
)
echo.
echo [*] Launching James Multi-Tool...
python james_multi_tool.py
pause
"""
    else:
        content = """#!/bin/bash
echo "[*] Checking if setup was already done..."
python3 -c "import requests, colorama, psutil" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "[*] Running setup first..."
    python3 setup.py
fi
echo ""
echo "[*] Launching James Multi-Tool..."
python3 james_multi_tool.py
"""
    
    with open(script_path, "w") as f:
        f.write(content)
    
    # Rendre exécutable sur Linux/Mac
    if platform.system() != "Windows":
        os.chmod(script_path, 0o755)
    
    print(f"{Colors.GREEN}[✓] Run script created: {script_name}{Colors.RESET}")

def main():
    """Fonction principale du setup"""
    print_banner()
    
    print(f"{Colors.CYAN}{Colors.BOLD}[*] System: {platform.system()} {platform.release()}{Colors.RESET}")
    print(f"{Colors.CYAN}[*] Architecture: {platform.machine()}{Colors.RESET}\n")
    
    # Étape 1: Vérifier Python
    if not check_python_version():
        input(f"\n{Colors.YELLOW}Press Enter to exit...{Colors.RESET}")
        sys.exit(1)
    
    # Étape 2: Vérifier pip
    if not check_pip():
        input(f"\n{Colors.YELLOW}Press Enter to exit...{Colors.RESET}")
        sys.exit(1)
    
    # Étape 3: Mettre à jour pip
    update_pip()
    
    # Étape 4: Installer les packages
    install_all()
    
    # Étape 5: Vérifier l'installation
    verify_installation()
    
    # Étape 6: Créer le script de lancement
    print(f"{Colors.CYAN}[*] Creating run script...{Colors.RESET}")
    create_run_script()
    
    # Résumé final
    print(f"\n{Colors.CYAN}{'='*50}{Colors.RESET}")
    print(f"{Colors.GREEN}{Colors.BOLD}  ✅ SETUP COMPLETE!{Colors.RESET}")
    print(f"{Colors.GREEN}  You can now run James Multi-Tool with:{Colors.RESET}")
    if platform.system() == "Windows":
        print(f"{Colors.CYAN}    > run_james.bat{Colors.RESET}")
        print(f"{Colors.CYAN}    > python james_multi_tool.py{Colors.RESET}")
    else:
        print(f"{Colors.CYAN}    $ ./run_james.sh{Colors.RESET}")
        print(f"{Colors.CYAN}    $ python3 james_multi_tool.py{Colors.RESET}")
    print(f"{Colors.CYAN}{'='*50}{Colors.RESET}")
    
    # Demander si on veut lancer directement
    print()
    choice = input(f"{Colors.YELLOW}Launch James Multi-Tool now? (y/n): {Colors.RESET}").lower()
    if choice == "y":
        print(f"\n{Colors.GREEN}[+] Launching...{Colors.RESET}")
        script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "james_multi_tool.py")
        if os.path.exists(script_path):
            os.system(f'{sys.executable} "{script_path}"')
        else:
            print(f"{Colors.RED}[!] james_multi_tool.py not found in current directory{Colors.RESET}")
            print(f"{Colors.YELLOW}[*] Make sure the main script is in the same folder as setup.py{Colors.RESET}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.RED}[!] Setup interrupted by user{Colors.RESET}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{Colors.RED}[!] Unexpected error: {e}{Colors.RESET}")
        sys.exit(1)
