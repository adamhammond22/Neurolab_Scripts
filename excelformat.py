import pandas as pd
import tkinter as tk
import re
from tkinter import filedialog

#from classes import *
#from helperfunctions import *
from createBehaviorDF import createBehaviorDF

#must pip install: pandas, tkinter, and jinja2

# ====== user selection window ====== #
root = tk.Tk()
root.withdraw() #Hide root window

#"Warning: could not parse header or footer"
#Benign issue- to remove: go to excel on the offending file.
#File->Info->CheckForIssues->InspectDocument(for headers/footers)->Remove header and footer
#I've done this once and it does not impact the program


#to make non-hardcoded just swap which one is commented
filepath = "C:/Users/Adam/Desktop/Aster/Neurolab_Scripts/A005_IDS_tab_new_corrected.xlsx" #HARDCODED FILEPATH
#filepath = filedialog.askopenfilename()

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


# ========== CREATE Behavior DF ========== #
BehaviorDF = createBehaviorDF(RawDF, SetupDF)

#Use ExcelWriter to write
with pd.ExcelWriter('ScriptOutput.xlsx') as writer:
	BehaviorDF.to_excel(writer, sheet_name='Behavior 4D', index=False);
	RawDF.to_excel(writer, sheet_name='Raw', index=False);
	#Add more sheets to write here!

print("Program finished")
