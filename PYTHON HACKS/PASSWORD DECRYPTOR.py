import bcrypt
import hashlib
import random
import string
import threading
import time
import base64
from hashlib import pbkdf2_hmac
import sys
from colorama import Fore

# Définition des couleurs
cyan = '\033[96m'
blue = '\033[94m'
red = '\033[91m'
yellow = '\033[93m'
white = '\033[97m'
reset = '\033[0m'

# Définition des préfixes
BEFORE = f"{blue}[{reset}"
AFTER = f"{blue}]{reset}"
ERROR = f"{red}[ERROR]{reset}"
WAIT = f"{yellow}[WAIT]{reset}"
ADD = f"{cyan}[SUCCESS]{reset}"
INPUT = f"{cyan}[INPUT]{reset}"


# Fonction pour afficher les erreurs
def Error(msg):
    print(f"{BEFORE}ERROR{AFTER} {red}{msg}{reset}")
    sys.exit(1)


# Fonction pour afficher les erreurs de choix
def ErrorChoice():
    print(f"{BEFORE}ERROR{AFTER} {red}[Choix invalide. Veuillez réessayer.]{reset}")
    sys.exit(1)


# Fonction pour afficher les erreurs sur les nombres
def ErrorNumber():
    print(f"{BEFORE}ERROR{AFTER} {red}[Veuillez entrer un nombre valide.]{reset}")
    sys.exit(1)


# Fonction pour le texte lent
def Slow(text):
    for c in text:
        sys.stdout.write(c)
        sys.stdout.flush()
        time.sleep(0.01)
    print()


# Fonction pour afficher le titre
def Title(title):
    print(f"\n{cyan}========== {title} =========={reset}\n")


# Fonction pour continuer après un succès
def Continue():
    input(f"{BEFORE}INFO{AFTER} {blue}[Appuyez sur Entrée pour continuer...]{reset}")


# Fonction pour réinitialiser le script (simuler un nettoyage)
def Reset():
    print(f"{BEFORE}INFO{AFTER} {yellow}[Réinitialisation du programme...]{reset}")
    time.sleep(1)
    sys.exit(0)


# Fonction pour afficher l'heure actuelle formatée
def current_time_hour():
    return time.strftime("%H:%M:%S")


# Début du programme
try:
    print(Fore.CYAN + """
              ^M@@@@@@@@@v
           v@@@@@@@@@@@@@@@@@
         _@@@@@@@}    ;a@@@@@@@
         M@@@@@            @@@@@@
        ;@@@@@              O@@@@@
          @@@@@v               @@@@@
           @@@@@;               @@@@@
           @@@@@;
           @@@@@;        
       @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
      @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
      @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
      @@@@@@@@@@@@@@@@j     @@@@@@@@@@@@@@@@          Made By Vaidx ! 
      @@@@@@@@@@@@@@@        @@@@@@@@@@@@@@@
      @@@@@@@@@@@@@@@v       @@@@@@@@@@@@@@@
      @@@@@@@@@@@@@@@@@    @@@@@@@@@@@@@@@@@
      @@@@@@@@@@@@@@@@@    @@@@@@@@@@@@@@@@@
      @@@@@@@@@@@@@@@@@_   @@@@@@@@@@@@@@@@@
      @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
      @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@|
       ^@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@O
""")                                               
    Slow(f"""
    {BEFORE}01{AFTER}{cyan}[BCRYPT]{reset}
    {BEFORE}02{AFTER}{cyan}[MD5]{reset}
    {BEFORE}03{AFTER}{cyan}[SHA-1]{reset}
    {BEFORE}04{AFTER}{cyan}[SHA-256]{reset}
    {BEFORE}05{AFTER}{cyan}[PBKDF2 (SHA-256)]{reset}
    {BEFORE}06{AFTER}{cyan}[Base64 Decode]{reset}
    """)

    choice = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} [Méthode de chiffrement] -> {reset}")

    if choice not in ['1', '01', '2', '02', '3', '03', '4', '04', '5', '05', '6', '06']:
        ErrorChoice()

    encrypted_password = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} [Mot de passe chiffré] -> {white}")
    try:
        threads_number = int(input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} [Nombre de threads] -> {white}"))
    except:
        ErrorNumber()
    try:
        characters_number = int(input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} [Nombre max de caractères] -> {white}"))
    except:
        ErrorNumber()

    Title(f"[Décryptage en cours] - Mot de passe chiffré: {encrypted_password}")
    print(f"{BEFORE + current_time_hour() + AFTER} {WAIT} [Brute force en cours...]{reset}")

    password = False
    generated_passwords = set()
    salt = "this_is_a_salt".encode('utf-8')

    all_characters = string.ascii_letters + string.digits + string.punctuation

    def error_decrypted():
        encryption_methods = {
            '1': "BCRYPT", '2': "MD5", '3': "SHA-1",
            '4': "SHA-256", '5': "PBKDF2 (SHA-256)", '6': "Base64 Decode"
        }
        encryption = encryption_methods.get(choice, "Inconnu")
        print(f'{BEFORE + current_time_hour() + AFTER} {ERROR} [Le mot de passe "{encrypted_password}" ne fonctionne pas avec "{encryption}".]')
        Continue()
        Reset()

    def check_password(password_test):
        try:
            if choice in ['1', '01']:
                return bcrypt.checkpw(password_test.encode('utf-8'), encrypted_password.encode('utf-8'))
            elif choice in ['2', '02']:
                return hashlib.md5(password_test.encode('utf-8')).hexdigest() == encrypted_password
            elif choice in ['3', '03']:
                return hashlib.sha1(password_test.encode('utf-8')).hexdigest() == encrypted_password
            elif choice in ['4', '04']:
                return hashlib.sha256(password_test.encode('utf-8')).hexdigest() == encrypted_password
            elif choice in ['5', '05']:
                return pbkdf2_hmac('sha256', password_test.encode('utf-8'), salt, 100000).hex() == encrypted_password
            elif choice in ['6', '06']:
                return base64.b64decode(encrypted_password.encode('utf-8')).decode('utf-8') == password_test
        except:
            error_decrypted()

    def generate_password():
        return ''.join(random.choice(all_characters) for _ in range(random.randint(1, characters_number)))

    def test_decrypted():
        global password
        while not password:
            password_test = generate_password()
            if password_test not in generated_passwords:
                generated_passwords.add(password_test)
                if check_password(password_test):
                    password = True
                    print(f"{BEFORE + current_time_hour() + AFTER} {ADD} [Mot de passe trouvé: {white}{password_test}{reset}]")
                    Continue()
                    Reset()

    threads = []
    for _ in range(threads_number):
        t = threading.Thread(target=test_decrypted)
        t.start()
        threads.append(t)

    for thread in threads:
        thread.join()

except Exception as e:
    Error(e)
