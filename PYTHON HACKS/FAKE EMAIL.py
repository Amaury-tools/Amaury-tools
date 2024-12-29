import pyperclip
import requests
import random
import string
import time
import sys
import re
import os

# Définition de l'API et des domaines
API = 'https://www.1secmail.com/api/v1/'
domainList = ['1secmail.com', '1secmail.net', '1secmail.org']
domain = random.choice(domainList)

# Initialisation de Colorama pour gérer les couleurs
from colorama import Fore, Style, init
init(autoreset=True)

# Définir les couleurs
CYAN = Fore.CYAN
BLUE = Fore.BLUE
GREEN = Fore.GREEN
RED = Fore.RED
YELLOW = Fore.YELLOW
WHITE = Fore.WHITE
RESET = Style.RESET_ALL

# Fonction de texte défilant
def slowprint(s):
    for c in s + '\n':
        sys.stdout.write(c)
        sys.stdout.flush()
        time.sleep(10 / 100)

# Fonction pour afficher le banner
def banner():
    print(f"""{CYAN}                                                                             
    ▄████  ██   █  █▀ ▄███▄   █▀▄▀█ ██   ▄█ █     
    █▀   ▀ █ █  █▄█   █▀   ▀  █ █ █ █ █  ██ █     
    █▀▀    █▄▄█ █▀▄   ██▄▄    █ ▄ █ █▄▄█ ██ █      Made By Vaidx ! 
    █      █  █ █  █  █▄   ▄▀ █   █ █  █ ▐█ ███▄  
     █        █   █   ▀███▀      █     █  ▐     ▀ 
      ▀      █   ▀              ▀     █           
         ▀                        ▀                   
    """)

# Fonction pour générer un nom d'utilisateur aléatoire
def generateUserName():
    name = string.ascii_lowercase + string.digits
    username = ''.join(random.choice(name) for i in range(10))
    return username

# Fonction pour extraire les informations de l'email
def extract():
    getUserName = re.search(r'login=(.*)&', newMail).group(1)
    getDomain = re.search(r'domain=(.*)', newMail).group(1)
    return [getUserName, getDomain]

# Fonction pour afficher la ligne de statut
def print_statusline(msg: str):
    last_msg_length = len(print_statusline.last_msg) if hasattr(print_statusline, 'last_msg') else 0
    print(' ' * last_msg_length, end='\r')
    print(msg, end='\r')
    sys.stdout.flush()
    print_statusline.last_msg = msg

# Fonction pour supprimer l'email
def deleteMail():
    url = 'https://www.1secmail.com/mailbox'
    data = {
        'action': 'deleteMailbox',
        'login': f'{extract()[0]}',
        'domain': f'{extract()[1]}'
    }

    print_statusline(f"{CYAN}Disposing your email address - {WHITE}{mail}{RESET}\n")
    req = requests.post(url, data=data)

# Fonction pour vérifier les mails
def checkMails():
    reqLink = f'{API}?action=getMessages&login={extract()[0]}&domain={extract()[1]}'
    req = requests.get(reqLink).json()
    length = len(req)
    if length == 0:
        print_statusline(f"{RED}Your mailbox is empty. Hold tight. Mailbox is refreshed automatically every 5 seconds.{RESET}")
    else:
        idList = []
        for i in req:
            for k, v in i.items():
                if k == 'id':
                    mailId = v
                    idList.append(mailId)

        x = 'mails' if length > 1 else 'mail'
        print_statusline(f"{GREEN}You received {length} {x}. (Mailbox is refreshed automatically every 5 seconds.){RESET}")

        current_directory = os.getcwd()
        final_directory = os.path.join(current_directory, r'All Mails')
        if not os.path.exists(final_directory):
            os.makedirs(final_directory)

        for i in idList:
            msgRead = f'{API}?action=readMessage&login={extract()[0]}&domain={extract()[1]}&id={i}'
            req = requests.get(msgRead).json()
            for k, v in req.items():
                if k == 'from':
                    sender = v
                if k == 'subject':
                    subject = v
                if k == 'date':
                    date = v
                if k == 'textBody':
                    content = v

            mail_file_path = os.path.join(final_directory, f'{i}.txt')

            with open(mail_file_path, 'w') as file:
                file.write(f"Sender: {sender}\nTo: {mail}\nSubject: {subject}\nDate: {date}\nContent: {content}\n")

# Bannière d'accueil
banner()

userInput1 = input(f"\n{CYAN}[+] Do you wish to use a custom domain name (Y/N): ").capitalize()

try:
    if userInput1 == 'Y' or userInput1 == 'y':
        userInput2 = input(f"\n{CYAN}[+] Enter the name that you wish to use as your domain name: ")
        newMail = f"{API}?login={userInput2}&domain={domain}"
        reqMail = requests.get(newMail)
        mail = f"{extract()[0]}@{extract()[1]}"
        pyperclip.copy(mail)
        slowprint(f"\n{YELLOW}Your temporary email is {mail} (Email address copied to clipboard.){RESET}\n")
        slowprint(f"{BLUE}---------------------------- | Inbox of {mail}| ----------------------------{RESET}\n")
        while True:
            checkMails()
            time.sleep(5)

    if userInput1 == 'N' or userInput1 == 'n':
        newMail = f"{API}?login={generateUserName()}&domain={domain}"
        reqMail = requests.get(newMail)
        mail = f"{extract()[0]}@{extract()[1]}"
        pyperclip.copy(mail)
        print(f"\n{GREEN}Your temporary email is {mail} (Email address copied to clipboard.){RESET}\n")
        print(f"{RED}---------------------------- | Inbox of {mail} | ----------------------------{RESET}\n")
        while True:
            checkMails()
            time.sleep(5)

except KeyboardInterrupt:
    deleteMail()
    print(f"\n{CYAN}Programme Interrupted{RESET}")
    os.system('cls' if os.name == 'nt' else 'clear')

except Exception as e:
    print(f"{RED}An error occurred: {e}{RESET}")

finally:
    input(f"\n{CYAN}[*] Press Enter to exit...{RESET}")
    time.sleep(2)
