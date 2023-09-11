# A Dendrite Branch is added by a PyramidalNeuron

# Adds potentials inserted by all action potentials
# in current timeslot to branch, and determines if
# a potential will be inserted deeper into the dendrite

from Globals import *
from PotentialRecord import *

class DendriteBranch:

	def __init__(self, threshold):
		self.conditionPermanence = False
		self.excitatoryInputs = []
		self.inhibitoryInputs = []
		self.inhibitoryInputWeights = []
		self.recentActivityOfInhibitoryInputs = []
		self.conditionRecordingManagementInputs = []
		self.conditionRecordingManagementInputWeights = []
		self.recentActivityOfConditionRecordingManagementInputs = []
		self.timeSinceLastActivityOfBranch = 100
		self.timeSinceBackpropagatedSomaActionPotential = 100
		self.potentialRecord = PotentialRecord()
		self.threshold = threshold
		self.firingStatus = False
		self.branchFirings = 0

    
	def presentSingleSourceExcitatoryInputsToBranch(self, inputs):
        #FIRST STEP IS TO SHIFT potentialRecord ALONG ONE TIMESLOT
		self.potentialRecord.shift()

        #NEXT, INCREASE timeSinceLastActivityOfBranch BY ONE
		timeSinceLastActivityOfBranch += 1

		# NEXT, INCREASE THE NUMBER OF TIMESLOTS SINCE CHANGE 
		# BY ONE FOR EVERY CHANGE TO EVERY INPUT.  THE CHANGE 
		# RECORD FOR INPUTS IS RECORDED IN recentWeightChangeHistory. 
		# EACH ELEMENT IN recentWeightChangeHistory IS THE RECORD FOR 
		# ONE INPUT. THE RECORD IS AN OrderedCollection MADE UP TO 
		# TWO OrderedCollection. THE FIRST OF THESE TWO OrderedCollections 
		# CONTAINS THE NUMBER OF TIMESLOTS SINCE THE CHANGE OCCURRED, 
		# THE SECOND CONTAINS THE MAGNITUDE OF THE CHANGE.
		
		for input in self.excitatoryInputs:
			input.advanceTime()

			# NEXT, IF MORE THAN 600 TIMESLOTS (= 200 MILLISECONDS) HAVE ELAPSED, 
			# REVERSE THE CHANGE AND DELETE THE RECORD IN recentWeightChangeHistory"
			input.handleMaxTimeSlots()

			# NEXT, CHECK IF THERE ARE FIVE (OR MORE, BUT THAT SHOULD NOT OCCUR) INCREASES 
			# FOR ANY INPUT, AND IF SO, MAKE THE INCREASES PERMANENT BY ELIMINATING THE 
			# ENTRIES IN recentWeightChangeHistory
			input.makeHighContributionPermanent()

			# NEXT, INCREASE recentActivityOfExcitatoryInputs BY ONE FOR EACH INPUT"
			self.recentActivity += 1

			# GO THROUGH THE excitatoryInputs OF THE BRANCH, AND CHECK IF THERE IS 
			# AN ACTION POTENTIAL FOR THAT INPUT. IF SO, SET TIME SINCE INPUT FOR 
			# THAT INPUT TO ZERO, AND INCREMENT ALL THE FIELDS OF potentialRecord 
			# FOR THE BRANCH"	See trace https://github.com/simuliinc/ReArc/issues/16

			if (inputs[input.getInput()]) == 1:
				input.recentActivity = 0
				self.potentialRecord.adjustPotentialByWeight(input.weight)

			# SET firingProbability AT 0% IF POTENTIAL IN CURRENT TIMESLOT IS LESS 
			# THAN OR EQUAL TO THRESHOLD, AT 100% IF POTENTIAL IS 10% OR MORE OVER 
			# THRESHOLD. SCALED BETWEEN 10% AND 100% PROBABILITIES WHEN POTENTIAL 
			# IS 1% TO 10% OVER THRESHOLD see PotentialRecord.py

			# IntegerCollection CONTAINS THE NUMBERS 0 TO 99. A NUMBER IS SELECTED 
			# AT RANDOM FROM IntegerCollection AND IF IT IS LESS THAN firingProbability 
			# THE BRANCH IF FIRING. THIS ALGORITHM IMPLEMENTS THE % PROBABILITY 
			# DETERMINED BY firingProbability

			if self.potentialRecord.fireforThreshold(self.threshold):
				# IF BRANCH FIRES, SET potentialRecord AND timeSinceLastActivityOfBranch TO ZERO
				self.firingStatus = True
				self.potentialRecord.reset()
				self.timeSinceLastActivityOfBranch = 0
				self.branchFirings += 1

		return self.firingStatus

             
class ExcitatoryInput:
	def __init__(self, input):
		self.input = input
		self.weight = CorticalConditionDefiningInputWeight
		self.recentActivity = 0
		self.connectionTime = 0
		self.changeMagnitude = 0
		self.branchFiringSinceWeightChange = 0
		self.permanentConnection = False
		self.history = [{'connectionTime':0, 'changeMagnitude':0}]

	def advanceTime(self):
		self.connectionTime += 1
		for item in self.history:
			item["connectionTime"] += 1

	def handleMaxTimeSlots(self):
		# IF MORE THAN 600 TIMESLOTS (= 200 MILLISECONDS) HAVE ELAPSED, 
		# REVERSE THE CHANGE AND DELETE THE RECORD IN recentWeightChangeHistory
		if self.history[0]['connectionTime'] > 600:
			self.weight /= self.history[0]['changeMagnitude']
			del self.history[0]

	def makeHighContributionPermanent(self):
		# NEXT, CHECK IF THERE ARE FIVE (Currently set to 3 RJT)(OR MORE, BUT THAT SHOULD NOT OCCUR) INCREASES 
		# FOR ANY INPUT, AND IF SO, MAKE THE INCREASES PERMANENT BY ELIMINATING THE 
		# ENTRIES IN recentWeightChangeHistory
		# added permanentConnection variable RJT

		if len(self.history) >= BranchContributionsWithin200msecForPermanentWeightChange:
			self.permanentConnection = True
			for history in self.history:
				del history

	def getInput(self):
		return self.input
	