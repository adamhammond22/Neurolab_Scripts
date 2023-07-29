import re # import regular expression library
import pandas as pd

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


# This function takes the specified filepath, and attemps to open the file and extract the relevant sheets into dataframes
# The function is looking for a sheet named raw or setup (in any case) in a .xlsx file
# Takes: a string representing a filepath
# Returns: (rawDataFrame, setupDataFrame, filename, directoryPath) in a tuple
def handleFileOpen(filepath = ""):

	# ensure some filename was given 
	if (filepath == ""):
		print("\nFile Open Error: No file given")
		exit()

	#find filename by splitting by / and taking last one we will use this in order to name our output
	filename = filepath.split('/')[-1]
	#find remaining filepath by splitting by / and taking every part except the last, and joining it together again
	directoryPath = "/".join(filepath.split('/')[:-1])

	print("Opening file '" + filename + "'\n")

	#remove last 5 chars '.xlsx', we add the file extension later
	filename = filename[:-5]

	# ========== Ensure path is to a .xlsx file ========== #
	if not re.search(".xlsx$", str(filepath)):
		print("\nFile Open Error: Please specify a .xlsx file.")
		exit()

	
	#Try opening the excel file
	try:
		excelFile = pd.ExcelFile(filepath)
	except Exception as err:
		print("\nFile Open Error: Could not read file '"+ filepath+ "'")
		print(f"Unexpected error: {err=}, {type(err)=}")
		exit()

	rawName = ''
	setupName = ''

	# ========== Try finding sheet names ========== #
	#Iterate through sheet names in the file
	for sheetName in excelFile.sheet_names:

		#Search for a sheet named RAW, raw, rAw, etc
		if re.search("^[rR][aA][wW]$", str(sheetName)):
			rawName = sheetName
		#Search for a sheet named SETUP, setup, Setup, etc
		elif re.search("^[sS][eE][tT][uU][pP]$", str(sheetName)):
			setupName = sheetName

	#Check that we've found proper sheet names for raw and setup
	if(rawName == ''):
		print("\nError: Program could not find a sheet named 'Raw'")
		exit()
	if(setupName == ''):
		print("\nError: Program could not find a sheet named 'Setup'")
		exit()	


	# ========== Try reading found sheets into dataframes ========== #

	# read just the top row to get the column names for our converter dict
	rawHeader = pd.read_excel(filepath, rawName, nrows=0)
	setupHeader = pd.read_excel(filepath, rawName, nrows=0)

	# this is a dict where the key is each column name, and the value is the stripSpaces function
	# this 2 dicts will strip spaces of all columns in the RawDFand SetupDF
	raw_converter_dict = {column: stripSpaces for column in rawHeader.columns}
	setup_converter_dict = {column: stripSpaces for column in setupHeader.columns}

	#Try reading raw sheet into a dataframe
	try:
		RawDF = pd.read_excel(filepath, rawName, converters=raw_converter_dict)
	except Exception as err:
		print("\nFile Open Error: Could not open file '"+ filepath +"' with sheet '" + rawName + "'")
		print(f"Unexpected {err=}, {type(err)=}")
		exit()

	#Try reading setup sheet into a dataframe
	try:
		#keep_default_na is nessecary to make sure n/as are not coverted to something unexpected
		SetupDF = pd.read_excel(filepath, setupName, keep_default_na=False, converters=setup_converter_dict)
	except Exception as err:
		print("\nFile Open Error: Could not open file '"+ filepath +"' with sheet '" + setupName + "'")
		print(f"Unexpected {err=}, {type(err)=}")
		exit()

	# return our dataframes
	return (RawDF, SetupDF, filename, directoryPath)


# strips spaces from text if it is a string
# intended to be used when reading excel files
def stripSpaces(text):
    if isinstance(text, str):
        return text.strip()
    return text