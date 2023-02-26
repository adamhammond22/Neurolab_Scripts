# Neurolab Scripts
Welcome!

This is a personal Repo for projects to assist a Neuroscience lab.

It will comprise of python scripts using the pandas library, in order to format and form statistics
reguarding the projects.

## Files:

1 - excelformat.py - Main program to run. Usage is documented below.

2 - createBehaviorDF.py -  Function to create the behavior dataframe. Converted to excel in main

3 - createDecisionTimeDF.py - Function to create the decision time dataframe. Converted to excel in main

4 - helperfunctions.py -  Holds all helper functions to format digs, determine dig correctness, and highlight dataframe rows accordingly.

5 - classes.py - Holds all objects or 'classes' which store simple counts for statistics, or current senses / behavior to pass to functions

6 - requirements.txt - Stores all python libraries for which this program is dependant on.

## First Time Installation:

### Windows:
1 - Download Python 3.10 from the Microsoft Store.

(Any version starting with a 3.<something> will probably work)


2 - Download all program files 'Neurolab_Scripts-main'and store them on local computer.

(By clicking 'Code'->'Download Zip' on github)


3 - Unzip 'Neurolab_Scripts-main' if it's zipped.

(By right clicking on it -> 'Extract All' -> 'Extract' button)


3 - Open Windows Command Prompt or Powershell

(By going to windows search bar and typing 'cmd' or 'pow', they should pop up)


4 - Change Directory in the Command Prompt or Powershell to the unzipped 'Neurolab_Scripts-main' folder.

(By typing 'cd <path/to/folder>/Neurolab_Scripts-main')

(Replace <path/to/folder> with actual filepath)

(You know you're in the correct directory if you enter 'dir' and it prints the files inside the Neurolab_Scripts-main folder)


5 - Enter 'python3 -m pip install -r requirements.txt'

(This should tell python's package manager pip to recursively install all the dependancies in requirements.txt)

If this is completed sucessfully, you should be able to simply run the program from here on out


## Running excelformat.py
### Windows:

1 - Change Directory in the Command Prompt or Powershell to the unzipped 'Neurolab_Scripts-main' folder.

(By typing 'cd <path/to/folder>/Neurolab_Scripts-main')
(Replace <path/to/folder> with actual filepath)
(You know you're in the correct directory if you enter 'dir' and it prints the files inside the Neurolab_Scripts-main folder)


2 - Run "python3 excelformat.py" in cmd prompt or powershell


Upon running, excelformat.py prompts user for  single .xlsx file with sheets "Raw" and "Setup".
Formats said file to specificaion. Outputs to file ScriptOutput.xlsx


### Common Errors:

#### "Pandas could not open file <filepath>.xlsx with sheet 'Raw'" 

	Script failed to open this file with the sheet named 'Raw', check filepath and sheet name.
	If filepath and sheetname are correct, check that ther Pandas library is installed


#### "Pandas could not open file <filepath>.xlsx with sheet 'Setup'" 

	Script failed to open this file with the sheet named 'Setup', check filepath and sheet name.
	If filepath and sheetname are correct, check that ther Pandas library is installed


#### "PermissionError: [errno 13] Permission denied: 'ScriptOutput.xlsx'"

	Script executed but was denied permission to write to 'ScriptOutput.xlsx'. This is usuallt because
	Excel has this file open and blocks it from being tampered with. Make sure this file is not open in
	excel before running.


#### "ModuleNotFoundError: No module named '<module_name>'"

	Python thinks this module is not installed.
	Try 'python3 -m pip <module_name>', or  'python3 -m pip install -r requirements.txt'
	Sometimes a computer can have multiple python clients, one may have pandas installed and 
	another may not! Try checking python version, and 'python3 -m pip list' to see modules installed.


### To Do:

[ ] regex to file names for raw and setup. maybe make 100_something?

[ ] algorithmically calculate and display correct and incorrect digs 

[ ] remove duplicate incorrect digs (only count first and last)

[ ] calculate avg, std, other statistics

[ ] make python auto-download required libraries for ease of use: maybe a .bat file?

