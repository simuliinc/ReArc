#Potential Record is a set of values that represent the current potential for
#a dendrite or branch to fire.
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
