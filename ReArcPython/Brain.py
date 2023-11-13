# The Brain is the main interface for reArc
from CorticalArea import *
from HippocampalSystemBlackBox import *
from Globals import *
from PresentOneCategoryInstance import *
from InputState import *

class Brain:
	def __init__(self, numberOfCorticalAreas=3):
		self.visualCortex = []
		for i in range(numberOfCorticalAreas):
			self.visualCortex.append(CorticalArea())
		self.auditoryCortex = []
		self.associationCortex = None
		self.perirhinalCortex = None
		self.parahippocampalCortex = None
		self.entorhinalCortex = None
		self.hippocampus = []
		for i in range(numberOfCorticalAreas):
			self.hippocampus.append(HippocampalSystemBlackBox())
		self.columnGroups = []
		self.anteriorThalamus = None
		self.mammillaryBodies = None
		self.amygdala = None

	def changeLayer3BranchThresholds(self, newLayer3CorticalBranchThreshold):
		for vc in self.visualCortex:
			vc.changeLayer3BranchThresholds(newLayer3CorticalBranchThreshold)

	def configureFirstArea(self, favouredInputs):
		# Only layer three pyramidals have inputs from hippocampal system, and there is only 
		# one such input, numbered 1
		# Interneurons in layer two have inputs only from layer two pyramidals and inhibit those 
		# pyramidals. In W, these interneurons have inputs from all columns except the one in 
		# which they are located

		# In smalltalk each column and nuron collection was terminated with false but that false was
		# never referenced.  We are leaving that out here (RJT) 
		
		# calcuate favored inputs no so that we can add them with the dendriteBranches (RJT)
		inputPopulation = {}
		for currentColumn in range(NumberOfColumns):
			inputPopulation[currentColumn] = list(range(InputSpaceSize))
			for i in range(BiasOnFavouredInputs):
				inputPopulation[currentColumn] += favouredInputs[currentColumn]

		self.visualCortex[0].addColumnQty(NumberOfColumns)
		self.visualCortex[0].addPyramidalToLayerQtyThreshold(1, PyramidalsPerColumnLayerOne, DendriticBranchThresholdLayerOne, inputPopulation)
		self.visualCortex[0].addPyramidalToLayerQtyThreshold(2, PyramidalsPerColumnLayerTwo, DendriticBranchThresholdLayerTwo, inputPopulation)
		self.visualCortex[0].addPyramidalToLayerQtyThreshold(3, PyramidalsPerColumnLayerThree, DendriticBranchThresholdLayerThree, inputPopulation)
		self.visualCortex[0].addInterneuronToLayerWithThreshold(1,NumberOfLayerOneInterneurons, LayerOneInterneuronThreshold)
		self.visualCortex[0].addInterneuronToLayerWithThreshold(2, NumberOfLayerTwoInterneurons, LayerTwoInterneuronThreshold)

		# THIS SECTION CONFIGURES THE NEURONS IN EACH COLUMN IN TURN, WITH APPROPRIATE BIAS ON INPUTS TO 
		# LAYER ONE PYRAMIDALS
		
		#moved earlier insted (RJT)
		# for currentColumn in range(NumberOfColumns):		
			
			# THE FOLLOWING CODE CREATES A POPULATION OF CONNECTION NUMBERS WITH A BIAS IN FAVOUR OF A SUBSET 
			# OF CONNECTIONS. THE INPUTS TO LAYER ONE OF EACH COLUMN WILL BE BIASED IN FAVOUR OF A DIFFERENT 
			# SUBSET. THE SUBSET IS CREATED BY DEFINING A SUBSET OF 50 INPUTS, THEN FINDING THE 25 IN THE 50 
			# THAT ARE MOST OFTEN ACTIVE AT SIMILAR TIMES. MOST OFTEN IS DETERMINED BY MEASURING THE NUMBER 
			# OF TIMES EACH INPUT IS ACTIVE AT THE SAME TIME AS AT LEAST 5 OTHER INPUTS IN THE 50, IN PERIODS 
			# OF 15 TIMECYCLES (5 MILLISECONDS) WITHIN 10 200 MILLISECOND PRESENTATIONS OF EACH OF FIVE 
			# CATEGORIES.
		#	inputPopulation = list(range(InputSpaceSize))
			# Following code adds BiasOnFavouredInputs extra copies of each of the favoured inputs for the 
			# currentColumn
		#	for i in BiasOnFavouredInputs:
		#		inputPopulation += favouredInputs[currentColumn]

			# CONFIGURATION OF LAYER ONE PYRAMIDALS

			# This is now configured durring initialization of the PyramidalNeuron, for configuration details
			# see CorticalColumn.py CorticalColumn >> addPyramidalToLayer and 
			# CorticalColumn >> configForLayer (RJT)
	
			# CONFIGURATION OF LAYER TWO PYRAMIDALS

			# This is now configured durring initialization of the PyramidalNeuron, for configuration details
			# see CorticalColumn.py CorticalColumn >> addPyramidalToLayer and 
			# CorticalColumn >> configForLayer (RJT) 

			# CONFIGURATION OF LAYER THREE PYRAMIDALS

			# This is now configured durring initialization of the PyramidalNeuron, for configuration details
			# see CorticalColumn.py CorticalColumn >> addPyramidalToLayer and 
			# CorticalColumn >> configForLayer (RJT) 

			# ADD CONDITION DEFINITION MANAGEMENT INPUTS FROM BLACK BOX HIPPOCAMPUS

			# This is now configured in CorticalColumn.py CorticalColumn >> configForLayer  
			# which is used in DendriteBranch.py DendriteBranch >> __init__()  (RJT)


			# CONFIGURATION OF LAYER ONE INTERNEURONS
			# EACH INTERNEURON HAS NumberOfInputsToLayerOneInterneuronsFromEachOtherColumn INPUTS FROM RANDOMLY 
			# SELECTED PYRAMIDALS IN EACH COLUMN EXCEPT ITS OWN AND NumberOfInputsToLayerOneInterneuronsFromOwnColumn 
			# INPUTS FROM RANDOMLY SELECTED PYRAMIDALS IN ITS OWN COLUMN
			
			# This is now done in CorticalArea.py CorticalArea >> addInterneuronToLayerWithThreshold

			# Also see CorticalColumn.py CorticalColumn >> configForLayer(self, corticalLayer, inputs): for
			# for the configuration options.

			# CONFIGURATION OF LAYER TWO INTERNEURONS"

			# EACH INTERNEURON HAS NumberOfInputsToLayerTwoInterneuronsFromEachOtherColumn INPUTS FROM RANDOMLY 
			# SELECTED PYRAMIDALS IN EACH COLUMN EXCEPT ITS OWN AND NumberOfInputsToLayerTwoInterneuronsFromOwnColumn 
			# INPUTS FROM RANDOMLY SELECTED PYRAMIDALS IN ITS OWN COLUMN"

			
	def configureSecondArea(self):

		assert False, "This method was not called in the Smalltalk Version of ReArch"
		# Only layer three pyramidals hve inputs from hippocampal system, and there is only one such input, numbered 1
		# Interneurons in layer two have inputs only from layer two pyramidals and inhibit those pyramidals. In W, these 
		# interneurons have inputs from all columns except the one in which they are located

		# The following code creates sourceColumnInputProbability, which implements the relative probability that a column 
		# in Area 1 will be the source of an input to the currentColumn in Area 2. SelectedSubsets contains a set of Area 1 
		# columns for each Area 2 column, and these Area 1 columns will be more likely to provide inputs to the Area 2 
		# columns. SelectedSubsets has been created by identifying groups of Area 1 columns that have often produced outputs 
		# at similar times in the past. 

		# sourceColumnInputProbability will contain one entry for each column in Area 1, plus InitialBiasOnSelectedColumns 
		# extra entries for each of the Area 1 columns favoured for bias. When basal dendrite branches of layer one 
		# pyramidals are configured later in this method, sourceColumnInputProbability is used the bias the selection of 
		# inputs.

		inputPopulation = {}
		for currentColumn in range(NumberOfColumns):
			inputPopulation[currentColumn] = list(range(NumberOfColumns))
			columnBias = SelectedSubsets[currentColumn]
			for j in range(columnBias):
				for biasedColumn in range(InitialBiasOnSelectedColumns):
					inputPopulation[currentColumn].appeend(columnBias[biasedColumn])

		self.visualCortex[1].addColumnQty(NumberOfColumnsArea2)
		self.visualCortex[1].addPyramidalToLayerQtyThreshold(1, PyramidalsPerColumnLayerOne, \
														DendriticBranchThresholdLayerOne, inputPopulation, \
														range(PyramidalsPerColumnLayerThree))
		self.visualCortex[1].addPyramidalToLayerQtyThreshold(2, PyramidalsPerColumnLayerTwo, \
													    DendriticBranchThresholdLayerTwo, inputPopulation)
		self.visualCortex[1].addPyramidalToLayerQtyThreshold(3, PyramidalsPerColumnLayerThree, \
													    DendriticBranchThresholdLayerThree, inputPopulation)
		self.visualCortex[1].addInterneuronToLayerWithThreshold(1,NumberOfLayerOneInterneurons, \
														  LayerOneInterneuronThreshold)
		self.visualCortex[1].addInterneuronToLayerWithThreshold(2, NumberOfLayerTwoInterneurons, \
														  LayerTwoInterneuronThreshold)

	def presentInputsInOneTimeslotToAreaWithBlackBoxHippocampus(self, excitatoryInputs, cortexArea = 1, shouldRecord = False):

		# This is the first edition of the presentInputs method, and assumes there is just one CorticalArea 
		# in visualCortex, and a CorticalArea in entorhinalCortex. excitatoryInputs contains the sensory 
		# action potential spikes in one timeslot, and the recording management inputs are obtained from the 
		# entorhinal cortex.

		# STEP ONE IS TO GET PREVIOUS OUTPUTS FROM HIPPOCAMPUS
		recordingManagementInputs = self.hippocampus[cortexArea].popCurrentHippocampalOutputs()

		# STEP TWO IS TO UPDATE CORTEX USING CURRENT SENSORY INPUTS AND PREVIOUS OUTPUTS FROM HIPPOCAMPUS
		brainActivity = self.visualCortex[cortexArea-1].presentInputsInOneTimeslotToCorticalArea(excitatoryInputs, recordingManagementInputs, multipleSource = False)

		# this is a global variable, I'm not sure what its purpose is (RJT)
		if shouldRecord:
			RecordingManagementInputsPerTimeslot.append(recordingManagementInputs)


		# STEP THREE IS TO UPDATE HIPPOCAMPUS USING UPDATED CORTEX LAYER TWO AND THREE ACTIVITY"
		layerTwoActivity = []
		layerThreeActivity = []
		for columnNum in range(len(self.visualCortex[cortexArea].columns)):
			# a better implementation might be column.getLayer(3).pyramidalActivity if the output
			# from presentInputsInOneTimeslotToCorticalArea is the same value as the what is stored
			# on the layer pyramidalActivity (RJT)
			layerTwoActivity.append(brainActivity[columnNum][1]) 	# layer 2
			layerThreeActivity.append(brainActivity[columnNum][2])	# layer 3

		self.hippocampus[cortexArea].updateHippocampalRecordsForMultipleModulationCyclesWithInternalActivity(layerThreeActivity,layerTwoActivity)	

		return brainActivity
	
	def totalAcrossTimeslots(self, recentPresentationOutputs, layer):
		# This is presented with the spikes generated by all neurons in all layers of a set of 
		# columns for 600 timelots, and returns the total number of spikes generated by all the 
		# neurons in one layer across the 600 timeslots
		# 600 timeslots, 15 columns, 3 layers, 10 potential spikes for 2 layers 
		# and 1 potential spike for the layer 3

		# This really needs to be cleaned up.  All of the values are represented positionally in arrays
		# at least we should change to a dictionary and add labels or change to use json.
		totalSpikes = [0]*600
		for i, timeSlot in enumerate(recentPresentationOutputs):
			for column in timeSlot:
				for spikes in column[layer - 1]:  # layer - 1 to account for 0 base indexes 
					totalSpikes[i] += spikes

	
	def presentDoubleCategoryInstanceWithSecondCategory(self, categoryInputSource, secondCategoryInputSource):

		# category is categoryInputSourceCategoryX
		# Y stores outputs of all the columns. Z stores the inputs, but not the null inputs.
		# PresentationRecord stores the total output spikes over one object presentation, from each 
		# column separately 

		# This method requires X to be set to some instance of Brain. Why?? is not clear.
		# Turns out that X.presentInputsInOneTimeslotToArea1WithBlackBoxHippocampus(inputs) is just self(RJT)
		
		for j in range(600):
			inputs = categoryInputSource.getSpikesInNextTimeslot(secondCategoryInputSource)
			# not sure what Z and Y are for (RJT)
			Z.append(inputs)
			Y.append(self.presentInputsInOneTimeslotToAreaWithBlackBoxHippocampus(inputs, 1, True))
		self.reportPresentationResults(Y[-599:])
		self.nullOutInputs()

	def nullOutInputs(self):
		# The following code presents null inputs (no spikes) to brain for 25 milliseconds (75 timeslots)
		# to ensure that previous presentation does not contribute to later presentation"
		inputs = [0]*200
		for i in range(75):			
			self.presentInputsInOneTimeslotToAreaWithBlackBoxHippocampus(inputs, 1, False)

	def reportPresentationResults(self, recentPresentationOutputs):	
		PresentationResults.append([[self.totalAcrossTimeslots(recentPresentationOutputs, 1)], 
							  [self.totalAcrossTimeslots(recentPresentationOutputs, 2)], 
							  [self.totalAcrossTimeslots(recentPresentationOutputs, 3)]])  # 4th July 2015 <- no idea what this is (RJT)


	def presentOneCategoryInstance(self, categoryInputSource):
		assert False, "this method wasn't used in Smalltalk"
		#category is categoryInputSourceCategoryX
		# Y stores outputs of all the columns. Z stores the inputs, but not the null inputs.
		# PresentationRecord stores the total output spikes over one object presentation, 
		# from each column separately 

		for j in range(600):
			inputs = categoryInputSource.getSpikesInNextTimeslot()
			Z.append(inputs)

			# the original Smalltalk code method Brain >> presentInputsInOneTimeslotToBrainWithBlackBoxHippocampus: 
			# which implied recording = True but the code did not actually do 
			# recording. I picked the intent here bassed on the name of the method had Andrew wanted
			# to not record he would have used Brain >> 
			# presentInputsInOneTimeslotToBrainWithBlackBoxHippocampusWithoutRecording:
			Y.append(self.presentInputsInOneTimeslotToAreaWithBlackBoxHippocampus(inputs,1,True))
		
		# The following code determines layer three outputs from each column in each modulation 
		# period, ans adds the results to PresentationResults


		currentPresentationOutputs = []
		# these values do not match HippocampalSystemBlackBox >> constructMultiplexedOutputsForNext25milliseconds
		# they also don't match he comments above each sectiion.
		self.addModulationSlots(currentPresentationOutputs,0,21)
		self.addModulationSlots(currentPresentationOutputs,27,45)
		self.addModulationSlots(currentPresentationOutputs,48,71)
		Y = []
		self.nullOutInputs()


	def addModulationSlots(self, currentPresentationOutputs, start, stop):
		for j in range(8):
			# modulation 1 - 10  (his appears to be 20 spots not 10 (RJT))
			for k in range(75*j+start, 75*j + stop):  # 0 to 20 then 75 to 94 (inclusive) (RJT)
				currentPresentationOutputs.append(Y[k])
		PresentationResults.append(self.totalAcrossTimeslots(currentPresentationOutputs, 3))

	def presentOneCategoryInstanceStoredInputs(self):
		# category is categoryInputSourceCategoryX
		# All inputs have previously been stored in Z, except null inputs between each presentation. 
		# Y stores outputs of all the columns.
		# PresentationRecord stores the total output spikes over one object presentation, from each 
		# column separately 
		assert False, "This code was not used in Smalltalk"
		for j in range(600):
			inputs = Z[InputNumber]  # InputNumber is a global that does not seem to be initialized in Smalltalk
			InputNumber += 1
			Y.append(self.presentInputsInOneTimeslotToAreaWithBlackBoxHippocampus(inputs,1,True))
		self.reportPresentationResults(Y[-599:])
		self.nullOutInputs()

	def presentTripleCategoryInstance(self, firstCategoryInputSource, secondCategoryInputSource, thirdCategoryInputSource,  cortexArea = 1, shouldRecord = False):
		# category is categoryInputSourceCategoryX
		# Y stores outputs of all the columns. Z stores the inputs, but not the null inputs.
		# PresentationRecord stores the total output spikes over one object presentation, from each column separately 

		# In 600 timeslots (200 msec) , there are 8 modulation periods of 75 timeslots (25 milliseconds). Each 
		# of three category instrances are presented once in each modulation period (i.e. for about 
		# 8 milliseconds). So a category instance is presented for a period of about 67 milliseconds

		for i in range(600):
			inputs = firstCategoryInputSource.getSpikesInNextTimeslot(secondCategoryInputSource, thirdCategoryInputSource)
			Y.append(self.presentInputsInOneTimeslotToAreaWithBlackBoxHippocampus(inputs, cortexArea, shouldRecord))

		# the following code totals spikes but is not used except to fill another global.
		# The globals filling code was commented out.  Leaving this out for performance (RJT).

		"""		
				# Total spikes in Layer 3"
				totalLayerThreeSpikesInTimeslot = self.totalAcrossTimeslots(recentPresentationOutputs, 1)
				1 to: NumberOfColumns do: [:columns| 
					totalLayerThreeSpikesInTimeslot := totalLayerThreeSpikesInTimeslot + ((((Y last) at: columns) at: 3) total). 
							]. "END do columns"
				"LayerThreeSpikesPerTimeslot addLast: (totalLayerThreeSpikesInTimeslot)."

		"Total spikes in Layer 2"
				totalLayerTwoSpikesInTimeslot := 0.
				1 to: NumberOfColumns do: [:columns| 
					totalLayerTwoSpikesInTimeslot := totalLayerTwoSpikesInTimeslot + ((((Y last) at: columns) at: 2) total). 
							]. "END do columns"
				"LayerTwoSpikesPerTimeslot addLast: (totalLayerTwoSpikesInTimeslot)."
				
		"Total spikes in Layer 1"
				totalLayerOneSpikesInTimeslot := 0.
				1 to: NumberOfColumns do: [:columns|
					totalLayerOneSpikesInTimeslot := totalLayerOneSpikesInTimeslot + ((((Y last) at: columns) at: 1) total).  
							]. "END do columns"
				"LayerOneSpikesPerTimeslot addLast: (totalLayerOneSpikesInTimeslot)."
				
		"Total input spikes
				InputSpikesPerTimeslot addLast: (inputs total)."
		"""				

		# The following code determines layer three outputs from each column in each modulation period, 
		# and adds the results to PresentationResults.
  	 	# NOTE that with setPhaseAtInitialTimeslot: 23, 
		# layer 3 outputs for the firstCategoryInputSource appear in timeslots 1 - 21.
		# layer 3 outputs for the secondCategoryInputSource appear in timeslots 48 - 71.
		# layer 3 outputs for the thirdCategoryInputSource appear in timeslots 27 - 45.
		# HENCE PresentationResults must capture results in that order to preserve the results in the same 
		# order as the presentations.
		self.reportPresentationResults(Y[-599:])

		# Resetting of Y can be eliminated to capture all neuron activity in all timeslots. However, for a 
		# long run this overloads the memory
		Y = []

		# YY addLast: (((hippocampus at: 1) showStrongActivityCount) deepCopy). 

		# The following code zeroes strongActivityCount. If multiple groups of objects are presented to Area2 
		# in different timeslots, this will require modification 
		self.hippocampus[0].zeroStrongActivityCount()
		self.hippocampus[1].zeroStrongActivityCount()

	
		# The following code presents null inputs (no spikes) to brain for 25 milliseconds (75 timeslots) to 
		# ensure that previous presentation does not contribute to later presentation
		self.nullOutInputs()

	def sleep(self):
		assert False, "This code would break with no cortiacal index if called and it doesn't appear to be called in Smalltalk"
		self.visualCortex.sleep()