import unittest
import numpy as np
import random
import PresentOneCategoryInstance


class TestSpikeEvaluator(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.currentTimeslot = 0
        cls.phaseAtInitialTimeslot = 23
        cls.modulationProbabilityFactor = [0, 0, 0, 0, 0, 0.2, 0.4, 0.8, 1.6, 3.2, 6.4, 12.8, 25.6, 12.8, 6.4, 3.2, 1.6, 0.8, 0.4, 0.2, 0, 0, 0, 0, 0]
        cls.integerCollectionForInputStateGeneration = np.arange(10000)
        cls.evaluator = PresentOneCategoryInstance.SpikeEvaluator(cls.currentTimeslot, cls.phaseAtInitialTimeslot, cls.modulationProbabilityFactor, cls.integerCollectionForInputStateGeneration)

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
