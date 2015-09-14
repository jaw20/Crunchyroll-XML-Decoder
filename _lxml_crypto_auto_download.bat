@echo off
rd /s /q temp 2>nul
md temp
crunchy-xml-decoder\functtest.py Crypto_ 2>nul ||(set "Crypto_stat=not installed")
crunchy-xml-decoder\functtest.py lxml_ 2>nul ||(set "lxml_stat=not installed")
rem pause

for /f "tokens=4" %%i in ('reg query HKEY_CLASSES_ROOT\Python.CompiledFile\shell\open\command /z /ve') do set python_p=%%i
rem set python_p="C:\Python33\New folder (2)\python.exe"
set python_p
rem pause
rem goto :eof
rem for /f "tokens=1,9" %%i in ('call %%python_p%% -c "import platform, sys;v=sys.version;print v"') do (
for /f "tokens=1,9" %%i in ('call %%python_p%% -c "import platform, sys;print(sys.version)"') do (
rem echo %%i,%%j 
set _ver=%%i
set _bit=%%j
call set _ver=%%_ver:~0,-2%%
)
call echo %%_ver%%,%%_bit%%
rem set "Crypto_stat=installed"
rem set "lxml_stat=installed"
call :download_ %%_ver%% %%_bit%% "%%Crypto_stat%%" "%%lxml_stat%%"
pause
rd /s /q temp
goto :eof


:download_
echo %~3
echo %~4
if %2==32 (
if %1==2.6 set lxml_get=https://pypi.python.org/packages/2.6/l/lxml/lxml-3.2.5.win32-py2.6.exe#md5=f93ea5c1bf9b72bdd8acbd72c794b1b5
if %1==2.7 set lxml_get=https://pypi.python.org/packages/2.7/l/lxml/lxml-3.2.5.win32-py2.7.exe#md5=00536d2ff2b5e9e0b221a936b6fff169
if %1==3.2 set lxml_get=https://pypi.python.org/packages/3.2/l/lxml/lxml-3.2.5.win32-py3.2.exe#md5=57479eea394d44c5ac0c66e383201029
if %1==2.6 set crypto_get=http://www.voidspace.org.uk/downloads/pycrypto26/pycrypto-2.6.win32-py2.6.exe
if %1==2.7 set crypto_get=http://www.voidspace.org.uk/downloads/pycrypto26/pycrypto-2.6.win32-py2.7.exe
if %1==3.2 set crypto_get=http://www.voidspace.org.uk/downloads/pycrypto26/pycrypto-2.6.win32-py3.2.exe
if %1==3.3 set crypto_get=http://www.voidspace.org.uk/downloads/pycrypto26/pycrypto-2.6.win32-py3.3.exe
)
if %2==64 (
if %1==2.6 set lxml_get=https://pypi.python.org/packages/2.6/l/lxml/lxml-3.2.5.win-amd64-py2.6.exe#md5=90d59a70db1ab0bce2425d0de2aaa0da
if %1==2.7 set lxml_get=https://pypi.python.org/packages/2.7/l/lxml/lxml-3.2.5.win-amd64-py2.7.exe#md5=4382f7e29ef288e60975017dcd2cf361
if %1==2.6 set crypto_get=http://www.voidspace.org.uk/downloads/pycrypto26/pycrypto-2.6.win-amd64-py2.6.exe
if %1==2.7 set crypto_get=http://www.voidspace.org.uk/downloads/pycrypto26/pycrypto-2.6.win-amd64-py2.7.exe
if %1==3.2 set crypto_get=http://www.voidspace.org.uk/downloads/pycrypto26/pycrypto-2.6.win-amd64-py3.2.exe
if %1==3.3 set crypto_get=http://www.voidspace.org.uk/downloads/pycrypto26/pycrypto-2.6.win-amd64-py3.3.exe
)
if %3=="not installed" call video-engine\wget.exe -c --no-check-certificate -O "temp\lxml.exe" %%lxml_get%%
if %4=="not installed" call video-engine\wget.exe -c --no-check-certificate -O "temp\crypto.exe" %%crypto_get%%
rem if %3=="not installed" call copy ..\lxml\%%lxml_get:~44,-37%% "temp\lxml.exe"
rem if %4=="not installed" call copy ..\lxml\%%crypto_get:~49%% "temp\crypto.exe"
video-engine\7z.exe x -otemp\ temp\ 1>nul 2>nul
move /Y temp\PLATLIB\Crypto crunchy-xml-decoder\ 1>nul 2>nul
move /Y temp\PLATLIB\lxml crunchy-xml-decoder\ 1>nul 2>nul
goto :eof

