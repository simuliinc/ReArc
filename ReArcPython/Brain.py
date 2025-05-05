# The Brain is the main interface for reArc
from CorticalArea import *
from HippocampalSystemBlackBox import *
from Globals import *
from PresentOneCategoryInstance import *
from InputState import *
import numpy as np

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
				for j in favouredInputs[currentColumn]:
					inputPopulation[currentColumn].append(j)

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

	def presentInputsInOneTimeslotToAreaWithBlackBoxHippocampus(self, excitatoryInputs, cortexArea = 1, shouldRecord = True):

		# This is the first edition of the presentInputs method, and assumes there is just one CorticalArea 
		# in visualCortex, and a CorticalArea in entorhinalCortex. excitatoryInputs contains the sensory 
		# action potential spikes in one timeslot, and the recording management inputs are obtained from the 
		# entorhinal cortex.

		# STEP ONE IS TO GET PREVIOUS OUTPUTS FROM HIPPOCAMPUS
		recordingManagementInputs = self.hippocampus[cortexArea-1].popCurrentHippocampalOutputs()

		# print("recordingManagementInputs: ", recordingManagementInputs)
		# print("cortexArea: ", cortexArea)

		# STEP TWO IS TO UPDATE CORTEX USING CURRENT SENSORY INPUTS AND PREVIOUS OUTPUTS FROM HIPPOCAMPUS
		brainActivity = self.visualCortex[cortexArea-1].presentInputsInOneTimeslotToCorticalArea(excitatoryInputs, recordingManagementInputs, multipleSource = False)

		# this is a global variable, I'm not sure what its purpose is (RJT)
		if shouldRecord:
			RecordingManagementInputsPerTimeslot.append(recordingManagementInputs)


		# STEP THREE IS TO UPDATE HIPPOCAMPUS USING UPDATED CORTEX LAYER TWO AND THREE ACTIVITY"
		layerTwoActivity = []
		layerThreeActivity = []
		for columnNum in range(len(self.visualCortex[cortexArea-1].columns)):
			# a better implementation might be column.getLayer(3).pyramidalActivity if the output
			# from presentInputsInOneTimeslotToCorticalArea is the same value as the what is stored
			# on the layer pyramidalActivity (RJT)
			layerTwoActivity.append(brainActivity[columnNum][1]) 	# layer 2
			layerThreeActivity.append(brainActivity[columnNum][2])	# layer 3

		# print("layerTwoActivity: ", layerTwoActivity)
		# print("layerThreeActivity: ", layerThreeActivity)

		self.hippocampus[cortexArea-1].updateHippocampalRecordsForMultipleModulationCyclesWithInternalActivity(layerThreeActivity,layerTwoActivity)	

		return brainActivity
	
	def totalAcrossTimeslots(self, recentPresentationOutputs, layer):
		# If no data, return empty list
		if not recentPresentationOutputs or not recentPresentationOutputs[0]:
			return []
		
		# Initialize t2 with zeros based on first presentation's size
		t2 = [0] * len(recentPresentationOutputs[0])
		
		# For each presentation (t7)
		for presentation in recentPresentationOutputs:
			# For each timeslot (t5)
			for t5 in range(len(presentation)):
				# Add the total from this layer at this timeslot
				# Note: layer-1 for 0-based indexing
				t2[t5] += sum(presentation[t5][layer-1])
		
		return t2
	
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
		inputs = [0 for _ in range(InputSpaceSize)]
		for i in range(75):			
			self.presentInputsInOneTimeslotToAreaWithBlackBoxHippocampus(inputs, 1, False)

	def reportPresentationResults(self, recentPresentationOutputs):	
		global PresentationResults
		PresentationResults.append([[self.totalAcrossTimeslots(recentPresentationOutputs, 1)], 
									[self.totalAcrossTimeslots(recentPresentationOutputs, 2)], 
									[self.totalAcrossTimeslots(recentPresentationOutputs, 3)]])  # 4th July 2015 <- no idea what this is (RJT)
		print(PresentationResults, True)
		return PresentationResults

	def reportPresentationResultsLayer3(self, recentPresentationOutputs):	
		global PresentationResults
		PresentationResults.append([[self.totalAcrossTimeslots(recentPresentationOutputs, 3)], 
									[self.totalAcrossTimeslots(recentPresentationOutputs, 3)], 
									[self.totalAcrossTimeslots(recentPresentationOutputs, 3)]])  # 4th July 2015 <- no idea what this is (RJT)
		print(PresentationResults, True)
		return PresentationResults

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


	def addModulationSlots(self, inputResults, start, stop, Y):
		"""Process modulation slots for a specific time range.
		
		Args:
			inputResults: List of brain activity results
			start: Start timeslot within each 75-slot period
			stop: End timeslot within each 75-slot period (inclusive)
		"""
		global PresentationResults
		currentPresentationOutputs = []
		
		# For each of the 8 modulation periods
		for j in range(8):
			period_start = 75 * j + start + 1
			period_end = 75 * j + stop
			
			# Collect outputs for this period if within bounds
			for k in range(period_start, period_end + 1):
				if k < len(inputResults):
					# currentPresentationOutputs.append(inputResults[k])
					currentPresentationOutputs.append(Y[k])
		
		# Calculate totals across timeslots for layer 3 and add to PresentationResults
		if currentPresentationOutputs:
			PresentationResults.append(self.totalAcrossTimeslots(currentPresentationOutputs, 3))

	def presentOneCategoryInstanceStoredInputs(self):
		global PresentationResults
		# category is categoryInputSourceCategoryXs
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

	def presentTripleCategoryInstance(self, firstCategoryInputSource, secondCategoryInputSource, thirdCategoryInputSource, cortexArea=1, shouldRecord=True):
		global Y, PresentationResults
		inputResults = []
		
		# Main 600 timeslot loop
		for i in range(600):
			inputs = firstCategoryInputSource.getSpikesInNextTimeslot(secondCategoryInputSource.category, thirdCategoryInputSource.category)
			
			result = self.presentInputsInOneTimeslotToAreaWithBlackBoxHippocampus(inputs, cortexArea, shouldRecord)
			Y.append(result)
			inputResults.append(Y[-1])  # Store the last result
		
		# Get last 600 entries for processing
		t5 = Y[-600:]
		
		# Process each category's modulation slots and add to PresentationResults
		# First category (timeslots 1-21)
		self.addModulationSlots(t5, 0, 21, Y) # 0 index is 1 in Smalltalk

		# Second category (timeslots 48-71)
		self.addModulationSlots(t5, 47, 71, Y) # 0 index is 1 in Smalltalk

		# Third category (timeslots 27-45)
		self.addModulationSlots(t5, 26, 45, Y) # 0 index is 1 in Smalltalk

		Y = []
		
		# Zero hippocampus counts
		self.hippocampus[0].zeroStrongActivityCount()
		self.hippocampus[1].zeroStrongActivityCount()
		
		# Present null inputs
		self.nullOutInputs()
		return inputResults

	def sleep(self):
		assert False, "This code would break with no cortiacal index if called and it doesn't appear to be called in Smalltalk"
		self.visualCortex.sleep()
  
	def categoryIdentifications(self, presentationResults, columnWeightsInFavourOfCategories, numberOfCategories, presentationStart, presentationStop):
		# Convert inputs to numpy arrays for vectorization
		results = np.array(presentationResults)
		weights = np.array(columnWeightsInFavourOfCategories)
		
		# Initialize output array (3 categories for each presentation)
		numPresentations = presentationStop - presentationStart + 1
		categoryIdentifications = np.zeros((numPresentations, 3))
		
		# Calculate category weights for all presentations at once
		# Matrix multiplication of results and weights
		categoryWeights = np.dot(results[presentationStart:presentationStop+1], weights.T)
		
		# Find top 3 categories for each presentation
		for i in range(numPresentations):
			# Get indices of top 3 maximum values
			top3_indices = np.argpartition(categoryWeights[i], -3)[-3:]
			# Sort them by their values in descending order
			top3_indices = top3_indices[np.argsort(-categoryWeights[i][top3_indices])]
			categoryIdentifications[i] = top3_indices
		
		return categoryIdentifications

	def calculationOfColumnWeightsInFavourOfThirtyCategories(self, presentationResults, startPoint=601, stopPoint=900, numberOfCategories=30, numberOfColumns=15, weightReductionFactor=1.035):
		# Get the slice from startPoint-1 to stopPoint since Python is 0-based
		resultsToBeProcessed = presentationResults[startPoint-1:stopPoint]
		numberOfPresentations = stopPoint - startPoint + 1

		print("presentationResults: ", len(presentationResults), 'x', len(presentationResults[0]))
		print("resultsToBeProcessed: ", len(resultsToBeProcessed), 'x', len(resultsToBeProcessed[0]))

		# Initialize column weights for categories (1-based indexing to match Smalltalk)
		# Add an extra row at index 0 that won't be used to maintain 1-based indexing
		columnWeightsInFavourOfCategories = np.zeros((numberOfCategories + 1, numberOfColumns), dtype=int)

		# Create target array with 1-based category indices
		# In Smalltalk this was: 1 to: (numberOfPresentations/numberOfCategories) do: [:cat1|
		#                           1 to: numberOfCategories do: [:k| target addLast: k]
		target = []
		for _ in range(numberOfPresentations // numberOfCategories):
			for k in range(1, numberOfCategories + 1):
				target.append(k)

		# Process each presentation
		for presentation in range(numberOfPresentations):
			# Get current category (1-based index)
			currentIdentity = target[presentation]
			currentPresentation = resultsToBeProcessed[presentation]
			
			# Calculate weights for each category
			weightsOfCategoriesInCurrentPresentation = np.zeros(numberOfCategories + 1)  # +1 for 1-based indexing
			for cat2 in range(1, numberOfCategories + 1):  # 1-based category indexing
				referenceWeightsOfCurrentCategory = columnWeightsInFavourOfCategories[cat2]
				currentCategoryWeightInCurrentPresentation = 0
				
				# Calculate weight for this category (matching Smalltalk's explicit iteration)
				for col2 in range(numberOfColumns):
					currentCategoryWeightInCurrentPresentation += (
						currentPresentation[col2] * referenceWeightsOfCurrentCategory[col2]
					)
				weightsOfCategoriesInCurrentPresentation[cat2] = currentCategoryWeightInCurrentPresentation
			
			# Find category with largest weight (adjusting for 1-based indexing)
			selectedCategory = np.argmax(weightsOfCategoriesInCurrentPresentation)
			if selectedCategory == 0:  # Handle case where argmax returns 0
				selectedCategory = np.argmax(weightsOfCategoriesInCurrentPresentation[1:]) + 1

			# Update weights for correct category
			columnWeightsInFavourOfCategories[currentIdentity] += currentPresentation
			
			# If selection was incorrect, reduce weights for incorrectly selected category
			if selectedCategory != currentIdentity:
				for col4 in range(numberOfColumns):
					if currentPresentation[col4] > 0:
						columnWeightsInFavourOfCategories[selectedCategory][col4] = int(
							columnWeightsInFavourOfCategories[selectedCategory][col4] / weightReductionFactor
						)

		return columnWeightsInFavourOfCategories[1:]  # Remove the padding row we added for 1-based indexing

class BrainActivity:

	# This is inteneded to organize the presentation results brain activity with more 
	# coordinated data that is easier to sum.  The sum in presentaion results takes half of the 
	# processing time (RJT)

	# 600 timeslots, 15 columns, 3 layers, 10 potential spikes for 2 layers 
	# and 1 potential spike for the layer 3

	def __init__(self, timeSlot, column, layer, spikes):
		pass


