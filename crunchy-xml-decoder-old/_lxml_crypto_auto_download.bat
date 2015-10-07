@echo off
@setlocal EnableExtensions
rd /s /q temp 2>nul
rem call echo %%PROCESSOR_ARCHITECTURE:64=%%
rem pause

md temp
crunchy-xml-decoder\functtest.py Crypto_ 2>nul ||(set "Crypto_stat=not installed")
crunchy-xml-decoder\functtest.py lxml_ 2>nul ||(set "lxml_stat=not installed")
rem pause

for /f "tokens=1-9 skip=2" %%i in ('reg query HKEY_CLASSES_ROOT\Python.CompiledFile\shell\open\command /z /ve') do (
call :_python_dir1 %%i %%j %%k %%l %%m %%n %%o %%p %%q
)
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
call :download_ %%_ver%% %%_bit%% "%%Crypto_stat%%" "%%lxml_stat%%" %%PROCESSOR_ARCHITECTURE%% %%PROCESSOR_ARCHITECTURE:64=%%
pause
rd /s /q temp
goto :eof


:download_
rem echo Crypto %~3
rem echo lxml %~4
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
if %5 EQU %6 video-engine\7z.exe x -otemp\ temp\ 
if not %5 EQU %6 video-engine\7z_64.exe x -otemp\ temp\
rem move /Y .\temp\PLATLIB\Crypto .\crunchy-xml-decoder\
xcopy .\temp\PLATLIB\Crypto .\crunchy-xml-decoder\Crypto /E /C /H /R /Y 1>nul 2>nul
rem move /Y .\temp\PLATLIB\lxml .\crunchy-xml-decoder\
xcopy .\temp\PLATLIB\lxml .\crunchy-xml-decoder\lxml /E /C /H /R /Y 1>nul 2>nul
goto :eof

:_python_dir1
for /l %%i in (1,1,9) do (
call set temp_data=%%%%i
call set temp_data=%%temp_data:^(=%%
call set temp_data=%%temp_data:^)=%%
call :_python_dir2 %%temp_data%%
)
goto :eof

:_python_dir2
if not [%1] equ [] if not [%1] equ [""] copy %1 nul 1>nul 2>nul &&(call set python_p=%1)
goto :eof
