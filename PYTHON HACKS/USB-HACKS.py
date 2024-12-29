import os
import subprocess
import psutil
import win32api
import win32file
from termcolor import colored
from datetime import datetime
from colorama import Fore

def clear_screen():
    """Effacer l'écran pour Windows."""
    os.system('cls')

def execute_devcon(command):
    """Exécuter une commande DevCon pour activer ou désactiver un périphérique."""
    try:
        subprocess.run(command, check=True, shell=True)
        print(colored(f"✅ Commande exécutée : {command}", 'green'))
    except subprocess.CalledProcessError as e:
        print(colored(f"❌ Erreur : Impossible d'exécuter la commande DevCon.", 'red'))

def afficher_peripheriques():
    clear_screen()
    print(colored("\n🔌 Affichage des informations des périphériques USB...", 'cyan'))
    print(colored("="*80, 'blue'))
    
    drives = win32api.GetLogicalDriveStrings().split('\000')[:-1]  # Liste des disques
    usb_devices_found = False

    for drive in drives:
        try:
            drive_type = win32file.GetDriveType(drive)
            if drive_type == 2:  # Vérifier si le lecteur est amovible (USB)
                usb_devices_found = True
                print(colored(f"\n🔑 Périphérique USB trouvé : {drive}", 'cyan'))
                print(colored("="*80, 'blue'))
                print(f"  Nom du périphérique      : {drive}")
                print(f"  Point de montage         : {drive}")
                
                for partition in psutil.disk_partitions():
                    if partition.device == drive:
                        print(f"  Type de système de fichiers : {partition.fstype}")
                
                device_id = drive
                print(f"  ID du périphérique USB   : {device_id}")
                print(f"  Statut du périphérique   : Amovible")
                
                usage = psutil.disk_usage(drive)
                total_space = usage.total / (1024**3)
                used_space = usage.used / (1024**3)
                free_space = usage.free / (1024**3)
                
                print(f"  Capacité totale          : {total_space:.2f} Go")
                print(f"  Capacité utilisée        : {used_space:.2f} Go")
                print(f"  Capacité libre           : {free_space:.2f} Go")
                
                if total_space < 32:
                    print(colored(f"  Type : Petite clé USB (moins de 32 Go)", 'cyan'))
                else:
                    print(colored(f"  Type : Grande clé USB ou disque dur portable", 'cyan'))
                
                # Vérification de la sécurité
                try:
                    # Vérifier si le périphérique est protégé par BitLocker (données chiffrées)
                    bitlocker_status = get_bitlocker_status(drive)
                    print(f"  Statut de sécurité : {bitlocker_status}")
                except Exception as e:
                    print(f"  Statut de sécurité : Non disponible (Erreur lors de la récupération).")
                
                print("-"*80)
        except Exception as e:
            print(colored(f"❌ Erreur : Impossible de récupérer le type du lecteur {drive}.", 'red'))
    
    if not usb_devices_found:
        print(colored("❌ Aucun périphérique USB trouvé.", 'red'))

    input("\n🔵 Press Enter to continue...")

def get_bitlocker_status(drive):
    """Vérifier si un lecteur est protégé par BitLocker."""
    command = f"manage-bde -status {drive}"
    result = subprocess.run(command, capture_output=True, text=True, shell=True)
    if "Fully decrypted" in result.stdout:
        return "Non chiffré"
    elif "Encryption in Progress" in result.stdout:
        return "Chiffrement en cours"
    elif "Fully encrypted" in result.stdout:
        return "Chiffré"
    else:
        return "Statut inconnu"

def details_peripherique():
    clear_screen()
    print(colored("\n🔍 Détails d'un périphérique spécifique...", 'cyan'))
    device_id = input("\n🔑 Entrez le nom du périphérique (ex: E:\\) : ")
    
    found = False
    devices = psutil.disk_partitions()

    for device in devices:
        if device.device == device_id:
            found = True
            print(colored(f"\n🔑 Détails du périphérique {device_id} :", 'cyan'))
            print(colored("="*80, 'blue'))
            print(f"  Nom du périphérique      : {device.device}")
            print(f"  Point de montage         : {device.mountpoint}")
            print(f"  Type de système de fichiers : {device.fstype}")
            print(f"  Options                  : {device.opts}")
            
            usage = psutil.disk_usage(device.device)
            total_space = usage.total / (1024**3)
            used_space = usage.used / (1024**3)
            free_space = usage.free / (1024**3)
            
            print(f"  Capacité totale          : {total_space:.2f} Go")
            print(f"  Capacité utilisée        : {used_space:.2f} Go")
            print(f"  Capacité libre           : {free_space:.2f} Go")
            
            # Statut de sécurité
            try:
                bitlocker_status = get_bitlocker_status(device.device)
                print(f"  Statut de sécurité : {bitlocker_status}")
            except Exception as e:
                print(f"  Statut de sécurité : Non disponible (Erreur lors de la récupération).")
            
            print("-"*80)
            break
    
    if not found:
        print(colored(f"❌ Erreur : Aucun périphérique trouvé avec le nom '{device_id}'.", 'red'))
    
    input("\n🔵 Press Enter to continue...")

def activer_desactiver_usb():
    clear_screen()
    print(colored("\n🔌 Activation/Désactivation d'un périphérique USB...", 'cyan'))
    device_id = input("🔑 Entrez le nom du périphérique (ex: E:\\) : ")
    
    action = input("⚡ Souhaitez-vous activer ou désactiver ce périphérique ? [1: Activer, 2: Désactiver] : ")
    
    # Vérifier que l'option choisie est valide
    if action not in ["1", "2"]:
        print(colored("❌ Erreur : Option invalide, veuillez choisir 1 ou 2.", 'red'))
        return

    # Trouver l'ID du périphérique (doit correspondre au format du périphérique dans DevCon)
    devcon_command = f"devcon find *{device_id}*"
    result = subprocess.run(devcon_command, capture_output=True, text=True, shell=True)
    
    if result.returncode == 0:  # Si périphérique trouvé
        if action == "1":
            command = f"devcon enable *{device_id}*"
            print(colored(f"⚡ Activation du périphérique {device_id}...", 'green'))
        elif action == "2":
            command = f"devcon disable *{device_id}*"
            print(colored(f"⚡ Désactivation du périphérique {device_id}...", 'red'))

        execute_devcon(command)
    else:
        print(colored("❌ Erreur : Périphérique non trouvé.", 'red'))

    input("\n🔵 Press Enter to continue...")

def menu():
    while True:
        clear_screen()
        print(colored("="*50, 'cyan'))
        print(colored("   Menu Principal : Gestion des Périphériques USB", 'cyan'))
        print(colored("="*50, 'cyan'))
        print(Fore.CYAN + """
        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⣷⣄⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⣿⣅⣹⣿⣷⣄⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⣷⣄⠈⠳⣄⠙⢿⣿⣿⣏⢙⣿⠗⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⣿⣿⣿⣿⣷⣄⠙⢷⣄⠙⢿⣿⠟⠁⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⣿⣿⣿⣿⣿⣿⣿⣿⣷⣄⠙⠳⣄⠁⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⢀⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣄⡈⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⢀⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠀⠀⠀⠀⠀⠀ Made By Vaidx !
⠀⠀⠀⢀⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠁⠀⠀⠀⠀⠀⠀⠀
⠀⢀⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠁⠀⠀⠀⠀⠀Educational Purposes Only ! ⠀⠀⠀⠀
⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠙⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠙⢿⣿⣿⣿⣿⣿⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠉⠉⠉⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
""")
        print("\n[1] Afficher tous les périphériques USB")
        print("[2] Détails d'un périphérique spécifique")
        print("[3] Activer/Désactiver un périphérique USB")
        print("[4] Quitter")
        
        choix = input("\n🔹 Choisissez une option [1-4] : ")

        if choix == "1":
            afficher_peripheriques()
        elif choix == "2":
            details_peripherique()
        elif choix == "3":
            activer_desactiver_usb()
        elif choix == "4":
            print(colored("\n👋 Script terminé. Merci d'avoir utilisé cet outil !", 'cyan'))
            break
        else:
            print(colored("❌ Erreur : Option invalide, veuillez réessayer !", 'red'))

if __name__ == "__main__":
    menu()

