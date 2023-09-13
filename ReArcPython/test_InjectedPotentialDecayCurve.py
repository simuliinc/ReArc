import unittest

from PotentialRecord import InjectedPotentialDecayCurve

class TestInjectedPotentialDecayCurve(unittest.TestCase):

	@classmethod
	def setUpClass(cls):
		cls.InjectedPotentialDecayCurve = [32.0, 57.0, 74.0, 86.0, 94.0, 98.0, 100.0, 100.0, 98.0, 95.0, 91.0, 86.0, 81.0, 76.0, 71.0, 66.0, 61.0, 57.0, 52.0, 48.0, 44.0, 40.0, 36.0, 33.0, 30.0, 27.0, 24.0, 22.0, 20.0, 18.0, 16.0, 14.0, 13.0, 11.0, 10.0, 9.0, 8.0, 7.0, 6.0, 6.0, 5.0, 4.0, 4.0, 3.0, 3.0, 3.0, 2.0, 2.0, 2.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    		cls.GlobalInjectedPotentialDecayCurve = InjectedPotentialDecayCurve().value

	def test(self):
	        InjectedPotentialDecayCurve = np.asarray(InjectedPotentialDecayCurve)
	        GlobalInjectedPotentialDecayCurve = np.asarray(GlobalInjectedPotentialDecayCurve)
		self.assert(InjectedPotentialDecayCurve.all() == GlobalInjectedPotentialDecayCurve).all()
 
if __name__ == '__main__':
    unittest.main()





