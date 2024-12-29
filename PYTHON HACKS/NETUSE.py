import os
import time
from colorama import Fore, Style, init
import signal

# Initialiser colorama
init(autoreset=True)

# Fonction pour nettoyer la console
def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

# Fonction pour exécuter une commande shell
def run_command(command):
    result = os.popen(command).read()
    return result.strip()

# Fonction pour ajouter une connexion réseau
def add_network_connection(drive_letter, network_path, username=None, password=None):
    print(Fore.YELLOW + f"Ajout de la connexion vers {network_path} sur le lecteur {drive_letter}...")
    command = f'net use {drive_letter}: {network_path}'
    if username and password:
        command += f' {password} /user:{username}'
    command += ' /persistent:yes'
    output = run_command(command)
    if "erreur" in output.lower() or "error" in output.lower():
        print(Fore.RED + "❌ Erreur lors de l'ajout de la connexion :")
        print(Fore.RED + output)
    else:
        print(Fore.GREEN + "✅ Connexion ajoutée avec succès!")

# Fonction pour lister les connexions réseau
def list_network_connections():
    print(Fore.YELLOW + "\nListe des connexions réseau existantes:")
    output = run_command('net use')
    if "Il n'y a aucune" in output or not output:
        print(Fore.RED + "⚠ Aucune connexion réseau existante.")
    else:
        print(Fore.CYAN + output)

# Fonction pour supprimer une connexion réseau
def delete_network_connection(drive_letter):
    print(Fore.YELLOW + f"Suppression de la connexion sur le lecteur {drive_letter}...")
    output = run_command(f'net use {drive_letter}: /delete /yes')
    if "succès" in output.lower() or "success" in output.lower():
        print(Fore.GREEN + "✅ Connexion supprimée avec succès!")
    else:
        print(Fore.RED + "❌ Erreur lors de la suppression de la connexion :")
        print(Fore.RED + output)

# Fonction pour confirmer la sortie (CTRL+C)
def confirm_exit(connections_made):
    print(Fore.YELLOW + "\n\nVoulez-vous vraiment quitter ? (O/N)")
    choice = input().strip().lower()
    if choice == 'o':
        print(Fore.CYAN + f"\nRésumé : {connections_made} connexion(s) gérée(s).")
        print(Fore.RED + "Fermeture du programme dans 5 secondes...")
        time.sleep(5)
        exit()
    else:
        print(Fore.GREEN + "Reprise du programme...")

# Message d'avertissement
def disclaimer():
    clear_console()
    print(Fore.RED + "==================== Avertissement ================================")
    print(Fore.YELLOW + "Ce programme gère les connexions réseau via la commande 'net use'.")
    print(Fore.YELLOW + "Veuillez utiliser ce programme de manière responsable.")
    print(Fore.RED + "===================================================================")
    time.sleep(5)

# Menu principal
def main_menu(target_set, username_set, password_set):
    clear_console()
    print(Fore.BLUE + """
 __   __  ______ ______     __  __  ______  ______    
/\ "-.\ \/\  ___/\__  _\   /\ \/\ \/\  ___\/\  ___\   
\ \ \-.  \ \  __\/_/\ \/   \ \ \_\ \ \___  \ \  __\    Made By Vaidx ! 
 \ \_\\"\_\ \_____\\ \_\    \ \_____\/\_____\ \_____\ 
  \/_/ \/_/\/_____/ \/_/     \/_____/\/_____/\/_____/ 
                                                      
""")
    print(Fore.CYAN + "\n==================== Menu Principal ===================")
    print(Fore.CYAN + f"1. Ajouter une connexion réseau {'(' + Fore.GREEN + 'SET' + Fore.CYAN + ')' if target_set else ''}")
    print(Fore.CYAN + f"2. Lister les connexions réseau")
    print(Fore.CYAN + f"3. Supprimer une connexion réseau")
    print(Fore.CYAN + "4. Quitter")

# Gestionnaire d'interruption (CTRL+C)
connections_made = 0
def signal_handler(sig, frame):
    confirm_exit(connections_made)

signal.signal(signal.SIGINT, signal_handler)

# Programme principal
if __name__ == "__main__":
    disclaimer()
    target_set = False
    username_set = False
    password_set = False
    
    while True:
        main_menu(target_set, username_set, password_set)
        choice = input(Fore.CYAN + "\nChoisissez une option (1-4) : ")
        
        if choice == '1':
            drive_letter = input(Fore.CYAN + "Entrez la lettre du lecteur (ex: Z) : ").upper()
            network_path = input(Fore.CYAN + "Entrez le chemin réseau (ex: \\\\serveur\\partage) : ")
            use_auth = input(Fore.CYAN + "Voulez-vous ajouter un identifiant/mot de passe ? (O/N) : ").strip().lower()
            username, password = None, None
            if use_auth == 'o':
                username = input(Fore.CYAN + "Entrez le nom d'utilisateur : ")
                password = input(Fore.CYAN + "Entrez le mot de passe : ")
                username_set, password_set = True, True
            
            add_network_connection(drive_letter, network_path, username, password)
            connections_made += 1
            target_set = True
            time.sleep(2)

        elif choice == '2':
            list_network_connections()
            time.sleep(2)

        elif choice == '3':
            drive_letter = input(Fore.CYAN + "Entrez la lettre du lecteur à supprimer (ex: Z) : ").upper()
            delete_network_connection(drive_letter)
            connections_made += 1
            time.sleep(2)

        elif choice == '4':
            confirm_exit(connections_made)
        else:
            print(Fore.RED + "Option invalide, veuillez réessayer.")
            time.sleep(1)
