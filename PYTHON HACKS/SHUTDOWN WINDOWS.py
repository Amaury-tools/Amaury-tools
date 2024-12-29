import os
import subprocess
from colorama import Fore
# Define color codes for cyan and blue
CYAN = "\033[96m"
BLUE = "\033[94m"
RESET = "\033[0m"

# Print the menu with the blue theme
os.system('cls')
print(Fore.CYAN + """
 ______  __  __  __  __  ______ _____   ______  __     __  __   __    
/\  ___\/\ \_\ \/\ \/\ \/\__  _/\  __-./\  __ \/\ \  _ \ \/\ "-.\ \   
\ \___  \ \  __ \ \ \_\ \/_/\ \\ \ \/\ \ \ \/\ \ \ \/ ".\ \ \ \-.  \    Made By Vaidx  !
 \/\_____\ \_\ \_\ \_____\ \ \_\\ \____-\ \_____\ \__/".~\_\ \_\\"\_\ 
  \/_____/\/_/\/_/\/_____/  \/_/ \/____/ \/_____/\/_/   \/_/\/_/ \/_/
""")  
print(f"{CYAN}1. Shutdown Computer Immediately{RESET}")
print(f"{CYAN}2. Shutdown Computer after Given Time{RESET}")
print(f"{CYAN}3. Restart Computer Immediately{RESET}")
print(f"{CYAN}4. Restart Computer after Given Time{RESET}")
print(f"{CYAN}5. Lock My Computer Screen{RESET}")
print(f"{CYAN}6. Exit{RESET}")
print(end=f"{BLUE}Enter Your Choice: {RESET}")
choice = int(input())

# Handle the user choice
if choice == 1:
    os.system("shutdown /s /t 0")
elif choice == 2:
    print(end=f"{BLUE}Enter Number of Seconds: {RESET}")
    sec = int(input())
    strOne = "shutdown /s /t "
    strTwo = str(sec)
    str = strOne + strTwo
    os.system(str)
elif choice == 3:
    os.system("shutdown /r /t 0")
elif choice == 4:
    print(end=f"{BLUE}Enter Number of Seconds: {RESET}")
    sec = int(input())
    strOne = "shutdown /r /t "
    strTwo = str(sec)
    str = strOne + strTwo
    os.system(str)
elif choice == 5:
    subprocess.call('rundll32.exe user32.dll, LockWorkStation')
elif choice == 6:
    exit()
else:
    print(f"{CYAN}Wrong Choice!{RESET}")
