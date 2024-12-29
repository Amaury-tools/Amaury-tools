import os
import sys
import socket
import subprocess
from win32com.client import Dispatch
from colorama import Fore, Style, init
import ctypes
import time

# Initialize colorama
init(autoreset=True)

def is_admin():
    """Check if the script is running with administrative privileges."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except:
        return False

def is_uac_bypass_vulnerable():
    """Check if the system is vulnerable to UAC bypass."""
    try:
        command = 'net session'
        result = subprocess.run(command, capture_output=True, text=True, shell=True)

        if result.returncode == 0:
            print(Fore.RED + "[❌] The system appears to be vulnerable to UAC bypass!")
            input(Fore.CYAN + "[+] Press any key to return to the main menu.")
            return True
        else:
            print(Fore.GREEN + "[✔️] The system seems to have UAC protections in place.")
            input(Fore.CYAN + "[+] Press any key to return to the main menu.")
            return False
    except Exception as e:
        print(Fore.RED + f"[❌] Error checking for UAC bypass vulnerability: {e}")
        input(Fore.CYAN + "[+] Press any key to return to the main menu.")
        return False

def check_smb_vulnerability():
    """Check if the system is vulnerable to EternalBlue (SMB vulnerability)."""
    try:
        command = 'powershell Get-WindowsFeature FS-SMB1'
        result = subprocess.run(command, capture_output=True, text=True, shell=True)
        
        if "Installed" in result.stdout:
            print(Fore.RED + "[❌] The system has SMB1 enabled, which is vulnerable to EternalBlue.")
        else:
            print(Fore.GREEN + "[✔️] SMB1 is disabled, no vulnerability to EternalBlue.")
        
        input(Fore.CYAN + "[+] Press any key to return to the main menu.")
    except Exception as e:
        print(Fore.RED + f"[❌] Error checking SMB vulnerability: {e}")
        input(Fore.CYAN + "[+] Press any key to return to the main menu.")

def check_open_ports():
    """Check for open ports (possible security risks)."""
    try:
        ip = '127.0.0.1'  # Localhost (can be changed to other IPs if needed)
        open_ports = []
        
        for port in range(1, 1025):  # Scanning the first 1024 ports (can be customized)
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = sock.connect_ex((ip, port))
            if result == 0:
                open_ports.append(port)
            sock.close()

        if open_ports:
            print(Fore.RED + "[❌] Open ports detected: " + ", ".join(map(str, open_ports)))
        else:
            print(Fore.GREEN + "[✔️] No open ports detected.")
        
        input(Fore.CYAN + "[+] Press any key to return to the main menu.")
    except Exception as e:
        print(Fore.RED + f"[❌] Error checking open ports: {e}")
        input(Fore.CYAN + "[+] Press any key to return to the main menu.")

def check_rdp_vulnerability():
    """Check if the system is vulnerable to Remote Desktop Protocol (RDP) attacks."""
    try:
        command = 'query user'
        result = subprocess.run(command, capture_output=True, text=True, shell=True)
        
        if "Active" in result.stdout:
            print(Fore.RED + "[❌] The system has active RDP sessions which can be a security risk.")
        else:
            print(Fore.GREEN + "[✔️] No active RDP sessions detected.")
        
        input(Fore.CYAN + "[+] Press any key to return to the main menu.")
    except Exception as e:
        print(Fore.RED + f"[❌] Error checking RDP vulnerability: {e}")
        input(Fore.CYAN + "[+] Press any key to return to the main menu.")

def create_shortcut():
    """Create a shortcut with UAC bypass."""
    if not is_admin():
        print(Fore.RED + "[❌] You need administrative privileges to create shortcuts.")
        return

    print(Fore.CYAN + "[+] Please enter the path to the program (e.g., C:\\Program Files (x86)\\yourprogram.exe):")
    program_path = input("   ➤ ")

    if not os.path.isfile(program_path):
        print(Fore.RED + "[❌] The provided path is not a valid file.")
        return
    
    shortcut_name = input(Fore.CYAN + "[+] Enter the name for the shortcut (e.g., Program Shortcut): ")
    desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
    shortcut_path = os.path.join(desktop_path, shortcut_name + ".lnk")

    shell = Dispatch('WScript.Shell')
    shortcut = shell.CreateShortcut(shortcut_path)
    shortcut.TargetPath = program_path
    shortcut.Arguments = ''
    shortcut.Description = 'Shortcut for ' + shortcut_name
    shortcut.WorkingDirectory = os.path.dirname(program_path)
    shortcut.Save()

    print(Fore.GREEN + f"[+] Shortcut created on Desktop: {shortcut_path}")

def delete_shortcut():
    """Delete a shortcut from the desktop."""
    if not is_admin():
        print(Fore.RED + "[❌] You need administrative privileges to delete shortcuts.")
        return
    
    print(Fore.CYAN + "[+] Please enter the name of the shortcut to delete (e.g., Program Shortcut):")
    shortcut_name = input("   ➤ ")
    desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
    shortcut_path = os.path.join(desktop_path, shortcut_name + ".lnk")

    if os.path.exists(shortcut_path):
        os.remove(shortcut_path)
        print(Fore.GREEN + f"[+] Shortcut deleted: {shortcut_path}")
    else:
        print(Fore.RED + "[❌] Shortcut not found on the desktop.")

def clear_screen():
    """Clear the console screen."""
    os.system('cls')  # Works on Windows

def main_menu():
    """Display the main menu."""
    while True:
        clear_screen()  # Clear screen after each action
        print(Fore.BLUE + """
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢾⣿⣿⠄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢘⡟⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡀⠀⢠⡿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣷⣾⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣾⣿⣿⣿⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣴⡿⢿⣿⣿⣿⣷⠀⠀⠀⠀⠀⠀⠀⠀⠀Made By Vaidx !⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⢀⡾⠋⠀⢈⣿⣿⣿⡿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠠⠤⡾⠁⠀⢀⣿⣿⣿⣿⣿⣆⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣾⣿⣿⡿⠿⣿⣿⣿⣿⣶⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⣠⣴⣾⡿⠟⠋⠁⠀⠀⠀⠈⠉⠛⠛⢿⣿⣦⣄⠀⠀⠀⠀⠀⠀
⠀⠀⠀⢀⣠⣾⡿⠛⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠛⢿⣷⣆⣀⠀⢀⡀
⢀⣤⣴⡿⠋⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠻⣿⠟⠋⠀
⠀⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
""")
        print(Fore.CYAN + "\n[+] Choose an option:")
        print(Fore.CYAN + "\n[1] Create a new shortcut")
        print(Fore.CYAN + "[2] Delete a shortcut")
        print(Fore.CYAN + "[3] Check if system is vulnerable to UAC bypass")
        print(Fore.CYAN + "[4] Check SMB vulnerability (EternalBlue)")
        print(Fore.CYAN + "[5] Check open ports")
        print(Fore.CYAN + "[6] Check RDP vulnerability")
        print(Fore.RED + "\n[7] Exit")
        choice = input("   ➤ ")

        if choice == '1':
            create_shortcut()
        elif choice == '2':
            delete_shortcut()
        elif choice == '3':
            clear_screen()
            is_uac_bypass_vulnerable()
        elif choice == '4':
            clear_screen()
            check_smb_vulnerability()
        elif choice == '5':
            clear_screen()
            check_open_ports()
        elif choice == '6':
            clear_screen()
            check_rdp_vulnerability()
        elif choice == '7':
            print(Fore.CYAN + "[+] Exiting...")
            sys.exit()
        else:
            print(Fore.RED + "[❌] Invalid option, please try again.")
            input(Fore.CYAN + "[+] Press any key to return to the main menu.")

# Start the main menu
main_menu()
