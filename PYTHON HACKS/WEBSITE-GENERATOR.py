import tkinter as tk
from ttkbootstrap import Style
from tkinter import ttk, messagebox
import random
import webbrowser
import requests
import pyperclip
import threading
import time
import socket
from concurrent.futures import ThreadPoolExecutor
import queue

# Configuration des données réalistes améliorées
DEFAULT_PATHS = [
    "products", "services", "blog", "news", "support", "about", "contact", "dashboard", "careers",
    "privacy-policy", "terms-of-service", "faq", "team", "projects", "events", "resources", "portfolio"
]
ADVANCED_PATHS = [
    "api", "assets", "login", "admin", "register", "checkout", "shop", "cart", "user", "profile",
    "logout", "payment", "dashboard", "order", "settings", "messages", "notifications", "help"
]
SECTORS = [
    "tech", "shop", "travel", "food", "sports", "news", "health", "finance", "education", "music",
    "gaming", "art", "fashion", "lifestyle", "media", "real-estate", "automotive", "home", "construction",
    "law", "energy", "environment", "real-estate", "ecommerce", "digital", "mobile", "entertainment",
    "startup", "corporate", "nonprofit"
]
SUBDOMAINS = [
    "www", "app", "news", "shop", "blog", "portal", "services", "admin", "store", "support", "team",
    "help", "forum", "community", "social", "events", "tech", "careers", "learning", "study", "guide",
    "members", "media", "projects", "updates", "resources"
]
BASE_NAMES = [
    "hub", "world", "online", "pro", "solutions", "space", "network", "cloud", "box", "center", "factory",
    "zone", "market", "base", "city", "team", "experts", "group", "worldwide", "core", "planet", "wave",
    "global", "vision", "partners", "universe", "makers"
]
AVAILABLE_DOMAINS = [
    ".com", ".net", ".org", ".io", ".tech", ".travel", ".shop", ".biz", ".co", ".us", ".store", ".online",
    ".tv", ".me", ".ai", ".app", ".xyz", ".pro", ".blog", ".mobi", ".dev", ".edu", ".info"
]
AVAILABLE_PROTOCOLS = ["http", "https", "ftp", "sftp", "ws", "wss", "file"]
ADJECTIVES = [
    "fast", "secure", "global", "best", "innovative", "reliable", "premium", "nextgen", "modern",
    "cutting-edge", "dynamic", "smart", "easy", "digital", "interactive", "creative", "advanced",
    "social", "affordable", "top", "eco", "high-performance", "cloud", "dedicated", "seamless"
]

stop_flag = threading.Event()  # Flag pour arrêter la génération
lock = threading.Lock()  # Lock pour synchronisation entre threads
url_queue = queue.Queue()  # Queue pour la gestion des URLs à valider

# Ports à vérifier et leurs descriptions
PORTS = {
    80: "HTTP",
    443: "HTTPS",
    21: "FTP",
    22: "SSH",
    25: "SMTP",
    110: "POP3",
    143: "IMAP",
}

# Variables de gestion d'état
status_var = None

def generate_random_url(protocol, domain, paths, use_long):
    """Génère une URL réaliste avec des combinaisons inspirées du réel."""
    subdomain = random.choice(SUBDOMAINS)
    sector = random.choice(SECTORS)
    path = random.choice(paths) if use_long else ""
    base_name = random.choice(BASE_NAMES) + "-" + random.choice(ADJECTIVES)

    structure = random.choice([  # Combinaison de base pour créer des URL
        f"{protocol}://{subdomain}.{base_name}{domain}/{path}",
        f"{protocol}://{base_name}{domain}/{path}",
        f"{protocol}://{subdomain}/{sector}/{path}",
        f"{protocol}://{base_name}{domain}/blog/{path}",
        f"{protocol}://{subdomain}.{sector}{domain}/{path}",
        f"{protocol}://{subdomain}/{base_name}-{sector}{domain}/{path}",
        f"{protocol}://{sector}-{base_name}{domain}/{path}",
    ])
    return structure

def verify_url(url):
    """Vérifie rapidement si une URL est accessible et si certains ports sont ouverts."""
    try:
        response = requests.head(url, timeout=3)
        if response.status_code < 400:
            open_ports = [port for port in PORTS if check_port(url, port)]
            return open_ports if open_ports else None
        return None
    except requests.RequestException:
        return None

def check_port(url, port):
    """Vérifie si un port spécifique est ouvert pour une URL donnée."""
    try:
        host = url.split("//")[1].split("/")[0]
        socket.create_connection((host, port), timeout=3)
        return True
    except Exception:
        return False

def validate_and_colorize(index, url):
    """Valide l'URL et applique une couleur (verte ou rouge) selon qu'elle est valide et a des ports ouverts."""
    open_ports = verify_url(url)
    if open_ports:
        listbox.itemconfig(index, {'fg': 'green'})
        url_with_ports = f"{url} (ports ouverts : {', '.join([f'{port} ({PORTS[port]})' for port in open_ports])})"
        valid_listbox.insert(tk.END, url_with_ports)
        valid_listbox.itemconfig(valid_listbox.size() - 1, {'fg': 'green'})
    else:
        listbox.itemconfig(index, {'fg': 'red'})

def update_status_message(message):
    """Met à jour le message d'état dans l'interface."""
    status_var.set(message)

def generate_until_valid_url():
    """Génère des URLs jusqu'à en trouver une valide, avec une logique arrêtable."""
    stop_flag.clear()  # Réinitialise le flag pour autoriser la génération
    selected_protocol = protocol_var.get()
    selected_domain = domain_var.get()
    use_long = url_length_var.get()
    selected_list = path_list_var.get()

    paths = {
        "Basique": DEFAULT_PATHS,
        "Avancé": ADVANCED_PATHS,
        "Commun": DEFAULT_PATHS + ADVANCED_PATHS
    }.get(selected_list, DEFAULT_PATHS)

    with ThreadPoolExecutor(max_workers=10) as executor:
        while not stop_flag.is_set():
            url = generate_random_url(selected_protocol, selected_domain, paths, use_long)
            listbox.insert(tk.END, url)
            listbox.yview(tk.END)
            update_status_message(f"Génération d'URL : {url}")

            # Soumettre la validation dans le thread pool
            executor.submit(validate_and_colorize, listbox.size() - 1, url)

            time.sleep(0.05)

def stop_generation():
    """Arrête la génération d'URLs."""
    stop_flag.set()  # Active le flag pour arrêter la génération
    update_status_message("La génération d'URLs a été arrêtée.")
    messagebox.showinfo("Génération arrêtée", "La génération d'URLs a été arrêtée.")

def clear_lists():
    """Vide les listes d'URLs générées et validées."""
    listbox.delete(0, tk.END)
    valid_listbox.delete(0, tk.END)
    update_status_message("Listes d'URLs effacées.")

def open_selected_urls():
    """Ouvre les URLs sélectionnées dans le valid_listbox."""
    selected_indices = valid_listbox.curselection()
    if not selected_indices:
        messagebox.showwarning("Attention", "Aucune URL sélectionnée à ouvrir.")
        return

    for index in selected_indices:
        url = valid_listbox.get(index)
        webbrowser.open(url)

def copy_selected_url():
    """Copie une URL valide dans le presse-papiers."""
    valid_urls = [valid_listbox.get(i) for i in range(valid_listbox.size())]
    if not valid_urls:
        messagebox.showwarning("Attention", "Aucune URL valide à copier.")
        return

    pyperclip.copy(valid_urls[0])
    messagebox.showinfo("Succès", f"L'URL '{valid_urls[0]}' a été copiée dans le presse-papiers.")

def show_initial_message():
    """Affiche un message expliquant le fonctionnement de l'outil."""
    messagebox.showinfo("Générateur d'URLs", "Bienvenue dans le générateur d'URLs !")

def ask_continue_confirmation():
    """Demande si l'utilisateur est sûr de vouloir continuer."""
    return messagebox.askyesno("Confirmation", "Êtes-vous sûr de vouloir continuer avec la génération d'URLs ?")

def generate_urls():
    """Cette fonction est appelée lors du clic sur 'Générer'."""
    show_initial_message()  # Affiche le message explicatif initial
    if ask_continue_confirmation():  # Demande la confirmation de l'utilisateur
        threading.Thread(target=generate_until_valid_url, daemon=True).start()
    else:
        messagebox.showinfo("Annulation", "La génération des URLs a été annulée.")

root = tk.Tk()
root.title("Générateur d'URLs")
style = Style(theme="cosmo")
root.geometry("800x600")

# Création de la frame principale
main_frame = ttk.Frame(root, padding=10)
main_frame.pack(fill="both", expand=True)

# Titre en gros en haut au centre
title_label = ttk.Label(main_frame, text="Générateur d'URLs - Par Amaury", font=("Cabin", 45), anchor="center")
title_label.pack(pady=10)

# Frame des options
options_frame = ttk.Frame(main_frame)
options_frame.pack(fill="x")

protocol_var = tk.StringVar(value="http")
domain_var = tk.StringVar(value=".com")
url_length_var = tk.BooleanVar(value=False)
path_list_var = tk.StringVar(value="Commun")

# Création de la variable `status_var` après la création de `root`
status_var = tk.StringVar(value="Prêt à générer des URLs")

# Création des options
for i, (label_text, variable, values) in enumerate([
    ("Protocole :", protocol_var, AVAILABLE_PROTOCOLS),
    ("Extension :", domain_var, AVAILABLE_DOMAINS),
    ("Liste de chemins :", path_list_var, ["Commun", "Basique", "Avancé"])
]):
    ttk.Label(options_frame, text=label_text).grid(row=i, column=0, padx=8, pady=8)
    ttk.Combobox(options_frame, textvariable=variable, values=values, state="readonly").grid(row=i, column=1, padx=5, pady=5)

ttk.Checkbutton(options_frame, text="URLs longues", variable=url_length_var).grid(row=3, column=0, columnspan=2, pady=10)

# Frame pour la légende colorée
legend_frame = ttk.Frame(main_frame)
legend_frame.pack(side="top", anchor="ne", padx=10, pady=10, fill="x")

# Légende avec couleurs
ttk.Label(legend_frame, text="Légende des couleurs : ", font=("Arial", 10)).pack(side="left")
ttk.Label(legend_frame, text="Valide", foreground="green", font=("Arial", 10)).pack(side="left", padx=5)
ttk.Label(legend_frame, text="Invalide", foreground="red", font=("Arial", 10)).pack(side="left", padx=5)

# Ajout de la légende des ports
port_legend_frame = ttk.Frame(main_frame)
port_legend_frame.pack(side="top", anchor="nw", padx=10, pady=10, fill="x")

# Légende des ports
ttk.Label(port_legend_frame, text="Légende des ports : ", font=("Arial", 10)).pack(side="left")
for port, desc in PORTS.items():
    ttk.Label(port_legend_frame, text=f"{port} ({desc})", font=("Arial", 10)).pack(side="left", padx=5)

# Liste d'URLs générées avec défilement
listbox_frame = ttk.Frame(main_frame)
listbox_frame.pack(fill="both", expand=True, padx=10, pady=10)

listbox_scrollbar = tk.Scrollbar(listbox_frame, orient="vertical")
listbox_scrollbar.pack(side="right", fill="y")

listbox = tk.Listbox(listbox_frame, width=50, height=15, font=("Courier", 10), bg="#f9f5e3", yscrollcommand=listbox_scrollbar.set)
listbox.pack(side="left", fill="both", expand=True)
listbox_scrollbar.config(command=listbox.yview)

# Liste des URLs valides avec défilement
valid_listbox_frame = ttk.Frame(main_frame)
valid_listbox_frame.pack(fill="both", expand=True, padx=10, pady=10)

valid_listbox_scrollbar = tk.Scrollbar(valid_listbox_frame, orient="vertical")
valid_listbox_scrollbar.pack(side="right", fill="y")

valid_listbox = tk.Listbox(valid_listbox_frame, width=50, height=15, font=("Courier", 10), bg="#e7f9e7", yscrollcommand=valid_listbox_scrollbar.set, selectmode=tk.MULTIPLE)
valid_listbox.pack(side="left", fill="both", expand=True)
valid_listbox_scrollbar.config(command=valid_listbox.yview)

# Repositionnement des boutons pour éviter le débordement
button_frame = ttk.Frame(main_frame)
button_frame.pack(pady=20, fill="x")

buttons = [
    ("Générer", generate_urls),
    ("Ouvrir", open_selected_urls),
    ("Copier", copy_selected_url),
    ("Stop", stop_generation),
    ("Vider", clear_lists)  # Bouton pour vider les listes
]

for i, (text, command) in enumerate(buttons):
    ttk.Button(button_frame, text=text, command=command).grid(row=0, column=i, padx=10, pady=5)

# Affichage de l'état
status_label = ttk.Label(main_frame, textvariable=status_var)
status_label.pack(pady=5)

# Passer en plein écran automatiquement
root.attributes('-fullscreen', True)

root.mainloop()