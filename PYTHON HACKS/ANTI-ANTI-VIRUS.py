import os
import sys
import time
import base64
import zipfile
from tkinter import filedialog
from tkinter import Tk

# Définir les couleurs
CYAN = '\033[96m'
BLUE = '\033[94m'
RESET = '\033[0m'
RED = '\033[91m'
BOLD = '\033[1m'

# Cadenas ASCII Art
LOCK_ART = r"""
            .-""-.
           / .--. \
          / /    \ \
          | |    | |
          | |.-""-.|
         ///`.::::.`\
        ||| ::/  \:: ;
        ||; ::\__/:: ;
         \\\ '::::' /
          `=':-..-'`⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
"""

def clear_screen():
    """Efface l'écran du terminal."""
    os.system('cls' if os.name == 'nt' else 'clear')

def xor_obfuscate(data, key=123):
    """Applique une obfuscation XOR sur les données."""
    return bytes([b ^ key for b in data])

def obfuscate_file(file_path, output_path, key=123):
    """Obfusque un fichier en utilisant l'obfuscation XOR."""
    try:
        with open(file_path, 'rb') as f:
            file_data = f.read()
        obfuscated_data = xor_obfuscate(file_data, key)
        with open(output_path, 'wb') as f:
            f.write(obfuscated_data)
        print(f"{CYAN}[INFO]{RESET} Fichier obfusqué et sauvegardé sous '{output_path}'.\n")
    except Exception as e:
        print(f"{RED}[ERREUR]{RESET} Une erreur s'est produite : {str(e)}\n")

def detect_file_type(file_path):
    """Détecte le type d'un fichier."""
    try:
        with open(file_path, 'rb') as f:
            data = f.read()
        # Base64
        try:
            decoded = base64.b64decode(data, validate=True)
            if base64.b64encode(decoded) == data:
                return "Base64"
        except:
            pass
        # PowerShell
        if data.startswith(b"#"):
            return "Script PowerShell (PS1)"
        # ZIP
        if zipfile.is_zipfile(file_path):
            return "Archive ZIP"
        # EXE
        if data[:2] == b"MZ":
            return "Exécutable Windows (EXE)"
        # Texte UTF-8
        try:
            data.decode('utf-8')
            return "Texte UTF-8"
        except:
            return "Type inconnu"
    except Exception as e:
        print(f"{RED}[ERREUR]{RESET} Impossible de lire le fichier : {str(e)}\n")
        return None

def display_disclaimer():
    """Affiche le disclaimer."""
    print(f"{RED}[DISCLAIMER]{RESET} Ce programme est conçu uniquement à des fins éducatives.")
    print(f"{CYAN}[INFO]{RESET} Utilisation responsable requise.")
    print(f"{CYAN}[INFO]{RESET} L'auteur décline toute responsabilité pour un mauvais usage.")
    print(f"{CYAN}[INFO]{RESET} Le programme démarre dans 5 secondes...\n")
    time.sleep(5)
    clear_screen()

def display_menu():
    """Affiche le menu principal."""
    print(f"{CYAN}{BOLD}Bienvenue dans l'outil d'obfuscation de fichier{RESET}")
    print(CYAN + LOCK_ART + RESET)
    print(f"{BLUE}[1]{RESET} Obfusquer un fichier")
    print(f"{BLUE}[2]{RESET} Détecter le type d'un fichier")
    print(f"{BLUE}[3]{RESET} Quitter\n")

def choose_file():
    """Demande à l'utilisateur de choisir un fichier."""
    while True:
        print(f"{CYAN}[INFO]{RESET} Faites glisser et déposez votre fichier ici (ou tapez 'q' pour revenir) : ", end="")
        file_path = input().strip()
        if file_path.lower() == 'q':
            return None
        elif os.path.isfile(file_path):
            return file_path
        else:
            print(f"{RED}[ERREUR]{RESET} Fichier introuvable. Réessayez.\n")

def choose_output_file():
    """Demande un nom de fichier de sortie."""
    while True:
        output_file = input(f"{CYAN}[INFO]{RESET} Nom du fichier de sortie (ex: output.txt) : ").strip()
        if output_file:
            return output_file
        print(f"{RED}[ERREUR]{RESET} Nom invalide. Réessayez.")

def main():
    """Fonction principale."""
    display_disclaimer()
    output_folder = os.getcwd()  # Utiliser le dossier actuel par défaut

    while True:
        clear_screen()
        display_menu()
        choice = input(f"{CYAN}[CHOIX]{RESET} Choisissez une option : ").strip()
        
        if choice == '1':
            clear_screen()
            file_path = choose_file()
            if not file_path:
                continue
            output_file = choose_output_file()
            key = input(f"{CYAN}[INFO]{RESET} Clé d'obfuscation (par défaut 123) : ").strip() or "123"
            try:
                key = int(key)
                output_path = os.path.join(output_folder, output_file)
                obfuscate_file(file_path, output_path, key)
                input(f"{CYAN}[INFO]{RESET} Appuyez sur Entrée pour continuer...")
            except ValueError:
                print(f"{RED}[ERREUR]{RESET} La clé doit être un nombre entier.")
        
        elif choice == '2':
            clear_screen()
            file_path = choose_file()
            if not file_path:
                continue
            file_type = detect_file_type(file_path)
            print(f"{CYAN}[INFO]{RESET} Le type de fichier est : {file_type}\n")
            input(f"{CYAN}[INFO]{RESET} Appuyez sur Entrée pour continuer...")
        
        elif choice == '3':
            print(f"{CYAN}[INFO]{RESET} Merci d'avoir utilisé l'outil d'obfuscation. À bientôt !")
            sys.exit()
        else:
            print(f"{RED}[ERREUR]{RESET} Option invalide. Réessayez.\n")
            time.sleep(2)

if __name__ == '__main__':
    main()
