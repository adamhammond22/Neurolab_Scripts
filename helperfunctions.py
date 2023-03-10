#Formats first and last given row indices within Dataframe, at column "Behavior" with given label
#Returns list of indices to drop (only keeping the first and last dig indices)
def formatDigs(df, indices, label):
	#Grab first row off of indices and set as label
	firstrow = indices.pop(0)
	df.iat[firstrow,1] = label
	
	if (len(indices) > 0): # if theres another element		
		#Grab last row off of indices and set label
		lastrow = indices.pop(len(indices)-1)
		df.iat[lastrow,1] = label

	#return remaining indices to drop
	return(indices)


#Determines the correctness of a dig given the setup df, mouse obj, and senses obj.
#We find the sense we're looking for, and determine if sense is on right or left.
#Then we return if the mouse approached from that direction.
#Returns True if dig is correct
#
#Taking the negation of this output gives the Leave correctness, because if a 
#dig is correct, then leaving was an incorrect rejection.
def dig_correctness(df, mouse, sense):
	#If we're testing for texture
	if(sense.testing == "texture"):
		CurrentLeftSense = df.at[mouse.trial-1, "L_Texture"]
	#Otherwise if we're testing for odor
	else:
		CurrentLeftSense = df.at[mouse.trial-1, "L_Odor"]
	#If Left sense is the correct sense
	if(CurrentLeftSense == sense.correct):
		#return true if we approached left
		return bool(mouse.Approached == "ApproachLeft")
	#If Right sense is the correct sense
	else:
		#return true if we approached right
		return bool(mouse.Approached == "ApproachRight")

#Returns a list of highlight colors for the Behavior Dataframe
#based on the behavior of that row. This is applied to each row of thre DF in style.apply()
def highlightBehaviorDF(s):
	#Highlight row based on behavior
	match s.Behavior:
		case "TrialStart":
			styleList = ['color: #4472C4'] * (len(s)-1) + ['color: black']
		case "ApproachRight":
			styleList =  ['color: #C65911'] * (len(s)-1) + ['color: black']
		case "ApproachLeft":
			styleList =  ['color: #C65911'] * (len(s)-1) + ['color: black']
		case "CorrectDig":
			styleList =  ['color: #FF0000'] * (len(s)-1) + ['color: black']
		case "IncorrectDig":
			styleList =  ['color: #548235'] * (len(s)-1) + ['color: black']
		case _:
			styleList =  ['color: black'] * len(s)
	
	#Add Green highlight to stats box
	#If 0 < trial < 8
	if((s.name < 8) and (0 < s.name)):
		#delete the last 4 els from list
		del styleList[5:9]
		#replace with green background color instead
		styleList = styleList + ['background-color: #C6E0B4']*4
	return styleList

#Returns a list of highlight colors for the Decision Time Dataframe
#based on the behavior of that row. This is applied to each row of thre DF in style.apply()
def highlightDecisionTimeDF(s):
	#2 orange rows always for approach
	styleList = ['color: #C65911']*2

	match str(s.EventBehavior):
		case "LeaveCR":
			styleList = styleList + ['color: #FF00C8']*3 + ['color: black']*(len(s)-5)
		case "Miss":
			styleList = styleList + ['color: #4472C4']*3 + ['color: black']*(len(s)-5)
		case "ApproachLeft":
			styleList = styleList + ['color: #C65911']*3 + ['color: black']*(len(s)-5)
		case "CorrectDig":
			styleList = styleList + ['color: #FF0000']*3 + ['color: black']*(len(s)-5)
		case "IncorrectDig":
			styleList = styleList + ['color: #548235']*3 + ['color: black']*(len(s)-5)
		case _:
			styleList =  ['color: black'] * len(s)

	return styleList

#Returns a list of highlight colors for the Dig Eat Dataframe
#based on the behavior of that row. This is applied to each row of thre DF in style.apply()
def highlightDigEatDF(s):

	styleList = []
	match str(s.DigBehavior):
		#Color the first 2 cells based on dig
		case "CorrectDig":
			styleList = ['color: #FF0000']*2
		case "IncorrectDig":
			styleList = ['color: #548235']*2
		case _:
			styleList =  ['color: black'] * 2

	#All other cells are black
	styleList = styleList + ['color: black']*(len(s)-2)
	return styleList