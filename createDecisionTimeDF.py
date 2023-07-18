import pandas as pd
from helperfunctions import dig_correctness
from classes import SensesObject, DecisionStatsObject, BehaviorObject
#must pip install: pandas, tkinter, and jinja2


def createDecisionTimeDF(BehaviorDF, SetupDF, senses):
	#Initalize output dataframe for "Behavior" sheet
	DecisionTimeDF = pd.DataFrame(columns=["ApproachTime","ApproachBehavior","EventTime","EventBehavior",
		"Trial","All","Correct Dig","Incorrect Dig","Correct Rejection","Miss", "Last Correct", "Last Incorrect"
	])

	hasApproached = False 
	ApproachTime = "" #Time it took to approach


	#Obj to pass to dig_correctness() function. Holds approach direction and trial
	mouse = BehaviorObject("", 0)
	
	#Obj holding counts of CD, ID, CR, Miss, for statistics line
	stats = DecisionStatsObject();

	#Iterate through our Behavior DF
	for index, row in BehaviorDF.iterrows():

		Behavior = row["Behavior"]
		#If mouse has approached, look for leave, dig, or eat	
		if hasApproached:
			timeTaken = "{0:.3f}".format(float(row["Time"]) - float(ApproachTime))

			match Behavior:
				case "Leave":
					mouse.trial = int(row["Trial"])
					#Determine correctness of this leave
					#It is simply the OPPOSITE of the correctness of a dig
					if not dig_correctness(SetupDF, mouse, senses):
						#If this leave was correct, it's a Miss
						stats.cr += 1
						DecisionTimeDF.loc[len(DecisionTimeDF)] = [ApproachTime,
							mouse.Approached, str(row["Time"]), "LeaveCR", str(row["Trial"]),
							timeTaken, "", "",timeTaken,"","",""]	

					else:
						#If this leave was incorrect, it's a Correct Rejection
						stats.ms += 1
						DecisionTimeDF.loc[len(DecisionTimeDF)] = [ApproachTime,
							mouse.Approached, str(row["Time"]), "Miss", str(row["Trial"]),
							timeTaken, "", "","",timeTaken,"",""]

				case "CorrectDig":
					stats.cd += 1
					DecisionTimeDF.loc[len(DecisionTimeDF)] = [ApproachTime,
						mouse.Approached, str(row["Time"]), Behavior, str(row["Trial"]),
						timeTaken, timeTaken, "","","","",""]

				case "IncorrectDig":
					stats.id += 1
					DecisionTimeDF.loc[len(DecisionTimeDF)] = [ApproachTime,
						mouse.Approached, str(row["Time"]), Behavior, str(row["Trial"]),
						timeTaken, "", timeTaken,"","","",""]
			hasApproached = False

		#If mouse has not approached, look for an approach
		else:

			if Behavior == "ApproachRight":
				hasApproached = True
				#Track whether it's right or left
				mouse.Approached = Behavior
				#Track time of approach
				ApproachTime = row["Time"]

			elif Behavior == "ApproachLeft":
				hasApproached = True
				#Track whether it's right or left
				mouse.Approached = Behavior
				#Track time of approach
				ApproachTime = row["Time"]

	#Compute Statistics in a list and save them
	#Avg statistics list
	avgLine = ['']*3 + ['Average', '', "{0:.3f}".format(pd.to_numeric(DecisionTimeDF['All']).mean()),
		"{0:.3f}".format(pd.to_numeric(DecisionTimeDF['Correct Dig']).mean()),
		"{0:.3f}".format(pd.to_numeric(DecisionTimeDF['Incorrect Dig']).mean()),
		"{0:.3f}".format(pd.to_numeric(DecisionTimeDF['Correct Rejection']).mean()),
		"{0:.3f}".format(pd.to_numeric(DecisionTimeDF['Miss']).mean()),
		"{0:.3f}".format(pd.to_numeric(DecisionTimeDF['Last Correct']).mean()),
		"{0:.3f}".format(pd.to_numeric(DecisionTimeDF['Last Incorrect']).mean())]
	#Standard Dev statistics list	
	stdLine = ['']*3 + ['StDev', '', "{0:.3f}".format(pd.to_numeric(DecisionTimeDF['All']).std()),
		"{0:.3f}".format(pd.to_numeric(DecisionTimeDF['Correct Dig']).std()),
		"{0:.3f}".format(pd.to_numeric(DecisionTimeDF['Incorrect Dig']).std()),
		"{0:.3f}".format(pd.to_numeric(DecisionTimeDF['Correct Rejection']).std()),
		"{0:.3f}".format(pd.to_numeric(DecisionTimeDF['Miss']).std()),
		"{0:.3f}".format(pd.to_numeric(DecisionTimeDF['Last Correct']).std()),
		"{0:.3f}".format(pd.to_numeric(DecisionTimeDF['Last Incorrect']).std())]
	#Counts of each one (this is saved in the stats structure)

	medianLine = ['']*3 + ['Median', '', "{0:.3f}".format(pd.to_numeric(DecisionTimeDF['All']).median()),
		"{0:.3f}".format(pd.to_numeric(DecisionTimeDF['Correct Dig']).median()),
		"{0:.3f}".format(pd.to_numeric(DecisionTimeDF['Incorrect Dig']).median()),
		"{0:.3f}".format(pd.to_numeric(DecisionTimeDF['Correct Rejection']).median()),
		"{0:.3f}".format(pd.to_numeric(DecisionTimeDF['Miss']).median()),
		"{0:.3f}".format(pd.to_numeric(DecisionTimeDF['Last Correct']).median()),
		"{0:.3f}".format(pd.to_numeric(DecisionTimeDF['Last Incorrect']).median())]
	#Counts of each one (this is saved in the stats structure)

	countsLine = ['']*3 + ['Total', '',stats.cd+stats.id+stats.cr+stats.ms,
		stats.cd, stats.id, stats.cr, stats.ms] + ['']*2


	#Blank line for spacing
	DecisionTimeDF.loc[len(DecisionTimeDF)] = ['']*12
	#Add all statistics lists onto the dataframe
	DecisionTimeDF.loc[len(DecisionTimeDF)] = avgLine
	DecisionTimeDF.loc[len(DecisionTimeDF)] = stdLine
	DecisionTimeDF.loc[len(DecisionTimeDF)] = medianLine
	DecisionTimeDF.loc[len(DecisionTimeDF)] = countsLine

	return DecisionTimeDF
