import pandas as pd #pandas for excel sheets and dataframes
import tkinter as tk #tk for file dialog (requires Jinja2!!!)
from tkinter import filedialog
import re #regex

from classes import SensesObject
from helperfunctions import highlightBehaviorDF, highlightDecisionTimeDF
from createBehaviorDF import createBehaviorDF
from createDecisionTimeDF import createDecisionTimeDF

#must pip install: pandas, tkinter, openpyxl and jinja2
#or pip install -r requirements.txt

# ====== user selection window ====== #
root = tk.Tk()
root.withdraw() #Hide root window

#"Warning: could not parse header or footer"
#This is a benign issue- to remove: go to excel on the offending file.
#File->Info->CheckForIssues->InspectDocument(for headers/footers)->Remove header and footer


#HARDCODED FILEPATH
#filepath = "C:/Users/Adam/Desktop/Aster/Neurolab_Scripts/A005_IDS_tab_new_corrected.xlsx"
#Filepath Determined by tk dialog
filepath = filedialog.askopenfilename()

# ========== Try reading file into input dataframes ========== #
if not filepath:
	print("No file given")
	exit()
try:
	RawDF = pd.read_excel(filepath, "Raw")
except:
	print("Pandas could not open file '"+ filepath +"' with sheet 'Raw'")
	exit()
try:
	#keep def n/a nessecary to make sure na is not coverted
	SetupDF = pd.read_excel(filepath, "Setup", keep_default_na=False)
except:
	print("Pandas could not open file '"+ filepath +"' with sheet 'Setup'")
	exit()

# ===== Verify Setup and Raw contain needed columns ===== #

#Checking Setup
required_cols = {"L_Texture","L_Odor","R_Texture","R_Odor","Trial",
		"CorrTexture","CorrOdor"}
if not (required_cols.issubset(required_cols)):
	print("Fatal Error: Unexpected Setup Column Names")
	print("Expected Columns:" + str(expected_cols))
	print("But recieved columns:" + str(cols))

#Checking Raw
cols = set(RawDF.columns)
required_cols = {"Behavior","Behavior type","Time"}
if not (required_cols.issubset(required_cols)):
	print("Fatal Error: cannot find needed Raw Columns")
	print("Needed Columns:" + str(required_cols))
	print("But recieved columns:" + str(cols))

# ===== Verify that Setup and Raw have same number of trials ===== #

#grab all raw rows with behavior 't'
trows = RawDF.loc[RawDF["Behavior"] == "t"]
#grab the setup row with the largest "Trial" value
setupTrials = SetupDF.loc[SetupDF["Trial"].idxmax()]

#compare them 
if(len(trows) != setupTrials["Trial"]):
	print("Fatal Error: Setup Trials and Raw 't' count do not match.")
	exit()

# ========== CREATE Sense Object ========== #
#Determine the sense we're testing for
try:
	CorrTexture = SetupDF.at[0, "CorrTexture"]
	#If CorrTexture is n/a, then we're testing for odor
	if (re.search("^[nN]/*[aA]$", str(CorrTexture))):
		senses = SensesObject("odor", SetupDF.at[0, "CorrOdor"])
	#Otherwise we're testing for texture
	else:
		senses = SensesObject("texture", CorrTexture)
except Exception as err:
	print("Fatal Error: Failed parsing CorrTexture or CorrOdor in 'Setup' sheet.")
	print(f"Unexpected {err=}, {type(err)=}")
	exit()


# ========== CREATE Behavior DF ========== #
BehaviorDF = createBehaviorDF(RawDF, SetupDF, senses)

# ========== CREATE Behavior 4D DF ========== #
DecisionTimeDF = createDecisionTimeDF(BehaviorDF, SetupDF, senses)

# ========== Apply Highlighting ========== #

BehaviorDF = BehaviorDF.style.apply(highlightBehaviorDF, axis=1)
DecisionTimeDF = DecisionTimeDF.style.apply(highlightDecisionTimeDF, axis=1)

#Use ExcelWriter to write
with pd.ExcelWriter('ScriptOutput.xlsx') as writer:
	RawDF.to_excel(writer, sheet_name='Raw', index=False);
	SetupDF.to_excel(writer, sheet_name='Setup', index=False);
	BehaviorDF.to_excel(writer, sheet_name='Behavior', index=False);
	DecisionTimeDF.to_excel(writer, sheet_name='Decision Time', index=False);
	#Add more sheets to write here!

print("Program Completed")
