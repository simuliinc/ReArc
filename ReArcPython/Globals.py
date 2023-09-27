# Globals.py is for global variables 

CorticalConditionDefiningInputWeight = 1.7
BranchContributionsWithin200msecForPermanentWeightChange = 3
LayerOneInterneuronOutputSynapticStrengths = -5
LayerTwoInterneuronOutputSynapticStrengths = 0
CorticalBasalDendriteThreshold = 985
NumberOfConditionRecordingOutputsFromBlackBoxHippocampus = 0  # used in DendriteBranch 0 turns off the ConditionRecordingManagement
CorticalConditionRecordingManagementInputWeight = 0.5
MaximumBranchSynapticWeight = 3.2 # used to limit the weights of Dendrite Branches
HippocampalWeightReductionFactor = 0.9999 # used in ConditionalRecordingManagementInputWeights of DendriteBranch
BranchFiringsToDecreaseInSynapticWeights = 4 # used in DendrichBranch >> adjustWeightsOfRecentlyActiveInputs
ModulationProbabilityFactor = [0]*75
IntegerCollectionSizeForInputStateGeneration = 10000
BDNFincrementPerFiring = 0.5
BDNFdecrementFollowingWeightReduction = 1
BDNFconcentrationReductionPerTimeslot = 0.9999
BDNFconcentrationThresholdForReductionInSynapticWeights = 17.5
FrequentFiringReductionInSynapticWeightsProportion = 0.9

def setModulationProbabilityFactor():
	startPosition = 11
	startValue = 0.2
	maxValue = 25.6
	size = 74
	value = 0
	maxValueAdded = False
	for i in range(0,size):
		# Add zeros then startValue at startPosition.
		# The modulation doubles for each pass to maxValuue 
		# then halves to 0 and adds zeros to size
		if i < startPosition:
			value = 0
		elif not maxValueAdded:
			if value == 0:
				value = startValue
			else: 
				value *= 2
			if value >= maxValue:
				value = maxValue
				maxValueAdded = True
		elif maxValueAdded:
			if value <= 0 or value <= startValue:
				value = 0
			else:
				value /= 2
		ModulationProbabilityFactor[i]=round(value, 2)
		
		# Other optoins for ModulationProbabilityFactor from notes in code (RJT)	
		# Sets the global variable ModulationProbabilityFactor. This variable defines how much the probability 
		# of spike generation will be changed by frequency modulation in each time slot in the 25 millisecond 
		# (40 Hz) modulation cycle

		# ModulationProbabilityFactor 
		# ((((((((((3.1415965*2)*i)/75) sin) raisedTo: 3)/2)*100) rounded) + 100)/(100.0)) would be:
		# 1.00 1.00 1.01 1.02 1.03 1.06 1.08 1.12 1.16 1.21 1.25 1.30 1.35 1.39 1.43 1.46 1.48 1.50 1.50 1.49 
		# 1.47 1.45 1.41 1.37 1.32 1.28 1.23 1.18 1.14 1.10 1.07 1.04 1.02 1.01 1.00 1.00 1.00 1.00 1.00 1.00 
		# 0.99 0.98 0.96 0.93 0.90 0.86 0.82 0.77 0.72 0.68 0.63 0.59 0.55 0.53 0.51 0.50 0.50 0.52 0.54 0.57 
		# 0.61 0.65 0.70 0.75 0.79 0.84 0.88 0.92 0.94 0.97 0.98 0.99 1.00 1.00 1.00

		# Hence at the peak of the modulation cycle, spike generation probability will be increased by 50%, and decreased by 50% at the minimum.

		# ModulationProbabilityFactor 
		# ((((((((((3.1415965*2)*i)/75) sin) raisedTo: 3))*100) rounded) + 100)/(100.0))	 would be
		# 1.00 1.00 1.02 1.04 1.07 1.11 1.17 1.24 1.32 1.41 1.51 1.60 1.70 1.78 1.86 1.92 1.97 1.99 2.00 1.98 
		# 1.95 1.89 1.82 1.74 1.65 1.55 1.46 1.36 1.28 1.20 1.14 1.09 1.05 1.02 1.01 1.00 1.00 1.00 1.00 0.99 
		# 0.98 0.95 0.91 0.86 0.80 0.72 0.64 0.54 0.45 0.35 0.26 0.18 0.11 0.05 0.02 0.00 0.01 0.03 0.08 0.14 
		# 0.22 0.30 0.40 0.49 0.59 0.68 0.76 0.83 0.89 0.93 0.96 0.98 1.00 1.00 1.00

		# ModulationProbabilityFactor 
		# ((((((((((3.1415965*2)*i)/75) sin) raisedTo: 5))*100) rounded) + 100)/(100.0))	 would be
		# 1.00 1.00 1.00 1.00 1.01 1.03 1.05 1.09 1.15 1.23 1.32 1.43 1.55 1.67 1.78 1.87 1.95 1.99 2.00 1.97 
		# 1.91 1.83 1.72 1.61 1.49 1.37 1.27 1.19 1.12 1.07 1.04 1.02 1.01 1.00 1.00 1.00 1.00 1.00 1.00 1.00 
		# 1.00 0.99 0.98 0.96 0.93 0.88 0.81 0.73 0.63 0.51 0.39 0.28 0.17 0.09 0.03 0.00 0.01 0.05 0.13 0.22 
		# 0.33 0.45 0.57 0.68 0.77 0.85 0.91 0.95 0.97 0.99 1.00 1.00 1.00 1.00 1.00

		# ModulationProbabilityFactor 
		# ((((((((((3.1415965*2)*i)/75) sin) raisedTo: 7))*100) rounded) + 100)/(100.0))	 would be
		# 1.00 1.00 1.00 1.00 1.00 1.01 1.02 1.04 1.07 1.13 1.20 1.31 1.43 1.57 1.70 1.83 1.93 1.99 2.00 1.96 
		# 1.88 1.77 1.64 1.50 1.37 1.25 1.16 1.10 1.05 1.02 1.01 1.00 1.00 1.00 1.00 1.00 1.00 1.00 1.00 1.00 
		# 1.00 1.00 1.00 0.99 0.98 0.95 0.90 0.84 0.75 0.63 0.50 0.36 0.23 0.12 0.04 0.00 0.01 0.07 0.17 0.30 
		# 0.43 0.57 0.69 0.80 0.87 0.93 0.96 0.98 0.99 1.00 1.00 1.00 1.00 1.00 1.00
			
		# "ModulationProbabilityFactor := OrderedCollection new.
		# 1 to: 75 do: [:i| ModulationProbabilityFactor addLast: ((((((((((3.1415965*2)*i)/75) sin) raisedTo: 7))*100) rounded) + 100)/(100.0))].


setModulationProbabilityFactor()

