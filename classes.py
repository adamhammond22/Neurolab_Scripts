#This stores the sense we're testing for, the correct sense for the test, the total trials
class SensesObject:
	def __init__(self, testing, correct, totalTrials):
			self.testing = testing
			self.correct = correct
			self.totalTrials = totalTrials

#This stores current behavior to be passed to dig_correctness()
#stores what side mouse approached, and trial number
class BehaviorObject:
	def __init__(self, trial):
			self.hasApproached = False
			self.approachDirection = ""
			self.trial = trial
			self.approachTime = ""
			self.isDigging = False

#This stores simple counts of all behaviors, for statistics
class BehaviorStatsObject:
	def __init__(self):
		self.t = 0
		self.l = 0
		self.r = 0
		self.v = 0
		self.e = 0
		self.cd = 0
		self.id = 0
		self.md = 0 #missed dig


#This stores simple counts of all decision time behaviors, for statistics
class DecisionStatsObject:
	def __init__(self):
		self.cd = 0
		self.id = 0
		self.cr = 0
		self.ms = 0


