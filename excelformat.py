import pandas as pd #pandas for excel sheets and dataframes
import tkinter as tk #tk for file dialog (requires Jinja2!!!)
from tkinter import filedialog, messagebox
import popupWindow
import re #regex
# must pip install: pandas, tkinter, openpyxl and jinja2
# or pip install -r requirements.txt


from classes import SensesObject
from helperfunctions import highlightBehaviorDF, highlightDecisionTimeDF, highlightDigEatDF, handleFileOpen
from createBehaviorDF import createBehaviorDF
from createDecisionTimeDF import createDecisionTimeDF
from createDigEatDF import createDigEatDF

# Required columns for our input sheets
required_setup_columns = {"L_Texture","L_Odor","R_Texture","R_Odor","Trial","CorrTexture","CorrOdor"}
required_raw_columns = {"Behavior","Behavior type","Time"}


# Based on this global "restartProgram" variable (declared in popupWindow.py) we will restart the program
popupWindow.restartProgram = True
while(popupWindow.restartProgram):

	# ====== user selection window ====== #
	root = tk.Tk()
	root.withdraw() #Hide root window

	# "Warning: could not parse header or footer"
	# This is a benign issue- to remove: go to excel on the offending file.
	# File->Info->CheckForIssues->InspectDocument(for headers/footers)->Remove header and footer

	# default action is terminate the program, so set the variable accordingly
	popupWindow.restartProgram = False

	# HARDCODED FILEPATH
	# filepath = "C:/Users/Adam/Desktop/Aster/Neurolab_Scripts/A005_IDS_tab_new_corrected.xlsx"
	# Filepath Determined by tk dialog
	filepath = filedialog.askopenfilename()

	# Open the file and extract raw and setup Dataframes as well as the filename (not the path)
	(RawDF, SetupDF, filename, directoryPath) = handleFileOpen(filepath)

	# ===== Verify Setup and Raw contain needed columns of data ===== #

	setup_cols_set = set(SetupDF.columns.tolist())
	#Checking Setup
	if not (required_setup_columns.issubset(setup_cols_set)):
		print("Fatal Error: Unexpected Setup Column Names")
		print("Expected Columns:" + str(required_setup_columns))
		print("But recieved columns:" + str(SetupDF.columns))

	#Checking Raw
	raw_cols_set = set(RawDF.columns.tolist())
	if not (required_raw_columns.issubset(raw_cols_set)):
		print("Fatal Error: cannot find needed Raw Columns")
		print("Needed Columns:" + str(required_raw_columns))
		print("But recieved columns:" + str(SetupDF.columns))

	# ===== Verify that Setup and Raw have same number of trials ===== #

	#grab all raw rows with behavior 't'
	trows = RawDF.loc[RawDF["Behavior"] == "t"]
	#grab the setup row with the largest "Trial" value
	setupTrials = SetupDF.loc[SetupDF["Trial"].idxmax()]

	#compare them 
	if(len(trows) != setupTrials["Trial"]):
		print("\nSanity Check Error: Setup Trials and Raw 't' count do not match.")
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
		print("\nFatal Error: Failed parsing CorrTexture or CorrOdor in 'Setup' sheet.")
		print(f"Unexpected {err=}, {type(err)=}")
		exit()


	# ========== CREATE Behavior DF ========== #

	BehaviorDF = createBehaviorDF(RawDF, SetupDF, senses)


	# ========== CREATE Behavior 4D DF ========== #

	DecisionTimeDF = createDecisionTimeDF(BehaviorDF, SetupDF, senses)


	# ========== CREATE Dig Eat ========== #

	DigEatDF = createDigEatDF(BehaviorDF)


	# ========== Apply Highlighting ========== #

	BehaviorDF = BehaviorDF.style.apply(highlightBehaviorDF, axis=1)
	DecisionTimeDF = DecisionTimeDF.style.apply(highlightDecisionTimeDF, axis=1)
	DigEatDF = DigEatDF.style.apply(highlightDigEatDF, axis=1)


	# ========== Write dataframes back into excel sheet ========== #
	Output_Filename = filename + '_ScriptOutput.xlsx'
	Output_Filepath = directoryPath + "/" + Output_Filename

	with pd.ExcelWriter(Output_Filepath) as writer:
		RawDF.to_excel(writer, sheet_name='Raw', index=False);
		SetupDF.to_excel(writer, sheet_name='Setup', index=False);
		BehaviorDF.to_excel(writer, sheet_name='Behavior', index=False);
		DecisionTimeDF.to_excel(writer, sheet_name='Decision Time', index=False);
		DigEatDF.to_excel(writer, sheet_name='Dig-eat', index=False);
		# New sheets will be added here!

	print("\nProgram Completed. Outputted to file " + Output_Filename +
		" in path " + Output_Filepath)


	# start the popup window
	popupWindow.initiatePopup(root)

	# Start the main event loop, this will pause the program until a choice in the popup completes
	root.mainloop()

