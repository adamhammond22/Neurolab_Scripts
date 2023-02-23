import pandas as pd
import tkinter as tk
import re
from tkinter import filedialog

from classes import SensesObject, BehaviorObject, StatsObject
from helperfunctions import formatDigs, dig_correctness, highlight

#must pip install: pandas, tkinter, and jinja2


def createBehaviorDF(RawDF, SetupDF):
	#Initalize output dataframe for "Behavior" sheet
	BehaviorDF = pd.DataFrame(columns=["Time", "Behavior", "Behavior type", "Trial"])
	
	dig_row_indices = [] #List of indices from most recent digs
	drop_indices = [] # List of all indices to drop
	
	#Determine sense we're testing for
	try:
		CorrTexture = SetupDF.at[0, "CorrTexture"]
		print(str(CorrTexture))
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
	
	#print("testing for " + str(senses.testing) +  " correct:" + str(senses.correct))
	
	#mouse is not digging and has not approached a side, and is at trial 0
	mouse = BehaviorObject(False, "", 0)
	stats = StatsObject();
	
	#Iterate over all rows in Raw Dataframe
	for index, row in RawDF.iterrows():
		#Write according text based on raw behavior character(s, t, v, etc...)
		rawBehavior = row["Behavior"]
		match rawBehavior:
			case "t":
				stats.t += 1
				mouse.trial += 1
				behavior = "TrialStart"
			case "l":
				stats.l += 1
				behavior = "ApproachLeft"
				mouse.hasApproached = "Left"
			case "r":
				stats.r += 1
				behavior = "ApproachRight"
				mouse.hasApproached = "Right"
			case "v":
				stats.v += 1
				behavior = "Leave"
				#If we were just digging, we need to check the setup to determine
				if mouse.isDigging:
					if (dig_correctness(SetupDF, mouse, senses)):
						drop_indices.extend(formatDigs(BehaviorDF, dig_row_indices, "CorrectDig"))
						stats.cd += 1
					else:
						drop_indices.extend(formatDigs(BehaviorDF, dig_row_indices, "IncorrectDig"))
						stats.id += 1
					mouse.isDigging = False
					dig_row_indices = []
			case "e":
				stats.e += 1
				behavior = "Eat"
				#If we were just digging, label all prev digs as correct
				if mouse.isDigging:
					#format our digs, adding extras to the drop list
					drop_indices.extend(formatDigs(BehaviorDF, dig_row_indices, "CorrectDig"))
					stats.cd += 1
					#Reset digging status and indices
					mouse.isDigging = False
					dig_row_indices = []
			case "d":
				#We cannot label digs as correct or incorrect until we hit 'e' or 'v'.
				#Mark placeholder, and update digging status + indices.
				if not mouse.isDigging:
					mouse.isDigging = True
				dig_row_indices.append(index);
				behavior = "DigPlaceholder"
			case _:
				#Default case: just print the undefined behavior and warn the user
				behavior = rawBehavior;
				print("Warning: Undefined Behavior"+ t +" encountered at index "+ index)
	
		#Append the new row of formatted data to Behavior Dataframe
		BehaviorDF.loc[len(BehaviorDF)] = [str(row["Time"]), behavior, row["Behavior type"], str(mouse.trial)]
	
	#Drop all of our tracked duplicate dig indices
	BehaviorDF = BehaviorDF.drop(labels=drop_indices, axis=0)
	
	# ========== Add basic statistics to Behavior Sheet ========== #
	stats = pd.concat([pd.Series([""]),
		pd.Series(["","TrialStart","ApproachRight","ApproachLeft",
		"CorrectDig","IncorrectDig","Eat","Leave"]),
		pd.Series(["", stats.t, stats.r, stats.l, stats.cd,
			stats.id, (stats.e//2), stats.v]),
		pd.Series(["","","Approach","","Dig"]),
		pd.Series(["","",(stats.l+stats.r),"",(stats.cd+stats.id)])],
	 		axis=1)
	#stats.rename(columns={0: "",1: "NamesA",2: "StatsA",3:"NamesB", 4:"StatsB"}, inplace=True)
	#stats.rename(columns={3: "",1: ""}, inplace=True)
	BehaviorDF = pd.concat([BehaviorDF, stats], axis=1)
	
	
	# ========== Apply Highlighting ========== #
	BehaviorDF = BehaviorDF.style.apply(highlight, axis=1)

	return BehaviorDF
