# ================================
#           SETUP SCRIPT          
# ================================
# Script de configuration pour installer Python et les modules nécessaires

# Configurer l'encodage en UTF-8 pour éviter les problèmes de caractères
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8

# Définir une fonction pour afficher les messages avec des couleurs
function Write-HostGreen {
    param([string]$Message)
    Write-Host ([System.Text.Encoding]::UTF8.GetString([System.Text.Encoding]::Default.GetBytes($Message))) -ForegroundColor Green
}

function Write-HostRed {
    param([string]$Message)
    Write-Host ([System.Text.Encoding]::UTF8.GetString([System.Text.Encoding]::Default.GetBytes($Message))) -ForegroundColor Red
}

# Définir une fonction pour vérifier si une commande existe
function Command-Exists {
    param([string]$command)
    $null -ne (Get-Command $command -ErrorAction SilentlyContinue)
}

# Définir une fonction pour installer un module Python
function Install-PythonModule {
    param([string]$ModuleName)
    Write-HostGreen "Installation du module $ModuleName..."
    try {
        & pip install $ModuleName
        Write-HostGreen "Module $ModuleName installé avec succès."
    } catch {
        Write-HostRed "Erreur lors de l'installation du module $ModuleName. Vérifiez les erreurs ci-dessus."
    }
}

# Vérifier si Python est installé
function Check-PythonInstallation {
    if (Command-Exists "python") {
        $pythonVersion = & python --version 2>&1
        return $pythonVersion
    }
    return $null
}

# Installer Python via winget si ce n'est pas déjà installé
$pythonVersion = Check-PythonInstallation
if ($pythonVersion -eq $null -or $pythonVersion -eq '') {
    Write-HostRed "Python n'est pas installé. Installation de Python..."
    try {
        winget install --id Python.Python.3.10 -e --source winget
    } catch {
        Write-HostRed "Échec de l'installation de Python. Veuillez l'installer manuellement."
        exit
    }

    # Vérifier à nouveau l'installation de Python
    $pythonVersion = Check-PythonInstallation
    if ($pythonVersion -eq $null -or $pythonVersion -eq '') {
        Write-HostRed "Échec de l'installation de Python. Veuillez vérifier votre connexion internet ou installer Python manuellement."
        exit
    } else {
        Write-HostGreen "Python installé avec succès: $pythonVersion"
    }
} else {
    Write-HostGreen "Python est déjà installé: $pythonVersion"
}

# Liste des modules populaires à installer via pip
$popularModules = @(
    "colorama", "requests", "numpy", "pandas", "matplotlib", "scipy", 
    "seaborn", "tensorflow", "scikit-learn", "keras", "pillow", "flask", 
    "django", "beautifulsoup4", "lxml", "plotly", "pyqt5", "opencv-python", 
    "sympy", "pygame", "sqlalchemy", "boto3", "twisted", "scrapy", "cryptography", 
    "pyinstaller", "pytest", "tox", "celery", "jupyter", "ipython", "mock", "dash", 
    "click", "pyodbc", "mysql-connector-python", "slack_sdk", "pytorch", "fastapi", 
    "bottle", "web3", "apscheduler", "schedule", "pydantic", "pytest-django", 
    "hypothesis", "asgiref", "paramiko", "geopy", "gevent", "h5py", "nltk", "spacy", 
    "gspread", "openpyxl", "xlrd", "pyautogui", "wxPython", "jsonpickle", "xlwt", 
    "pyqrcode", "faker", "pytz", "python-dotenv", "redis", "ansible", "flake8"
)

# Liste des modules moins connus / rares
$rareModules = @(
    "fade", "pyfiglet", "termcolor", "progressbar2", "pyperclip", "watchdog", 
    "requests-html", "mechanize", "pexpect", "sqlalchemy-utils", "txtorcon", 
    "fabric", "schematics", "pluton", "pyttsx3", "cherrypy", "pytesseract", 
    "plotly-express", "loguru", "colorlog", "wxpython", "openai", "chatterbot", 
    "textblob", "fuzzywuzzy", "pyjokes", "googlesearch-python", "humanize", "whois", 
    "pillow-simd", "pikepdf", "pdfminer.six", "paramiko", "pyserial", "podman", 
    "pytz-deprecation-shim", "beautifulsoup4", "xlwings", "mpmath", "pygame", "graphene", 
    "sphinx", "reportlab", "pyspatial", "opencv-contrib-python", "pyodbc", "bottle", 
    "thonny", "keras-tuner", "retrying"
)

# Liste des modules ajoutés
$addedModules = @(
    "socket", "tkinter", "threading", "subprocess", "pprint", "bs4", "urllib3"
)

# Installer les modules populaires
foreach ($module in $popularModules) {
    Install-PythonModule -ModuleName $module
}

# Installer les modules moins connus
foreach ($module in $rareModules) {
    Install-PythonModule -ModuleName $module
}

# Installer les modules ajoutés
foreach ($module in $addedModules) {
    Install-PythonModule -ModuleName $module
}

Write-HostGreen "Tous les modules nécessaires ont été installés avec succès."

# Garder le script actif pour voir les messages
Read-Host -Prompt "Appuyez sur Entrée pour quitter le script"
