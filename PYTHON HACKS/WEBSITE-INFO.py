import socket
import concurrent.futures
import requests
from urllib.parse import urlparse
import ssl
import urllib3
from requests.exceptions import RequestException
import time
import re
import dns.resolver
from bs4 import BeautifulSoup
import whois
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# Disable SSL warnings for unverified requests
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Helper function to get the current time in hour
def current_time_hour():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())

# Helper function to print output in colored format
def print_output(label, value, color=Fore.CYAN):
    print(f"{color}[{current_time_hour()}] {label}: {value}{Style.RESET_ALL}")

def website_found_url(url):
    if not urlparse(url).scheme:
        website_url = "https://" + url
    else:
        website_url = url
    print_output("Website", website_url, Fore.BLUE)
    return website_url

def website_domain(website_url):
    parsed_url = urlparse(website_url)
    domain = parsed_url.netloc
    print_output("Domain", domain, Fore.BLUE)
    return domain

def website_ip(domain):
    try:
        ip = socket.gethostbyname(domain)
    except socket.gaierror:
        ip = "None"
    if ip != "None":
        print_output("IP", ip, Fore.BLUE)
    return ip

def ip_type(ip):
    if ':' in ip:
        ip_type = "ipv6"
    elif '.' in ip:
        ip_type = "ipv4"
    else:
        ip_type = "Unknown"
    print_output("IP Type", ip_type, Fore.BLUE)

def website_secure(website_url):
    secure = website_url.startswith("https://")
    print_output("Secure", secure, Fore.BLUE)

def website_status(website_url):
    try:
        response = requests.get(website_url, timeout=5)
        status_code = response.status_code
    except RequestException:
        status_code = 404
    print_output("Status Code", status_code, Fore.BLUE)

def ip_info(ip):
    api_url = f"https://ipinfo.io/{ip}/json"
    try:
        response = requests.get(api_url)
        api = response.json()
    except RequestException:
        api = {}

    host_country = api.get('country', 'None')
    if host_country != "None":
        print_output("Host Country", host_country, Fore.CYAN)

    host_name = api.get('hostname', 'None')
    if host_name != "None":
        print_output("Host Name", host_name, Fore.CYAN)

    host_isp = api.get('isp', 'None')
    if host_isp != "None":
        print_output("Host ISP", host_isp, Fore.CYAN)

    host_org = api.get('org', 'None')
    if host_org != "None":
        print_output("Host Org", host_org, Fore.CYAN)

    host_as = api.get('asn', 'None')
    if host_as != "None":
        print_output("Host AS", host_as, Fore.CYAN)

def website_port(ip):
    port_protocol_map = {
        21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP", 53: "DNS", 80: "HTTP", 443: "HTTPS"
    }

    port_list = [21, 22, 23, 25, 53, 80, 443]

    def scan_port(ip, port):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((ip, port))
            if result == 0:
                protocol = port_protocol_map.get(port, "Unknown")
                print_output(f"Port {port} Status", f"Open Protocol: {protocol}", Fore.CYAN)
            sock.close()
        except:
            pass

    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = {executor.submit(scan_port, ip, port): port for port in port_list}
    concurrent.futures.wait(results)

def http_headers(website_url):
    try:
        response = requests.get(website_url, timeout=5)
        headers = response.headers
        for header, value in headers.items():
            print_output(f"HTTP Header: {header}", value, Fore.CYAN)
    except RequestException:
        pass

def check_ssl_certificate(website_url):
    try:
        context = ssl.create_default_context()
        with context.wrap_socket(socket.socket(), server_hostname=urlparse(website_url).hostname) as sock:
            sock.settimeout(5)
            sock.connect((urlparse(website_url).hostname, 443))
            cert = sock.getpeercert()
        for key, value in cert.items():
            print_output(f"SSL Certificate Key: {key}", value, Fore.CYAN)
    except:
        pass

def check_security_headers(website_url):
    headers_of_interest = ['Content-Security-Policy', 'Strict-Transport-Security', 'X-Content-Type-Options', 'X-Frame-Options', 'X-XSS-Protection']
    try:
        response = requests.get(website_url, timeout=5)
        headers = response.headers
        for header in headers_of_interest:
            if header in headers:
                print_output(f"Security Header: {header}", headers[header], Fore.CYAN)
            else:
                print_output(f"Missing Security Header: {header}", "None", Fore.CYAN)
    except RequestException:
        pass

def analyze_cookies(website_url):
    try:
        response = requests.get(website_url, timeout=5)
        cookies = response.cookies
        for cookie in cookies:
            secure = 'Secure' if cookie.secure else 'Not Secure'
            httponly = 'HttpOnly' if cookie.has_nonstandard_attr('HttpOnly') else 'Not HttpOnly'
            print_output(f"Cookie: {cookie.name}", f"Secure: {secure}, HttpOnly: {httponly}", Fore.CYAN)
    except RequestException:
        pass

def check_redirections(website_url):
    try:
        response = requests.get(website_url, timeout=5, allow_redirects=True)
        if response.history:
            for resp in response.history:
                print_output(f"Redirection", f"URL: {resp.url} Status: {resp.status_code}", Fore.CYAN)
            print_output(f"Final URL", f"{response.url} Status: {response.status_code}", Fore.CYAN)
    except RequestException:
        pass

def analyze_dns(domain):
    try:
        result = dns.resolver.resolve(domain, 'A')
        for ipval in result:
            print_output(f"DNS A Record", ipval.to_text(), Fore.CYAN)

        try:
            result = dns.resolver.resolve(domain, 'MX')
            for exdata in result:
                print_output(f"DNS MX Record", exdata.exchange, Fore.CYAN)
        except dns.resolver.NoAnswer:
            print_output("DNS MX Record", "No MX record found", Fore.CYAN)

        try:
            result = dns.resolver.resolve(domain, 'TXT')
            for txtdata in result:
                print_output(f"DNS TXT Record", txtdata.to_text(), Fore.CYAN)
        except dns.resolver.NoAnswer:
            print_output("DNS TXT Record", "No TXT record found", Fore.CYAN)

        try:
            result = dns.resolver.resolve(domain, 'NS')
            for nsdata in result:
                print_output(f"DNS NS Record", nsdata.to_text(), Fore.CYAN)
        except dns.resolver.NoAnswer:
            print_output("DNS NS Record", "No NS record found", Fore.CYAN)

    except Exception as e:
        print(f"DNS Lookup Failed: {e}")


def analyze_whois(domain):
    try:
        whois_info = whois.whois(domain)
        if whois_info.registrar:
            print_output("WHOIS Registrar", whois_info.registrar, Fore.CYAN)
        if whois_info.creation_date:
            print_output("WHOIS Creation Date", whois_info.creation_date, Fore.CYAN)
        if whois_info.expiration_date:
            print_output("WHOIS Expiration Date", whois_info.expiration_date, Fore.CYAN)
        if whois_info.name_servers:
            print_output("WHOIS Name Servers", ', '.join(whois_info.name_servers), Fore.CYAN)
    except:
        pass

def analyze_website(url):
    print(f"{Fore.BLUE}Scanning website: {url}{Style.RESET_ALL}")
    website_url = website_found_url(url)
    domain = website_domain(website_url)
    ip = website_ip(domain)
    ip_type(ip)
    website_secure(website_url)
    website_status(website_url)
    ip_info(ip)
    website_port(ip)
    http_headers(website_url)
    check_ssl_certificate(website_url)
    check_security_headers(website_url)
    analyze_cookies(website_url)
    check_redirections(website_url)
    analyze_dns(domain)
    analyze_whois(domain)

if __name__ == "__main__":
    print(Fore.BLUE + r"""
            ______
         .-'      `-.
       .'            `.
      /                \
     ;                 ;`
     |  Made By Vaidx ! |;
     ;                 ;|
     \'               / ;
      '`.           .' /
       `.`-._____.-' .'
         / /`_____.-'
        / / /
       / / /
      / / /
     / / /
    / / /
   / / /   Educational Purposes Only !
  / / /
 / / /
/ / /
\/_/ 
""")
    url = input(Fore.CYAN + "[+] Enter the website URL : ")
    analyze_website(url)
    input(Fore.BLUE + "[*] Press Enter to exit...")
