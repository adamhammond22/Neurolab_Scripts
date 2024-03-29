# Neurolab Scripts
Welcome!

This is a personal Repo for projects to assist a Neuroscience lab.

It will comprise of python scripts using the pandas library, in order to format and form statistics
reguarding the projects.

If you have questions, issues, or feedback reguarding my work, feel free to reach out to me at abhammond22@gmail.com! :)

## Files:

The list of files in this project.

1 - excelformat.py - Main program to run. Usage is documented below.

2 - createBehaviorDF.py -  Function to create the behavior dataframe. Converted to excel in main

3 - createDecisionTimeDF.py - Function to create the decision time dataframe. Converted to excel in main

4 - helperfunctions.py -  Holds all helper functions to format digs, determine dig correctness, and highlight dataframe rows accordingly.

5 - classes.py - Holds all objects or 'classes' which store simple counts for statistics, or current senses / behavior to pass to functions

6 - requirements.txt - Stores all python libraries for which this program is dependant on.

7 - LICENSE - GNU General Public License v3. Anyone is allowed to use it for free, it can be redistributed as long as I get credit and it's made free.



## Getting Python and downloading this Repository:

#### For Windows:

1 - Download Python 3.10 from the Microsoft Store.

	(Any version starting with a 3.<something> will probably work)


2 - Download all program files 'Neurolab_Scripts-main'and store them on local computer.

	(By clicking 'Code'->'Download Zip' on github)


3 - Unzip 'Neurolab_Scripts-main' if it's zipped.

	(By right clicking on it -> 'Extract All' -> 'Extract' button)


## Running the Program:

### Automatic Usage:

To automatically start the program I used a windows batchfile.

It checks for a correct python version as well as depenancies every time it's run, so no setup is needed.

	Simply navigate to the directory of the script and open "startExcelFormat.bat"

### Manual Usage:

Requires a first time setup if you have not used this on this computer before.

#### First time Setup:

Here are the steps to install this program's dependancies.

1 - Open Windows Command Prompt or Powershell

	(By going to windows search bar and typing 'cmd' or 'pow', they should pop up)


2 - Change Directory in the Command Prompt or Powershell to the unzipped 'Neurolab_Scripts-main' folder.

	(By typing 'cd <path/to/folder>/Neurolab_Scripts-main')

	(Replace <path/to/folder> with actual filepath)

	(You know you're in the correct directory if you enter 'dir' and it prints the files inside the Neurolab_Scripts-main folder)


3 - Enter 'python3 -m pip install -r requirements.txt'

	(This should tell python's package manager pip to recursively install all the dependancies in requirements.txt)
	
	If it stops after 10 seconds hit enter a couple times, it's finished when "<filepath>/Neuro_Scripts-main>" returns

	If this is completed sucessfully, you should be able to simply run the program from here on out


#### Running Program Manually:

1 - Open Windows Command Prompt or Powershell

	(By going to windows search bar and typing 'cmd' or 'pow', they should pop up)

2 - Change Directory in the Command Prompt or Powershell to the unzipped 'Neurolab_Scripts-main' folder.

	(By typing 'cd <path/to/folder>/Neurolab_Scripts-main')
	
	(Replace <path/to/folder> with actual filepath)
	
	(You know you're in the correct directory if you enter 'dir' and it prints the files inside the Neurolab_Scripts-main folder)


3 - Run "python3 excelformat.py" in cmd prompt or powershell


## Using the Program:
	
How to run the program is indended to be used.

The program takes for input: 1 .xlsx Excel file.

	This file requires 2 Sheets: 
	
	1 - "RAW" sheet of raw boris data with AT LEAST columns "Behavioral category", "Behavior type", and "Time". These columns need to be named EXACTLY THIS!
	
	2 - "SETUP" sheet of manually imputted data about the test. The program needs to know what texture / odor is correct, and which side the correct sense is on, in order to determine correctness of Digs, Leaves, etc. It must have columns "L_Texture","L_Odor","R_Texture","R_Odor","Trial", "CorrTexture","CorrOdor". The columns need to be named EXACTLY THIS!

	
The program outputs 1 .xlsx File named <Original_File_Name>ScriptOutput.xlsx, in the same directory as the program.
	
	This file contains:
	
	1 - Raw sheet from input file
	
	2 - Setup sheet from input file
	
	3 - Behavior sheet
	
	4 - Decision Time sheet
	
	5 - Dig-eat sheet

### Common Errors:

#### "Pandas could not read file <filepath>"
	
	Pandas either couldn't find the file specified in filepath, or something is wrong with pandas.
	If filepath is correct, check that the Pandas library is installed.
	
	
#### "Program could not find a sheet named 'Raw'"
	
	Make sure excel data sheet is named something like "raw", "rAw", "RaW", "RAW", etc.

#### "Program could not find a sheet named 'Setup'"
	
	Make sure excel data sheet is named something like "setup", "seTUp", "SETUP", etc.
	
#### "Pandas could not open file <filepath>.xlsx with sheet 'Raw'" 

	Script failed to open this file with the sheet named 'Raw', check filepath and sheet name.
	If filepath and sheetname are correct, check that the Pandas library is installed


#### "Pandas could not open file <filepath>.xlsx with sheet 'Setup'" 

	Script failed to open this file with the sheet named 'Setup', check filepath and sheet name.
	If filepath and sheetname are correct, check that the Pandas library is installed


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
[ ] Behavior DF has an incredibly rare failure where it fails to concatenate (correctly computed) stats onto the existing df. I am ignoring this unless it happens twice. If so I should Look into using merge(), or adding a bunch of series

[ ] ERROR CHECKING: ONLY 1 set of DIGS PER TRIAL

[ ] Implement a graphing utility
	
[ ] More statistics!
	
[ ] both ways of running the program assume the default windows execution alias of "python3". This is incredibly limiting and may cause problems in the future

