# a PyramidalNeuron holds both an ApicalDendrite and BaislDendrite and is part of a CorticalColumn
from Globals import *
import PotentialRecord
from Dendrites import *

class PyramidalNeuron:

	def __init__(self, numOfBasilDendriteBranches, threshold, numOfInputs, inputs, source=None, managementInputs=0):
		self.apicalDendrite = ApicalDendrite()
		self.basalDendrite = BasilDendrite(numOfBasilDendriteBranches, threshold, numOfInputs, \
									  inputs, source, managementInputs)
		self.potentialRecord = PotentialRecord()
		self.timeSincePreviousFiring = 48
		self.threshold = CorticalBasalDendriteThreshold
		self.firingStatus = False
		self.synapticWeightReductionTendency = 0

	def presentInputs(self, excitatoryInputs, interneuronActivity, multipleSource = False, managementInputs = []):
		# presents inputs to branches on distal apicalDendrite, eventually as required to proximal apical dendrite 
		# and basal dendrite. At the moment (March 2008) the firing status of the apical dendrite is the firing 
		# status of the neuron"
	

		# ADDS ONE TIMESLOT TO THE COUNT OF TIMESLOTS SINCE PREVIOUS FIRING	
		self.timeSincePreviousFiring += 1

		# SETS FIRING STATUS AS THE FIRING STATUS OF THE apicalDendrite	
		self.firingStatus = self.basalDendrite.presentInputs(excitatoryInputs, interneuronActivity, multipleSource, managementInputs)

		# IF THE NEURON IS FIRING, SETS THE COUNT OF TIMESLOTS SINCE PREVIOUS FIRING TO ZERO
		if self.firingStatus: 
			self.timeSincePreviousFiring = 0

			# IF NEURON IS FIRING, INCREASE THE WEIGHTS OF INPUTS TO BRANCHES THAT HAVE RECENTLY 
			# BEEN ACTIVE (UP TO A MAXIMUM WEIGHT), PROVIDED THAT THE BRANCH HAS BEEN ACTIVE AS A 
			# WHOLE. THE TEST THAT THE BRANCH HAS BEEN ACTIVE OCCURS WITHIN THE BRANCH METHOD"
			self.basalDendrite.adjustWeightsOfRecentlyActiveInputs(False, None)

			if not len(managementInputs):
				# only run this code if there are no management inputs (RJT)
				# THE FOLLOWING CODE DECREASES ALL THE SYNAPTIC WEIGHTS ON THE NEURON IF FIRING HAS RECENTLY 
				# OCCURRED TOO FREQUENTLY. THE VARIABLE synapticWeightReductionTendency CAN BE VIEWED AS CORRESPONDING 
				# WITH RELEASE OF BDNF THAT REDUCES SYNAPTIC WEIGHTS. WHEN A NEURON FIRES, synapticWeightReductionTendency 
				# IS INCREASED BY 1. IN EVERY TIMESLOT, synapticWeightReductionTendency IS REDUCED BY 0.01%. 
				# IF synapticWeightReductionTendency BECOMES GREATER THAT 17.5, SYNAPTIC WEIGHTS ALL OVER THE NEURON ARE 
				# REDUCED. WITH A BIOLOGICALLY PLAUSIBLE ALGORITHM, IF synapticWeightReductionTendency REACHES 18.5, 
				# IT WILL TAKE ABOUT 600 TIMESLOTS TO GET BELOW 17.5 AGAIN. HENCE FrequentFiringReductionInSynapticWeightsProportion 
				# WOULD BE APPLIED ABOUT 600 TIMES. TO REDUCE PROCESSING TIME, THE REDUCTION IS MADE ONCE AND 
				# synapticWeightReductionTendency IS THEN REDUCED BY 1
				self.synapticWeightReductionTendency += BDNFincrementPerFiring
				if self.synapticWeightReductionTendency > BDNFconcentrationThresholdForReductionInSynapticWeights:
					self.reduceSynapticWeights(FrequentFiringReductionInSynapticWeightsProportion)
					self.synapticWeightReductionTendency -= BDNFdecrementFollowingWeightReduction
				self.synapticWeightReductionTendency *= BDNFconcentrationReductionPerTimeslot

		return int(self.firingStatus)

	def reduceSynapticWeights(self, proportion):
		self.basalDendrite.reduceSynapticWeights(proportion)

	def changeBasalDendriteThresholds(self, newBranchThreshold):
		self.basalDendrite.changeBranchThresholds()


	def updatePotentialRecord(self, spike):
		assert False, "This method is currently not used, if you want to use this method remove this assert"
		# Updates potentialRecord for next timeslot. If there is an action potential being presented to the 
		# neuron during the timeslot, the variable spike will be 1, otherwise 0"
		if spike:
			self.potentialRecord.shift()
			self.advanceExcitatoryPotential()
