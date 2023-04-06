::Batchfile to start excelformat.py
::Also checks for dependant packages each time
::ASSUMES pip is installed
::ASSUMES the DEFAULT execution alias of "python3" is setup in windows.
@echo off
cls
echo Beginning.
echo.

::set local so errorlevel is set EACH iteration!
setlocal ENABLEDELAYEDEXPANSION

::Variable to only install Reqs a maximum of 2 times
SET /A a=0

::  ==== Check for Python Installation ==== 
echo Checking Python version.
python --version | find "Python 3" >NUL 2>NUL

:: if Python 3 not found, it's a bad python version
if errorlevel 1 goto errorBadPython


::  ==== Check for Python Installed Packages ==== 
:checkReqs
echo Checking installed requirements. Found these packages:
::Iterate over each line 'L' in requirements.txt
for /F "tokens=*" %%L in  (requirements.txt) do (
	::delimit the line by equalsigns into dependancy 'd'
	for /f "tokens=1,2 delims==" %%d IN ("%%L") do (

		::search pip freeze (which has all installed packages) for this requirement
		python3 -m pip freeze | find "%%d"

		::if dependancy d is not found in the pip freeze - try to install it
		if !errorlevel!==1 (goto installReqs)
	)
)
::If we go through the loop, we can safely launch
goto launch


:: ==== Install Reqs ====
:installReqs
echo Pip detected a lacking requirement package. Attempting to install requirements.txt.
python3 -m pip install -r requirements.txt

::If this is the first iteration(a=0), retry check reqs. otherwise (a=1) we give up
if !a! == 0 (SET /A a=1 & goto checkReqs) else (goto reqInstallFail)


:: ==== Launch python script ==== 
:launch
echo Launching excelformat.
echo.
echo.
python3 excelformat.py
goto end


::Error msg if python is outdated or not installed
:errorBadPython
echo.
echo.
echo Error^: ERROR: Python is not version 3 or is not installed.
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
echo Press any button to close this window...
:: Pause for user input
pause > nul