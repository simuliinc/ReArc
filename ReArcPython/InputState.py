# An InputState is a harness for brain runs
from Globals import *
import random
import numpy as np
from tqdm import tqdm
class InputState:

	def __init__(self, category):
		self.category = category
		self.phaseAtInitialTimeslot = 23
		self.currentTimeslot = 0
		self.currentPhase = 0
		self.secondCateogry = []

	def getSpikesInNextTimeslot(self, secondCategory = [], thirdCategory = []):
		# Returns the identities of the inputs that contain an action potential spike in the next timeslot"
		categorySize = len(self.category)
		spikes = np.zeros(categorySize, dtype=int)
		
		# Handle categories
		if len(secondCategory):
			self.secondCategory = secondCategory  # Fix typo
		else:
			self.secondCategory = np.zeros(categorySize, dtype=int)
		if len(thirdCategory):
			self.thirdCategory = thirdCategory
		else:
			self.thirdCategory = np.zeros(categorySize, dtype=int)
		
		self.currentTimeslot += 1
		
		# Match Smalltalk's 1-75 phase calculation
		self.currentPhase = (self.currentTimeslot - 1 + self.phaseAtInitialTimeslot) % 75
		if self.currentPhase == 0:
			self.currentPhase = 75
		
		# Calculate second and third phases (1-75 range)
		secondPhase = self.currentPhase + 25
		if secondPhase > 75:
			secondPhase -= 75
		thirdPhase = secondPhase + 25
		if thirdPhase > 75:
			thirdPhase -= 75
		
		# Get modulation factors
		mpf1 = ModulationProbabilityFactor[self.currentPhase - 1]  # -1 for 0-based array access
		mpf2 = ModulationProbabilityFactor[secondPhase - 1]
		mpf3 = ModulationProbabilityFactor[thirdPhase - 1]
		
		# Generate spikes
		for i, (firstCatValue, secondCatValue, thirdCatValue) in enumerate(zip(self.category, self.secondCategory, self.thirdCategory)):
			currentInputSpikeProbability = (firstCatValue * mpf1) + (secondCatValue * mpf2) + (thirdCatValue * mpf3)
			spikes[i] = int(currentInputSpikeProbability > np.random.randint(0, IntegerCollectionSizeForInputStateGeneration))
		
		return spikes
	
	def addInputSimultaneityMeasureForOnePeriod(self, existingMeasure, setOfInputs):
		# This method is addressed to the InputState for a category. It is provided with an OrderedCollection existingMeasure 
		# and a SortedCollection setOfInputs. existingMeasure  contains the frequency with which the inputs contained in 
		# setOfInputs have occurred in the past at the same time as other inputs in setOfInputs. The method examines a time 
		# interval of 600 timeslots (200 milliseconds) during which an instance of the category is presented. This interval 
		# is broken up into periods of 15 timeslots (5 milliseconds). In this period, if one or more spikes are generated 
		# by an input in setOfInputs, the corresponding element in combinedInput is set at 1. Next, the total number of 
		# inputs in setOfInputs that produced one or more spikes in the 15 timeslot period is determined and recorded in 
		# the variable simultaneityCount. If this total exceeds the limit simultaneityCountLimit (specified within the 
		# method), then the variable existingMeasure is updated.
		simultaneityCountLimit = 5

		for period in (range(40)):
			combinedInput = np.zeros(len(setOfInputs), dtype=int)

			# Accumulate spikes over 15 timesteps
			for _ in range(15):
				inputs = self.getSpikesInNextTimeslot()
				for i, soi in enumerate(setOfInputs):
					if inputs[soi] == 1:
						combinedInput[i] = 1

			# Only update if co-activation exceeds threshold
			simultaneityCount = np.sum(combinedInput)
			if simultaneityCount > simultaneityCountLimit:
				for i in range(len(setOfInputs)):
					if combinedInput[i] == 1:
						existingMeasure[i] += 1

		return existingMeasure

	def getHippocampalSpikesInNextTimeslot(self):
		assert False, "This method was translated for hisorical reasons and should not be used"
		# Returns the identities of the inputs that contain an action potential spike in the next timeslot"

		# !!! This method appears to be unused.  It's called by Brain >> presentInputsInOneTimeslotToBrain:
		# but the method is not completely implemented and contains a note
		# 	This is the first edition of the presentInputs method, and assumes there is just one CorticalArea 
		#   in visualCortex, and a CorticalArea in entorhinalCortex. excitatoryInputs contains the sensory action 
		#   potential spikes in one timeslot, and the recording management inputs are obtained from the entorhinal 
		#   cortex.

		self.currentTimeslot += 1

		# hippocampus gets currentPhase from global CurrentPhase, which is set by sensory input InputState"
		
		# currentPhase := CurrentPhase.  This global is no longer used.  This method is historical so if it is 
		# implemented you should uncomments this and create the Global CurrentPhase  (RJT)

		spikes = np.zeros(len(self.category), dtype=int)

		# SPIKE PROBABILITIES IN category ARE NUMBERS FROM 1 TO 200 currentInputSpikeProbability IS A NUMBER 
		# BETWEEN 0 AND 200. A RANDOM NUMBER IS SELECTED FROM IntegerCollectionForInputStateGeneration, WHICH 
		# CONTAINS THE NUMBERS 0 TO 9999. IF currentInputSpikeProbability IS GREATER THAN THE RANDOMLY SELECTED 
		# NUMBER, A SPIKE IS PRESENT. HENCE IF, FOR EXAMPLE, SPIKE PROBABILITY IN THE CURRENT TIMESLOT IS 200, 
		# THE CHANCE OF A SPIKE IS 200/10000 = 0.02

		# ModulationProbabilityFactor IS A NUMBER THAT DETERMINES HOW PROBABLE A SPIKE WILL BE AT DIFFERENT 
		# STAGES OF THE MODULATION CYCLE. IT INCREASES THE PROBABILITY AT MODULATION PEAKS AND DECREASES IT 
		# AT MODULATION MINIMA, BUT SPIKE AVERAGED PROBABILITY OVER THE MODULATION INTERVAL IS THE SAME 
		
		for i,cat in enumerate(self.category):
			if (cat * ModulationProbabilityFactor[self.currentPhase]) > random.choice(range(IntegerCollectionSizeForInputStateGeneration)):
				spikes[i]=1
		return spikes
	
