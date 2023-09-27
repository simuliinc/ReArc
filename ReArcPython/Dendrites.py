
# An ApicalDendrite is the output of a pyramidal cell. The Dendrite acts by modulating
# the excitatory and inhibitory signals.

from Globals import *
from PotentialRecord import *
import itertools

class ApicalDendrite:
	def __init__(self):
		self.proximalInputs = []
		self.proximalInputWeights = []
		self.distalBranches = []
		self.potentialRecord = PotentialRecord()
		self.threshold = None  #CorticalApicalDendriteThreshold
		self.firingStatus = False

	def adjustWeightsOfRecentlyActiveInputs(self, multipleSources = False, source=None):
		for branch in self.distalBranches:
			branch.adjustWeightsOfRecentlyActiveInputs(multipleSources, source)

	def changeBranchThresholds(self, newThreshold):
		for branch in self.distalBranches:
			branch.changeBranchThreshold(newThreshold)

	def changeBranchThreshold(self, newThreshold):
		self.threshold = newThreshold

	def addNewProximalInput(self, connection):
		self.proximalInputs.append(connection)

	def addNewProximalInputWeight(self, weight):
		self.proximalInputWeights.append(weight)

	def reduceSynapticWeights(self, proportion):
		for branch in self.distalBranches:
			branch.reduceSynapticWeight(proportion)

	def presentInputs(self, excitatoryInputs, modulatoryInputs, multipleSource = False, managementInputs=[]):
        #MODULATORY INPUTS CAN BE EXCITATORY OR INHIBITORY, DEPENDING ON
        #THE PROXIMAL INPUT WEIGHTS WITHIN THE TARGET APICAL DENDRITE INSTANCE

        #FIRST STEP IS TO SHIFT potentialRecord ALONG ONE TIMESLOT
		self.potentialRecord.shift()
        
		currentPotential = self.potentialRecord[0]
		firingProbability = 1000 * ((currentPotential - self.threshold)/self.threshold)
		emptyBranches = []
		currentLargest = None
        
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
			for proximalnput, proximalWeight in zip(self.proximalInputs, self.proximalInputWeights):
				if modulatoryInputs[proximalnput] == 1:
					self.potentialRecord.adjustPotentialByWeight(proximalWeight)
					
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
	def __init__(self):
		super().__init__()
		self.threshold = CorticalBasalDendriteThreshold

