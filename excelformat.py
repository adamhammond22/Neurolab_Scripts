import pandas as pd
import tkinter as tk
import re
import xlsxwriter #removable - was supposed to work w duplicate column names but cant do that bc styling
from tkinter import filedialog
#must pip install: pandas, tkinter, and jinja2

# ====== user selection window ====== #
root = tk.Tk()
root.withdraw() #Hide root window

#"Warning: could not parse header or footer"
#Benign issue- to remove: go to excel on the offending file.
#File->Info->CheckForIssues->InspectDocument(for headers/footers)->Remove header and footer
#I've done this once and it does not impact the program

#This stores test and correct sense that we're testing for
class SensesObject:
	def __init__(self, testing, correct):
			self.testing = testing
			self.correct = correct
#This stores current behavior like digging, approached, and sense
class BehaviorObject:
	def __init__(self, isDigging, hasApproached, trial):
			self.isDigging = isDigging
			self.hasApproached = hasApproached
			self.trial = trial

#This stores simple counts of all behaviors, for statistics
class StatsObject:
	def __init__(self):
		self.t = 0
		self.l = 0
		self.r = 0
		self.v = 0
		self.e = 0
		self.cd = 0
		self.id = 0

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
	print(len(s))
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
	#Should work in theory but does not
	# if((s.name < 8) and (0 < s.name)):
	# 	#print("doing thing, len = " + str(len(styleList)))
	# 	del styleList[5:9]
	# 	styleList.extend(['background-color: green'] for i in range(4))
	# 	#print("after our thing, len" + str(len(styleList)))
	return styleList

#to make non-hardcoded just swap which one is commented
filepath = "C:/Users/Adam/Desktop/Aster/Neurolab_Scripts/A005_IDS_tab_new_corrected.xlsx" #HARDCODED FILEPATH
#filepath = filedialog.askopenfilename()

# ========== Try reading file into input dataframes ========== #
if not filepath:
	print("No file given")
	exit()
try:
	RawDF = pd.read_excel(filepath, "Raw")
except:
	print("Pandas could not open file '"+ filepath +"' with sheet 'Raw'")
	exit()
try:
	#keep def n/a nessecary to make sure na is not coverted
	SetupDF = pd.read_excel(filepath, "Setup", keep_default_na=False)
except:
	print("Pandas could not open file '"+ filepath +"' with sheet 'Setup'")
	exit()

# ===== Verify Setup and Raw contain needed columns ===== #

#Checking Setup
required_cols = {"L_Texture","L_Odor","R_Texture","R_Odor","Trial",
		"CorrTexture","CorrOdor"}
if not (required_cols.issubset(required_cols)):
	print("Fatal Error: Unexpected Setup Column Names")
	print("Expected Columns:" + str(expected_cols))
	print("But recieved columns:" + str(cols))

#Checking Raw
cols = set(RawDF.columns)
required_cols = {"Behavior","Behavior type","Time"}
if not (required_cols.issubset(required_cols)):
	print("Fatal Error: cannot find needed Raw Columns")
	print("Needed Columns:" + str(required_cols))
	print("But recieved columns:" + str(cols))

# ===== Verify that Setup and Raw have same number of trials ===== #

#grab all raw rows with behavior 't'
trows = RawDF.loc[RawDF["Behavior"] == "t"]
#grab the setup row with the largest "Trial" value
setupTrials = SetupDF.loc[SetupDF["Trial"].idxmax()]

#compare them 
if(len(trows) != setupTrials["Trial"]):
	print("Fatal Error: Setup Trials and Raw 't' count do not match.")
	exit()

# ========== Init Variables and Objects ========== #

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

# ========== Iterate Through Raw File ========== #

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

# BehaviorDF = BehaviorDF.insert(5, "", ["","TrialStart","ApproachRight",
# 		"ApproachLeft","CorrectDig","IncorrectDig","Eat","Leave"])

stats = pd.concat([pd.Series([""]),
	pd.Series(["","TrialStart","ApproachRight","ApproachLeft",
	"CorrectDig","IncorrectDig","Eat","Leave"]),
	pd.Series(["", stats.t, stats.r, stats.l, stats.cd,
		stats.id, (stats.e//2), stats.v]),
	pd.Series(["","","Approach","","Dig"]),
	pd.Series(["","",(stats.l+stats.r),"",(stats.cd+stats.id)])],
 		axis=1)
stats.rename(columns={0: "",1: "NamesA",2: "StatsA",3:"NamesB", 4:"StatsB"}, inplace=True)
#stats.rename(columns={3: "",1: ""}, inplace=True)
print(stats)
# BehaviorDF[""] = pd.Series(["","TrialStart","ApproachRight",
#  		"ApproachLeft","CorrectDig","IncorrectDig","Eat","Leave"])
BehaviorDF	= pd.concat([BehaviorDF, stats], axis=1)
#Apply the highlight to our dataframe rows
BehaviorDF = BehaviorDF.style.apply(highlight, axis=1)

#Use ExcelWriter to write
with pd.ExcelWriter('ScriptOutput.xlsx', engine='xlsxwriter') as writer:
	BehaviorDF.to_excel(writer, sheet_name='Behavior 4D', index=False);
	#Add more sheets to write here!

print("Program finished")
