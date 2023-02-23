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

def dig_correctness(df, mouse, sense):
	#print("beginning dig correctness, testing for" + str(sense.testing))
	#If we're testing for texture
	if(sense.testing == "texture"):
		CurrentLeftSense = df.at[mouse.trial-1, "L_Texture"]
	#Otherwise if we're testing for odor
	else:
		CurrentLeftSense = df.at[mouse.trial-1, "L_Odor"]

	#If Left sense is the correct sense
	if(CurrentLeftSense == sense.correct):
		#return true if we approached left
		#print("Left sense was correct, we aproeached" + mouse.hasApproached)
		#print("Returning" + str(bool(mouse.hasApproached == "Left")))
		return bool(mouse.hasApproached == "Left")
	#If Right sense is the correct sense
	else:
		#return true if we approached right
		#print("Right sense was correct, we aproeached" + mouse.hasApproached)
		#print("Returning" + str(bool(mouse.hasApproached == "Right")))
		return bool(mouse.hasApproached == "Right")

#Highlights a Dataframe row based on the behavior of that row
def highlight(s):
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
	if((s.name < 8) and (0 < s.name)):
		del styleList[5:9]
		styleList = styleList + ['background-color: #C6E0B4']*4
	return styleList

