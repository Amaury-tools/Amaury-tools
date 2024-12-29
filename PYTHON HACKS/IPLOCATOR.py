import socket
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import requests
from PIL import Image, ImageTk
import io
import threading
import subprocess
import time

# Variables globales pour la carte
lat, lon, current_zoom = 0, 0, 10
map_type = 'map'  # Type de carte initial (carte classique)

# Variable pour stocker le chemin de la wordlist
wordlist_path = ""

# Fonction utilitaire pour afficher des messages dans la zone de résultats
def show_message(text, is_error=False):
    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, text)
    result_text.config(bg="#FF6347" if is_error else "#333333")

# Fonction pour zoomer sur la carte
def zoom_in():
    global current_zoom
    current_zoom = min(current_zoom + 1, 17)
    update_map(lat, lon, current_zoom)

def zoom_out():
    global current_zoom
    current_zoom = max(current_zoom - 1, 1)
    update_map(lat, lon, current_zoom)

# Fonction pour afficher la carte en fonction du type de carte
def update_map(lat, lon, zoom=10, map_type='map'):
    try:
        map_url = f"https://static-maps.yandex.ru/1.x/?lang=en_US&ll={lon},{lat}&z={zoom}&l={map_type}&size=650,450&pt={lon},{lat},pm2rdm"
        map_response = requests.get(map_url)
        map_response.raise_for_status()

        map_image_data = Image.open(io.BytesIO(map_response.content))
        map_image = map_image_data.resize((650, 450), Image.Resampling.LANCZOS)
        map_photo = ImageTk.PhotoImage(map_image)

        map_label.configure(image=map_photo)
        map_label.image = map_photo
    except requests.RequestException as e:
        show_message(f"Erreur de chargement de la carte : {e}", is_error=True)
        clear_map()

# Fonction pour effacer la carte
def clear_map():
    map_label.configure(image="")
    map_label.image = None

# Fonction pour localiser une adresse IP publique
def get_ip_and_location():
    global lat, lon, current_zoom, map_type
    domain = entry.get().strip()

    if not domain:
        messagebox.showerror("Erreur", "Veuillez entrer un nom de domaine valide.")
        return

    thread = threading.Thread(target=process_ip_location, args=(domain,))
    thread.start()

    loading_label.grid(row=5, column=0, columnspan=2, pady=20)

    entry.config(state=tk.DISABLED)
    search_button.config(state=tk.DISABLED)

def process_ip_location(domain):
    global lat, lon, current_zoom, map_type
    try:
        ip = socket.gethostbyname(domain)
        response = requests.get(f"http://ip-api.com/json/{ip}")
        response.raise_for_status()
        data = response.json()

        if data['status'] == 'success':
            lat, lon = data['lat'], data['lon']
            current_zoom = 10

            whois_data = get_whois_data(domain)
            open_ports = check_open_ports(domain)
            security_report = assess_server_security(open_ports, whois_data)

            location_info = f"""
🌍 Adresse IP: {ip}
🇺🇸 Pays : {data['country']} ({data['countryCode']})
🗺 Région : {data['regionName']} ({data['region']})
🏙 Ville : {data['city']}
📮 Code postal : {data['zip']}

🌐 Latitude : {lat}
🌐 Longitude : {lon}

⏰ Fuseau horaire : {data['timezone']}
📡 Fournisseur : {data['isp']}
🏢 Organisation : {data['org']}
🔧 AS : {data['as']}

💡 Type de connexion: {data.get('connection', 'Non disponible')}
🌐 Proxy : {data.get('proxy', 'Non renseigné')}
🖥 Nom d'hôte : {data.get('reverse', 'Non disponible')}
🌍 Version API : {data.get('version', 'Non disponible')}
🔗 Site Web* : {data.get('website', 'Non disponible')}

📚 Informations WHOIS :
{whois_data}

🔌 Ports ouverts :
{open_ports}

⚠️ Évaluation de la sécurité :
{security_report}
"""
            show_message(location_info)
            update_map(lat, lon, current_zoom, map_type)

        else:
            show_message("❌ Erreur : Impossible de localiser l'adresse IP.", is_error=True)
            clear_map()

    except socket.gaierror:
        show_message("Nom de domaine invalide ou introuvable.", is_error=True)
        clear_map()
    except requests.RequestException as e:
        show_message(f"Erreur réseau : {e}", is_error=True)
        clear_map()
    except Exception as e:
        show_message(f"Une erreur s'est produite : {e}", is_error=True)
        clear_map()

    loading_label.grid_forget()
    entry.config(state=tk.NORMAL)
    search_button.config(state=tk.NORMAL)

# Fonction pour vérifier les ports ouverts
def check_open_ports(domain):
    common_ports = [21, 22, 23, 25, 53, 80, 443, 8080]
    open_ports = []
    for port in common_ports:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((domain, port))
            if result == 0:
                open_ports.append(str(port))
            sock.close()
        except socket.error:
            continue

    return ", ".join(open_ports) if open_ports else "Aucun port ouvert détecté"

# Fonction pour évaluer la sécurité du serveur
def assess_server_security(open_ports, whois_data):
    open_ports_count = len(open_ports.split(", ")) if open_ports != "Aucun port ouvert détecté" else 0

    if open_ports_count > 5:
        port_risk = "Risque élevé : Trop de ports ouverts"
    elif open_ports_count > 2:
        port_risk = "Risque moyen : Plusieurs ports ouverts"
    else:
        port_risk = "Risque faible : Peu de ports ouverts"

    whois_risk = "Risque moyen : Informations WHOIS incomplètes" if "Non renseigné" in whois_data else "Risque élevé : WHOIS suspect" if "obscur" in whois_data else "Risque faible : WHOIS complet et valide"

    return f"{port_risk}\n{whois_risk}"

# Fonction pour obtenir les données WHOIS via l'API WhoisXML
def get_whois_data(domain):
    api_key = 'at_FfezlHAQVlXqZgfCpcXUr6N8sqMBJ'
    url = f'https://www.whoisxmlapi.com/whoisserver/WhoisService?apiKey={api_key}&domainName={domain}&outputFormat=JSON'

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        return data['WhoisRecord'].get('registryData', {}).get('createdDate', 'Date non disponible') if 'WhoisRecord' in data and 'domainName' in data['WhoisRecord'] else "Informations WHOIS non disponibles"

    except requests.RequestException as e:
        return f"Erreur WHOIS : {e}"

# Fonction pour ouvrir le dialogue de sélection de fichier pour la wordlist
def choose_wordlist():
    global wordlist_path
    wordlist_path = filedialog.askopenfilename(title="Choisir une wordlist", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if wordlist_path:
        wordlist_label.config(text=f"Wordlist sélectionnée: {wordlist_path}")

# Fonction pour lancer le bruteforce de Gobuster et afficher la sortie en temps réel
def get_admin_page_gobuster():
    bruteforce = messagebox.askyesno("Bruteforce", "Voulez-vous bruteforcer la page de connexion du domaine ?")

    if bruteforce:
        print("D'accord, je commence le LoginBrute...")
        domain = entry.get().strip()

        if domain and wordlist_path:
            command = [
                r'C:\gobuster.exe', 'dir', '-u', f'http://{domain}', '-w', wordlist_path,
                '-t', '50', '-x', 'php,html,asp', '-status-codes', '200,301', '-exclude-status-codes', '404'
            ]

            try:
                process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

                def read_output():
                    for line in process.stdout:
                        show_message(line.strip())
                    for line in process.stderr:
                        show_message(line.strip(), is_error=True)

                threading.Thread(target=read_output, daemon=True).start()

            except Exception as e:
                show_message(f"Erreur lors de l'exécution de Gobuster : {e}", is_error=True)
        else:
            show_message("Veuillez entrer un domaine valide et sélectionner une wordlist", is_error=True)

# Interface Utilisateur
root = tk.Tk()
root.title("Scanner IP avec Carte et Infos Détaillées")
root.attributes("-fullscreen", True)
root.configure(bg="#2C2A24")

# Style ttk
style = ttk.Style()
style.theme_use("clam")
style.configure("TLabel", background="#2C2A24", foreground="#FFFFFF", font=("Helvetica", 16))
style.configure("TButton", background="#A67C52", foreground="#FFFFFF", font=("Helvetica", 14, "bold"))

# Grille principale
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=2)
root.rowconfigure(0, weight=1)
root.rowconfigure(1, weight=1)
root.rowconfigure(2, weight=3)

# Champ de saisie pour le nom de domaine
domain_label = tk.Label(root, text="Nom de domaine :", bg="#2C2A24", fg="#FFFFFF", font=("Helvetica", 16))
domain_label.grid(row=1, column=0, sticky="w", padx=20)
entry = ttk.Entry(root, width=50, font=("Helvetica", 16))
entry.grid(row=1, column=0, sticky="e", padx=20)

# Bouton pour rechercher
search_button = ttk.Button(root, text="🔍 Localiser", command=get_ip_and_location)
search_button.grid(row=1, column=1, padx=20)

# Zone des résultats
result_text = tk.Text(root, wrap=tk.WORD, font=("Helvetica", 14), bg="#333333", fg="#FFFFFF", padx=10, pady=10, height=15)
result_text.grid(row=2, column=0, sticky="nsew", padx=20, pady=20)

# Carte
map_label = tk.Label(root, bg="#2C2A24")
map_label.grid(row=2, column=1, padx=20, pady=20)

# Grille pour les boutons de zoom et carte
button_frame = tk.Frame(root, bg="#2C2A24")
button_frame.grid(row=3, column=0, columnspan=2, pady=10)

zoom_in_button = ttk.Button(button_frame, text="Zoom +", command=zoom_in)
zoom_in_button.grid(row=0, column=0, padx=20, pady=10)

zoom_out_button = ttk.Button(button_frame, text="Zoom -", command=zoom_out)
zoom_out_button.grid(row=0, column=1, padx=20, pady=10)

# Boutons pour changer le type de carte
map_button_frame = tk.Frame(root, bg="#2C2A24")
map_button_frame.grid(row=4, column=0, columnspan=2, pady=10)

satellite_button = ttk.Button(map_button_frame, text="Carte Satellite", command=lambda: update_map(lat, lon, current_zoom, 'sat'))
satellite_button.grid(row=0, column=0, padx=20)

hybrid_button = ttk.Button(map_button_frame, text="Carte Hybride", command=lambda: update_map(lat, lon, current_zoom, 'sat,skl'))
hybrid_button.grid(row=0, column=1, padx=20)

routine_button = ttk.Button(map_button_frame, text="Carte Routière", command=lambda: update_map(lat, lon, current_zoom, 'map'))
routine_button.grid(row=0, column=2, padx=20)

# Bouton Bruteforce
bruteforce_button = ttk.Button(root, text="🔐 Bruteforce Admin Page", command=get_admin_page_gobuster)
bruteforce_button.grid(row=5, column=0, columnspan=2, pady=20)

# Sélection de la wordlist
choose_wordlist_button = ttk.Button(root, text="Choisir une Wordlist", command=choose_wordlist)
choose_wordlist_button.grid(row=6, column=0, columnspan=2, pady=20)

wordlist_label = tk.Label(root, text="Aucune wordlist sélectionnée", bg="#2C2A24", fg="#FFFFFF", font=("Helvetica", 14))
wordlist_label.grid(row=7, column=0, columnspan=2)

# Zone de chargement
loading_label = tk.Label(root, text="Chargement... Veuillez patienter...", bg="#2C2A24", fg="#FFFFFF", font=("Helvetica", 18, "bold"))

# Lancement de l'application
root.mainloop()
