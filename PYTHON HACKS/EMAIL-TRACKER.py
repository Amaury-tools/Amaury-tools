from bs4 import BeautifulSoup
import requests
import time
from colorama import init, Fore
import sys
import os

# Initialize colorama for colored output
init()

# Define the color codes for cyan and blue
CYAN = '\033[96m'
BLUE = '\033[94m'
RESET = '\033[0m'
GREEN = Fore.GREEN
RED = Fore.RED
YELLOW = Fore.YELLOW

user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"

# Helper function to handle HTTP request errors
def handle_request_error(response):
    error_messages = {
        "429": "Too Many Requests",
        "404": "Page Not Found",
        "400": "Bad Request",
        "401": "Unauthorized",
        "403": "Forbidden",
        "500": "Internal Server Error",
        "502": "Bad Gateway",
        "503": "Service Unavailable",
        "504": "Gateway Timeout"
    }

    return f"{CYAN}{error_messages.get(str(response.status_code), f'Error: {response.status_code}')}{RESET}"

# Function to simulate typing effect
def type_effect(text, delay=0.05):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()  # Move to the next line after the text

# Magnifying Glass Animation
def magnifying_glass_animation():
    frames = ['🔍', '🔎', '🔍', '🔎']
    for frame in frames:
        print(f"{CYAN}{frame} Scanning...{RESET}", end="\r")
        time.sleep(0.5)

# Check Instagram email availability
def Instagram(email):
    try:
        session = requests.Session()
        headers = {
            'User-Agent': user_agent,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Origin': 'https://www.instagram.com',
            'Connection': 'keep-alive',
            'Referer': 'https://www.instagram.com/'
        }

        response = session.get("https://www.instagram.com/accounts/emailsignup/", headers=headers)
        if response.status_code != 200:
            return handle_request_error(response)

        token = session.cookies.get('csrftoken')
        if not token:
            return f"{CYAN}Error: Token Not Found.{RESET}"

        headers["x-csrftoken"] = token
        headers["Referer"] = "https://www.instagram.com/accounts/emailsignup/"

        data = {"email": email}
        response = session.post("https://www.instagram.com/api/v1/web/accounts/web_create_ajax/attempt/", headers=headers, data=data)

        if response.status_code == 200:
            if "Another account is using the same email." in response.text or "email_is_taken" in response.text:
                return True
            return False
        return handle_request_error(response)
    except Exception as e:
        return f"{CYAN}Error: {e}{RESET}"

# Check other social media platforms similarly (similar functions for each platform)

def Google(email):
    try:
        session = requests.Session()
        response = session.get("https://accounts.google.com/signup/v2/webcreateaccount", params={"email": email})
        if response.status_code == 200:
            if "This email address is already taken" in response.text:
                return True
            return False
        return handle_request_error(response)
    except Exception as e:
        return f"{CYAN}Error: {e}{RESET}"

# Check GitHub email availability
def GitHub(email):
    try:
        session = requests.Session()
        response = session.get("https://github.com/join", params={"email": email})
        if response.status_code == 200:
            if "This email is already associated with an account" in response.text:
                return True
            return False
        return handle_request_error(response)
    except Exception as e:
        return f"{CYAN}Error: {e}{RESET}"

# Check Facebook email availability
def Facebook(email):
    try:
        session = requests.Session()
        response = session.get("https://www.facebook.com/r.php?email=" + email)
        if response.status_code == 200:
            if "This email is already in use" in response.text:
                return True
            return False
        return handle_request_error(response)
    except Exception as e:
        return f"{CYAN}Error: {e}{RESET}"

# Additional sites to check
def Pinterest(email):
    try:
        session = requests.Session()
        response = session.get(f"https://www.pinterest.com/_ngjs/resource/EmailExistsResource/get/?source_url=/&data={{\"options\":{{\"email\":\"{email}\"}},\"context\":{{}}}}")
        if response.status_code == 200:
            message = response.json()["resource_response"]["message"]
            if message == "Invalid email.":
                return False
            if message == "ok":
                return True
        return handle_request_error(response)
    except Exception as e:
        return f"{CYAN}Error: {e}{RESET}"

def LinkedIn(email):
    try:
        session = requests.Session()
        response = session.get(f"https://www.linkedin.com/uas/request-password-reset?email={email}")
        if response.status_code == 200:
            if "This email is already in use" in response.text:
                return True
            return False
        elif response.status_code == 999:
            return f"{RED}Error: CAPTCHA or rate-limiting triggered (Error 999). Please try again later.{RESET}"
        return handle_request_error(response)
    except Exception as e:
        return f"{CYAN}Error: {e}{RESET}"

def Snapchat(email):
    try:
        session = requests.Session()
        response = session.get(f"https://accounts.snapchat.com/accounts/signup?email={email}")
        if response.status_code == 200:
            if "This email address is already taken" in response.text:
                return True
            return False
        return handle_request_error(response)
    except Exception as e:
        return f"{CYAN}Error: {e}{RESET}"

def TikTok(email):
    try:
        session = requests.Session()
        response = session.get(f"https://www.tiktok.com/signup/email?email={email}")
        if response.status_code == 200:
            if "This email is already in use" in response.text:
                return True
            return False
        return handle_request_error(response)
    except Exception as e:
        return f"{CYAN}Error: {e}{RESET}"

def Spotify(email):
    try:
        session = requests.Session()
        response = session.get(f"https://www.spotify.com/signup/?email={email}")
        if response.status_code == 200:
            if "This email address is already in use" in response.text:
                return True
            return False
        return handle_request_error(response)
    except Exception as e:
        return f"{CYAN}Error: {e}{RESET}"

def Yahoo(email):
    try:
        session = requests.Session()
        response = session.get(f"https://login.yahoo.com/account/create?email={email}")
        if response.status_code == 200:
            if "This email is already taken" in response.text:
                return True
            return False
        return handle_request_error(response)
    except Exception as e:
        return f"{CYAN}Error: {e}{RESET}"

# Clear console function for better experience
def clear_console():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

# Main script execution
def main():
    try:
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
        email = input(f"{BLUE}[+] Enter email to check: {RESET}")
        print(Fore.CYAN + "==================================================")
        type_effect(f"{CYAN}[-] Scanning...{RESET}", delay=0.1)

        # Run magnifying glass animation for scanning
        magnifying_glass_animation()

        # Check each site
        results = {
            "Instagram": Instagram(email),
            "Google": Google(email),
            "GitHub": GitHub(email),
            "Facebook": Facebook(email),
            "Pinterest": Pinterest(email),
            "LinkedIn": LinkedIn(email),
            "Snapchat": Snapchat(email),
            "TikTok": TikTok(email),
            "Spotify": Spotify(email),
            "Yahoo": Yahoo(email),
        }

        print(Fore.CYAN + "==================================================")

        for site, result in results.items():
            if result == True:
                print(f"{GREEN}\nThe email is taken on {site}.{RESET}")
            elif result == False:
                print(f"{YELLOW}\nThe email is available on {site}.{RESET}")
            else:
                print(f"{RED}Error checking {site}: {result}{RESET}")

        print(Fore.CYAN + "==================================================")

        # Retry option for LinkedIn if error 999 occurs
        if 'Error: CAPTCHA or rate-limiting triggered' in results["LinkedIn"]:
            print(f"{YELLOW}\n[!] LinkedIn triggered rate-limiting. Retry after some time.")
            retry = input(f"{CYAN}[+] Would you like to retry LinkedIn? (Y/N): {RESET}")
            if retry.lower() == 'y':
                clear_console()
                main()

        input(f"{BLUE}Press Enter to exit...{RESET}")
    except KeyboardInterrupt:
        sys.stdout.write(Fore.CYAN)
        print("\n[!] Voulez-vous vraiment quitter ? (Y/N)", end=" ", flush=True)
        time.sleep(0.1)
        user_input = input().strip().lower()
        if user_input == 'y':
            print(RESET)
            print("Au revoir !")
            sys.exit(0)
        elif user_input == 'n':
            clear_console()
            main()

if __name__ == "__main__":
    main()
