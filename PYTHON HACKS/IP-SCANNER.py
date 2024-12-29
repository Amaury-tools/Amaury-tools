import requests
import subprocess
import socket
import sys
import ssl
import concurrent.futures
from requests.exceptions import RequestException
from colorama import Fore, Style, init

# Initialisation de Colorama
init(autoreset=True)

# Définition des couleurs
CYAN = Fore.CYAN
BLUE = Fore.BLUE
WHITE = Fore.WHITE
RED = Fore.RED
RESET = Style.RESET_ALL

# Fonctions pour afficher les messages d'erreur et autres
def Error(message):
    print(f"{RED}[ERROR] {WHITE}{message}{RESET}")

def current_time_hour():
    from datetime import datetime
    return datetime.now().strftime("%H:%M:%S")

def Slow(func):
    import time
    time.sleep(1)  # Simule un délai avant l'exécution de la fonction

def Continue():
    print(f"{CYAN}[INFO] {WHITE}Processus terminé, continuation...{RESET}")

def Reset():
    print(f"{CYAN}[INFO] {WHITE}Réinitialisation...{RESET}")

try:
    def ip_type(ip):
        if ':' in ip:
            type = "ipv6"
        elif '.' in ip:
            type = "ipv4"
        else:
            type = "Unknown"
            return
        
        print(f"{CYAN}[INFO] {WHITE}IP Type: {BLUE}{type}{RESET}")

    def ip_ping(ip):
        try:
            if sys.platform.startswith("win"):
                result = subprocess.run(['ping', '-n', '1', ip], capture_output=True, text=True, timeout=1)
            else:
                result = subprocess.run(['ping', '-c', '1', '-W', '1', ip], capture_output=True, text=True, timeout=1)
            if result.returncode == 0:
                ping = "Succeed"
            else:
                ping = "Fail"
        except:
            ping = "Fail"

        print(f"{CYAN}[INFO] {WHITE}Ping: {BLUE}{ping}{RESET}")

    def ip_port(ip):
        port_protocol_map = {
            21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP", 53: "DNS", 69: "TFTP",
            80: "HTTP", 110: "POP3", 123: "NTP", 143: "IMAP", 194: "IRC", 389: "LDAP",
            443: "HTTPS", 161: "SNMP", 3306: "MySQL", 5432: "PostgreSQL", 6379: "Redis",
            1521: "Oracle DB", 3389: "RDP"
        }

        port_list = [21, 22, 23, 25, 53, 69, 80, 110, 123, 143, 194, 389, 443, 161, 3306, 5432, 6379, 1521, 3389]

        def scan_port(ip, port):
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                result = sock.connect_ex((ip, port))
                if result == 0:
                    protocol = identify_protocol(ip, port)
                    print(f"{CYAN}[INFO] {WHITE}Port: {BLUE}{port}{RESET} Status: {WHITE}Open{RESET} Protocol: {BLUE}{protocol}{RESET}")
                sock.close()
            except:
                pass

        def identify_protocol(ip, port):
            try:
                if port in port_protocol_map:
                    return port_protocol_map[port]
                else:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(1)
                    sock.connect((ip, port))
                    
                    sock.send(b"GET / HTTP/1.1\r\nHost: {}\r\n\r\n".format(ip).encode('utf-8'))
                    response = sock.recv(100).decode('utf-8')
                    if "HTTP" in response:
                        return "HTTP"

                    sock.send(b"\r\n")
                    response = sock.recv(100).decode('utf-8')
                    if "FTP" in response:
                        return "FTP"

                    sock.send(b"\r\n")
                    response = sock.recv(100).decode('utf-8')
                    if "SSH" in response:
                        return "SSH"

                    return "Unknown"
            except:
                return "Unknown"

        with concurrent.futures.ThreadPoolExecutor() as executor:
            results = {executor.submit(scan_port, ip, port): port for port in port_list}
        concurrent.futures.wait(results)

    def ip_dns(ip):
        try:
            dns, aliaslist, ipaddrlist = socket.gethostbyaddr(ip)
        except:
            dns = "None"
        if dns != "None":
            print(f"{CYAN}[INFO] {WHITE}DNS: {BLUE}{dns}{RESET}")

    def ip_host_info(ip):
        api_url = f"https://ipinfo.io/{ip}/json"
        try:
            response = requests.get(api_url)
            api = response.json()
        except RequestException:
            api = {}

        host_country = api.get('country', 'None')
        if host_country != "None":
            print(f"{CYAN}[INFO] {WHITE}Host Country: {BLUE}{host_country}{RESET}")

        host_name = api.get('hostname', 'None')
        if host_name != "None":
            print(f"{CYAN}[INFO] {WHITE}Host Name: {BLUE}{host_name}{RESET}")

        host_isp = api.get('org', 'None')
        if host_isp != "None":
            print(f"{CYAN}[INFO] {WHITE}Host ISP: {BLUE}{host_isp}{RESET}")

        host_as = api.get('asn', 'None')
        if host_as != "None":
            print(f"{CYAN}[INFO] {WHITE}Host AS: {BLUE}{host_as}{RESET}")

    def ssl_certificate_check(ip):
        port = 443
        try:
            sock = socket.create_connection((ip, port), timeout=1)
            context = ssl.create_default_context()
            with context.wrap_socket(sock, server_hostname=ip) as ssock:
                cert = ssock.getpeercert()
                print(f"{CYAN}[INFO] {WHITE}SSL Certificate: {BLUE}{cert}{RESET}")
        except Exception as e:
            print(f"{CYAN}[INFO] {WHITE}SSL Certificate Check Failed: {BLUE}{e}{RESET}")


    print(Fore.CYAN + """
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⡀⠀⠀⠀⢀⣀⡠⠤⠴⠚⣿⠃
⠀⠸⣿⡭⣭⣿⣽⣿⣿⣿⣿⣿⣿⣿⣽⣿⡿⠓⠚⠉⣉⣀⣤⡤⣴⠀⣿⠀
⠀⠀⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⠀⢰⠞⢩⠀⢻⡏⠀⡏⠀⣿⠄
⠀⢠⣟⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⠀⢸⠀⢸⠀⢸⡇⠀⠃⠀⣿⠂
⠀⢘⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⠀⢸⠀⢸⠀⢸⡇⠀⡇⠀⣿⡇
⠀⠈⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⠀⢸⠀⢸⠀⢸⡇⠀⣷⠀⣿⡇
⠀⣠⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⠀⢸⠀⢸⠀⢸⡇⠀⣿⣼⣿⡇    Made By Vaidx ! 
⠀⡃⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⠀⠘⠛⠛⠒⠛⠓⠛⠛⣿⣿⡇
⠀⠀⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⠀⢰⠦⢠⠀⢤⣤⣤⣄⠋⣿⡇
⠀⠀⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⠀⢸⠀⢸⠀⢸⡇⠈⣿⠀⣿⡇
⠀⢸⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⠀⢸⠀⢸⠀⢸⡇⠀⣿⠀⣿⡇
⠀⠀⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⠀⢸⣄⢸⠠⣼⡇⠀⣿⠀⣿⡇
⠀⣸⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⠀⠀⠉⠉⠀⠛⠚⠯⠿⠀⣿⡇
⠠⢿⣿⣷⣶⣶⣶⠶⢶⡶⢶⣶⣶⣶⣶⢿⣶⣤⣄⣀⣀⠀⠀⠀⢨⠀⣿⡇
⠀⠀⠀⠈⠀⠐⠒⠒⠀⠀⠀⠘⠁⠈⠀⠀⠀⠀⠉⠉⢛⠉⠑⠒⠠⠤⢿⠇
""")
    ip = input(f"{CYAN}[INFO] {WHITE}Ip -> {RESET}")
    print(f"{CYAN}[INFO] {WHITE}Information Recovery..{RESET}")
    print(f"{CYAN}[INFO] {WHITE}Ip: {BLUE}{ip}{RESET}")
    ip_type(ip)
    ip_ping(ip)
    ip_dns(ip)
    ip_port(ip)
    ip_host_info(ip)
    ssl_certificate_check(ip)
    Continue()
    Reset()

    # Demande de sortie avant la fermeture du script
    input(f"{CYAN}[INFO] {WHITE}[*] Appuyer Sur Entrée Pour Quitter...{RESET}")

except Exception as e:
    Error(e)
