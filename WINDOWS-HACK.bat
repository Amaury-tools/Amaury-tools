@echo off
cd files >nul
mode 100, 30
color 0B
title PsExec
set success=[92m[+][0m
set warning=[91m[!][0m
set info=[94m[*][0m
set servicename=winrm%random%

:start
cls
chcp 65001 >nul
call :banner

:input_section
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

:menu
cls
call :banner
echo.
echo %info% Connected to %domain%
echo.
echo [95m[1][0m » Shell
echo [95m[2][0m » Files
echo [95m[3][0m » Information
echo [95m[4][0m » Shutdown
echo [95m[5][0m » Disconnect
echo [95m[6][0m » Run Application
echo [95m[7][0m » Start Service
echo [95m[8][0m » Kill Process
echo [95m[9][0m » Reboot Remote Machine
echo [95m[10][0m » List Running Processes
echo [95m[11][0m » Delete Specific File
echo [95m[12][0m » Rickroll the User
echo [95m[13][0m » Edit Remote Text File
echo [95m[14][0m » Capture Screenshot
echo [95m[15][0m » Send Message
echo.
set /p "option=[+] Choose an option : "

if "%option%" == "1" (
  cls
  echo.
  echo %success% Opening Remote Shell...
  echo.
  rem Opens remote cmd with WinRS
  winrs -r:%domain% -u:%user% -p:%pass% cmd
  goto menu
)

if "%option%" == "2" (
  cls
  echo.
  echo %info% Opening File Share...
  start "" "\\%domain%\C$"
  cls
  goto menu
)

if "%option%" == "3" (
  cls
  echo.
  echo %info% Gathering System Information...
  copy "info.bat" "\\%domain%\C$\ProgramData\info.bat" >nul
  winrs -r:%domain% -u:%user% -p:%pass% C:\ProgramData\info.bat
  pause
  del "\\%domain%\C$\ProgramData\info.bat"
  goto menu
)

if "%option%" == "4" (
  cls
  echo.
  echo %info% Initiating Shutdown...
  winrs -r:%domain% -u:%user% -p:%pass% "shutdown /s /f /t 0"
  goto menu
)

if "%option%" == "5" (
  cls
  echo.
  echo %info% Disconnecting...
  net use \\%domain% /d /y >nul 2>&1
  goto start
)

if "%option%" == "6" (
  cls
  echo.
  set /p "app=[+] Enter Application Path (e.g., C:\\Windows\\System32\\notepad.exe) : "
  echo %info% Running Application...
  winrs -r:%domain% -u:%user% -p:%pass% %app%
  goto menu
)

if "%option%" == "7" (
  cls
  echo.
  set /p "svc=[+] Enter Service Name to Start : "
  echo %info% Starting Service...
  winrs -r:%domain% -u:%user% -p:%pass% "sc start %svc%"
  goto menu
)

if "%option%" == "8" (
  cls
  echo.
  set /p "pid=[+] Enter Process ID to Kill : "
  echo %info% Killing Process...
  winrs -r:%domain% -u:%user% -p:%pass% "taskkill /PID %pid% /F"
  goto menu
)

if "%option%" == "9" (
  cls
  echo.
  echo %info% Rebooting Remote Machine...
  winrs -r:%domain% -u:%user% -p:%pass% "shutdown /r /f /t 0"
  goto menu
)

if "%option%" == "10" (
  cls
  echo.
  echo %info% Listing Running Processes...
  winrs -r:%domain% -u:%user% -p:%pass% "tasklist"
  pause
  goto menu
)

if "%option%" == "11" (
  cls
  echo.
  set /p "filepath=[+] Enter Full File Path to Delete : "
  echo %info% Deleting File...
  winrs -r:%domain% -u:%user% -p:%pass% "del /F /Q \"%filepath%\""
  goto menu
)

if "%option%" == "12" (
  cls
  echo.
  echo %info% Rickrolling the User...
  winrs -r:%domain% -u:%user% -p:%pass% "start https://www.youtube.com/watch?v=dQw4w9WgXcQ"
  goto menu
)

if "%option%" == "13" (
  cls
  echo.
  set /p "editfile=[+] Enter Full Path of Text File to Edit : "
  echo %info% Opening File for Editing...
  winrs -r:%domain% -u:%user% -p:%pass% "notepad \"%editfile%\""
  goto menu
)

if "%option%" == "14" (
  cls
  echo.
  echo %info% Capturing Screenshot...
  winrs -r:%domain% -u:%user% -p:%pass% "powershell -Command \"Add-Type -TypeDefinition 'using System;using System.Drawing;using System.Windows.Forms;public class Screenshot{public static void Capture() {Bitmap bmp = new Bitmap(Screen.PrimaryScreen.Bounds.Width, Screen.PrimaryScreen.Bounds.Height);Graphics g = Graphics.FromImage(bmp);g.CopyFromScreen(0, 0, 0, 0, bmp.Size);bmp.Save('C:\\Temp\\screenshot.png');}}' -TypeName Screenshot;[Screenshot]::Capture()\""
  goto menu
)

if "%option%" == "15" (
  cls
  echo.
  set /p "message=[+] Enter Message to Send : "
  echo %info% Sending Message to User...
  winrs -r:%domain% -u:%user% -p:%pass% "powershell -Command \"[System.Windows.Forms.MessageBox]::Show('%message%', 'Message from %user%')\""
  goto menu
)

:banner
echo.
echo  ⠀⠀⠀⣤⣴⣾⣿⣿⣿⣿⣿⣶⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⡄
echo  ⠀⠀⢀⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⢰⣦⣄⣀⣀⣠⣴⣾⣿⠃
echo  ⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⡏⠀⠀⣼⣿⣿⣿⣿⣿⣿⣿⣿⠀
echo  ⠀⠀⣼⣿⡿⠿⠛⠻⠿⣿⣿⡇⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⡿⠀
echo  ⠀⠀⠉⠀⠀⠀⢀⠀⠀⠀⠈⠁⠀⢰⣿⣿⣿⣿⣿⣿⣿⣿⠇⠀
echo  ⠀⠀⣠⣴⣶⣿⣿⣿⣷⣶⣤⠀⠀⠀⠈⠉⠛⠛⠛⠉⠉⠀⠀⠀
echo  ⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⣶⣦⣄⣀⣀⣀⣤⣤⣶⠀⠀
echo  ⠀⣾⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⢀⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀
echo  ⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⠁⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⠁⠀
echo  ⠀⢠⣿⡿⠿⠛⠉⠉⠉⠛⠿⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀
echo  ⠀⠘⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠻⢿⣿⣿⣿⣿⣿⠿⠛⠀⠀
echo.
echo  Made By Vaidx!
echo.
