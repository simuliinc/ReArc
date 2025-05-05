from Brain import *
from PresentOneCategoryInstance import *
import random
from datetime import *
import psutil

def report_memory_usage():
    # Get the current process
    process = psutil.Process()
    
    # Get memory info
    memory_info = process.memory_info()
    
    # Report memory usage in bytes
    print(f"Memory Usage: {memory_info.rss / (1024 ** 2):.2f} MB")  # Resident Set Size (RSS)
    print(f"Memory Usage (Virtual): {memory_info.vms / (1024 ** 2):.2f} MB")  # Virtual Memory Size (VMS)


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
	global PresentationResults
	# PresentationResults = []
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
	# for ii in tqdm(range(NumberOfColumns)): # NumberOfColumns = 15
	# 	startingSelection = set()
	# 	for randomInputs in range(50):
	# 		startingSelection.add(random.choice(range(InputSpaceSize)))
	# 	simultaneityCount = [0]*len(startingSelection)
	# 	for presentationCycles in (range(10)):  # review this Looks wrong to Rachel
	# 		for categoryNumber in range(30):
	# 			simultaneityCount = spikeEvaluator.asInputState(categoryNumber).addInputSimultaneityMeasureForOnePeriod(simultaneityCount, startingSelection)
	# 	startingSelection = list(startingSelection)
	# 	# sort the index, value of simultaneityCount by largest values and take the top 25 indexes (RJT)
	# 	inputs = sorted(list(enumerate(simultaneityCount)), key=lambda value: value[1], reverse=True)
	# 	indexes = list(map(lambda index: index[0], inputs[:25]))
	# 	favouredInputs.append(list(map(lambda index: startingSelection[index], indexes)))

	# The favoured inputs are recorded for later analysis if required
	# FavoredInputs = favouredInputs
	favouredInputs = [[267, 38, 346, 309, 14, 325, 122, 12, 103, 96, 40, 341, 214, 45, 291, 1, 374, 307, 59, 50, 28, 334, 285, 89, 159], [134, 5, 304, 69, 319, 284, 357, 149, 119, 58, 72, 188, 217, 92, 291, 352, 330, 323, 3, 88, 365, 286, 302, 32, 83], [162, 105, 359, 5, 133, 107, 255, 299, 166, 86, 154, 284, 303, 188, 374, 326, 66, 311, 42, 142, 300, 122, 59, 197, 367], [109, 337, 124, 105, 63, 51, 188, 218, 333, 335, 127, 193, 291, 231, 156, 202, 40, 217, 142, 314, 184, 100, 347, 330, 382], [55, 312, 196, 154, 86, 130, 96, 119, 357, 188, 265, 268, 187, 346, 212, 76, 200, 327, 70, 1, 349, 21, 90, 385, 27], [359, 93, 236, 134, 398, 391, 353, 56, 14, 138, 341, 137, 306, 334, 61, 111, 367, 184, 78, 340, 27, 330, 217, 87, 349], [5, 376, 196, 304, 270, 144, 218, 56, 325, 303, 380, 50, 352, 12, 136, 334, 10, 279, 42, 272, 59, 287, 308, 123, 254], [162, 93, 236, 341, 304, 103, 86, 119, 17, 43, 374, 326, 136, 70, 3, 231, 32, 131, 363, 352, 367, 307, 147, 112, 117], [376, 170, 5, 267, 18, 357, 211, 392, 240, 278, 297, 101, 57, 363, 172, 164, 290, 122, 66, 367, 127, 70, 3, 233, 197], [252, 5, 69, 49, 304, 305, 270, 119, 336, 263, 325, 357, 14, 16, 103, 138, 382, 300, 363, 92, 374, 122, 266, 251, 393], [162, 105, 6, 267, 5, 219, 102, 346, 133, 48, 43, 375, 16, 329, 263, 137, 144, 319, 233, 251, 32, 257, 90, 176, 343], [86, 376, 258, 154, 166, 391, 172, 150, 149, 34, 92, 333, 325, 188, 327, 58, 90, 142, 85, 62, 368, 399, 248, 208, 293], [252, 162, 152, 166, 98, 211, 357, 353, 14, 309, 150, 240, 299, 96, 135, 85, 91, 365, 297, 45, 138, 65, 3, 100, 62], [204, 225, 124, 392, 175, 346, 72, 368, 380, 62, 10, 100, 299, 14, 147, 50, 40, 323, 117, 28, 192, 352, 293, 248, 71], [219, 220, 187, 18, 149, 391, 10, 153, 166, 90, 62, 231, 61, 290, 374, 329, 45, 78, 335, 367, 65, 87, 343, 251, 176]]
	FavoredInputs = favouredInputs
	# Store favored inputs to file
	# with open('favoredInputs.txt', 'w') as f:
	# 	f.write('Favored Inputs:\n')
	# 	for i, inputs in enumerate(FavoredInputs):
	# 		f.write(f'Column {i}: {inputs}\n')
	print(FavoredInputs)
	print("Configuring the Brain\n")
	brain = Brain(2)
	brain.configureFirstArea(favouredInputs)

	# Each category instance is presented for 200 milliseconds. The black box thalamus puts a 40 Hz 
	# frequency modulation on the spikes so that they are much more likely to occur within a 
	# 5 millisecond segment of each 25 millisecond modulation interval. To save on computation 
	# time and to test working memory simultaneous handling of multiple objects, three different 
	# category instances are presented in each 200 millisecond period, in three different modulation 
	# phases
	cycles = 40 # normally 40 
	print("Presenting data\n", flush=True)
	for presentationCycle in tqdm(range(cycles)):
		startCycleTime = datetime.now()
		print ("Cycle: "+str(presentationCycle)+" of "+str(cycles)+"\n", flush=True)
		for category in tqdm(range(0,30,3)):  # Test 30 categories
			# print ("Category: "+str(category)+"-"+str(category+2)+" of 30\n", flush=True)
			brain.presentTripleCategoryInstance(spikeEvaluator.asInputState(category), 
				spikeEvaluator.asInputState(category + 1),
				spikeEvaluator.asInputState(category + 2))
		
		# Write current PresentationResults to file
		# with open('result.txt', 'w') as f:
		# 	f.write('Presentation Results so far:\n')
		# 	f.write(str(PresentationResults))

		report_memory_usage()
		endCycleTime = datetime.now()
		print('Time to run cycle: '+repr(endCycleTime-startCycleTime), flush=True)
	endTime = datetime.now()
	# presentationResults = brain.reportPresentationResultsLayer3(Y[-599:])
	columnWeightsInFavourOfCategories = brain.calculationOfColumnWeightsInFavourOfThirtyCategories(PresentationResults, startPoint=601, stopPoint=900, numberOfCategories=30, numberOfColumns=15, weightReductionFactor = 1.035)
	categoryIdentifications = brain.categoryIdentifications(PresentationResults, columnWeightsInFavourOfCategories, numberOfCategories = 30, presentationStart=601, presentationStop=900)
	print(categoryIdentifications)
	# Store results to file
	# with open('result.txt', 'w') as f:
	# 	f.write('Category Identifications:\n')
	# 	f.write(str(categoryIdentifications))
	# 	f.write('\n\nColumn Weights:\n')
	# 	f.write(str(columnWeightsInFavourOfCategories))
	# 	f.write('\n\nPresentation Results:\n')
	# 	f.write(str(PresentationResults))
	print('Time to Run: '+repr(endTime-startTime), flush=True)

################## Main function
typeABrainRun()