#This stores test and correct sense that we're testing for
class SensesObject:
	def __init__(self, testing, correct):
			self.testing = testing
			self.correct = correct
#This stores current behavior like digging, approached, and sense
class BehaviorObject:
	def __init__(self, Approached, trial):
			self.Approached = Approached
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


