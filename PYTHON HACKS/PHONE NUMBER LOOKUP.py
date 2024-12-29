import phonenumbers
from phonenumbers import geocoder, carrier, timezone
import time
import sys
from colorama import Fore

# Définition des couleurs
cyan = '\033[96m'
blue = '\033[94m'
red = '\033[91m'
yellow = '\033[93m'
white = '\033[97m'
reset = '\033[0m'

# Définition des préfixes
BEFORE = f"{blue}[{reset}"
AFTER = f"{blue}]{reset}"
INFO = f"{yellow}[INFO]{reset}"
WAIT = f"{yellow}[WAIT]{reset}"
ERROR = f"{red}[ERROR]{reset}"
INFO_ADD = f"{cyan}[INFO]{reset}"
INPUT = f"{cyan}[INPUT]{reset}"


# Fonctions manquantes
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


def Slow(text):
    for c in text:
        sys.stdout.write(c)
        sys.stdout.flush()
        time.sleep(0.01)
    print()


# Début du programme
try:
    print(Fore.CYAN + """
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣀⠤⠤⠤⠀⠒⠒⠒⠒⠒⠒⠒⠒⠒⠀⠤⢤⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⠤⠔⠒⠉⠉⠀⢀⣀⡠⠤⠤⠒⠒⠒⣚⡋⠭⡉⠉⠉⠉⠉⠒⠚⠳⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⢀⡠⠔⠊⠉⠀⠀⣀⠤⠔⣒⣉⡉⠀⠀⠀⠀⢀⣀⣠⠏⢆⠀⠹⠀⠀⠀⠀⠀⠀⠀⠹⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⣀⠴⠊⠁⠀⢀⡠⠔⠊⠉⠀⠀⡟⡇⠀⢱⠔⠒⠊⠉⠉⠙⠢⣄⢸⠀⠀⡆⠀⠀⠀⠀⠀⠀⠀⣷⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⣼⠉⠓⣤⠔⠊⠁⠀⠀⢠⡀⢠⠞⠁⢠⠀⠘⡆⠀⠀⢀⣀⡠⠤⠤⠿⠓⠒⠛⠳⢶⣦⣤⣄⣤⣴⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⢰⣇⠀⠀⡏⠀⠀⠀⠀⠀⠀⠙⣇⠀⠀⠸⣄⠤⠓⠂⠉⠁⣀⡤⠤⠲⡶⣶⠒⠒⠤⠤⣀⡙⠲⣤⡴⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⢀⡞⠿⡙⡄⡇⠀⠀⠀⠀⠀⣠⡾⠛⠀⢀⠎⠀⠀⠀⢀⣴⠋⠛⢧⣤⠶⣟⣟⠛⣏⣲⢾⣤⡈⠑⠪⣳⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⡾⣍⠳⣷⠃⠀⠀⠀⣀⣤⡾⠋⠀⡸⢀⢏⠀⠀⠀⠀⣾⣟⡄⢰⡟⠨⡇⣼⡿⠛⠛⠻⢶⣇⠈⠳⣄⠈⠻⣷⡀⠀⠀⠀⠀⠀⠀⠀⠀ Made By Vaidx ! 
⠀⡗⠦⣳⣿⠛⠛⠛⠛⠋⠁⠀⣠⠾⠖⠋⠈⠣⡀⠀⢰⣀⠀⠀⣇⡨⠭⡉⡇⡄⠀⠀⠀⠀⢹⢱⣀⣈⣦⡔⡜⡟⢦⡀⠀⠀⠀⠀⠀⠀
⠰⣯⣙⣾⡉⠳⡶⠀⠒⠒⠊⠉⠀⠀⠀⠀⠀⠀⠘⢄⠀⣟⡖⠆⠸⣌⣲⠧⡘⠮⣒⠤⠤⠤⣊⠜⡟⠫⣽⠻⠇⢸⠀⠳⣄⠀⠀⠀⠀⠀
⠀⣷⢒⣺⣇⠀⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢢⠘⢆⢀⡀⠈⠫⣖⠂⡖⠲⡉⡩⢍⣰⡒⡮⢠⠟⠠⢄⣾⠀⠀⠘⢆⠀⠀⠀⠀
⠀⢹⣁⠤⠿⣶⣟⣦⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠱⡌⠳⣟⠇⠀⠀⠙⠚⠭⠤⠽⠶⠥⠴⠚⢁⠀⠀⣾⠏⠀⠀⠀⠈⢧⡀⠀⠀
⠀⠀⠹⣖⣋⠭⢿⣮⣉⠛⢦⣀⠀⠀⡀⠀⠀⠀⠀⠀⠀⠀⠘⢄⠀⠙⠢⢜⣺⢷⠀⠀⠀⣴⣄⡀⠀⣸⡿⠟⠁⠀⠀⢠⣤⣄⠀⢳⠀⠀
⠀⠀⠀⠙⠳⣖⣩⠔⣩⠛⡿⠋⡟⢻⠙⡆⠀⠀⠀⠀⠀⠀⠀⠈⢦⠀⠀⠀⠀⠉⠑⠒⠒⠛⠛⠛⠉⣁⣀⠀⡞⠛⡆⠘⠧⣞⣀⠬⢧⠀
⠀⠀⠀⠀⠀⠀⠉⠒⠣⠴⠇⠼⠥⠮⠼⠳⣄⡀⠀⠀⠀⠀⠀⠀⠀⢣⠀⠀⠀⠀⣀⣀⠀⢰⠶⡆⠀⠧⠸⢀⣈⠭⠔⠒⠉⠁⠀⠀⠘⡄
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⠦⣄⠀⠀⠀⠀⠀⠀⠳⡀⠀⠀⠯⠹⠀⢈⣚⠥⠄⠒⠉⠁⠀⠀⠀⠀⠀⣀⣠⠤⢶⡃
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠓⢦⣀⠀⠀⠀⠀⢡⠀⠠⠤⠒⠋⠁⠀⠀⠀⠀⠀⢀⣀⠤⠖⠚⠋⠥⠤⠤⠚⠁
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠳⠤⠀⠀⢈⡆⠀⠀⠀⠀⠀⠀⡤⡤⠒⠋⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
""")
    phone_number = input(f"\n{BEFORE + current_time_hour() + AFTER} {INPUT} Phone Number -> {white}")
    print(f"{BEFORE + current_time_hour() + AFTER} {WAIT} Information Recovery..{reset}")
    try:
        # Analyse et validation du numéro
        parsed_number = phonenumbers.parse(phone_number, None)
        status = "Valid" if phonenumbers.is_valid_number(parsed_number) else "Invalid"

        # Code du pays
        if phone_number.startswith("+"):
            country_code = "+" + phone_number[1:3]
        else:
            country_code = "None"

        # Opérateur
        try:
            operator = carrier.name_for_number(parsed_number, "fr")
        except:
            operator = "None"

        # Type de numéro
        try:
            type_number = "Mobile" if phonenumbers.number_type(parsed_number) == phonenumbers.PhoneNumberType.MOBILE else "Fixe"
        except:
            type_number = "None"

        # Fuseau horaire
        try:
            timezones = timezone.time_zones_for_number(parsed_number)
            timezone_info = timezones[0] if timezones else "None"
        except:
            timezone_info = "None"

        # Pays
        try:
            country = phonenumbers.region_code_for_number(parsed_number)
        except:
            country = "None"

        # Région
        try:
            region = geocoder.description_for_number(parsed_number, "fr")
        except:
            region = "None"

        # Formatage du numéro
        try:
            formatted_number = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.NATIONAL)
        except:
            formatted_number = "None"

        # Affichage des résultats
        print(f"""
    {INFO_ADD} Phone        : {white}{phone_number}{reset}
    {INFO_ADD} Formatted    : {white}{formatted_number}{reset}
    {INFO_ADD} Status       : {white}{status}{reset}
    {INFO_ADD} Country Code : {white}{country_code}{reset}
    {INFO_ADD} Country      : {white}{country}{reset}
    {INFO_ADD} Region       : {white}{region}{reset}
    {INFO_ADD} Timezone     : {white}{timezone_info}{reset}
    {INFO_ADD} Operator     : {white}{operator}{reset}
    {INFO_ADD} Type Number  : {white}{type_number}{reset}
        """)
        Continue()
        Reset()

    except:
        print(f"{BEFORE + current_time_hour() + AFTER} {INFO} Invalid Format !")
        Continue()
        Reset()

except Exception as e:
    Error(e)
