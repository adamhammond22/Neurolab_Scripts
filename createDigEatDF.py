import pandas as pd
from classes import DecisionStatsObject
#must pip install: pandas, tkinter, and jinja2


def createDigEatDF(BehaviorDF):
	#Initalize output dataframe for "Behavior" sheet
	DigEatDF = pd.DataFrame(columns=["DigTime","DigBehavior","EventTime","EventBehavior",
		"Trial","Delta-Time","CD-Eat Time","ID-Leave Time"
	])

	hasDug = False 
	DigType = ''
	DigTime = "" #Time of the dig


	
	#we can just use the Decision obj because it has CD and ID.
	stats = DecisionStatsObject();

	#Iterate through our Behavior DF
	for index, row in BehaviorDF.iterrows():
		Behavior = row["Behavior"]
		#If mouse has dug, look for leave or eat	
		if hasDug:			

			match Behavior:

				case "Leave":
					#If leave found, print our line, and times
					deltaTime = "{0:.3f}".format(float(row["Time"]) - float(DigTime))
					DigEatDF.loc[len(DigEatDF)] = [DigTime,
						DigType, str(row["Time"]), Behavior, str(row["Trial"]),
						deltaTime, "", deltaTime]
					hasDug = False #set hasDug false so we look for the next dig

				case "Eat":
					#If eat found, print our line and times
					deltaTime = "{0:.3f}".format(float(row["Time"]) - float(DigTime))
					DigEatDF.loc[len(DigEatDF)] = [DigTime,
						DigType, str(row["Time"]), Behavior, str(row["Trial"]),
						deltaTime, deltaTime, ""]
					hasDug = False #set hasDug false so we look for the next dig

		#If mouse has not dug, look for a dig
		else:
			#If we find the start of a correct dig
			if Behavior == "CorrectDig" and (row['Behavior type'] == 'START'):
				stats.cd += 1
				hasDug = True
				#Track whether it's correct or incorrect
				DigType = Behavior
				#Track time of dig
				DigTime = row["Time"]
			#If we find the start of an incorrect dig
			elif Behavior == "IncorrectDig" and (row['Behavior type'] == 'START'):
				stats.id += 1
				hasDug = True
				#Track whether it's correct or incorrect
				DigType = Behavior
				#Track time of dig
				DigTime = row["Time"]

	#Compute Statistics in a list and save them
	#Avg statistics list
	avgLine = ['']*3 + ['Average', '', "{0:.3f}".format(pd.to_numeric(DigEatDF['Delta-Time']).mean()),
		"{0:.3f}".format(pd.to_numeric(DigEatDF['CD-Eat Time']).mean()),
		"{0:.3f}".format(pd.to_numeric(DigEatDF['ID-Leave Time']).mean())]
	#Standard Dev statistics list	
	stdLine = ['']*3 + ['StDev', '', "{0:.3f}".format(pd.to_numeric(DigEatDF['Delta-Time']).std()),
		"{0:.3f}".format(pd.to_numeric(DigEatDF['CD-Eat Time']).std()),
		"{0:.3f}".format(pd.to_numeric(DigEatDF['ID-Leave Time']).std())]
	#Counts of each one (this is saved in the stats structure)
	countsLine = ['']*3 + ['Total', '',stats.cd+stats.id,
		stats.cd, stats.id]


	#Blank line for spacing
	DigEatDF.loc[len(DigEatDF)] = ['']*8
	#Add all statistics lists onto the dataframe
	DigEatDF.loc[len(DigEatDF)] = avgLine
	DigEatDF.loc[len(DigEatDF)] = stdLine
	DigEatDF.loc[len(DigEatDF)] = countsLine

	return DigEatDF
