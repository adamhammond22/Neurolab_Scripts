import pandas as pd
from helperfunctions import dig_correctness
from classes import SensesObject, DecisionStatsObject, BehaviorObject
#must pip install: pandas, tkinter, and jinja2


def createDecisionTimeDF(BehaviorDF, SetupDF, senses):
	#Initalize output dataframe for "Behavior" sheet
	DecisionTimeDF = pd.DataFrame(columns=["ApproachTime","ApproachBehavior","EventTime","EventBehavior",
		"Trial","All","Correct Dig","Incorrect Dig","Correct Rejection","Miss"
	])

	hasApproached = False 
	ApproachTime = "" #Time it took to approach


	#Obj to pass to correctness function with approach direction and trial
	mouse = BehaviorObject("", 0)
	
	#Obj holding statistics for n counts
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
							timeTaken, "", "",timeTaken,""]	

					else:
						#If this leave was incorrect, it's a Correct Rejection
						stats.ms += 1
						DecisionTimeDF.loc[len(DecisionTimeDF)] = [ApproachTime,
							mouse.Approached, str(row["Time"]), "Miss", str(row["Trial"]),
							timeTaken, "", "","",timeTaken]

				case "CorrectDig":
					stats.cd += 1
					DecisionTimeDF.loc[len(DecisionTimeDF)] = [ApproachTime,
						mouse.Approached, str(row["Time"]), Behavior, str(row["Trial"]),
						timeTaken, timeTaken, "","",""]

				case "IncorrectDig":
					stats.id += 1
					DecisionTimeDF.loc[len(DecisionTimeDF)] = [ApproachTime,
						mouse.Approached, str(row["Time"]), Behavior, str(row["Trial"]),
						timeTaken, "", timeTaken,"",""]
			hasApproached = False

		#If mause has not approached, look for an approach
		else:

			if Behavior == "ApproachRight":
				hasApproached = True
				mouse.Approached = Behavior
				ApproachTime = row["Time"]

			elif Behavior == "ApproachLeft":
				hasApproached = True
				mouse.Approached = Behavior
				ApproachTime = row["Time"]

	#Compute Statistics and save them
	avgLine = ['']*3 + ['Average', '', "{0:.3f}".format(pd.to_numeric(DecisionTimeDF['All']).mean()),
		"{0:.3f}".format(pd.to_numeric(DecisionTimeDF['Correct Dig']).mean()),
		"{0:.3f}".format(pd.to_numeric(DecisionTimeDF['Incorrect Dig']).mean()),
		"{0:.3f}".format(pd.to_numeric(DecisionTimeDF['Correct Rejection']).mean()),
		"{0:.3f}".format(pd.to_numeric(DecisionTimeDF['Miss']).mean())]
	stdLine = ['']*3 + ['StDev', '', "{0:.3f}".format(pd.to_numeric(DecisionTimeDF['All']).std()),
		"{0:.3f}".format(pd.to_numeric(DecisionTimeDF['Correct Dig']).std()),
		"{0:.3f}".format(pd.to_numeric(DecisionTimeDF['Incorrect Dig']).std()),
		"{0:.3f}".format(pd.to_numeric(DecisionTimeDF['Correct Rejection']).std()),
		"{0:.3f}".format(pd.to_numeric(DecisionTimeDF['Miss']).std())]
	countsLine = ['']*3 + ['Total', '',stats.cd+stats.id+stats.cr+stats.ms,
		stats.cd, stats.id, stats.cr, stats.ms]

	#Add all statistics
	DecisionTimeDF.loc[len(DecisionTimeDF)] = ['']*10
	#Print Average Stats
	DecisionTimeDF.loc[len(DecisionTimeDF)] = avgLine
	DecisionTimeDF.loc[len(DecisionTimeDF)] = stdLine
	DecisionTimeDF.loc[len(DecisionTimeDF)] = countsLine

	return DecisionTimeDF
