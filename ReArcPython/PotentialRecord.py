#Potential Record is a set of values that represent the current potential for
#a dendrite or branch to fire.
from math import exp
import random
import numpy as np

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
        # optimize with NP
        i_values = np.arange(1, 61)
        self.value = (a * i_values * np.exp(b * i_values)).astype(int)
        #for i in range(1,61):
        #    self.value.append(int(a*i* exp(b*i)))
        # convert to np array for vector evaluations
        self.value = np.array(self.value)

GlobalInjectedPotentialDecayCurve=np.array(InjectedPotentialDecayCurve().value)

class PotentialRecord:
	def __init__(self):
		self.record = np.zeros(48)

	def shift(self):
		# Shift the array left and add a new value (0) at the end
		self.record = np.roll(self.record, -1)  # Shift elements to the left
		self.record[-1] = 0  # Set the last element to 0

	def advanceExcitatoryPotential(self):
		# add potential based on GlobalInjectedPotentialDecayCurve
		# should be called for each branch that injects potential
		num_elements = min(len(self.record), len(GlobalInjectedPotentialDecayCurve))
		self.record[:num_elements] += GlobalInjectedPotentialDecayCurve[:num_elements]
		# i = 0
		# for curve in GlobalInjectedPotentialDecayCurve:
		#	try:
		#		self.record[i] += curve
		#		i += 1
		#	except IndexError:
		#		return 
	
	def adjustPotentialByWeight(self, weight):
		# INCREMENT ALL THE FIELDS OF potentialRecord FOR THE BRANCH
		# (multiply the weight by the Decay Curve and add it to the record RJT)

		#i = 0
		#for curve in GlobalInjectedPotentialDecayCurve:
		#	try:
		#		self.record[i] += curve * weight
		#		i += 1
		#	except IndexError:
		#		return 
		# Use NumPy's vectorized operation for better performance
		num_elements = min(len(self.record), len(GlobalInjectedPotentialDecayCurve))
		self.record[:num_elements] += GlobalInjectedPotentialDecayCurve[:num_elements] * weight
			
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
