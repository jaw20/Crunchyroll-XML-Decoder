@ECHO OFF
del /f "cookies" 1>nul 2>nul
:choice
set /P c=Do you have an account [Y/N]?
if /I "%c%" EQU "Y" goto :yes
if /I "%c%" EQU "N" goto :no
goto :choice


:yes
"crunchy-xml-decoder\login.py" yes
goto :continue

:no
"crunchy-xml-decoder\login.py" no

:continue
pause 
rem exit