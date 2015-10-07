@ECHO off
if "%1"=="debug" (
echo debuging
call "%~dpf0" debuging 2>&1|video-engine\tee.exe -a debug.c.log

goto :eof
)
IF "%1"=="debuging" ECHO on
@md export 2>nul
@setlocal EnableExtensions
rem Crunchyroll Export Script DX - Last Updated 2015/02/09
rem Removes need for rtmpExplorer
rem ORIGINAL SOURCE - http://www.darkztar.com/forum/showthread.php?219034-Ripping-videos-amp-subtitles-from-Crunchyroll-%28noob-friendly%29
if not exist cookies call :_make_cookies
call :_lxml_crypto_auto_download "%~1"
:_check_settings_file
copy settings.ini nul 1>nul 2>nul ||(
echo [SETTINGS]>settings.ini
echo # Set this to the preferred quality. Possible values are: "android" ^(hard-subbed^), "360p", "480p", "720p", "1080p", or "highest" for highest available.>>settings.ini
echo # Note that any quality higher than 360p still requires premium, unless it's available that way for free ^(some first episodes^).>>settings.ini
echo # We're not miracle workers.>>settings.ini
echo video_quality = highest>>settings.ini
echo:>>settings.ini
echo # Set this to the desired subtitle language. If the subtitles aren't available in that language, it reverts to the second language option ^(below^).>>settings.ini
echo # Available languages: English, Espanol, Espanol_Espana, Francais, Portugues, Turkce, Italiano, Arabic, Deutsch>>settings.ini
echo language = English>>settings.ini
echo:>>settings.ini
echo # If the first language isn't available, what language would you like as a backup? Only if then they aren't found, then it goes to English as default>>settings.ini
echo language2 = English>>settings.ini
echo:>>settings.ini
echo # Set this if you want to use --forced-track rather than --default-track for subtitle>>settings.ini
echo forcesubtitle = False>>settings.ini
echo # Set this if you want to use a US session ID>>settings.ini
echo forceusa = False>>settings.ini
)
:_starthere
echo ____________________________________

if "%2"=="" (set epnum=1) else (set epnum=%2)
if "%3"=="" (set seasonnum=1) else (set seasonnum=%3)
IF not "%1"=="" (
	IF not "%1"=="debuging" (
	SET video_url=%1
	) else (
	ECHO Please Enter CrunchyRoll Video URL or Function (c,cookies,s,subs-only,q,queue^)
	SET /p video_url=
	)
) else (
ECHO Please Enter CrunchyRoll Video URL or Function (c,cookies,s,subs-only,q,queue^)
SET /p video_url=
)
if /I "%video_url%" EQU "c" call :_make_cookies & goto :_starthere
if /I "%video_url%" EQU "cookies" call :_make_cookies & goto :_starthere
if /I "%video_url%" EQU "s" goto :SETUP
if /I "%video_url%" EQU "subs-only" goto :SETUP
if /I "%video_url%" EQU "q" goto :_run_queue_list
if /I "%video_url%" EQU "queue" goto :_run_queue_list
if not [%1]==[debuging] (
call ".\crunchy-xml-decoder\ultimate.py" %video_url% %epnum% %seasonnum%
) else (
call ".\crunchy-xml-decoder\debug.py"  %video_url% %epnum% %seasonnum%
) 
pause
GOTO :eof
rem Function
:_run_queue_list
copy queue.txt nul 1>nul 2>nul &&(start /wait queue.txt) ||(
echo #add links to this file, save then close the file>queue.txt
start /wait queue.txt
)
for /f "tokens=*" %%i in (queue.txt) do (
set "templist=%%i"
call :_check_queue_list "%%templist%%" "%%templist:~0,1%%"
)
pause
goto :eof

:_check_queue_list
if not [%~2] equ [#] call ".\crunchy-xml-decoder\ultimate.py" %~1 %epnum% %seasonnum%
goto :eof

:_make_cookies
del /f "cookies" 1>nul 2>nul
:choice
set /P c=Do you have an account [Y/N]?
if /I "%c%" EQU "Y" "crunchy-xml-decoder\login.py" yes & GOTO :eof
if /I "%c%" EQU "N" "crunchy-xml-decoder\login.py" no & GOTO :eof
goto :choice
GOTO :eof
:_lxml_crypto_auto_download
echo Start up
rd /s /q temp 1>nul 2>nul
rem call echo %%PROCESSOR_ARCHITECTURE:64=%%
rem pause

md temp
crunchy-xml-decoder\functtest.py Crypto_ 2>nul &&(set "Crypto_stat=installed") ||(set "Crypto_stat=not installed")
crunchy-xml-decoder\functtest.py lxml_ 2>nul &&(set "lxml_stat=installed") ||(set "lxml_stat=not installed")
rem pause

rem for /f "tokens=4" %%i in ('reg query HKEY_CLASSES_ROOT\Python.CompiledFile\shell\open\command /z /ve') do set python_p=%%i
for /f "tokens=1-9 skip=2" %%i in ('reg query HKEY_CLASSES_ROOT\Python.CompiledFile\shell\open\command /z /ve') do (
call :_python_dir1 %%i %%j %%k %%l %%m %%n %%o %%p %%q
)
rem set python_p="C:\Python33\New folder (2)\python.exe"
rem set python_p
call echo python directory=%%python_p%%
rem pause
rem goto :eof
rem for /f "tokens=1,9" %%i in ('call %%python_p%% -c "import platform, sys;v=sys.version;print v"') do (
for /f "tokens=1,9" %%i in ('call %%python_p%% -c "import platform, sys;print(sys.version)"') do (
rem echo %%i,%%j 
set _ver=%%i
set _bit=%%j
call set _ver=%%_ver:~0,-2%%
)
call echo python version=%%_ver%% %%_bit%%Bit
for /f "usebackq skip=2 tokens=*" %%k in (`reg query "HKLM\Software\Microsoft\Windows NT\CurrentVersion" /v "ProductName"`) do (
set winname_=%%k
call set winname_=%%winname_:ProductName=%%
call set winname_=%%winname_:REG_SZ=%%
call set winname_=%%winname_:^(1^)=%%
call set winname_=%%winname_:  =%%
call echo OS Name=%%winname_%%
)
for /f "usebackq tokens=*" %%k in (`ver^|findstr Windows`) do echo OS Version=%%k
rem ver|findstr Windows
call echo system type=%%PROCESSOR_ARCHITECTURE%%
rem set "Crypto_stat=installed"
rem set "lxml_stat=installed"
call :download_ %%_ver%% %%_bit%% "%%Crypto_stat%%" "%%lxml_stat%%" %%PROCESSOR_ARCHITECTURE%% %%PROCESSOR_ARCHITECTURE:64=%% "%~1"

rd /s /q temp
goto :eof

:download_
echo Crypto %~3
echo lxml %~4
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
IF not "%~7"=="debuging" (
.\video-engine\7z.exe x -otemp\ temp\  1>nul 2>nul
.\video-engine\7z_64.exe x -otemp\ temp\ 1>nul 2>nul
xcopy .\temp\PLATLIB\Crypto .\crunchy-xml-decoder\Crypto /E /C /H /R /Y 1>nul 2>nul
xcopy .\temp\PLATLIB\lxml .\crunchy-xml-decoder\lxml /E /C /H /R /Y 1>nul 2>nul
) else (
.\video-engine\7z.exe x -otemp\ temp\
.\video-engine\7z_64.exe x -otemp\ temp\
xcopy .\temp\PLATLIB\Crypto .\crunchy-xml-decoder\Crypto /E /C /H /R /Y
xcopy .\temp\PLATLIB\lxml .\crunchy-xml-decoder\lxml /E /C /H /R /Y
)
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

GOTO STEP1-GETVIDEO

:STEP1-GETVIDEO

	IF "%1"=="" GOTO Enter-URL
	SET video_url=%1
	GOTO Continue-1

:Enter-URL
	ECHO Please Enter CrunchyRoll Video URL
	SET /p video_url=
	GOTO Continue-1

:Continue-1
	if "%3"=="" GOTO Continue-2
	set epnum=%2
	set seasonnum=%3
	".\crunchy-xml-decoder\ultimate.py" %video_url% %epnum% %seasonnum%
	GOTO STEP4

:Continue-2
	if "%2"=="" GOTO Continue-3
	set epnum=%2
	".\crunchy-xml-decoder\ultimate.py" %video_url% %epnum% 1
	GOTO STEP4

:Continue-3
	".\crunchy-xml-decoder\ultimate.py" %video_url% 1 1
	GOTO STEP4


:STEP4

	ECHO ****** Job completed successfully *****
	ECHO.
rem	EXIT
rem	PAUSE
:SETUP

	ECHO.
	ECHO --------------------------
	ECHO ---- Start New Export ----
	ECHO --------------------------
	ECHO.
	ECHO CrunchyRoll Downloader Toolkit DX v0.98
	ECHO.
	ECHO This script downloads just the subtitles, for purposes nefarious or otherwise.
	ECHO.
	ECHO ----------
	ECHO.

	IF "%1"=="" GOTO Enter-URL
		set video_url=%1
		goto Continue

	:Enter-URL
		ECHO Please Enter CrunchyRoll Video URL
		set /p video_url=
		goto Continue

	:Continue
	ECHO Extracting subtitles from %video_url%

	"crunchy-xml-decoder\decode.py" %video_url%

	ECHO.
	ECHO ----------
	ECHO.
	ECHO.

	echo ****** Job completed successfully *****
	echo.
	PAUSE
