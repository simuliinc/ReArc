### PLEASE WRITE THE SMALLTALK CODE TO THE PYTHON SCRIPT HERE FOR THE TWO FUNCTIONS BELOW.
#### SOME CODE HAS BEEN PROVIDED FOR INITIALIZATION.
import numpy as np
import random
from InputState import *
from Globals import *
#----------------------------

class SpikeEvaluator:
	def __init__(self, currentTimeSlot = 0, phaseAtInitialTimeslot = 23, \
					mpf = ModulationProbabilityFactor, \
					integerCollectionForInputStateGeneration = np.arange(10000)):
			self.currentTimeSlot = currentTimeSlot
			self.phaseAtInitialTimeslot = phaseAtInitialTimeslot
			self.modulationProbablityFactor = mpf
			self.integerCollectionForInputStateGeneration = integerCollectionForInputStateGeneration
			self.availableProbabilities = []
			self.category = np.empty((30,400))
			self.currentPhase = phaseAtInitialTimeslot - 1
			self.currentPhaseLimit = len(self.modulationProbablityFactor)
			self.currentStrikeProbability = []
			self.defineAvailableProbabilities()
			self.defineObjectCategories()
			self.inputs = []
			
	def defineAvailableProbabilities(self):
			""" add integers 1 to 40, 5 times
								41 to 89, 4 times ...
								161 to 200 1 times """
			step = 40
			probabilityMultiplier = 6
			for i in range(1,201):
					for j in range(1, probabilityMultiplier - ((i-1) // step)):
							self.availableProbabilities.append(i)
			return self.availableProbabilities

	def defineObjectCategories(self):

			"""There are 400 inputs to the system, each a stream of action potential spikes. For an object category, the spike rates these 400 inputs are specified.

			Spike rates are between 1 and 60 Hz, but for an object input are between 5 and 60 Hz. The probabilities are:

				0.3 Hz	spike probability in one (one third of a millisecond) timeslot = 0.0001  (0.01%)
				1   Hz	spike probability in one (one third of a millisecond) timeslot = 0.0003  (0.03%)
				5   Hz	spike probability in one (one third of a millisecond) timeslot = 0.0017 	 (0.17%)
				60   Hz	spike probability in one (one third of a millisecond) timeslot = 0.0200  (2%)

			A category is specified by a spike rate for each of the 400 inputs.


			A new category is defined by random selection of a spike probability for each input. Each spike probability from 0.0001 to 0,0200 has a probability of selection. 
					Probabilities from 0.0001 to 0.0040 have 5 chances in 600 of being selected
					Probabilities from 0.0041 to 0.0080 have 4 chances in 600 of being selected
					Probabilities from 0.0081 to 0.0120 have 3 chances in 600 of being selected
					Probabilities from 0.0121 to 0.0160 have 2 chances in 600 of being selected
					Probabilities from 0.0161 to 0.0040 have 1 chance  in 600 of being selected
					This makes the average spike rate ?Hz .

			CategoryOneSpikeProbabilities total  27980/400.0 69.9

			"""
			for i in range(0,30):
					for j in range(0,400):
							self.category[i][j]=random.choice(self.availableProbabilities)

	def getCurrentPhase(self):
			"answer a incrementing number starting at currentPhase and looping from currentPhaseLimit back to 1"
			self.currentPhase += 1
			cp = (self.currentPhase % self.currentPhaseLimit)
			return cp

	def getSpikesInNextTimeslot(self, categoryCollectionNumber):
			"There are 30 CategorySpikeProbabilities the categoryCollectionNumber represents which probablity to use"

			"""SPIKE PROBABILITIES IN category ARE NUMBERS FROM 1 TO 200 currentInputSpikeProbability
			IS A NUMBER BETWEEN 0 AND 200. A RANDOM NUMBER IS SELECTED FROM IntegerCollectionForInputStateGeneration,
			WHICH CONTAINS THE NUMBERS 0 TO 9999. IF currentInputSpikeProbability IS GREATER THAN THE RANDOMLY SELECTED
			NUMBER, A SPIKE IS PRESENT. HENCE IF, FOR EXAMPLE, SPIKE PROBABILITY IN THE CURRENT TIMESLOT IS 200, THE
			CHANCE OF A SPIKE IS 200/10000 = 0.02


			ModulationProbabilityFactor IS A NUMBER THAT DETERMINES HOW PROBABLE A SPIKE WILL BE AT DIFFERENT STAGES
			OF THE MODULATION CYCLE. IT INCREASES THE PROBABILITY AT MODULATION PEAKS AND DECREASES IT AT MODULATION
			MINIMA, BUT SPIKE AVERAGED PROBABILITY OVER THE MODULATION INTERVAL IS THE SAME"""

			self.inputs = []
			for i in range(0, len(self.category[categoryCollectionNumber])):
					cp = self.getCurrentPhase()
					currentInputSpikeProbability = self.category[categoryCollectionNumber][i] * self.modulationProbablityFactor[cp]
					if currentInputSpikeProbability > random.choice(self.integerCollectionForInputStateGeneration):
							self.inputs.append(1)
					else:
							self.inputs.append(0)
			return self.inputs

	def asInputState(self, categoryNumber):
		return InputState(self.category[categoryNumber])


## Evaluation run code
# currentTimeslot = 0
# phaseAtInitialTimeslot = 23
# modulationProbabilityFactor = [0, 0, 0, 0, 0, 0.2, 0.4, 0.8, 1.6, 3.2, 6.4, 12.8, 25.6, 12.8, 6.4, 3.2, 1.6, 0.8, 0.4, 0.2, 0, 0, 0, 0, 0]
# integerCollectionForInputStateGeneration = np.arange(10000)

# evaluator = SpikeEvaluator(currentTimeslot, phaseAtInitialTimeslot, modulationProbabilityFactor, integerCollectionForInputStateGeneration)
# inputSourceCategories = np.empty((30,400))
# for i in range(30):
#         inputSourceCategories[i]= evaluator.getSpikesInNextTimeslot(i)
#         j = 0
#         for value in inputSourceCategories[i]:
#                 if value > 0:
#                          print('Category Collection Number'+str(i))
#                          print(str(j)+': '+str(value)+' ')
#                 j += 1

