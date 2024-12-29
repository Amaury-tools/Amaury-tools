from scapy.all import sniff, IP, TCP, UDP, DNS, DNSQR, Raw
from colorama import Fore, Style, init
import os
import socket

# Initialisation de colorama
init(autoreset=True)

# Fonction pour obtenir le nom d'hôte
def get_hostname(ip):
    try:
        return socket.gethostbyaddr(ip)[0]
    except socket.herror:
        return "Nom d'hôte introuvable"

# Fonction pour afficher les paquets de manière formatée
def display_packet(packet, seen_ips):
    try:
        # Vérification si les IPs source et destination ont déjà été affichées
        ip_src = packet[IP].src
        ip_dst = packet[IP].dst
        if (ip_src, ip_dst) in seen_ips:
            return  # Ignorer les paquets déjà affichés
        seen_ips.add((ip_src, ip_dst))

        if packet.haslayer(IP):
            hostname_src = get_hostname(ip_src)
            hostname_dst = get_hostname(ip_dst)

            # Informations IP
            print(Fore.CYAN + """
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⡾⠃⠀⠀⠀⠀⠀⠀⠰⣶⡀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⡿⠁⣴⠇⠀⠀⠀⠀⠸⣦⠈⢿⡄⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣾⡇⢸⡏⢰⡇⠀⠀⢸⡆⢸⡆⢸⡇⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⡇⠘⣧⡈⠃⢰⡆⠘⢁⣼⠁⣸⡇⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢿⣄⠘⠃⠀⢸⡇⠀⠘⠁⣰⡟⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠃⠀⠀⢸⡇⠀⠀⠘⠋⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀
⠀⢸⣿⣟⠉⢻⡟⠉⢻⡟⠉⣻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀
⠀⢸⣿⣿⣷⣿⣿⣶⣿⣿⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀
⠀⠈⠉⠉⢉⣉⣉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⣉⣉⡉⠉⠉⠉⠁⠀
⠀⠀⠀⠀⠉⠉⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠉⠉⠀⠀⠀⠀
""")
                                          
            print(Fore.CYAN + f"IP Source: {ip_src} -> IP Destination: {ip_dst}")
            print(Fore.GREEN + f"Protocole: {get_protocol(packet[IP].proto)}")
            print(Fore.CYAN + f"Hostname Source: {hostname_src}")
            print(Fore.CYAN + f"Hostname Destination: {hostname_dst}")

            # Informations TCP/UDP si disponibles
            if packet.haslayer(TCP):
                print(Fore.YELLOW + f"TCP: {packet[TCP].sport} -> {packet[TCP].dport}")
            elif packet.haslayer(UDP):
                print(Fore.YELLOW + f"UDP: {packet[UDP].sport} -> {packet[UDP].dport}")

            # Informations DNS si disponibles
            if packet.haslayer(DNS) and packet.getlayer(DNS).qr == 0:
                print(Fore.BLUE + f"DNS Request: {packet[DNSQR].qname.decode('utf-8')}")

            # Informations HTTP/HTTPS si disponibles
            if packet.haslayer(Raw):
                try:
                    payload = packet[Raw].load.decode('utf-8', errors='ignore')
                    if payload:
                        print(Fore.MAGENTA + "Raw Payload:")
                        print(payload)
                        if packet[TCP].dport == 80 or packet[TCP].sport == 80:
                            if "Host:" in payload:
                                host = payload.split("Host: ")[1].split("\r\n")[0]
                                print(Fore.MAGENTA + f"HTTP Host: {host}")
                            headers = payload.split("\r\n")
                            for header in headers:
                                if header:
                                    print(Fore.MAGENTA + f"HTTP Header: {header}")
                        elif packet[TCP].dport == 443 or packet[TCP].sport == 443:
                            print(Fore.MAGENTA + "HTTPS Payload (chiffré) détecté.")
                            hex_payload = ' '.join(f'{ord(x):02x}' for x in payload)
                            print(Fore.MAGENTA + f"Raw Payload (hex): {hex_payload}")
                    else:
                        print(Fore.MAGENTA + "Aucune charge utile (Payload) disponible.")
                except UnicodeDecodeError:
                    print(Fore.RED + "Erreur de décodage du payload HTTP/HTTPS")
            print(Style.RESET_ALL)
            print("-" * 60)
    except Exception as e:
        print(Fore.RED + f"Erreur lors de l'affichage du paquet: {str(e)}")
        print(Style.RESET_ALL)

# Fonction pour obtenir le nom du protocole
def get_protocol(proto):
    protocols = {1: "ICMP", 6: "TCP", 17: "UDP"}
    return protocols.get(proto, f"Autre (Code {proto})")

# Fonction pour démarrer la capture des paquets avec filtre IP
def start_sniffer(filter_expr):
    print(Fore.CYAN + """
⠀⠀⣤⡤⠀⣠⣤⣤⣤⣤⡤⠄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠋⣠⣾⣿⣿⡿⠛⣉⣤⣶⠀⠀⠀⣀⣠⣤⣤⣶⣶⠖⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⣾⣿⣿⡟⢋⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠋⣠⣿⠟⠉⠀⠀⠀⠀⠀⠀
⠀⣿⡿⢋⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠇⣼⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀
⠀⡟⢁⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⢠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣿⣿⣿⣿⣇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⣿⠇⢹⣿⣿⣿⣿⣿⣿⣿⣿⣿⡀⢻⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⣿⡆⠸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣄⡉⢻⣿⡏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠈⠉⠀⠙⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡏⠀⠀⢀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠈⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⠀⠀⢸⡇⠀⠀⢀⡀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠈⢿⣿⣿⣿⣿⣿⣿⣿⣿⡄⠀⠘⠀⠀⣴⣿⡿⠆⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠻⣿⣿⣿⣿⣿⡿⠛⠁⠀⠀⠀⠊⠉⠀⠀⢀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠹⣿⣿⣿⡏⠀⠀⣠⡇⠀⠀⠀⠀⠈⠙⠛⠀⠀⠀
⠀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣐⣶⣒⣀⣀⣀⠀
⠀⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠀
""")
    print(Fore.MAGENTA + "Démarrage de la capture des paquets... (Appuyez sur Ctrl+C pour arrêter)\n")
    seen_ips = set()  # Ensemble pour stocker les paires d'IP déjà affichées
    try:
        sniff(prn=lambda packet: display_packet(packet, seen_ips), store=0, filter=filter_expr)
    except KeyboardInterrupt:
        print(Fore.GREEN + "\nCapture des paquets arrêtée.")
    except Exception as e:
        print(Fore.RED + f"Erreur lors de la capture des paquets: {str(e)}")
        print(Style.RESET_ALL)

# Fonction pour construire le filtre avec IP source et destination
def build_filter(base_filter):
    ip_src = input(Fore.YELLOW + "Entrez l'IP source à filtrer (appuyez sur Entrée pour ignorer) : ")
    ip_dst = input(Fore.YELLOW + "Entrez l'IP destination à filtrer (appuyez sur Entrée pour ignorer) : ")
    if ip_src:
        base_filter += f" and src host {ip_src}"
    if ip_dst:
        base_filter += f" and dst host {ip_dst}"
    return base_filter

# Fonction pour afficher le menu
def show_menu():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(Fore.CYAN + """
  ____  _   _ ___ _____ _____ _____ ____  
 / ___|| \ | |_ _|  ___|  ___| ____|  _ \ 
 \___ \|  \| || || |_  | |_  |  _| | |_) |    Made By Vaidx ! 
  ___) | |\  || ||  _| |  _| | |___|  _ < 
 |____/|_| \_|___|_|   |_|   |_____|_| \_\
""")
    print(Fore.BLUE + "\n===== Menu de Capture de Paquets =====")
    print(Fore.BLUE + "1. Capturer tous les paquets IP")
    print(Fore.BLUE + "2. Capturer les paquets TCP")
    print(Fore.BLUE + "3. Capturer les paquets UDP")
    print(Fore.BLUE + "4. Capturer les paquets ICMP")
    print(Fore.BLUE + "5. Capturer les requêtes DNS")
    print(Fore.BLUE + "6. Capturer les paquets HTTP/HTTPS")
    print(Fore.BLUE + "7. Quitter")
    print(Style.RESET_ALL)

# Fonction pour gérer les choix du menu
def menu():
    while True:
        show_menu()
        choice = input(Fore.YELLOW + "Entrez votre choix : ")
        if choice == '1':
            start_sniffer("ip")
        elif choice == '2':
            start_sniffer("tcp")
        elif choice == '3':
            start_sniffer("udp")
        elif choice == '4':
            start_sniffer("icmp")
        elif choice == '5':
            filter_expr = build_filter("udp port 53 or tcp port 53")
            start_sniffer(filter_expr)
        elif choice == '6':
            filter_expr = build_filter("tcp port 80 or tcp port 443")
            start_sniffer(filter_expr)
        elif choice == '7':
            print(Fore.GREEN + "Sortie du programme.")
            break
        else:
            print(Fore.RED + "Choix invalide. Veuillez réessayer.")

if __name__ == "__main__":
    menu()
