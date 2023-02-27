#This stores the sense we're testing for, and the correct sense for the test
class SensesObject:
	def __init__(self, testing, correct):
			self.testing = testing
			self.correct = correct

#This stores current behavior to be passed to dig_correctness()
#stores what side mouse approached, and trial number
class BehaviorObject:
	def __init__(self, Approached, trial):
			self.Approached = Approached
			self.trial = trial

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


#This stores simple counts of all decision time behaviors, for statistics
class DecisionStatsObject:
	def __init__(self):
		self.cd = 0
		self.id = 0
		self.cr = 0
		self.ms = 0


