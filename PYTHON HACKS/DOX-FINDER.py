import webbrowser
import time
import sys
from colorama import Fore

# Définition des couleurs
cyan = '\033[96m'
blue = '\033[94m'
red = '\033[91m'
yellow = '\033[93m'
white = '\033[97m'
green = '\033[92m'
reset = '\033[0m'

# Définition des préfixes
BEFORE = f'{blue}[{white}'
AFTER = f'{blue}]'

BEFORE_GREEN = f'{green}[{white}'
AFTER_GREEN = f'{green}]'

INPUT = f'{BEFORE}>{AFTER} |'
INFO = f'{BEFORE}!{AFTER} |'
ERROR = f'{BEFORE}x{AFTER} |'
ADD = f'{BEFORE}+{AFTER} |'
WAIT = f'{BEFORE}~{AFTER} |'

# Fonctions utilitaires
def current_time_hour():
    return time.strftime("%H:%M:%S")

def Error(msg):
    print(f"{BEFORE}ERROR{AFTER} {red}{msg}{reset}")
    sys.exit(1)

def Continue():
    input(f"{BEFORE}INFO{AFTER} {blue}[Appuyez sur Entrée pour continuer...]{reset}")

def Reset():
    print(f"{BEFORE}INFO{AFTER} {yellow}[Réinitialisation du programme...]{reset}")
    time.sleep(1)
    sys.exit(0)

def Censored(text):
    print(f"{BEFORE}INFO{AFTER} Recherche pour: {white}{text}{reset}")
    time.sleep(1)

def Slow(text):
    for c in text:
        sys.stdout.write(c)
        sys.stdout.flush()
        time.sleep(0.01)
    print()

# Menu principal
try:
    print(Fore.CYAN + r"""
                  .:+*#%%#####*++++-.             
                :#%%*+*+-.....                    
             .=%%+++:..                           
           .=%#++=.                               
          -%%+++.                                 
      .  =%%++-          ....                     
      #%+#%++=.        .:#%%%*:                   
      :#@%#+=          :*+:-*%#:                  
       .*@@#.         .-%*::-%%#.                 
        .-%@@%-.      .=%%--%%%-                  
          .:--=*+-:.:-#%%%%%%%%*.                  
               .:-*#%%%%%%%%%%%%%-                
                  .+%%%*+*%%%%%%%%+...            
                  .+%@@%%%%*#%%%%%%%%%*-.         
                   .*%@%%%%%%%%%%%%%%%%%#-.       
                   .*%%%%%%%%%%%+#%%%%%%%%%*-.          Made By Vaidx ! 
                  .=%%%%%%%%%%%%@%*%%%%%####=-==  
                  :*%%%%%%%%%%%%%%%*#%%%%#+=-==+  
                 .+=*%#%%%%%%%%%%%%%**%%#+**+-:-  
                .-=::*-%%%%%%%%%%%%###*-*%###+:   
                ...:..%%%%%%%%%%%%%%#:=*+-:.      
                     *%%%%%%%%%%%%%%%%.           
                    :#%%%%%%%%%%%%%%%%+           
                   .*%%%%%%%%%%%%%%%%%#.          
                  .=%%%%%%%%%%%%%%%%%%#:          
                  .+%%%%%%%%%%%%%%%%%%%*.         
                    :+*#%%%@%%%%%%%%%%%%#:.       
                      ..:==+*#%#*=-:.:-+***:  

[00] Back
[01] Username
[02] LastName, FirstName
[03] Other
    """)

    search_type = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Search Type -> {reset}")

    if search_type in ['00', '0']:
        Reset()

    if search_type in ['01', '1']:
        search = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Username -> {reset}")
        Censored(search)

    elif search_type in ['02', '2']:
        name = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} LastName -> {reset}")
        first_name = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} FirstName -> {reset}")
        search = f"{name} {first_name}"  # Update the search variable
        Censored(search)

    elif search_type in ['03', '3']:
        search = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Search -> {reset}")
        Censored(search)

    else:
        Error("Choix invalide!")

    while True:
        print(f"""
[00] Back
[01] Facebook
[02] YouTube
[03] Twitter
[04] TikTok
[05] PeekYou
[06] Tumblr
[07] PagesJaunes
        """)

        choice = input(f"{BEFORE + current_time_hour() + AFTER} {INPUT} Site -> {reset}")

        if choice in ['0', '00']:
            Reset()

        sites = {
            '01': f"https://www.facebook.com/search/top/?q={search}",
            '02': f"https://www.youtube.com/results?search_query={search}",
            '03': f"https://twitter.com/search?q={search}",
            '04': f"https://www.tiktok.com/search?q={search}",
            '05': f"https://www.peekyou.com/{search}",
            '06': f"https://www.tumblr.com/search/{search}",
            '07': f"https://www.pagesjaunes.fr/pagesblanches/recherche?quoiqui={search}"
        }

        if choice in sites.keys():
            webbrowser.open(sites[choice])
        else:
            Error("Choix invalide!")

except Exception as e:
    Error(str(e))
