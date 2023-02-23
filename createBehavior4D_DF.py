import pandas as pd
from helperfunctions import dig_leave_correctness
from classes import SensesObject, BehaviorObject
#must pip install: pandas, tkinter, and jinja2


def createBehavior4D_DF(BehaviorDF, SetupDF, senses):
	#Initalize output dataframe for "Behavior" sheet
	Behavior4D_DF = pd.DataFrame(columns=["ApproachTime","ApproachBehavior","EventTime","EventBehavior",
		"Trial","All","Correct Dig","Incorrect Dig","Correct Rejection","Miss"
	])

	hasApproached = False 
	ApproachTime = "" #Time it took to approach
	#Obj to pass to correctness function with approach direction and trial
	mouse = BehaviorObject("", 0)

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
					if dig_leave_correctness(SetupDF, mouse, senses):
						#If this leave was correct, it's a Miss
						Behavior4D_DF.loc[len(Behavior4D_DF)] = [ApproachTime,
							mouse.Approached, str(row["Time"]), "Miss", str(row["Trial"]),
							timeTaken, "", "","",timeTaken]	

					else:
						#If this leave was incorrect, it's a Correct Rejection
						Behavior4D_DF.loc[len(Behavior4D_DF)] = [ApproachTime,
							mouse.Approached, str(row["Time"]), "LeaveCR", str(row["Trial"]),
							timeTaken, "", "",timeTaken,""]

				case "CorrectDig":
					Behavior4D_DF.loc[len(Behavior4D_DF)] = [ApproachTime,
						mouse.Approached, str(row["Time"]), Behavior, str(row["Trial"]),
						timeTaken, timeTaken, "","",""]

				case "IncorrectDig":
					Behavior4D_DF.loc[len(Behavior4D_DF)] = [ApproachTime,
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
	

	return Behavior4D_DF
