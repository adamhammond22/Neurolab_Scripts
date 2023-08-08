import pandas as pd
from helperfunctions import dig_correctness, calcSeriesMean, calcSeriesMedian, calcSeriesStd
from classes import SensesObject, DecisionStatsObject, BehaviorObject
import warnings
#must pip install: pandas, tkinter, and jinja2

# The number of "last correct" digs to show
NumberOfLastCorrectToShow = 6

def createDecisionTimeDF(BehaviorDF, SetupDF, senses):
	#Initalize output dataframe for "Behavior" sheet
	DecisionTimeDF = pd.DataFrame(columns=["ApproachTime","ApproachBehavior","EventTime","EventBehavior",
		"Trial","All","Correct Dig","Incorrect Dig","Correct Rejection","Miss", "Last Correct", "Last Incorrect", "Last Correct Digs"
	])

	# Obj to pass to dig_correctness() function. As well as to generally track what the mouse's behavior is
	# holds hasApproached, approachDirection, trial, approachTime
	mouse = BehaviorObject(0)
	
	#Obj holding counts of CD, ID, CR, Miss, for statistics line
	stats = DecisionStatsObject()

	# Initalize 
	totalTrials = int(senses.totalTrials)
 
 	# Initalize last correct variables
	lastCorrectString = ""
	lastIncorrectString = ""
	lastCorrectDigsString = ""
	lastDigCorrect = None

	#Iterate through our Behavior DF
	for index, row in BehaviorDF.iterrows():

		Behavior = row["Behavior"]
		#If mouse has approached, look for leave, dig, or eat	
		if mouse.hasApproached:
			timeTaken = "{0:.3f}".format(float(row["Time"]) - float(mouse.approachTime))

			match Behavior:
				case "Leave":
					mouse.trial = int(row["Trial"])
					#Determine correctness of this leave
					#It is simply the OPPOSITE of the correctness of a dig
					if not dig_correctness(SetupDF, mouse, senses):
						#If this leave was correct, it's a Miss
						stats.cr += 1
						DecisionTimeDF.loc[len(DecisionTimeDF)] = [mouse.approachTime,
							mouse.approachDirection, str(row["Time"]), "LeaveCR", str(row["Trial"]),
							timeTaken, "", "",timeTaken,"","","",""]	

					else:
						#If the mouse left even though the dig was correct, it's a miss
						stats.ms += 1
						DecisionTimeDF.loc[len(DecisionTimeDF)] = [mouse.approachTime,
							mouse.approachDirection, str(row["Time"]), "Miss", str(row["Trial"]),
							timeTaken, "", "","",timeTaken,"","",""]

				case "CorrectDig":
					stats.cd += 1

     				# ========== Last Correct Logic ========== #
					# If the last dig was correct, put the time taken in the last correct string
					if (lastDigCorrect == True):
						lastCorrectString = timeTaken
						lastIncorrectString = ""
					# If the last dig was not correct, put the time taken in the last incorrect string
					elif (lastDigCorrect == False):
						lastCorrectString = ""
						lastIncorrectString = timeTaken
					# Set the lastDigCorrect variable for future use
					lastDigCorrect = True

					# ========== Last Correct Digs Logic ========== #
					if((totalTrials - int(row["Trial"])) <= NumberOfLastCorrectToShow):
						lastCorrectDigsString = timeTaken
					else:
						lastCorrectDigsString = ""
     
					DecisionTimeDF.loc[len(DecisionTimeDF)] = [mouse.approachTime,
						mouse.approachDirection, str(row["Time"]), Behavior, str(row["Trial"]),
						timeTaken, timeTaken, "","","",lastCorrectString, lastIncorrectString, lastCorrectDigsString]
					


				case "IncorrectDig":
					stats.id += 1
          
					# If the last dig was correct, put the time taken in the last correct string
					if (lastDigCorrect == True):
						lastCorrectString = timeTaken
						lastIncorrectString = ""
					# If the last dig was not correct, put the time taken in the last incorrect string
					elif (lastDigCorrect == False):
						lastCorrectString = ""
						lastIncorrectString = timeTaken
					# Set the lastDigCorrect variable for future use
					lastDigCorrect = False				

					DecisionTimeDF.loc[len(DecisionTimeDF)] = [mouse.approachTime,
						mouse.approachDirection, str(row["Time"]), Behavior, str(row["Trial"]),
						timeTaken, "", timeTaken,"","",lastCorrectString, lastIncorrectString, ""]

				case "MissDig":
						#If the mouse left after a correct dig (meaning it didnt eat), that's also a miss
						stats.ms += 1
						DecisionTimeDF.loc[len(DecisionTimeDF)] = [mouse.approachTime,
							mouse.approachDirection, str(row["Time"]), "Miss", str(row["Trial"]),
							timeTaken, "", "","",timeTaken,"","", ""]

			mouse.hasApproached = False

		#If mouse has not approached, look for an approach
		else:

			if Behavior == "ApproachRight":
				mouse.hasApproached = True
				#Track whether it's right or left
				mouse.approachDirection = Behavior
				#Track time of approach
				mouse.approachTime = row["Time"]

			elif Behavior == "ApproachLeft":
				mouse.hasApproached = True
				#Track whether it's right or left
				mouse.approachDirection = Behavior
				#Track time of approach
				mouse.approachTime = row["Time"]


	# Compute Statistics in a list and save them
	# Avg statistics list


	#RuntimeWarnings in this block may occur for empty columns. Ignore them. 
	with warnings.catch_warnings():
		warnings.simplefilter("ignore", category=RuntimeWarning)

		avgLine = ['']*3 + ['Average', '', "{0:.3f}".format(pd.to_numeric(DecisionTimeDF['All']).mean()),
			calcSeriesMean(DecisionTimeDF['Correct Dig']),
			calcSeriesMean(DecisionTimeDF['Incorrect Dig']),
			calcSeriesMean(DecisionTimeDF['Correct Rejection']),
			calcSeriesMean(DecisionTimeDF['Miss']),
			calcSeriesMean(DecisionTimeDF['Last Correct']),
			calcSeriesMean(DecisionTimeDF['Last Incorrect']),
			calcSeriesMean(DecisionTimeDF['Last Correct Digs'])]
		#Standard Dev statistics list	
		stdLine = ['']*3 + ['StDev', '', "{0:.3f}".format(pd.to_numeric(DecisionTimeDF['All']).std()),
			calcSeriesStd(DecisionTimeDF['Correct Dig']),
			calcSeriesStd(DecisionTimeDF['Incorrect Dig']),
			calcSeriesStd(DecisionTimeDF['Correct Rejection']),
			calcSeriesStd(DecisionTimeDF['Miss']),
			calcSeriesStd(DecisionTimeDF['Last Correct']),
			calcSeriesStd(DecisionTimeDF['Last Incorrect']),
			calcSeriesStd(DecisionTimeDF['Last Correct Digs'])]
		#Counts of each one (this is saved in the stats structure)

		medianLine = ['']*3 + ['Median', '', "{0:.3f}".format(pd.to_numeric(DecisionTimeDF['All']).median()),
			calcSeriesMedian(DecisionTimeDF['Correct Dig']),
			calcSeriesMedian(DecisionTimeDF['Incorrect Dig']),
			calcSeriesMedian(DecisionTimeDF['Correct Rejection']),
			calcSeriesMedian(DecisionTimeDF['Miss']),
			calcSeriesMedian(DecisionTimeDF['Last Correct']),
			calcSeriesMedian(DecisionTimeDF['Last Incorrect']),
			calcSeriesMedian(DecisionTimeDF['Last Correct Digs'])]
		#Counts of each one (this is saved in the stats structure)

		countsLine = ['']*3 + ['Total', '',stats.cd+stats.id+stats.cr+stats.ms,
			stats.cd, stats.id, stats.cr, stats.ms] + ['']*3


		#Blank line for spacing
		DecisionTimeDF.loc[len(DecisionTimeDF)] = ['']*13
		#Add all statistics lists onto the dataframe
		DecisionTimeDF.loc[len(DecisionTimeDF)] = avgLine
		DecisionTimeDF.loc[len(DecisionTimeDF)] = stdLine
		DecisionTimeDF.loc[len(DecisionTimeDF)] = medianLine
		DecisionTimeDF.loc[len(DecisionTimeDF)] = countsLine

	return DecisionTimeDF
