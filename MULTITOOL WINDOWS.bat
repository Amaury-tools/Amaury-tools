@echo off
chcp 65001 > nul
color 0B
cls

:: Activation des variables différées
setlocal enabledelayedexpansion

:: Couleurs pour les messages
set info=🔵
set success=🟢
set warning=🔴
set error=🔴

:: Vérification des privilèges administrateurs
net session >nul 2>&1 || goto :no_admin

:menu
cls
:: Affichage de la bannière
echo ===================================================
echo                 🔵 UTILITAIRE VAIDX 🔵
echo          Script Multi-Outils pour Windows
echo ===================================================
echo.
echo   [1] Connect to a Domain
echo   [2] Files Domain
echo   [3] Clean Up System Traces
echo   [4] Configure Remote Desktop (RDP)
echo   [5] ZIP Password Cracker
echo   [6] Remote Shutdown
echo   [7] Remote Disconnect
echo   [8] CMD Bypass
echo   [9] List Processes on Remote PC
echo   [10] Remote Computer Info
echo   [11] Exit
echo.
echo ===================================================
echo.
set /p choice="  [+] Choose an option: "

if "%choice%"=="1" goto connect
if "%choice%"=="2" goto files
if "%choice%"=="3" goto clear_traces
if "%choice%"=="4" goto RDP_sploit
if "%choice%"=="5" goto ZIP_CRACKER
if "%choice%"=="6" goto remote_shutdown
if "%choice%"=="7" goto remote_disconnect
if "%choice%"=="8" goto cmd_bypass
if "%choice%"=="9" goto list_processes
if "%choice%"=="10" goto remote_info
if "%choice%"=="11" exit
goto invalid

:connect
cls
echo ===================================================
echo                🔵 CONNECT TO A DOMAIN 🔵
echo ===================================================
echo.
echo  ╔════════════════════╗
echo  ║  Enter Domain      ║
echo  ╚════════════════════╝
set /p domain=">> "
echo.
echo  ╔════════════════════╗
echo  ║  Enter Username    ║
echo  ╚════════════════════╝
set /p username=">> "
echo.
echo  ╔════════════════════╗
echo  ║  Enter Password    ║
echo  ╚════════════════════╝
set /p password=">> "
echo.

:: Displaying connection attempt
echo.
echo 🔵 [+] Attempting to connect to %domain%...

:: Attempt to connect to the domain
net use \\%domain% /user:%username% %password%
if errorlevel 1 (
    echo.
    echo 🔴 [ERROR] Unable to connect to the domain. Please check the credentials and try again.
    pause
    goto menu
) else (
    echo.
    echo 🟢 [+] Connected successfully to %domain%.
    echo.
    
    :: Displaying message for remote shell launch
    echo 🔵 [+] Opening remote shell in a new window...
    
    rem Launching the remote shell in a new window (cmd)
    start cmd.exe /k "winrs -r:http://%domain%:5985/wsman -u:%username% -p:%password% cmd"

    echo.
    echo 🟢 [+] Remote shell opened successfully in a new window.
    echo.
)

pause
goto menu

:list_processes
cls
echo ===================================================
echo     🔵 LIST PROCESSES ON REMOTE PC 🔵
echo ===================================================
echo.
set /p domain=" [+] Enter the target PC name : "
set /p user=" [+] Enter the User PC name : "
set /p pass=" [+] Enter the Password : "
echo.

:: List processes using PowerShell
echo 🔵 [+] Listing processes on %domain%...
winrs -r:%domain% -u:%user% -p:%pass% tasklist
echo.
echo 🟢 [+] Processes listed successfully on %domain%.
pause
goto menu

:remote_info
cls
echo ===================================================
echo     🔵 REMOTE COMPUTER INFO 🔵
echo ===================================================
echo.
echo.
echo  ╔════════════════════╗
echo  ║  Enter Domain      ║
echo  ╚════════════════════╝
set /p domain=">> "
echo.
echo  ╔════════════════════╗
echo  ║  Enter Username    ║
echo  ╚════════════════════╝
set /p user=">> "
echo.
echo  ╔════════════════════╗
echo  ║  Enter Password    ║
echo  ╚════════════════════╝
set /p pass=">> "
echo.

echo %info% Connecting to %domain%...

rem Disconnect any existing connections
net use \\%domain% /user:%user% %pass% >nul 2>&1
rem Reconnect using SMB
net use \\%domain% /user:%user% %pass% >nul 2>&1

if /I "%errorlevel%" NEQ "0" (
  echo %warning% Invalid Credentials or Network Issue. Please check your details and network connection.
  pause
  goto start
)

echo %success% Connected!
echo.

echo 🔵 [+] Retrieving info for %domain%...
echo.
echo %info% Gathering System Information...
echo.
echo System Information:
echo ---------------------
echo Hostname: %domain%
winrs -r:%domain% -u:%user% -p:%pass% hostname
echo.
echo Operating System:
winrs -r:%domain% -u:%user% -p:%pass% systeminfo | findstr /B /C:"OS"
echo.
echo Memory Info:
winrs -r:%domain% -u:%user% -p:%pass% systeminfo | findstr /B /C:"Total Physical Memory"
echo.
echo Disk Info:
winrs -r:%domain% -u:%user% -p:%pass% powershell -Command "Get-WmiObject -Class Win32_DiskDrive | Select-Object Model, Size"
pause
goto menu

:files
cls
echo ===================================================
echo                 🔵 FILES DOMAIN 🔵
echo ===================================================
echo.
set /p "folder=  [+] Enter the domain folder path: "
echo.
echo 🔵 [+] Opening the requested folder...
start \\%folder%
echo.
echo 🟢 [+] Folder opened successfully.
pause
goto menu

:clear_traces
cls
echo ===================================================
echo            🔵 CLEAN UP SYSTEM TRACES 🔵
echo ===================================================
echo.
echo 🔵 [+] Cleaning up temporary files...
del /f /s /q "%temp%\*.*" >nul 2>&1
rmdir /s /q "%temp%" >nul 2>&1

echo 🔵 [+] Cleaning browser traces...
for %%b in ("Google\Chrome\User Data\Default\Cache" "Microsoft\Edge\User Data\Default\Cache" "Mozilla\Firefox\Profiles") do (
    del /f /s /q "%LOCALAPPDATA%\%%b\*.*" >nul 2>&1
    echo 🟢 Cleared %%b traces.
)

echo 🔵 [+] Cleaning recent files list...
del /f /s /q "%APPDATA%\Microsoft\Windows\Recent\*.*" >nul 2>&1

echo 🔵 [+] Cleaning event logs...
for /f "tokens=*" %%G in ('wevtutil el') do wevtutil cl "%%G" >nul 2>&1

echo.
echo 🟢 [+] System traces cleared successfully!
pause
goto menu

:RDP_sploit
cls
echo ===================================================
echo       🔵 CONFIGURE REMOTE DESKTOP (RDP) 🔵
echo ===================================================
echo.
echo 🔵 [+] Enabling Remote Desktop...
reg add "HKLM\SYSTEM\CurrentControlSet\Control\Terminal Server" /v fDenyTSConnections /t REG_DWORD /d 0 /f >nul 2>&1
echo.
echo 🟢 [+] Remote Desktop enabled successfully!
pause
goto menu

:ZIP_CRACKER
cls
echo ===================================================
echo             🔵 ZIP PASSWORD CRACKER 🔵
echo ===================================================
echo.
set /p "zipfile=  [+] Enter the ZIP file path: "
echo.
set /p "wordlist=  [+] Enter the wordlist path: "
echo.
echo 🔵 [+] Starting password cracking...
for /f %%p in (%wordlist%) do (
    echo Testing password: %%p
    unzip -P %%p %zipfile% >nul 2>&1 && echo 🟢 [+] Password found: %%p && pause && goto menu
)
echo.
echo 🔴 [ERROR] No password found in the wordlist.
pause
goto menu

:remote_shutdown
cls
echo ===================================================
echo              🔵 REMOTE SHUTDOWN 🔵
echo ===================================================
echo.
set /p "target_pc=  [+] Enter the target PC name: "
echo.
echo 🔵 [+] Sending shutdown command...
shutdown /s /m \\%target_pc% /f
if errorlevel 1 (
    echo.
    echo 🔴 [ERROR] Failed to shutdown %target_pc%.
) else (
    echo.
    echo 🟢 [+] Shutdown command sent to %target_pc%.
)
pause
goto menu

:remote_disconnect
cls
echo ===================================================
echo         🔵 DISCONNECT REMOTE SESSION 🔵
echo ===================================================
echo.
set /p "target_pc=  [+] Enter the target PC name: "
echo.
echo 🔵 [+] Disconnecting remote session...
tsdiscon /server:%target_pc% >nul 2>&1
if errorlevel 1 (
    echo.
    echo 🔴 [ERROR] Failed to disconnect session for %target_pc%.
) else (
    echo.
    echo 🟢 [+] Remote session disconnected for %target_pc%.
)
pause
goto menu

:cmd_bypass
cls
echo ===================================================
echo                🔵 CMD BYPASS 🔵
echo ===================================================
echo.
set /p "payload=  [+] Enter the payload (Leave blank for CMD.exe): "
if "%payload%"=="" (set "PAYLOAD=cmd.exe") else set "PAYLOAD=%payload%"

echo.
echo 🔵 [+] Attempting to execute payload...
powershell -c Start-Process "%PAYLOAD%" -Verb runas
echo.
echo 🟢 [+] CMD Bypass executed successfully!
pause
goto menu

:no_admin
cls
echo ===================================================
echo           🔴 [ERROR] NO ADMIN PRIVILEGES 🔴
echo ===================================================
echo.
echo 🔴 [ERROR] Administrator privileges are required to run this script.
pause
goto menu

:invalid
cls
echo ===================================================
echo           🔴 [ERROR] INVALID CHOICE 🔴
echo ===================================================
echo.
echo 🔴 [ERROR] Please select a valid option.
pause
goto menu
