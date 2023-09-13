# Python Code

# Code explanation and depiction

### Globals.py:

Globals.py is for global variables 

``` py
CorticalConditionDefiningInputWeight = 1.7
BranchContributionsWithin200msecForPermanentWeightChange = 3
LayerOneInterneuronOutputSynapticStrengths = -5
LayerTwoInterneuronOutputSynapticStrengths = 0
CorticalBasalDendriteThreshold = 985
```

### Dendrites.py:


An ApicalDendrite is the output of a pyramidal cell. The Dendrite acts by modulating
the excitatory and inhibitory signals.

``` py
from Globals import *
from PotentialRecord import *
import itertools

class ApicalDendrite:
	def __init__(self):
		self.proximalInputs = []
		self.proximalInputWeights = []
		self.distalBranches = []
		self.potentialRecord = PotentialRecord()
		self.threshold = None  #CorticalApicalDendriteThreshold
		self.firingStatus = False

	def changeBranchThresholds(self, newThreshold):
		for branch in self.distalBranches:
			branch.changeBranchThreshold(newThreshold)

	def changeBranchThreshold(self, newThreshold):
		self.threshold = newThreshold

	def addNewProximalInput(self, connection):
		self.proximalInputs.append(connection)

	def addNewProximalInputWeight(self, weight):
		self.proximalInputWeights.append(weight)

	def presentInputs(self, excitatoryInputs, modulatoryInputs):
        #MODULATORY INPUTS CAN BE EXCITATORY OR INHIBITORY, DEPENDING ON
        #THE PROXIMAL INPUT WEIGHTS WITHIN THE TARGET APICAL DENDRITE INSTANCE

        #FIRST STEP IS TO SHIFT potentialRecord ALONG ONE TIMESLOT
		self.potentialRecord.shift()
        
		currentPotential = self.potentialRecord[0]
		firingProbability = 1000 * ((currentPotential - self.threshold)/self.threshold)
		emptyBranches = []
		currentLargest = None
        
        #GO THROUGH EACH BRANCH AND DETERMINE WHETHER IT INJECTS POTENTIAL
        #INTO THE apicalDendrite. IF SO, INCREASE THE potentialRecord ACCORDINGLY"

		for branch in self.distalBranches:
			if branch.presentSingleSourceExcitatoryInputsToBranch(excitatoryInputs):
				self.potentialRecord.advanceExcitatoryPotential()
        
		# ADD POTENTIAL INJECTED BY MODULATORY PROXIMAL INPUTS TO potentialRecord. 
		# NOTE: USING SAME POTENTIAL DECAY CURVE AS FOR APICAL DENDRITE BRANCHES"
		for proximalnput, proximalWeight in zip(self.proximalInputs, self.proximalInputWeights):
			if modulatoryInputs[proximalnput] == 1:
				self.potentialRecord.adjustPotentialByWeight(proximalWeight)
				
		# SET firingProbability AT 0% IF POTENTIAL IN CURRENT TIMESLOT IS LESS 
		# THAN OR EQUAL TO THRESHOLD, AT 100% IF POTENTIAL IS 10% OR MORE OVER 
		# THRESHOLD. SCALED BETWEEN 10% AND 100% PROBABILITIES WHEN POTENTIAL 
		# IS 1% TO 10% OVER THRESHOLD" 
		self.firingStatus = self.potentialRecord.fireforThreshold(self.threshold)
		if self.firingStatus:
			# IF apicalDendrite FIRES, SET potentialRecord TO ZERO
			self.potentialRecord.reset()

		# IF ANY BRANCH HAS <3 INPUTS, REMOVE IT"
		self.distalBranches = list(itertools.filterfalse(lambda x: len(x.excitatoryInputs) < 3, self.distalBranches))

		return self.firingStatus
        
class BasilDendrite(ApicalDendrite):
	def __init__(self):
		super().__init__()
		self.threshold = CorticalBasalDendriteThreshold
```

### DendriteBranch.py

A Dendrite Branch is added by a PyramidalNeuron, Adds potentials inserted by all action potentials in current timeslot to branch, and determines if a potential will be inserted deeper into the dendrite

```py
from Globals import *
from PotentialRecord import *

class DendriteBranch:

	def __init__(self, threshold):
		self.conditionPermanence = False
		self.excitatoryInputs = []
		self.inhibitoryInputs = []
		self.inhibitoryInputWeights = []
		self.recentActivityOfInhibitoryInputs = []
		self.conditionRecordingManagementInputs = []
		self.conditionRecordingManagementInputWeights = []
		self.recentActivityOfConditionRecordingManagementInputs = []
		self.timeSinceLastActivityOfBranch = 100
		self.timeSinceBackpropagatedSomaActionPotential = 100
		self.potentialRecord = PotentialRecord()
		self.threshold = threshold
		self.firingStatus = False
		self.branchFirings = 0

    
	def presentSingleSourceExcitatoryInputsToBranch(self, inputs):
        #FIRST STEP IS TO SHIFT potentialRecord ALONG ONE TIMESLOT
		self.potentialRecord.shift()

        #NEXT, INCREASE timeSinceLastActivityOfBranch BY ONE
		timeSinceLastActivityOfBranch += 1

		# NEXT, INCREASE THE NUMBER OF TIMESLOTS SINCE CHANGE 
		# BY ONE FOR EVERY CHANGE TO EVERY INPUT.  THE CHANGE 
		# RECORD FOR INPUTS IS RECORDED IN recentWeightChangeHistory. 
		# EACH ELEMENT IN recentWeightChangeHistory IS THE RECORD FOR 
		# ONE INPUT. THE RECORD IS AN OrderedCollection MADE UP TO 
		# TWO OrderedCollection. THE FIRST OF THESE TWO OrderedCollections 
		# CONTAINS THE NUMBER OF TIMESLOTS SINCE THE CHANGE OCCURRED, 
		# THE SECOND CONTAINS THE MAGNITUDE OF THE CHANGE.
		
		for input in self.excitatoryInputs:
			input.advanceTime()

			# NEXT, IF MORE THAN 600 TIMESLOTS (= 200 MILLISECONDS) HAVE ELAPSED, 
			# REVERSE THE CHANGE AND DELETE THE RECORD IN recentWeightChangeHistory"
			input.handleMaxTimeSlots()

			# NEXT, CHECK IF THERE ARE FIVE (OR MORE, BUT THAT SHOULD NOT OCCUR) INCREASES 
			# FOR ANY INPUT, AND IF SO, MAKE THE INCREASES PERMANENT BY ELIMINATING THE 
			# ENTRIES IN recentWeightChangeHistory
			input.makeHighContributionPermanent()

			# NEXT, INCREASE recentActivityOfExcitatoryInputs BY ONE FOR EACH INPUT"
			self.recentActivity += 1

			# GO THROUGH THE excitatoryInputs OF THE BRANCH, AND CHECK IF THERE IS 
			# AN ACTION POTENTIAL FOR THAT INPUT. IF SO, SET TIME SINCE INPUT FOR 
			# THAT INPUT TO ZERO, AND INCREMENT ALL THE FIELDS OF potentialRecord 
			# FOR THE BRANCH"	See trace https://github.com/simuliinc/ReArc/issues/16

			if (inputs[input.getInput()]) == 1:
				input.recentActivity = 0
				self.potentialRecord.adjustPotentialByWeight(input.weight)

			# SET firingProbability AT 0% IF POTENTIAL IN CURRENT TIMESLOT IS LESS 
			# THAN OR EQUAL TO THRESHOLD, AT 100% IF POTENTIAL IS 10% OR MORE OVER 
			# THRESHOLD. SCALED BETWEEN 10% AND 100% PROBABILITIES WHEN POTENTIAL 
			# IS 1% TO 10% OVER THRESHOLD see PotentialRecord.py

			# IntegerCollection CONTAINS THE NUMBERS 0 TO 99. A NUMBER IS SELECTED 
			# AT RANDOM FROM IntegerCollection AND IF IT IS LESS THAN firingProbability 
			# THE BRANCH IF FIRING. THIS ALGORITHM IMPLEMENTS THE % PROBABILITY 
			# DETERMINED BY firingProbability

			if self.potentialRecord.fireforThreshold(self.threshold):
				# IF BRANCH FIRES, SET potentialRecord AND timeSinceLastActivityOfBranch TO ZERO
				self.firingStatus = True
				self.potentialRecord.reset()
				self.timeSinceLastActivityOfBranch = 0
				self.branchFirings += 1

		return self.firingStatus

             
class ExcitatoryInput:
	def __init__(self, input):
		self.input = input
		self.weight = CorticalConditionDefiningInputWeight
		self.recentActivity = 0
		self.connectionTime = 0
		self.changeMagnitude = 0
		self.branchFiringSinceWeightChange = 0
		self.permanentConnection = False
		self.history = [{'connectionTime':0, 'changeMagnitude':0}]

	def advanceTime(self):
		self.connectionTime += 1
		for item in self.history:
			item["connectionTime"] += 1

	def handleMaxTimeSlots(self):
		# IF MORE THAN 600 TIMESLOTS (= 200 MILLISECONDS) HAVE ELAPSED, 
		# REVERSE THE CHANGE AND DELETE THE RECORD IN recentWeightChangeHistory
		if self.history[0]['connectionTime'] > 600:
			self.weight /= self.history[0]['changeMagnitude']
			del self.history[0]

	def makeHighContributionPermanent(self):
		# NEXT, CHECK IF THERE ARE FIVE (Currently set to 3 RJT)(OR MORE, BUT THAT SHOULD NOT OCCUR) INCREASES 
		# FOR ANY INPUT, AND IF SO, MAKE THE INCREASES PERMANENT BY ELIMINATING THE 
		# ENTRIES IN recentWeightChangeHistory
		# added permanentConnection variable RJT

		if len(self.history) >= BranchContributionsWithin200msecForPermanentWeightChange:
			self.permanentConnection = True
			for history in self.history:
				del history

	def getInput(self):
		return self.input
```

### TestDendrites.py

```py
import unittest

from Dendrites import *

class TestDendrites(unittest.TestCase):

	@classmethod
	def setUpClass(cls):
		pass

	def test(self):
		pass
 
if __name__ == '__main__':
    unittest.main()

```

### PotentialRecord.py

Potential Record is a set of values that represent the current potential for a dendrite or branch to fire.

```py
from math import exp
import random

class InjectedPotentialDecayCurve(object):
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(InjectedPotentialDecayCurve, cls).__new__(cls)
        return cls.instance

    def __delete__(self):
        del self

    def __init__(self):
        a = 37.63
        b = -0.1375
        self.value = []
        for i in range(1,61):
            self.value.append(int(a*i* exp(b*i)))

GlobalInjectedPotentialDecayCurve=InjectedPotentialDecayCurve().value

class PotentialRecord:
	def __init__(self):
		self.record = [0]*48

	def shift(self):
		self.record.append(0)
		del self.record[0]

	def advanceExcitatoryPotential(self):
        # add potential based on GlobalInjectedPotentialDecayCurve
        # should be called for each branch that injects potential
		i = 0
		for curve in GlobalInjectedPotentialDecayCurve:
			try:
				self.record[i] += curve
				i += 1
			except IndexError:
				return 
	
	def adjustPotentialByWeight(self, weight):
		# INCREMENT ALL THE FIELDS OF potentialRecord FOR THE BRANCH
		# (multiply the weight by the Decay Curve and add it to the record RJT)

		i = 0
		for curve in GlobalInjectedPotentialDecayCurve:
			try:
				self.record[i] += curve * weight
				i += 1
			except IndexError:
				return 
			
	def firingPotentialForThreshold(self, aThreshold):
		# SET firingProbability AT 0% IF POTENTIAL IN CURRENT TIMESLOT IS LESS 
		# THAN OR EQUAL TO THRESHOLD, AT 100% IF POTENTIAL IS 10% OR MORE OVER 
		# THRESHOLD. SCALED BETWEEN 10% AND 100% PROBABILITIES WHEN POTENTIAL 
		# IS 1% TO 10% OVER THRESHOLD
		
		return min(max((1000 * ((self.record[0] - aThreshold) / aThreshold)),0),100) 

	def fireforThreshold(self, aThreshold):
		return self.firingPotentialForThreshold(aThreshold) > random.choice(range(0,100))

	def reset(self):
		self.__init__()

```

### PresentOneCategoryInstance.py

```py
import numpy as np
import random
#----------------------------


class SpikeEvaluator():

        def __init__(self, currentTimeSlot, phaseAtInitialTimeslot, modulationProbablityFactor, integerCollectionForInputStateGeneration):
                self.currentTimeSlot = currentTimeSlot
                self.phaseAtInitialTimeslot = phaseAtInitialTimeslot
                self.modulationProbablityFactor = modulationProbablityFactor
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




## Evaluation run code
currentTimeslot = 0
phaseAtInitialTimeslot = 23
modulationProbabilityFactor = [0, 0, 0, 0, 0, 0.2, 0.4, 0.8, 1.6, 3.2, 6.4, 12.8, 25.6, 12.8, 6.4, 3.2, 1.6, 0.8, 0.4, 0.2, 0, 0, 0, 0, 0]
integerCollectionForInputStateGeneration = np.arange(10000)

evaluator = SpikeEvaluator(currentTimeslot, phaseAtInitialTimeslot, modulationProbabilityFactor, integerCollectionForInputStateGeneration)
inputSourceCategories = np.empty((30,400))
for i in range(30):
        inputSourceCategories[i]= evaluator.getSpikesInNextTimeslot(i)
        j = 0
        for value in inputSourceCategories[i]:
                if value > 0:
                         print('Category Collection Number'+str(i))
                         print(str(j)+': '+str(value)+' ')
                j += 1
```

### test_PresentOneCategoryInstance.py

```py
import unittest
import numpy as np
import random
import testcode


class TestSpikeEvaluator(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.currentTimeslot = 0
        cls.phaseAtInitialTimeslot = 23
        cls.modulationProbabilityFactor = [0, 0, 0, 0, 0, 0.2, 0.4, 0.8, 1.6, 3.2, 6.4, 12.8, 25.6, 12.8, 6.4, 3.2, 1.6, 0.8, 0.4, 0.2, 0, 0, 0, 0, 0]
        cls.integerCollectionForInputStateGeneration = np.arange(10000)
        cls.evaluator = testcode.SpikeEvaluator(cls.currentTimeslot, cls.phaseAtInitialTimeslot, cls.modulationProbabilityFactor, cls.integerCollectionForInputStateGeneration)

    def test_getCurrentPhase(self):
        self.assertEqual(TestSpikeEvaluator.evaluator.getCurrentPhase(), TestSpikeEvaluator.phaseAtInitialTimeslot)

    def test_currentPhaseLimit(self):
        phaseMax = 0
        for i in range(len(TestSpikeEvaluator.modulationProbabilityFactor)*2):
               phaseMax = max(phaseMax, TestSpikeEvaluator.evaluator.getCurrentPhase())
        self.assertTrue(phaseMax, len(TestSpikeEvaluator.modulationProbabilityFactor))

    def test_defineAvailableProbabilities(self):
        availableProb = TestSpikeEvaluator.evaluator.defineAvailableProbabilities()
        self.assertTrue(availableProb[0],1)
        self.assertTrue(availableProb[4],1)
        self.assertTrue(availableProb[(40*5)-1],41)
        self.assertTrue(availableProb[(40*5)-1+4],41)
        self.assertTrue(availableProb[(40*5)-1+5],42)
        self.assertTrue(availableProb[(40*5)-1+9],42)
        self.assertTrue(availableProb[(40*5)-1+10],43)
        self.assertTrue(availableProb[-1],200)

if __name__ == '__main__':
    unittest.main()
```