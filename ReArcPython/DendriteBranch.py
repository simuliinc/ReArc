# A Dendrite Branch is added by a PyramidalNeuron

# Adds potentials inserted by all action potentials
# in current timeslot to branch, and determines if
# a potential will be inserted deeper into the dendrite

from Globals import *
from PotentialRecord import *
import itertools

class DendriteBranch:

	def __init__(self, threshold):
		self.conditionPermanence = False
		self.excitatoryInputs = []
		self.inhibitoryInputs = []
		self.inhibitoryInputWeights = []
		self.recentActivityOfInhibitoryInputs = []
		self.conditionRecordingManagementInputs = []
		self.timeSinceLastActivityOfBranch = 100
		self.timeSinceBackpropagatedSomaActionPotential = 100
		self.potentialRecord = PotentialRecord()
		self.threshold = threshold
		self.firingStatus = False
		self.branchFirings = 0

    
	def presentExcitatoryInputsToBranch(self, inputs, multipleSource = False, managementInputs=[]):
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
			input.recentActivity += 1

			# GO THROUGH THE excitatoryInputs OF THE BRANCH, AND CHECK IF THERE IS 
			# AN ACTION POTENTIAL FOR THAT INPUT. IF SO, SET TIME SINCE INPUT FOR 
			# THAT INPUT TO ZERO, AND INCREMENT ALL THE FIELDS OF potentialRecord 
			# FOR THE BRANCH"	See trace https://github.com/simuliinc/ReArc/issues/16

			if (inputs[input.getInput()]) == 1:
				input.recentActivity = 0
				self.potentialRecord.adjustPotentialByWeight(input.weight)

		
		# GO THROUGH THE conditionRecordingManagementInputs AND CHECK IF THERE IS AN 
		# ACTION POTENTIAL FOR THAT INPUT. IF SO, INCREMENT ALL THE FIELDS OF potentialRecord
		
		if len(managementInputs):
			for input in self.conditionRecordingManagementInputs:
				if managementInputs[input.value] == 1:
					self.potentialRecord.adjustPotentialByWeight(input.conditionWeight)

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

	def addConditionRecordingManagementInput(self, connection):
		# Adds a connection identity (connection) to conditionRecordingManagementInputs, 
		# makes the corresponding connection weight CorticalConditionRecordingManagementInputWeight 
		# in conditionRecordingManagementInputWeights.
		#
		#  ****************************************************************************************************
		#  * (Currently turned off because NumberOfConditionRecordingOutputsFromBlackBoxHippocampus = 0 RJT)  *
		#  ****************************************************************************************************
		#
		self.managementInputs.append(RecordingManagementInputs(connection, CorticalConditionRecordingManagementInputWeight))

	def reduceSynapticWeights(self, proportion):
		for input in self.excitatoryInputs:
			input.reduceSynapticWeight(proportion)

	def addExcittatoryInput(self, connection):
		# Adds a connection identity (connection) to excitatoryInputs, makes the corresponding connection weight 
		# 10 in excitatoryInputWeights, and makes the time since the input was last active 100 timeslots in 
		# recentActivityOfExcitatoryInputs.  
		# branchFiringsSinceLastIncreaseInExcitatoryWeights is set initially at true for each input. The first time 
		# the DendriteBranch instance fires and receives a backpropagating action potential from the neuron, 
		# if the input weight is increased this variable will be set at 0, and set at 2 if the input does not 
		# fire with the timing to have a weight increase. Each subsequent time the DendriteBranch instance 
		# fires followed by a backpropagating action potential, this variable will be set at 0 if the input 
		# weight is increased, and increased by 1 if the input does not fire with the timing to have a weight 
		# increase. If the variable reaches 5, the corresponding input weight is decreased by 10%. If the weight 
		# is less that 1.0, the input is deleted. 
		# When a weight reaches its maximum and is confirmed at that maximum, there will be no further changes. 
		# This will be achieved by setting its corresponding lastIncreaseInExcitatoryWeights element to false.

		input = ExcitatoryInput(connection)
		input.weight = CorticalConditionDefiningInputWeight
		input.recentActivity = 100
		input.branchFiringSinceWeightChange = True
		self.excitatoryInputs.append(input)	
		self.conditionPermanence = False

	def addExcitatoryInputFromSource(self, connection, source):
		# Adds a connection identity (connection) to excitatoryInputs, makes the corresponding connection weight 10 
		# in excitatoryInputWeights, and makes the time since the input was last active 100 timeslots in 
		# recentActivityOfExcitatoryInputs.
		# branchFiringsSinceLastIncreaseInExcitatoryWeights is set initially at true for each input. The first time 
		# the DendriteBranch instance fires and receives a backpropagating action potential from the neuron, 
		# if the input weight is increased this variable will be set at 0, and set at 2 if the input does not 
		# fire with the timing to have a weight increase. Each subsequent time the DendriteBranch instance fires 
		# followed by a backpropagating action potential, this variable will be set at 0 if the input weight is 
		# increased, and increased by 1 if the input does not fire with the timing to have a weight increase. 
		# If the variable reaches 5, the corresponding input weight is decreased by 10%. If the weight is less that 1.0, 
		# the input is deleted. 
		# When a weight reaches its maximum and is confirmed at that maximum, there will be no further changes. This will 
		# be achieved by setting its corresponding lastIncreaseInExcitatoryWeights element to false.
		
		input = ExcitatoryInput(connection, source)
		input.weight = 1
		input.recentActivity = 100
		input.branchFiringSinceWeightChange = True
		input.history.append({'connectionTime':0, 'changeMagnitude':0})
		self.conditionPermanence = False

	def addExcitatoryInputWithWeight(self, connection, initialSynapticWeight):
		# Adds a connection identity (connection) to excitatoryInputs, makes the corresponding connection 
		# weight 10 in excitatoryInputWeights, and makes the time since the input was last active 100 
		# timeslots in recentActivityOfExcitatoryInputs.
		# branchFiringsSinceLastIncreaseInExcitatoryWeights is set initially at true for each input. 
		# The first time the DendriteBranch instance fires and receives a backpropagating action potential 
		# from the neuron, if the input weight is increased this variable will be set at 0, and set at 2 if 
		# the input does not fire with the timing to have a weight increase. Each subsequent time the 
		# DendriteBranch instance fires followed by a backpropagating action potential, this variable will 
		# be set at 0 if the input weight is increased, and increased by 1 if the input does not fire with 
		# the timing to have a weight increase. If the variable reaches 5, the corresponding input weight 
		# is decreased by 10%. If the weight is less that 1.0, the input is deleted. 
		# When a weight reaches its maximum and is confirmed at that maximum, there will be no further changes. 
		# This will be achieved by setting its corresponding lastIncreaseInExcitatoryWeights element to false.
		input = ExcitatoryInput(connection)
		input.weight = initialSynapticWeight
		input.recentActivity = 100
		input.branchFiringSinceWeightChange = True
		self.conditionPermanence = False
	
	def adjustWeightsOfRecentlyActiveMultipleSourceInputs(self, numberOfSources):
		for source in range(1, numberOfSources):
			self.adjustWeightsOfRecentlyActiveInputs(True, source)
	
	def adjustWeightsOfRecentlyActiveInputs(self, multipleSources = False, source=None):

		# NOTE MARCH 10th 2008:
		# MAY NEED TO REVERSE INCREASE IF DOES NOT REPEAT WITHIN, SAY, 100 MSEC. IN OTHER WORDS, 
		# A CONDITION MUST OCCUR MULTIPLE TIMES WITHIN THE SAME ATTENTION PERIOD FOR IT TO BE ESTABLISHED. 
		# AT THE MOMENT, ONLY DECREASES IF CONNECTION WAS NOT RECENTLY ACTIVE WHEN A BACKPROPAGATING ACTION 
		# POTENTIAL IS RECEIVED
		# When the neuron fires, it sends a backpropagating action potential into its dendrite.This backpropagating 
		# action potential increases the weights of synapses that have recently received an action potential, provided 
		# that the branch has fired recently.
		# IF the branch has fired within the last 5 milliseconds, all synapses that have received an action potential 
		# within the last 5 milliseconds will have their weights increased.
		# Activity of synapse
		# Timeslots before		% increase
		# 1				10
		# 2				10
		# 3				10
		# 4				15
		# 5				15
		# 6				15
		# 7				20
		# 8				20
		# 9				20
		# 10			15
		# 11			15
		# 12			15
		# 13			10
		# 14			10
		# 15			10

		#WEIGHTS CAN ONLY BE ADJUSTED IF conditionPermanence = false
		if not self.conditionPermanence:
			# WEIGHTS ARE ONLY ADJUSTED IF THE BRANCH HAS FIRED WITHIN THE LAST 5 MILLISECONDS OR 15 TIMESLOTS"
			if self.timeSinceLastActivityOfBranch < 16:	
	
				# THE FOLLOWING CODE IS ONLY INVOKED THE FIRST TIME THE BRANCH RECEIVES A BACKPROPAGATING ACTION 
				# POTENTIAL. THE CODE SETS ALL THE ELEMENTS IN branchFiringsSinceLastIncreaseInExcitatoryWeights TO 1."
				if multipleSources: 
					inputs = self.excitatoryInputsForSoruce(source)
				else: 
					inputs = self.excitatoryInputs

				i = 0
				for input in inputs:
					input.receiveBackPropogation()
					
					# THE FOLLOWING CODE INCREASES THE CONNECTION WEIGHT IF THE INPUT HAS BEEN ACTIVE SHORTLY BEFORE 
					# THE BACKPROPAGATING ACTION POTENTIAL WAS RECEIVED FROM THE NEURON"	
					
					# Use the reecent activity value as an index to loook up the weight increase
					# Modify the recent activity value to account for 0 based Python lookup and ensure that we don't 
					# index over 14 which is the last position we define for percent increase  
					index =  min((input.recentActivity - 1),14)
					input.increaseConnectionWeightForIndex(index)
										
					# THE FOLLOWING CODE INCREASES branchFiringsSinceLastIncreaseInExcitatoryWeights IF THE CORRESPONDING CONNECTION 
					# WEIGHT WAS NOT INCREASED (INDICATED BY branchFiringsSinceLastIncreaseInExcitatoryWeights NOT EQUAL TO 0). 
					# NOTE THAT THE FIRST TIME THE BRANCH RECEIVES THE adjustWeightsOfRecentlyActiveInputs MESSAGE, THE ELEMENT IN 
					# branchFiringsSinceLastIncreaseInExcitatoryWeights CORRESPONDING WITH INPUTS THAT WERE NOT RECENTLY ACTIVE IS 
					# SET AT 2. SUBSEQUENT TIMES IT IS INCREASED BY 1
					input.decreaseInactiveConnectionWeight()
					
				# THE FOLLOWING CODE REMOVES ALL THE CONNECTIONS SET AT false (now marked as deleteMe RJT) BECAUSE THEIR INPUT 
				# WEIGHT WAS <= 1 AFTER 10 INCREASES IN ACTIVE BRANCH WEIGHTS. 
				self.excitatoryInputs = list(itertools.filterfalse(lambda x: x.excitatoryInputs.deleteMe, self.excitatoryInputs))
				
				# Multiple Sources do not adjust the Hippocampus
				if not multipleSources:
					for recordingManagementInput in self.conditionRecordingManagementInputs:
						# THIS CODE DECREASES THE WEIGHT OF THE HIPPOCAMPAL INPUTS
						recordingManagementInput.adjustWeightForHippocampus()

	def excitatoryInputsForSoruce(self, source):
		inputs = list(filter(lambda x: (x.source == source), self.excitatoryInputs))	



class ExcitatoryInput:
	def __init__(self, input, source=1):
		self.input = input
		self.source = source # use this index to identify multiple sources of inputs being processed
		self.weight = CorticalConditionDefiningInputWeight
		self.recentActivity = 0
		self.connectionTime = 0
		self.changeMagnitude = 0
		self.branchFiringSinceWeightChange = 0
		self.backpropagatingActionPotentialRecieved = False
		self.permanentConnection = False
		self.history = [{'connectionTime':0, 'changeMagnitude':0}]
		self.weightIncreasePercentage=[]
		self.initWeightIncreasePercentage()
		self.deleteMe = False

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
	
	def initWeightIncreasePercentage(self):
		# Timeslots before		% increase (documented) % increase (in code RJT)
		# 1						10						5
		# 2						10						5
		# 3						10						5
		# 4						15						10
		# 5						15						10
		# 6						15						10	
		# 7						20						15
		# 8						20						15
		# 9						20						15
		# 10					15						10
		# 11					15						10
		# 12					15						10
		# 13					10						5
		# 14					10						5
		# 15					10						5
		self.weightIncreasePercentage = [5]*3 + [10]*3 + [15]*3 + [10]*3 + [5]*3

	def increaseConnectionWeightForIndex(self, index):
		percent = 1 + self.weightIncreasePercentage[index]/100
		self.weight *= 1 + percent
		self.weight = min(MaximumBranchSynapticWeight, self.weight)
		self.history.append([{'connectionTime':0, 'changeMagnitude':percent}])
		self.branchFiringSinceWeightChange = 0

	def decreaseInactiveConnectionWeight(self):
		# THE FOLLOWING CODE INCREASES branchFiringsSinceLastIncreaseInExcitatoryWeights IF THE CORRESPONDING CONNECTION 
		# WEIGHT WAS NOT INCREASED (INDICATED BY branchFiringsSinceLastIncreaseInExcitatoryWeights NOT EQUAL TO 0). 
		# NOTE THAT THE FIRST TIME THE BRANCH RECEIVES THE adjustWeightsOfRecentlyActiveInputs MESSAGE, THE ELEMENT IN 
		# branchFiringsSinceLastIncreaseInExcitatoryWeights CORRESPONDING WITH INPUTS THAT WERE NOT RECENTLY ACTIVE IS 
		# SET AT 2. SUBSEQUENT TIMES IT IS INCREASED BY 1
		if self.branchFiringSinceWeightChange > 0:
			self.branchFiringSinceWeightChange += 1
		if self.branchFiringSinceWeightChange > BranchFiringsToDecreaseInSynapticWeights:
			self.weight /= 1.1
		if self.weight < 1:
			self.deleteMe = True

	def reduceSynapticWeight(self, proportion):
		self.weight *= proportion

	def receiveBackPropogation(self):
		# THE FOLLOWING CODE IS ONLY INVOKED THE FIRST TIME THE BRANCH RECEIVES A BACKPROPAGATING ACTION 
		# POTENTIAL. THE CODE SETS ALL THE ELEMENTS IN branchFiringsSinceLastIncreaseInExcitatoryWeights TO 1."
		if not self.backpropagatingActionPotentialRecieved:
			self.branchFiringSinceWeightChange = 1
			self.backpropagatingActionPotentialRecieved = True

class RecordingManagementInputs:

	def __init__(self, connection, conditionWeight):
		self.value = connection
		self.conditionWeight = conditionWeight
		self.recentActivityOfCondition = 0
	
	def adjustWeightForHippocampus(self):
		self.conditionWeight *= HippocampalWeightReductionFactor

	