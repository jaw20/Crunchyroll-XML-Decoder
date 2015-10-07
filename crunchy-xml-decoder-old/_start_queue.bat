@echo off
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
if not [%~2] equ [#] call ".\crunchy-xml-decoder\ultimate.py" %~1 1 1
goto :eof