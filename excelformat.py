import pandas as pd
import tkinter as tk
from tkinter import filedialog
#must pip install: pandas, tkinter, and jinja2

# ====== user selection window ====== #
root = tk.Tk()
root.withdraw() #Hide root window

#"Warning: could not parse header or footer"
#Benign issue- to remove: go to excel on the offending file.
#File->Info->CheckForIssues->InspectDocument(for headers/footers)->Remove header and footer
#I've done this once and it does not impact the program



#to make non-hardcoded just swap which one is commented
filepath = "C:/Users/Adam/Desktop/Aster/A005_EDS_tab_new.xlsx" #HARDCODED FILEPATH
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
	SetupDF = pd.read_excel(filepath, "Setup")
except:
	print("Pandas could not open file '"+ filepath +"' with sheet 'Setup'")
	exit()

# ===== Verify that Setup and Raw have same number of trials ===== #

#grab all raw rows with behavior 't'
trows = RawDF.loc[RawDF["Behavior"] == "t"]

#grab the setup row with the largest "Trial" value
setupTrials = SetupDF.loc[SetupDF["Trial"].idxmax()]

#compare them 
if(len(trows) != setupTrials["Trial"]):
	print("Fatal Error: Setup Trials and Raw 't' count do not match.")
	exit()

# ========== Initalize output dataframes =========== #

#Initalize output dataframe for "Behavior" sheet
BehaviorDF = pd.DataFrame(columns=["Time", "Behavior", "Behavior type", "Trial"])


# ========== Iterate Through Raw File ========== #

trial = 0 #Counter to track Trial Number

#Iterate over all rows in Raw Dataframe
for index, row in RawDF.iterrows():

	#Write according text based on raw behavior character(s, t, v, etc...)
	rawBehavior = row["Behavior"]
	match rawBehavior:
		case "t":
			#Increment trial every time we see a new trial
			trial += 1
			behavior = "TrialStart"
		case "l":
			behavior = "ApproachLeft"
		case "r":
			behavior = "ApproachRight"
		case "v":
			behavior = "Leave"
		case "e":
			behavior = "Eat"
		case "d":
			behavior = "Dig"
		case _:
			#Default case: just print the undefined behavior and warn the user
			behavior = rawBehavior;
			print("Warning: Undefined Behavior"+ t +" encountered at index "+ index)

	#Append new row of collected data to Behavior Dataframe
	BehaviorDF.loc[len(BehaviorDF)] = [str(row["Time"]), behavior, row["Behavior type"], str(trial)]



#Highlights a row based on the behavior of that row
def highlight(s):
	match s.Behavior:
		case "TrialStart":
			return ['color: #4472C4'] * len(s)
		case "ApproachRight":
			return ['color: #C65911'] * len(s)
		case "ApproachLeft":
			return ['color: #C65911'] * len(s)
		case "Dig":
			return ['color: #FF0000'] * len(s)
		case _:
			return ['color: black'] * len(s)

#Apply the highlight to our dataframe rows
BehaviorDF = BehaviorDF.style.apply(highlight, axis=1)

#Use ExcelWriter to write
with pd.ExcelWriter('ScriptOutput.xlsx') as writer:
	BehaviorDF.to_excel(writer, sheet_name='Behavior', index=False);
	#Add more sheets to write here!

print("Program finished")
