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

def totalLen(aList):
	totalLength = 0
	for collection in aList:
		totalLength += len(collection) 
	return totalLength