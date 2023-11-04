# The HippocampalSystemBlackBox is the controler for presenting evaluating and storing inputs

from Globals import *

class HippocampalSystemBlackBox:
	def __init__(self):
		self.inputsFromLayerTwo = []
		self.inputsFromLayerThree = []
		self.resetLayerThree()
		self.strongActivityCount = [0]*3
		self.longTermEpisodicRecord = []

	def resetLayerThree(self):
		self.outputsToLayerThree = [[0]*NumberOfColumns]*75

	def constructMultiplexedNULLOutputsForNext25milliseconds(self, columnsToGetInputFromHippocampus): 
		# This constructs outputs from the hippocampus (outputsToLayerThree) for the next 25 milliseconds 
		# and stores them in the instance variable outputsToLayerThree
		# columnsToGetInputFromHippocampus is an OrderedCollection which contains three OrderedCollections. 
		# Each of these three contains the identities of the columns to receive inputs in the next 75 timeslots, 
		# in the three different timeslots respectively. The outputs from the hippocampus must arrive in the 
		# same timeslots as the outputs from layer two, so that they arrive in synch in layer three. Hence they 
		# are located in timeslots 1- 10, 26 - 35, or 51 - 60. NOTE that the first period is one timeslot shorter. 
		# It should not make any significant difference. The complications of 

		# In the current simulation, there is one hippocampal output neuron for each column. For selected columns, 
		# the method then puts a spike from the corresponding neuron in every timeslot (i.e. every 1/3 millisecond) 
		# in the indicated timeslot range . Note that this would be too high a rate for one single neuron, tha assumption 
		# is that it reflects the outputs of a number of hippocampal neurons. However, the implication is that all these 
		# hippocampal neurons target every location on every layer three pyramidal neuron

		# Construct outputsToLayerThree for next 25 milliseconds, but with no spikes.
		# outputsToLayerThree is an OrderedCollection containing 75 OrderedCollections, one for each timeslot in the next 
		# 25 milliseconds. Each of the 75 OrderedCollections contains one number for each column, one if the hippocampal 
		# neuron targetting the column is firing, zero otherwise.

		# This method Does not use the parameter columnsToGetInputFromHippocampus in the method and the comments 
		# do not appear to match what the method does (RJT)
		self.resetLayerThree()


 
	def constructMultiplexedOutputsForNext25milliseconds(self, collectionOfColumnsToGetInputFromHippocampus):
		# This constructs outputs from the hippocampus (outputsToLayerThree) for the next 25 milliseconds and stores 
		# them in the instance variable outputsToLayerThree. columnsToGetInputFromHippocampus is an OrderedCollection 
		# which contains three OrderedCollections. Each of these three contains the identities of the columns to receive 
		# inputs in the next 75 timeslots, in the three different timeslots respectively. The outputs from the hippocampus 
		# must arrive in the same timeslots as the outputs from layer two, so that they arrive in synch in layer three. 
		# Hence they are located in timeslots 1- 10, 26 - 35, or 51 - 60. NOTE that the first period is one timeslot shorter. 
		# It should not make any significant difference. The complications of 

		# In the current simulation, there is one hippocampal output neuron for each column. For selected columns, the method 
		# then puts a spike from the corresponding neuron in every timeslot (i.e. every 1/3 millisecond) in the indicated timeslot 
		# range . Note that this would be too high a rate for one single neuron, tha assumption is that it reflects the outputs 
		# of a number of hippocampal neurons. However, the implication is that all these hippocampal neurons target every location 
		# on every layer three pyramidal neuron

		# Construct outputsToLayerThree for next 25 milliseconds, but with no spikes.
		# outputsToLayerThree is an OrderedCollection containing 75 OrderedCollections, one for each timeslot in the next 
		# 25 milliseconds. Each of the 75 OrderedCollections contains one number for each column, one if the hippocampal 
		# neuron targetting the column is firing, zero otherwise
		
		self.resetLayerThree()

		# Inserting spikes for first three modulation periods"
		layer = 0
		for collection in collectionOfColumnsToGetInputFromHippocampus:
			for column in collection:
				if layer == 0:
					for timeSlotA in range(10):  # 10 spots 0-9 (RJT)
						self.outputsToLayerThree[timeSlotA][column] = 1
				if layer == 1:
					for timeSlotB in range(25,35): # 10 spots 25-34 (RJT)
						self.outputsToLayerThree[timeSlotB][column] = 1
				if layer == 2:
					for timeSlotC in range(50,60): # 10 spots 50-59 (RJT)
						self.outputsToLayerThree[timeSlotC][column] = 1
			# The following code adds the number of output spikes from the hippocampus in the next 25 milliseconds 
			# to strongActivityCount. NOTE that there is only one OrderedCollection for each timeslot, with an element 
			# for each column which is whether or not there is a hippocampal spike going to the neurons in that column 
			# in the timeslot
			self.strongActivityCount[layer] += len(collection)
			layer += 1

	def constructOutputsForNext25milliseconds(self, columnsToGetInputFromHippocampus, modulationControl):
	
		# This constructs outputs from the hippocampus (outputsToLayerThree) for the next 25 milliseconds and stores them 
		# in the instance variable outputsToLayerThree modulationControl indicates where in the 75 milliseconds the 
		# hippocampal outputs should be located.. The method finds the block of 15 timeslots in modulationControl with the 
		# largest number of spikes (note: cannot just calculate average spike position, because if spikes are concentrated at 
		# beginning and end of 75 timeslot modulation period, the average would be n the middle. 

		# The method then puts a spike every timeslot (i.e. every 1/3 millisecond) in the 15 timeslots.  Note that this would 
		# be too high a rate for one neuron, tha assumption is that it reflects the outputs of a number of hippocampal neurons. 
		# However, the implication is that all these hippocampal neurons target every location on every layer three pyramidal 
		# neuron

		# columnsToGetInputFromHippocampus is an OrderedCollection which contains the identities of the columns to receive 
		# inputs in the next 75 timeslots (RJT)
	   
		# First step: find 5 msec modulation peak in modulationControl"
		modulationPeak = modulationControl.index(max(modulationControl))  # NOTE: in Smalltalk OrderedCollection >> largest was implemented 
																		  # with > not >= so in the case that there are multiple instances 
																		  # of a max number it would have chosen the first max value.  
																		  # This does the same (RJT)

		# Construct outputsToLayerThree for next 25 milliseconds, but with no spikes
		self.resetLayerThree()

	
		# If there is no layer two activity in the previous 25 milliseconds, there will 
		# be no activity reflected in modulationControl, so nothing to guide expansions. 
		# So outputsToLayerThree is left with no spikes.
		
		for currentColumn in columnsToGetInputFromHippocampus:
			if sum(modulationControl) > 0:
				for i in range(15):
					# Add spikes in appropriate places
					self.outputsToLayerThree[(modulationPeak-7+i)%75][currentColumn] = 1

	def constructThreeSpikeOutputsInFirstModulationPeriodForNext25milliseconds(self, collectionOfColumnsToGetInputFromHippocampus): 
		# This constructs outputs from the hippocampus (outputsToLayerThree) for the next 25 milliseconds and stores 
		# them in the instance variable outputsToLayerThree 
		# columnsToGetInputFromHippocampus is an OrderedCollection which contains three OrderedCollections. 
		# Each of these three contains the identities of the columns to receive inputs in the next 75 timeslots, 
		# in the three different timeslots respectively. The outputs from the hippocampus must arrive in the same 
		# timeslots as the outputs from layer two, so that they arrive in synch in layer three. Hence they are located 
		# in timeslots 1- 10, 26 - 35, or 51 - 60. NOTE that the first period is one timeslot shorter. It should 
		# not make any significant difference. The complications of 
		# In the current simulation, there is one hippocampal output neuron for each column. For selected columns, 
		# the method then puts a spike from the corresponding neuron in every timeslot (i.e. every 1/3 millisecond) 
		# in the indicated timeslot range . Note that this would be too high a rate for one single neuron, tha 
		# assumption is that it reflects the outputs of a number of hippocampal neurons. However, the implication 
		# is that all these hippocampal neurons target every location on every layer three pyramidal neuron


		# Construct outputsToLayerThree for next 25 milliseconds, but with no spikes.
		self.resetLayerThree()
		# Inserting spikes for first modulation period at timeslots 5 and 8"
		for column in collectionOfColumnsToGetInputFromHippocampus[0]:
			for timeslot in range(4,7):
				self.outputsToLayerThree[timeslot][column] = 1

		# Inserting spikes for second modulation period No spikes in this method

		# Inserting spikes for third modulation period No spikes in this method

	def constructTwoSpikeOutputsInFirstModulationPeriodForNext25milliseconds(self, collectionOfColumnsToGetInputFromHippocampus): 
	
		# This constructs outputs from the hippocampus (outputsToLayerThree) for the next 25 milliseconds and stores them 
		# in the instance variable outputsToLayerThree
		# columnsToGetInputFromHippocampus is an OrderedCollection which contains three OrderedCollections. Each of these 
		# three contains the identities of the columns to receive inputs in the next 75 timeslots, in the three different 
		# timeslots respectively. The outputs from the hippocampus must arrive in the same timeslots as the outputs from 
		# layer two, so that they arrive in synch in layer three. Hence they are located in timeslots 1- 10, 26 - 35, 
		# or 51 - 60. NOTE that the first period is one timeslot shorter. It should not make any significant difference. 
		# The complications of 

		# In the current simulation, there is one hippocampal output neuron for each column. For selected columns, the 
		# method then puts a spike from the corresponding neuron in every timeslot (i.e. every 1/3 millisecond) in the 
		# indicated timeslot range . Note that this would be too high a rate for one single neuron, tha assumption is that 
		# it reflects the outputs of a number of hippocampal neurons. However, the implication is that all these hippocampal 
		# neurons target every location on every layer three pyramidal neuron

		# Construct outputsToLayerThree for next 25 milliseconds, but with no spikes.
		# outputsToLayerThree is an OrderedCollection containing 75 OrderedCollections, one for each timeslot in the next 25 
		# milliseconds. Each of the 75 OrderedCollections contains one number for each column, one if the hippocampal neuron 
		# targetting the column is firing, zero otherwise.

		self.resetLayerThree()

		# Inserting spikes for first modulation period at timeslots 5 and 8
		# in Python (0 based): Inserting spikes for first modulation period at timeslots 4 and 7  (RJT)
		for column in collectionOfColumnsToGetInputFromHippocampus[0]:
			self.outputsToLayerThree[4][column] = 1
			self.outputsToLayerThree[7][column] = 1

		# Inserting spikes for second modulation period No spikes in this method

		# Inserting spikes for third modulation period No spikes in this method

	def constructMultiplexedNULLOutputsForNext25milliseconds(self, collectionOfColumnsToGetInputFromHippocampus): 
	
		assert False, "this method is not sent it also matches constructMultiplexedNULLOutputsForNext25milliseconds, added here to preserve comments"

		# This constructs outputs from the hippocampus (outputsToLayerThree) for the next 25 milliseconds and stores them in the 
		# instance variable outputsToLayerThree 
		# columnsToGetInputFromHippocampus is an OrderedCollection which contains three OrderedCollections. Each of these three 
		# contains the identities of the columns to receive inputs in the next 75 timeslots, in the three different timeslots 
		# respectively. The outputs from the hippocampus must arrive in the same timeslots as the outputs from layer two, so that 
		# they arrive in synch in layer three. Hence they are located in timeslots 1- 10, 26 - 35, or 51 - 60. NOTE that the first 
		# period is one timeslot shorter. It should not make any significant difference. The complications of 

		# In the current simulation, there is one hippocampal output neuron for each column. For selected columns, the method then 
		# puts a spike from the corresponding neuron in every timeslot (i.e. every 1/3 millisecond) in the indicated timeslot range. 
		# Note that this would be too high a rate for one single neuron, tha assumption is that it reflects the outputs of a number 
		# of hippocampal neurons. However, the implication is that all these hippocampal neurons target every location on every layer 
		# three pyramidal neuron

		# Construct outputsToLayerThree for next 25 milliseconds, but with no spikes.
		# outputsToLayerThree is an OrderedCollection containing 75 OrderedCollections, one for each timeslot in the next 25 milliseconds. 
		# Each of the 75 OrderedCollections contains one number for each column, one if the hippocampal neuron targetting the column is 
		# firing, zero otherwise.
		self.resetLayerThree()

	def determineColumnActivityOver75timeslotsForEachModulation(self):

		# This method calculates the total layer three spikes generated in the past 75 timeslots by each column, in each of three 
		# modulation periods. The modulation periods for layer 3 are timeslots 4 - 10, 29 - 39, and 54 - 64. This assumes the input 
		# spikes to the columns have been determined with the inputSourceCategory phases set at zero initially in the top level 
		# BrainRun, and the second and third category instances are 25 and 50 timeslots later than the first

		# The method returns totalInputsFromLayerThreeInPrevious25msecByModulationPeriodAndColumn. This variable is an OrderedCollection 
		# that contains three OrderedCollections, one for each modulation period. Each of these three OrderedCollections contains a 
		# number for each column, the number being the number of spikes generated by layer three of the column in the modulation period 
		# over the last 75 timeslots

		# This code creates the structure for totalInputsFromLayerThreeInPrevious25msecByModulationPeriodAndColumn. It is an 
		# OrderedCollection containing one OrderedCollection for each of three modulation periods. Each of these OrderedCollections 
		# has an element corresponding with each column that is initially set to zero"

		totalInputsFromLayerThreeInPrevious25msecByModulationPeriodAndColumn = [[0]*NumberOfColumns]*3

		# This code goes through timeslots 4 to 10 in the inputsFromLayerThree for each column, and adds any spikes produced by 
		# any column to the total count for the column in the first OrderedCollection in 
		# totalInputsFromLayerThreeInPrevious25msecByModulationPeriodAndColumn
		for timeslot in range(3,13):  # 10 slots 3-12 (RJT)
			for column in range(NumberOfColumns):
				totalInputsFromLayerThreeInPrevious25msecByModulationPeriodAndColumn[0][column] \
					+= sum(self.inputsFromLayerThree[timeslot][column])
				
		# This code goes through timeslots 29 to "39" [sic should say 38] in the inputsFromLayerThree for each column, and adds any 
		# spikes produced by any column to the total count for the column in the second OrderedCollection in 
		# totalInputsFromLayerThreeInPrevious25msecByModulationPeriodAndColumn"	
		for timeslot in range(28,38):  # 10 slots 28-37 (RJT)
			for column in range(NumberOfColumns):
				totalInputsFromLayerThreeInPrevious25msecByModulationPeriodAndColumn[1][column] \
					+= sum(self.inputsFromLayerThree[timeslot][column])

		# This code goes through timeslots 54 to "64"[sic should say 63] in the inputsFromLayerThree for each column, and adds any spikes 
		# produced by any column to the total count for the column in the third OrderedCollection in 
		# totalInputsFromLayerThreeInPrevious25msecByModulationPeriodAndColumn"
		for timeslot in range(53,63):  # 10 slots 53-62 (RJT)
			for column in range(NumberOfColumns):
				totalInputsFromLayerThreeInPrevious25msecByModulationPeriodAndColumn[2][column] \
					+= sum(self.inputsFromLayerThree[timeslot][column])

		return totalInputsFromLayerThreeInPrevious25msecByModulationPeriodAndColumn
	
	def determineIntermediateLayerColumnActivityOver75timeslotsForEachModulation(self):
		# The following code counts how many spikes were generated from all the layer two neurons in each column in each 
		# of three modulation periods over the past 75 timeslots, and records the numbers in 
		# totalInputsFromLayerThreeInPrevious25msec. The modulation periods for layer 2 are timeslots 1 - 10, 26 - 35, and 51 - 60.
		# totalInputsFromLayerTwoInPrevious25msecByModulationPeriodAndColumn is an OrderedCollection containing one OrderedCollection 
		# for each of three modulation periods. Each of these OrderedCollections has an element corresponding with each column that is 
		# the total number of spikes produced by the middle later of the column in the modulation period

		# This code creates the structure for totalInputsFromLayerTwoInPrevious25msecByModulationPeriodAndColumn. It is an 
		# OrderedCollection containing one OrderedCollection for each of three modulation periods. Each of these OrderedCollections 
		# has an element corresponding with each column that is initially set to zero
		totalInputsFromLayerTwoInPrevious25msecByModulationPeriodAndColumn = [[0]*NumberOfColumns]*3

		# This code goes through timeslots 1 to 10 in the inputsFromLayerTwo for each column, and adds any spikes produced by 
		# any column to the total count for the column in the first OrderedCollection in 
		# totalInputsFromLayerTwoInPrevious25msecByModulationPeriodAndColumn
		for timeslot in range(10):  # 10 slots 0-9 (RJT)
			for column in range(NumberOfColumns):
				totalInputsFromLayerTwoInPrevious25msecByModulationPeriodAndColumn[1][column] \
					+= sum(self.inputsFromLayerThree[timeslot][column])
		
		# This code goes through timeslots 26 to 35 in the inputsFromLayerTwo for each column, and adds any spikes 
		# produced by any column to the total count for the column in the second OrderedCollection in 
		# totalInputsFromLayerTwoInPrevious25msecByModulationPeriodAndColumn
		for timeslot in range(25,35):  # 10 slots 25-34 (RJT)
			for column in range(NumberOfColumns):
				totalInputsFromLayerTwoInPrevious25msecByModulationPeriodAndColumn[2][column] \
					+= sum(self.inputsFromLayerThree[timeslot][column])

		# This code goes through timeslots 51 to 60 in the inputsFromLayerTwo for each column, and adds any spikes 
		# produced by any column to the total count for the column in the third OrderedCollection in 
		# totalInputsFromLayerTwoInPrevious25msecByModulationPeriodAndColumn"
		for timeslot in range(50,60):  # 10 slots 50-59 (RJT)
			for column in range(NumberOfColumns):
				totalInputsFromLayerTwoInPrevious25msecByModulationPeriodAndColumn[3][column] \
					+= sum(self.inputsFromLayerThree[timeslot][column])
	
		return totalInputsFromLayerTwoInPrevious25msecByModulationPeriodAndColumn
 

	def popCurrentHippocampalOutputs(self):
		# This was called showCurrentHippocampalOutputs (RJT)
		# This returns the outputs from the hippocampus for the current timeslot.. These outputs are the first element in 
		# outputsToLayerThree, and are deleted once they have been selected"

		return self.outputsToLayerThree.pop(0)

	def updateColumnInputsWithInternalActivity(self, layerThreeActivity, layerTwoActivity):
		# Each timeslot, this method gets layer one and layer two activity and updates the activity records in inputsFromLayerTwo 
		# and inputsFromLayerThree.. Every 75 timeslots, outputsToLayerThree will have become empty, and if this is the case it is 
		# calculated for the next 75 timeslots using the information recorded during the previous 75 timeslots in inputsFromLayerTwo 
		# and inputsFromLayerThree
		assert False, "this method is not called and doesn't appear to have been properly implemented"
		if len(self.inputsFromLayerThree) == 75:
			# This is criterion for recalculating outputsToLayerThree 
			pass
		else:
			# This is criterion for just adding current inputs recalculating outputsToLayerThree
			pass
		self.inputsFromLayerThree= []
		self.resetLayerThree() 

	def updateColumnLayerTwoActivityRecord(self):
		# This method has no body so was never implememented but it is called from Brain >> presentInputsInOneTimeslotToBrain
		pass

	def updateHippocampalRecordsWithInternalActivity(self, layerThreeActivity, layerTwoActivity):
		# In each timeslot, the hippocampus first sends outputs to columns, the activity of the columns is calculated and they 
		# return output activity to the hippocampus

		# Each timeslot, this method gets layer one and layer two activity and updates the activity records in inputsFromLayerTwo 
		# and inputsFromLayerThree.. Every 75 timeslots, outputsToLayerThree will have become empty, and if this is the case it is 
		# calculated for the next 75 timeslots using the information recorded during the previous 75 timeslots in inputsFromLayerTwo 
		# and inputsFromLayerThree

		# NOTE that layerTwoActivity and layerThreeActivity are both OrderedCollection made up or NumberOfColumns OrderedCollections. 
		# In each of these individual column OrderedCollections there is an element for each pyramidal neuron in the layer of the 
		# column. This element is one if the neuron was producing a spike in the timeslot, otherwise zero"
		assert False, "This method is never called"

		self.inputsFromLayerThree.append(layerThreeActivity) 
		self.inputsFromLayerTwo.append(layerTwoActivity) 
	
		if len(self.outputsToLayerThree) == 0:
			# This is criterion for recalculating outputsToLayerThree 

			# The following code counts how many spikes were generated from all the layer three neurons in each 
			# column over the past 75 timeslots, and records the numbers in totalInputsFromLayerThreeInPrevious25msec
			totalInputsFromLayerThreeInPrevious25msec = [0] * NumberOfColumns

			for timeslot in range(75): 
				for column in range(NumberOfColumns):
					totalInputsFromLayerThreeInPrevious25msec[column] \
						+= sum(self.inputsFromLayerThree[timeslot][column])
	
			# In this code, the number of columns that produced at least two outputs in the past 25 milliseconds is 
			# recorded in numberOfColumnsWithOutput

			numberOfColumnsWithOutput = 0
			for input in totalInputsFromLayerThreeInPrevious25msec:
				if input > 1:
					numberOfColumnsWithOutput += 1
	
			# THE FOLLOWING CODE CALCULATES THE OUTPUTS FROM THE HIPPOCAMPUS OVER THE NEXT 75 TIMESLOTS

			# First, determine the outputs from the middle layer neurons in each column in each timeslot 
			# and record in totalMiddleLayerInputsByTimeslot. This variable ends up as an OrderedCollection 
			# of 75 OrderedCollections, each of the 75 being an OrderedCollection with NumberOfColumns elements, 
			# an element being the number of middle layer neurons in a column that fired in the timeslot.
			totalMiddleLayerInputsByTimeslot = [[0]*NumberOfColumns]*75
			for timeslot in range(75): 
				for column in range(NumberOfColumns):
					totalInputsFromLayerThreeInPrevious25msec[timeslot][column] \
						+= sum(self.inputsFromLayerThree[timeslot][column])
			
			# The following code determines how may middle layer outputs there were in each timeslot across all columns and 
			# records in modulationControl. This variable is used to determine the relative probability of hippocampal output 
			# spikes in each of the next 75 timeslots 
			modulationControl = [0]*75 
			for timeslotB in range(75):
				modulationControl[timeSlotB] = sum(totalMiddleLayerInputsByTimeslot[timeslotB])
	
			# The following code determines the total middle level firing in each column across all timeslots and records it in 
			# middleLayerFiringOfEachColumnTotalAcross25milliseconds

			middleLayerFiringOfEachColumnTotalAcross25milliseconds = [[0]*NumberOfColumns]*75	
			for timeslotC in range(75): 
				for columnD in range(NumberOfColumns):
					totalInputsFromLayerThreeInPrevious25msec[columnD] \
						+= sum(self.inputsFromLayerTwo[timeslotC][columnD])
		
			# The following code determines which columns will receive ouputs from the hippocampus in the next 25 milliseconds. 
			# It selects two columns if no column produced layer three output in the last 25 milliseconds, one column if only one 
			# column produced output, otherwise no columns. The identities of the columns to receive hippocampal input in the next 
			# 25 milliseconds are recorded in columnsToGetInputFromHippocampus

			columnsToGetInputFromHippocampus = []
			if numberOfColumnsWithOutput == 1:
				columnsToGetInputFromHippocampus.append(middleLayerFiringOfEachColumnTotalAcross25milliseconds.index \
											(max(middleLayerFiringOfEachColumnTotalAcross25milliseconds))[1])
			elif numberOfColumnsWithOutput == 0:
				columnsToGetInputFromHippocampus.append(middleLayerFiringOfEachColumnTotalAcross25milliseconds.index \
											(max(middleLayerFiringOfEachColumnTotalAcross25milliseconds))[1])			
				middleLayerFiringOfEachColumnTotalAcross25milliseconds[columnsToGetInputFromHippocampus[0]] = 0
				columnsToGetInputFromHippocampus.append(middleLayerFiringOfEachColumnTotalAcross25milliseconds.index \
											(max(middleLayerFiringOfEachColumnTotalAcross25milliseconds))[1])

			# The following code constructs the outputs from the hippocampus for the next 25 milliseconds"
			self.constructOutputsForNext25milliseconds(self, columnsToGetInputFromHippocampus, modulationControl)

			# This empties the record for the last 75 timeslots"	
			inputsFromLayerThree = [] 
			inputsFromLayerTwo = [] 
	
	def eliminateColumnsWithStrongLayerThreeActivity(self, collectionOfThreeColumnsData, totalInputsFromLayerThreeInPrevious25msecByModulationPeriodAndColumn):
		# This method is addressed to an OrderedCollection that contains three OrderedCollections corresponding with three phases of 
		# modulation over a 75 timeslot period. Each of the three OrderedCollections contains a set of numbers, each number being the 
		# number of spikes generated by the middle layer of one column during the same modulation phase over the 75 timeslots.

		# collectionOfThreeColumnsData is now he ordered collection in the above note so that we can pull this method off of collection (RJT)

		# totalInputsFromLayerThreeInPrevious25msecByModulationPeriodAndColumn contains three OrderedCollections corresponding with three 
		# phases of modulation over a 75 timeslot period. Each of the three OrderedCollections contains a set of numbers, each number 
		# being the number of spikes generated by the output layer of one column during the same modulation phase over the 75 timeslots.

		# For each modulation period, this method sets the record of intermediate layer activity of a column to zero if the column has 
		# strong output layer activity (i.e. more than 2 spikes over the 75 timeslots)
		for modulationPeriod in range(3):
			for column in range(NumberOfColumns):
				if totalInputsFromLayerThreeInPrevious25msecByModulationPeriodAndColumn[modulationPeriod][column] > 1:
					collectionOfThreeColumnsData[modulationPeriod][column] = 0

	def updateHippocampalRecordsForMultipleModulationCyclesWithInternalActivity(self, layerThreeActivity, layerTwoActivity):
		# In every 600 timeslots, the same three categories are presented to the cortical area. The 600 timeslots are divided 
		# into eight 75 timeslot periods, and each 75 timeslots divided into three 25 timeslot periods. So the same category 
		# is presented in eight 25 timeslot periods over a 600 timeslot time

		# In each timeslot, the hippocampus first sends outputs to the output layer (layer 3) of columns. Functionally, these 
		# hippocampal outputs encourage receptive field expansions. The activity of the columns in response to these and other 
		# inputs is calculated, and the columns return middle layer (layer 2) activity to the hippocampus

		# Each timeslot, this method gets layer one and layer two activity and updates the activity records in inputsFromLayerTwo 
		# and inputsFromLayerThree.. Every 75 timeslots, outputsToLayerThree will have become empty, and if this is the case it is 
		# calculated for the next 75 timeslots using the information recorded during the previous 75 timeslots in inputsFromLayerTwo 
		# and inputsFromLayerThree

		# NOTE that layerTwoActivity and layerThreeActivity are both OrderedCollections made up of NumberOfColumns OrderedCollections. 
		# In each of these individual column OrderedCollections there is an element for each pyramidal neuron in the layer of the 
		# column. This element is one if the neuron was producing a spike in the timeslot, otherwise zero

		# The following code updates the instance variable of the hippocampus to add the layer two and layer three activity in the 
		# current timeslot. Every 75 timeslots this information is used to calculate the outputs of the hippocampus for the next 75 
		# timeslots
		self.inputsFromLayerThree.append(layerThreeActivity)
		self.inputsFromLayerTwo.append(layerTwoActivity) 

		if len(self.outputsToLayerThree) == 0:
			# This is criterion for recalculating outputsToLayerThree. If true, all the 75 outputs calculated earlier will have 
			# been delivered

			# The following code counts how many spikes were generated from all the layer three neurons in each column in each 
			# of three modulation periods over the past 75 timeslots, and records the numbers in totalInputsFromLayerThreeInPrevious25msec. 
			# The modulation periods for layer 3 are timeslots 4 - 10, 29 - 39, and 54 - 64.
			# totalInputsFromLayerThreeInPrevious25msecByModulationPeriodAndColumn is an OrderedCollection containing one 
			# OrderedCollection for each of three modulation periods. Each of these OrderedCollections has an element 
			# corresponding with each column that is the total number of spikes produced by the column in the modulation period

			totalInputsFromLayerThreeInPrevious25msecByModulationPeriodAndColumn = self.determineColumnActivityOver75timeslotsForEachModulation()

			# In the following code, for each of the three modulation periods, the number of columns that produced at least two 
			# outputs in the past 25 milliseconds is recorded in numberOfColumnsWithOutputInEachModulationPeriod. This variable 
			# is anOrderedCollection which will have three elements, one for each modulation period

			numberOfColumnsWithOutputInEachModulationPeriod = []
		
			# This section of code iterates through the three modulation periods kk. In each period it sets up the variable 
			# totalInputsFromLayerThreeInCurrentModulation which is the OrderedCollection in 
			# totalInputsFromLayerThreeInPrevious25msecByModulationPeriodAndColumn corresponding with the period.

			for mp in range(3):
				totalInputsFromLayerThreeInCurrentModulation = totalInputsFromLayerThreeInPrevious25msecByModulationPeriodAndColumn[mp]
				numberOfColumnsWithOutputInCurrentModulationPeriod = 0
				for column in NumberOfColumns:
					if totalInputsFromLayerThreeInCurrentModulation[column] > 1:
						numberOfColumnsWithOutputInCurrentModulationPeriod += 1
				numberOfColumnsWithOutputInEachModulationPeriod.append(numberOfColumnsWithOutputInCurrentModulationPeriod)

	
			# THE FOLLOWING CODE CALCULATES WHICH COLUMNS WILL RECEIVE OUTPUTS FROM THE HIPPOCAMPUS OVER THE NEXT 75 TIMESLOTS, 
			# BY MODULATION PERIOD

			# The following code counts how many spikes were generated from all the layer two neurons in each column in each of 
			# three modulation periods over the past 75 timeslots, and records the numbers in totalInputsFromLayerThreeInPrevious25msec. 
			# The modulation periods for layer 2 are timeslots 1 - 9, 26 - 35, and 51 - 60.
			# totalInputsFromLayerThreeInPrevious25msecByModulationPeriodAndColumn is an OrderedCollection containing one 
			# OrderedCollection for each of three modulation periods. Each of these OrderedCollections has an element corresponding 
			# with each column that is the total number of spikes produced by the column in the modulation period
			hmc = HippocampalMaxColumn(self)

			# The following was moved to HippocampalMaxColumn >> __init__()  (RJT)
			# totalInputsFromLayerTwoInPrevious25msecByModulationPeriodAndColumn =  \
			#	self.determineIntermediateLayerColumnActivityOver75timeslotsForEachModulation()

			# Hippocampal outputs need to be directed to columns with strong internal activity but no output. 
			# totalInputsFromLayerTwoInPrevious25msecByModulationPeriodAndColumn is therefore modified to set to zero the count of 
			# intermediate level activity of any columns with strong outputs

			hmc.eliminateColumnsWithStrongLayerThreeActivity(totalInputsFromLayerThreeInPrevious25msecByModulationPeriodAndColumn)
		
			# The following code selects the columns to receive hippocampal input in each of the three modulation periods in the next 
			# 25 milliseconds. Two columns are selected if no column produced layer three output in that modulation period in the past 
			# 5 timeslots, one column if only one column produced output, otherwise no columns. The identities of the columns to receive 
			# hippocampal input are recorded in columnsToGetInputFromHippocampus. columnsToGetInputFromHippocampus is an OrderedCollection 
			# that contains three OrderedCollections. The first OrderedCollection contains the identities of the columns to receive inputs 
			# in the first modulation period, and so on.

			# NOTE that the OrderedCollection method largest returns an OrderedCollection with two numbers. The first number is the largest 
			# number in the target OrderedCollection, the second number is the index of largest number in the target. This index is the 
			# number of the column with the largest number of spikes. Hence ((OC largest) at: 2) returns the column identity. HOWEVER, if 
			# the method largest is addressed to an OrderedCollection in which all the elements are 0, it will return 0 and the index of 
			# the first element. Hence if ((OC largest) at: 1) is zero, the column identity is not added because there was actually no 
			# firing in the middle layer.
			
			# The following was moved to HippocampalMaxColumn >> __init__()  (RJT)
			# columnsToGetInputFromHippocampus = [[],[],[]]
			
			for mp in range(3):    # kkk tracks the three modulation periods [renamed to mp (RJT)]
				# If no columns had activity in the middle layer in one modulation period of a 75 timeslot interval, no column will 
				# be selected to get hippocampal inputs in the next 75 timeslots. So if the largest column activity is zero for a 
				# modulation interval kkk, no columns will be added to the list of those to get input in that interval
				if hmc.columnHasSpikes:
					# If two columns produced output in one modulation period of the last 75 timelots, one column needs to be selected 
					# to get input from the hippocampus in the next 75 timeslots.
					if numberOfColumnsWithOutputInEachModulationPeriod[mp] == 2:
						hmc.appendMaxColumn(mp)

					# If one column produced output in one modulation period of the last 75 timelots, two columns need to be selected 
					# to get input from the hippocampus in the next 75 timeslots. When one column has been selected, its middle layer 
					# activity number is set to zero so that the 'largest' method will then select the next largest..
					# NOTE: this means that if no input is presented in one timeslot, there will be no hippocampal activity in that 
					# timeslot
					if numberOfColumnsWithOutputInEachModulationPeriod[mp] == 1: 		
						hmc.appendMaxColumn(mp)
						hmc.zeroLastIndex(mp)
						hmc.appendMaxColumn(mp)

					# If no columns produced output iin one modulation period of the last 75 timelots, three columns need to be 
					# selected to get input from the hippocampus in the next 75 timeslots. When one column has been selected, its 
					# middle layer activity number is set to zero so that the 'largest' method will then select the next largest..
					# NOTE: this means that if no input is presented in one timeslot, there will be no hippocampal activity in that 
					# timeslot
	
					if numberOfColumnsWithOutputInEachModulationPeriod[mp] == 0:		
						hmc.appendMaxColumn(mp)	
						hmc.zeroLastIndex(mp)
						hmc.appendMaxColumn(mp)	
						hmc.zeroLastIndex(mp)
						hmc.appendMaxColumn(mp)	

			# The following comment was in the Smalltalk Code (RJT)
			# "Y3 addLast: (columnsToGetInputFromHippocampus deepCopy)."


			# The following code constructs the outputs from the hippocampus for the next 25 milliseconds
			self.constructMultiplexedOutputsForNext25milliseconds: hmc.columnsToGetInputFromHippocampus

			# This empties the record for the last 75 timeslots	
			self.inputsFromLayerThree = [] 
			self.inputsFromLayerTwo = []
	
	def zeroStrongActivityCount(self):
		# This method had no comments or Code in Smalltalk
		# but it is called by the following Smalltalk methods
		# Brain >> presentTripleCategoryInstance:withSecondCategory:withThirdCategory: 
		# Brain >> presentTripleCategoryInstanceTwoAreas:withSecondCategory:withThirdCategory:
		# Brain >> presentTripleCategoryInstanceWithTargetedHippocampusInputs:withSecondCategory:withThirdCategory:
		pass

class HippocampalMaxColumn:
	# HippocampalMaxColumn is a utility class (method to class pattern) to simplify the code in 
	# HippocampalSystemBlackBox >> updateHippocampalRecordsForMultipleModulationCyclesWithInternalActivity
	# and make it more undertandable.

	def __init__(self, hippocampalBB):
		self.hippocampalBB = hippocampalBB
		self.totalInputsFromLayerThreeInPrevious25msecByModulationPeriodAndColumn = hippocampalBB.determineColumnActivityOver75timeslotsForEachModulation()
		self.columnsToGetInputFromHippocampus = [[],[],[]]
		self.lastIndex = 0
	
		# Hippocampal outputs need to be directed to columns with strong internal activity but no output. 
		# totalInputsFromLayerTwoInPrevious25msecByModulationPeriodAndColumn is therefore modified to set to zero the count of 
		# intermediate level activity of any columns with strong outputs

		def eliminateColumnsWithStrongLayerThreeActivity(self, totalInputsFromLayerThreeInPrevious25msecByModulationPeriodAndColumn):
			self.hippocampalBB.eliminateColumnsWithStrongLayerThreeActivity(self.totalInputsFromLayerTwoInPrevious25msecByModulationPeriodAndColumn, \
													totalInputsFromLayerThreeInPrevious25msecByModulationPeriodAndColumn)

	def appendMaxColumn(self, modulationPeriod):
		if max(self.totalInputsFromLayerTwoInPrevious25msecByModulationPeriodAndColumn[modulationPeriod]) > 0: 
			self.lastIndex = self.columnsToGetInputFromHippocampus[modulationPeriod].  \
				append(self.totalInputsFromLayerTwoInPrevious25msecByModulationPeriodAndColumn. \
					index(max(self.totalInputsFromLayerTwoInPrevious25msecByModulationPeriodAndColumn[modulationPeriod])))

	def zeroLastIndex(self, modulationPeriod):
		self.totalInputsFromLayerTwoInPrevious25msecByModulationPeriodAndColumn[modulationPeriod][self.lastIndex][0] = 0


	def columnHasSpikes(self, modulationPeriod):
		 return max(self.totalInputsFromLayerTwoInPrevious25msecByModulationPeriodAndColumn[modulationPeriod]) != 0