@echo off

:: Set the console color to cyan text on black background
color 0B

:: Display a title for the script
title WinRAR Password Cracker

:: Check if WinRAR is installed
if not exist "C:\Program Files\WinRAR\" (
    echo [ERROR] WinRAR not installed!
    pause
    exit /b
)

:: Prompt for the archive full path
echo.
set /p archive="Enter Archive Full Path: "
echo.

:: Check if the archive exists
if not exist "%archive%" (
    echo [ERROR] Archive not found!
    pause
    exit /b
)

:: Prompt for the wordlist full path
set /p wordlist="Enter Wordlist Full Path: "
echo.

:: Check if the wordlist exists
if not exist "%wordlist%" (
    echo [ERROR] Wordlist not found!
    pause
    exit /b
)

:: Start the cracking process
echo [INFO] Starting password search...
echo.

:: Process each word in the wordlist
for /f "tokens=*" %%a in (%wordlist%) do (
    set "pass=%%a"
    call :attempt
)

:: Inform the user if no password was found
if %errorlevel% NEQ 0 (
    echo [ERROR] Shitty wordlist, no password found.
) else (
    echo [SUCCESS] Password Found: %pass%
)

pause
exit /b

:attempt
:: Attempt to extract the archive with the password
"C:\Program Files\WinRAR\WinRAR.exe" x -p%pass% "%archive%" -o"cracked" -y >nul 2>&1

:: Show the current password being tried
echo [INFO] Attempting: %pass%

:: Check if the password was correct
if /I %errorlevel% EQU 0 (
    exit /b
)
