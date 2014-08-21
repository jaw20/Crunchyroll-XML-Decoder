@echo off
echo Starting proxy...
tasklist /FI "IMAGENAME eq privoxy.exe" 2>nul | find /I /N "privoxy.exe">nul
if "%ERRORLEVEL%"=="0" echo Privoxy is running
if "%ERRORLEVEL%"=="1" cd ".\proxy\" & start "" "privoxy.exe"
cd ..\
tasklist /FI "IMAGENAME eq tor.exe" 2>nul | find /I /N "tor.exe">nul
if "%ERRORLEVEL%"=="0" echo Tor is running
if "%ERRORLEVEL%"=="1" start "" ".\proxy\tor.exe" -f ".\proxy\torrc"
echo Proxy should be started now.
echo DO NOT CONTINUE UNTIL YOU HAVE FINISHED DOWNLOADING
pause
taskkill /IM "tor.exe"
taskkill /IM "privoxy.exe"