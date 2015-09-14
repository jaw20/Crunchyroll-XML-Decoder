@ECHO off
@md export 2>nul
rem Crunchyroll Export Script DX - Last Updated 2015/02/09
rem Removes need for rtmpExplorer
rem ORIGINAL SOURCE - http://www.darkztar.com/forum/showthread.php?219034-Ripping-videos-amp-subtitles-from-Crunchyroll-%28noob-friendly%29
if not exist cookies call _make_cookies.bat

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