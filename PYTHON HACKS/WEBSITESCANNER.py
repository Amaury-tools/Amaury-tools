from colorama import Fore
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re
import time

# Définition des couleurs
cyan = '\033[96m'
blue = '\033[94m'
red = '\033[91m'
yellow = '\033[93m'
white = '\033[97m'
reset = '\033[0m'
green = Fore.GREEN

# Préfixes
BEFORE = f"{blue}[{reset}"
AFTER = f"{blue}]{reset}"
INPUT = f"{cyan}[INPUT]{reset}"
ADD = f"{yellow}[ADD]{reset}"
INFO = f"{green}[INFO]{reset}"
ERROR = f"{red}[ERROR]{reset}"

# Fonction pour afficher l'heure actuelle
def current_time_hour():
    return time.strftime("%H:%M:%S")

# Fonction pour afficher l'erreur
def Error(e):
    print(f"{ERROR} Une erreur est survenue: {str(e)}")

# Fonction pour censurer l'URL
def Censored(url):
    print(f"{INFO} URL censurée: {url}")

# Fonction pour réinitialiser
def Reset():
    print(f"{INFO} Réinitialisation du processus terminé.")

# Fonction pour continuer
def Continue():
    print(f"{INFO} Continuer...")

# Liste pour stocker tous les liens
all_links = []

def find_secret_urls(website_url, domain):
    global all_links

    temp_all_links = []

    response = requests.get(website_url)
    if response.status_code != 200:
        return

    soup = BeautifulSoup(response.content, 'html.parser')

    def is_valid_extension(url):
        return re.search(r'\.(html|xhtml|php|js|css)$', url) or not re.search(r'\.\w+$', url)

    for tag in soup.find_all(['a', 'link', 'script', 'img', 'iframe', 'button', 'form']):
        href = tag.get('href')
        src = tag.get('src')
        action = tag.get('action')

        if href:
            full_url = urljoin(website_url, href)
            if full_url not in all_links and domain in full_url and is_valid_extension(full_url):
                temp_all_links.append(full_url)
                all_links.append(full_url)

        if src:
            full_url = urljoin(website_url, src)
            if full_url not in all_links and domain in full_url and is_valid_extension(full_url):
                temp_all_links.append(full_url)
                all_links.append(full_url)

        if action:
            full_url = urljoin(website_url, action)
            if full_url not in all_links and domain in full_url and is_valid_extension(full_url):
                temp_all_links.append(full_url)
                all_links.append(full_url)

    for form in soup.find_all('form'):
        action = form.get('action')
        if action:
            full_url = urljoin(website_url, action)
            if full_url not in all_links and domain in full_url and is_valid_extension(full_url):
                temp_all_links.append(full_url)
                all_links.append(full_url)

    for script in soup.find_all('script'):
        if script.string:
            urls_in_script = re.findall(r'(https?://\S+)', script.string)
            for url in urls_in_script:
                if url not in all_links and domain in url and is_valid_extension(url):
                    temp_all_links.append(url)
                    all_links.append(url)

    for link in temp_all_links:
        print(f"{BEFORE + current_time_hour() + AFTER} {ADD} Url: {white}{link}{reset}")

def find_all_secret_urls(website_url, domain):
    find_secret_urls(website_url, domain)

    visited_links = set()
    while True:
        try:
            new_links = [link for link in all_links if link not in visited_links]
            if not new_links:
                break
            for link in new_links:
                if requests.get(link).status_code == 200:
                    find_secret_urls(link, domain)
                    visited_links.add(link)
        except Exception as e:
            pass

# Interface utilisateur
print(Fore.CYAN + """
    ⢀⡴⠑⡄⠀⠀⠀⠀⠀⣀⣀⣤⣤⣤⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
   ⠀⠿⡀⠀⠀⠀⣀⡴⢿⣿⣿⣿⣿⣿⣿⣿⣷⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠑⢄⣠⠾⠁⣀⣄⡈⠙⣿⣿⣿⣿⣿⣿⣿⣿⣆⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⢀⡀⠁⠀⠀⠈⠙⠛⠂⠈⣿⣿⣿⣿⣿⠿⡿⢿⣆⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⢀⡾⣁⣀⠀⠴⠂⠙⣗⡀⠀⢻⣿⣿⠭⢤⣴⣦⣤⣹⠀⠀⠀⢀⢴⣶⣆
⠀⠀⢀⣾⣿⣿⣿⣷⣮⣽⣾⣿⣥⣴⣿⣿⡿⢂⠔⢚⡿⢿⣿⣦⣴⣾⠁⠸⣼⡿
⠀⢀⡞⠁⠙⠻⠿⠟⠉⠀⠛⢹⣿⣿⣿⣿⣿⣌⢤⣼⣿⣾⣿⡟⠉⠀⠀⠀⠀⠀
⠀⣾⣷⣶⠇⠀⠀⣤⣄⣀⡀⠈⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀
⠀⠉⠈⠉⠀⠀⢦⡈⢻⣿⣿⣿⣶⣶⣶⣶⣤⣽⡹⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠉⠲⣽⡻⢿⣿⣿⣿⣿⣿⣿⣷⣜⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣷⣶⣮⣭⣽⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⣀⣀⣈⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠇⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠃⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠛⠻⠿⠿⠿⠿⠛⠉
""")
website_url = input(f"\n{BEFORE + current_time_hour() + AFTER} {INPUT} Website Url -> {reset}")
Censored(website_url)

if "https://" not in website_url and "http://" not in website_url:
    website_url = "https://" + website_url
domain = re.sub(r'^https?://', '', website_url).split('/')[0]

print(f"""
 {BEFORE}01{AFTER}{white} Only Url
 {BEFORE}02{AFTER}{white} All Website
""")

choice = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Choice -> {reset}")

if choice in ['1', '01']:
    find_secret_urls(website_url, domain)

elif choice in ['2', '02']:
    find_all_secret_urls(website_url, domain)

demande=input(Fore.CYAN + "\n[*] Appuyer sur Entrée Pour Quitter : ")
Continue()
Reset()
