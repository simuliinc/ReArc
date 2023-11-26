from Brain import *
from PresentOneCategoryInstance import *
import random
from datetime import *

def typeABrainRun():
	startTime = datetime.now()
	#Global variables capture a range of information about brain activity at different points
	Y = []
	Y2 = []

	# Y3 records columnsToGetInputFromHippocampus in method Hippocampus 
	# updateHippocampalRecordsForMultipleModulationCycles: layerThreeActivity 
	# withInternalActivity: layerTwoActivity. Currently suspended
	Y3 = []

	# YY records hippocampal showStrongActivityCount in method Brain presentTripleCategoryInstance: 
	# firstCategoryInputSource withSecondCategory: secondCategoryInputSource withThirdCategory: 
	# thirdCategoryInputSource . Currently suspended
	YY = []

	# Z records the number of spikes in each input state in method InputState getSpikesInNextTimeslot: 
	# secondCategoryInputSource withThirdCategory: thirdCategoryInputSource. Currently suspended
	Z = []
	ZZ = []

	# Collection of the following five variables (spikes in each timeslot) in method presentTripleCategoryInstance: 
	# firstCategoryInputSource withSecondCategory: secondCategoryInputSource withThirdCategory: 
	# thirdCategoryInputSource have been INACTIVATED

	InputSpikesPerTimeslot = [] 
	LayerOneSpikesPerTimeslot = []
	LayerTwoSpikesPerTimeslot = []
	LayerThreeSpikesPerTimeslot = []
	RecordingManagementInputsPerTimeslot = []

	# PresentationResults global variables capture the layer three column outputs in response to each category 
	# instance presentation. This information is used by the black box basal ganglia to determine behaviour
	PresentationResults = []
	PresentationResults2 = []
	print("Defining Categories\n")
	spikeEvaluator = SpikeEvaluator()

	# THE FOLLOWING CODE (to END do: ii) CREATES favouredInputs, WHICH IS AN ORDEREDCOLLECTION OF 
	# NumberOfColumns ORDEREDCOLLECTIONS. EACH OF THESE ORDEREDCOLLECTIONS CONTAINS A SET OF INPUTS 
	# THAT WILL BE FAVOURED IN CREATING INPUTS TO THE COLUMN. EACH SET IS CREATED BY DEFINING A GROUP 
	# OF 50 INPUTS, THEN FINDING THE 25 IN THE 50 THAT ARE MOST OFTEN ACTIVE AT SIMILAR TIMES. MOST 
	# OFTEN IS DETERMINED BY MEASURING THE NUMBER OF TIMES EACH INPUT IS ACTIVE AT THE SAME TIME AS 
	# AT LEAST 5 OTHER INPUTS IN THE 50, IN PERIODS OF 15 TIMECYCLES (5 MILLISECONDS) WITHIN 10 200 
	# MILLISECOND PRESENTATIONS OF EACH OF FIVE CATEGORIES.
	print("Calculating FavoredInputs\n")
	favouredInputs = []
	for ii in range(NumberOfColumns): 
		startingSelection = set()
		for randomInputs in range(50):
			startingSelection.add(random.choice(range(InputSpaceSize)))
		simultaneityCount = [0]*len(startingSelection)
		for presentationCycles in range(10):
			for categoryNumber in range(30):
				simultaneityCount = spikeEvaluator.asInputState(categoryNumber).addInputSimultaneityMeasureForOnePeriod(simultaneityCount, startingSelection)
		startingSelection = list(startingSelection)
		# sort the index, value of simultaneityCount by largest values and take the top 25 indexes (RJT)
		inputs = sorted(list(enumerate(simultaneityCount)), key=lambda value: value[1], reverse=True)
		indexes = list(map(lambda index: index[0], inputs[:25]))
		favouredInputs.append(list(map(lambda index: startingSelection[index], indexes)))

	# The favoured inputs are recorded for later analysis if required
	FavoredInputs = favouredInputs
	print("Configuring the Brain\n")
	brain = Brain(2)
	brain.configureFirstArea(favouredInputs)

	# Each category instance is presented for 200 milliseconds. The black box thalamus puts a 40 Hz 
	# frequency modulation on the spikes so that they are much more likely to occur within a 
	# 5 millisecond segment of each 25 millisecond modulation interval. To save on computation 
	# time and to test working memory simultaneous handling of multiple objects, three different 
	# category instances are presented in each 200 millisecond period, in three different modulation 
	# phases
	print("Presenting data\n")
	for presentationCycle in range(40):
		print ("Cycle: "+str(presentationCycle)+" of 40\n")
		for category in range(0,30,3):
			print ("Category: "+str(category)+"-"+str(category+2)+" of 30\n")
			brain.presentTripleCategoryInstance(spikeEvaluator.asInputState(category), 
									  spikeEvaluator.asInputState(category + 1),
									  spikeEvaluator.asInputState(category + 2))

	endTime = datetime.now()
	print('Time to Run: '+repr(endTime-startTime))

################## Main function
typeABrainRun()