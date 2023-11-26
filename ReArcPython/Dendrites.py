
# An ApicalDendrite is the output of a pyramidal cell. The Dendrite acts by modulating
# the excitatory and inhibitory signals.

from Globals import *
from PotentialRecord import *
import itertools
from DendriteBranch import *

class ApicalDendrite:
	def __init__(self, numOfBranches=0, threshold=None, numOfInputs = 0, inputs=[], source = None, managementInputs = 0):
		self.proximalInputs = []
		self.proximalInputWeights = []
		self.distalBranches = []
		self.addDendriteBranches(numOfBranches, threshold, numOfInputs, inputs, source)
		self.potentialRecord = PotentialRecord()
		self.threshold = threshold  #CorticalApicalDendriteThreshold
		self.firingStatus = False

	def adjustWeightsOfRecentlyActiveInputs(self, multipleSources = False, source=None):
		for branch in self.distalBranches:
			branch.adjustWeightsOfRecentlyActiveInputs(multipleSources, source)

	def changeBranchThresholds(self, newThreshold):
		for branch in self.distalBranches:
			branch.changeBranchThreshold(newThreshold)

	def changeThreshold(self, newThreshold):
		self.threshold = newThreshold

	def addInputAndWeightForSource(self, input, weight, source=0):
		self.proximalInputs.append(ExcitatoryInput(input, weight, source))

	# Don't use these, Changed to use ExcitatoryInput so that the InterNeuron's with multiple sources will match
	# The same pattern (RJT)
	# 	
	# def addNewProximalInput(self, connection):
	#	self.proximalInputs.append(connection)

	# def addNewProximalInputWeight(self, weight):
	# 	self.proximalInputWeights.append(weight)

	def addDendriteBranch(self, threshold, numOfInputs, inputs, source = None, managementInputs = 0):
		self.distalBranches.append(DendriteBranch(threshold, numOfInputs, inputs, source, managementInputs))
	
	def addDendriteBranches(self, numberOfBranches, threshold, numOfInputs, inputs, source = None, managementInputs = 0):
		for i in range(numberOfBranches):
			self.addDendriteBranch(threshold, numOfInputs, inputs, managementInputs, source)

	def reduceSynapticWeights(self, proportion):
		for branch in self.distalBranches:
			branch.reduceSynapticWeights(proportion)

	def presentInputs(self, excitatoryInputs, modulatoryInputs, multipleSource = False, managementInputs=[]):
        #MODULATORY INPUTS CAN BE EXCITATORY OR INHIBITORY, DEPENDING ON
        #THE PROXIMAL INPUT WEIGHTS WITHIN THE TARGET APICAL DENDRITE INSTANCE

        #FIRST STEP IS TO SHIFT potentialRecord ALONG ONE TIMESLOT
		self.potentialRecord.shift()
        
        #GO THROUGH EACH BRANCH AND DETERMINE WHETHER IT INJECTS POTENTIAL
        #INTO THE apicalDendrite. IF SO, INCREASE THE potentialRecord ACCORDINGLY"

		for branch in self.distalBranches:
			if branch.presentExcitatoryInputsToBranch(excitatoryInputs, multipleSource, managementInputs):
				self.potentialRecord.advanceExcitatoryPotential()
        
		# ADD POTENTIAL INJECTED BY MODULATORY PROXIMAL INPUTS TO potentialRecord. 
		# NOTE: USING SAME POTENTIAL DECAY CURVE AS FOR APICAL DENDRITE BRANCHES"
		if len(managementInputs) > 0:  # this guard is here because on the management Inputs this code wasn't called
									   # if this code should be called when management Inputs are present remove 
									   # this guard (RJT)
			for proximalInput in self.proximalInputs:
				if modulatoryInputs[proximalInput.input] == 1:
					self.potentialRecord.adjustPotentialByWeight(proximalInput.weight)
					
		# SET firingProbability AT 0% IF POTENTIAL IN CURRENT TIMESLOT IS LESS 
		# THAN OR EQUAL TO THRESHOLD, AT 100% IF POTENTIAL IS 10% OR MORE OVER 
		# THRESHOLD. SCALED BETWEEN 10% AND 100% PROBABILITIES WHEN POTENTIAL 
		# IS 1% TO 10% OVER THRESHOLD" 
		self.firingStatus = self.potentialRecord.fireforThreshold(self.threshold)
		if self.firingStatus:
			# IF apicalDendrite FIRES, SET potentialRecord TO ZERO
			self.potentialRecord.reset()

		# IF ANY BRANCH HAS <3 INPUTS, REMOVE IT"
		
		self.distalBranches = list(itertools.filterfalse(lambda x: len(x.excitatoryInputs) < 3, self.distalBranches))

		return self.firingStatus

class BasilDendrite(ApicalDendrite):
	def __init__(self, numOfBranches = 0, threshold = CorticalBasalDendriteThreshold, numOfInputs = 0, \
			  inputs = [], source = None, managementInputs = 0):
		super().__init__(numOfBranches, threshold, numOfInputs, inputs, source, managementInputs)
		assert self.threshold != None

class InhibitoryInterneuron(ApicalDendrite):
	def __init__(self, threshold = LayerOneInterneuronThreshold, numOfInputs = 0, inputs=[], source=None):
		super().__init__()
		self.timeSincePreviousFiring = 100
		self.threshold = threshold

	#don't use these methods, changed to us Excitatoryinput for proximal input using
	# addInputAndWeightForSource
	
	#def addNewInput(self, connection):
		# named differently in Basil Dendrite but functionally the same
	#	self.proximalInputs.append(connection)

	#def addNewInputWeight(self, weight):
		# named differently in Basil Dendrite but functionally the same
	#	self.proximalInputWeights.append(weight)

	def presentInputs(self, currentInputs, modularyInputs = [], multipleSource = False, managmentInputs=[]):
		# assert False, "this code is turned off because CortaclColumn >> updateLayerTwoInterneuronActivityInternalConnectivityOnly: is not sent"
		# This method can work for multipleSource present inputs used by CorticalColumn >> updateLayerOneInterneuronActivity:
		# the difference between the presentInputs on BasilDendrite is the dendriteBranches. Since there are no
		# dendriteBranches on a InhibitoryIntterneuoron the code is the same (RNT)
		# ADDS ONE TIMESLOT TO THE COUNT OF TIMESLOTS SINCE PREVIOUS FIRING
		self.timeSincePreviousFiring += 1
		super().presentInputs(currentInputs, modularyInputs, multipleSource, managmentInputs)		
		return self.firingStatus
