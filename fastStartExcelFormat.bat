::Batchfile to start excelformat.py
::Also checks for dependant packages each time
::ASSUMES pip is installed
::ASSUMES the DEFAULT execution alias of "python3" is setup in windows.
@echo off
cls
echo Beginning excelformat Fast Start...
echo.

::Variable to only install Reqs a maximum of 2 times
SET /A a=0

::  ==== Check for Python Installation ==== 
echo Checking Python version...
echo.
python --version | find "Python 3" >NUL 2>NUL

:: if Python 3 not found, it's a bad python version
if errorlevel 1 goto errorBadPython


:: ==== Launch python script ==== 
:launch
echo Launching excelformat...
python3 excelformat.py
goto end


::Error msg if python is outdated or not installed
:errorBadPython
echo.
echo.
echo Error^: ERROR: ExecutionAlias Python3 is not present. 
echo                Either Python v3 is not installed, or the executionAlias must be enabled in windows settings.
goto end

::Error message if we tried installing requirements and failed
:reqInstallFail
echo.
echo.
echo Error^: ERROR: Could not install requirements listed in requirements.txt.
goto end


:: ==== End of Script ==== 
:end
echo.
echo.
echo.
echo Press any button to close this window...
:: Pause for user input
pause > nul