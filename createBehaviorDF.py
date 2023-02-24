import pandas as pd
import re

from classes import SensesObject, BehaviorObject, BehaviorStatsObject
from helperfunctions import formatDigs, dig_correctness

#must pip install: pandas, tkinter, and jinja2


def createBehaviorDF(RawDF, SetupDF, senses):
	#Initalize output dataframe for "Behavior" sheet
	BehaviorDF = pd.DataFrame(columns=["Time", "Behavior", "Behavior type", "Trial"])
	
	dig_row_indices = [] #List of indices from most recent digs
	drop_indices = [] # List of all indices to drop

	
	#print("testing for " + str(senses.testing) +  " correct:" + str(senses.correct))
	
	#Obj to pass to correctness function with approach direction and trial
	mouse = BehaviorObject("", 0)
	isDigging = False
	stats = BehaviorStatsObject();
	
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
				mouse.Approached = behavior
			case "r":
				stats.r += 1
				behavior = "ApproachRight"
				mouse.Approached = behavior
			case "v":
				stats.v += 1
				behavior = "Leave"
				#If we were just digging, we need to check the setup to determine
				if isDigging:
					if (dig_correctness(SetupDF, mouse, senses)):
						drop_indices.extend(formatDigs(BehaviorDF, dig_row_indices, "CorrectDig"))
						stats.cd += 1
					else:
						drop_indices.extend(formatDigs(BehaviorDF, dig_row_indices, "IncorrectDig"))
						stats.id += 1
					isDigging = False
					dig_row_indices = []
			case "e":
				stats.e += 1
				behavior = "Eat"
				#If we were just digging, label all prev digs as correct
				if isDigging:
					#format our digs, adding extras to the drop list
					drop_indices.extend(formatDigs(BehaviorDF, dig_row_indices, "CorrectDig"))
					stats.cd += 1
					#Reset digging status and indices
					isDigging = False
					dig_row_indices = []
			case "d":
				#We cannot label digs as correct or incorrect until we hit 'e' or 'v'.
				#Mark placeholder, and update digging status + indices.
				if not isDigging:
					isDigging = True
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
	

	return BehaviorDF
