import unittest

from Brain import *
from PresentOneCategoryInstance import *

class TestBrain(unittest.TestCase):

	@classmethod
	def setUpClass(cls):
		# These favoredInputs come directly from Smalltalk Global variable 
		favoredInputs = [[66, 237, 278, 214, 178, 41, 10, 350, 136, 141, 241, 316, 79, 19, 164, 63, 124, 174, 96, 200, 67, 155, 272, 38, 53], 
				   	[317, 40, 209, 81, 295, 24, 291, 10, 175, 299, 297, 263, 373, 348, 176, 178, 198, 37, 397, 276, 222, 164, 141, 153, 382],  
					[330, 237, 278, 1, 295, 367, 331, 133, 231, 145, 275, 312, 50, 124, 197, 22, 267, 328, 114, 323, 355, 194, 69, 73, 91], 
					[66, 281, 283, 166, 121, 24, 314, 250, 359, 57, 94, 74, 98, 369, 62, 345, 247, 204, 7, 159, 127, 208, 297, 377, 31], 
					[319, 314, 163, 291, 298, 133, 390, 327, 90, 275, 42, 368, 241, 299, 324, 89, 192, 141, 183, 349, 181, 85, 190, 301, 51],  
					[185, 17, 235, 363, 254, 10, 196, 231, 252, 348, 154, 176, 61, 353, 198, 98, 284, 305, 223, 52, 55, 85, 202, 124, 190], 
					[335, 347, 278, 363, 380, 235, 369, 364, 184, 11, 312, 298, 220, 145, 7, 323, 307, 261, 19, 197, 46, 164, 35, 151, 174], 
					[317, 298, 184, 364, 136, 173, 327, 305, 94, 399, 80, 183, 325, 176, 141, 394, 45, 137, 52, 96, 2, 397, 104, 189, 97], 
					[335, 283, 278, 41, 247, 336, 149, 1, 325, 192, 256, 206, 136, 297, 222, 323, 384, 89, 397, 231, 109, 253, 88, 60, 301], 
					[12, 166, 185, 236, 37, 314, 110, 298, 223, 348, 296, 291, 254, 373, 261, 280, 231, 286, 275, 345, 198, 305, 115, 19, 97],  
					[335, 24, 331, 209, 32, 296, 173, 133, 329, 284, 74, 354, 254, 168, 332, 87, 141, 384, 305, 98, 145, 23, 50, 69, 183], 
					[236, 347, 144, 367, 17, 314, 57, 280, 24, 291, 192, 263, 149, 286, 98, 354, 262, 332, 271, 321, 349, 216, 200, 376, 370], 
					[66, 281, 288, 331, 41, 106, 348, 1, 251, 298, 11, 57, 94, 345, 297, 261, 223, 369, 14, 394, 323, 2, 194, 355, 274], 
					[203, 237, 280, 57, 168, 211, 267, 44, 316, 231, 394, 35, 349, 202, 271, 301, 72, 384, 194, 54, 161, 73, 399, 233, 260], 
					[283, 166, 41, 363, 40, 251, 280, 304, 80, 154, 397, 62, 126, 394, 349, 46, 71, 68, 333, 392, 272, 27, 398, 28, 134]]
		cls.brain = Brain(2) 
		cls.brain.configureFirstArea(favoredInputs)
		cls.evaluator = SpikeEvaluator()
	def testVisualCortexSize(self):
		assert len(TestBrain.brain.visualCortex) == 2

	def testCategories(self):
		assert len(TestBrain.evaluator.asInputState(1).category) == 400

	def testInputs(self):
		inputs = TestBrain.evaluator.asInputState(1).getSpikesInNextTimeslot(TestBrain.evaluator.asInputState(2).category,TestBrain.evaluator.asInputState(3).category)
		# the following is a collection of 15 collections of 3 elements with the first 2 having len of 40 and the 3rd len of 4
		inputResult = TestBrain.brain.presentInputsInOneTimeslotToArea1WithBlackBoxHippocampus(inputs, 1, False)
		assert (len(inputResult) == 15) & (len(inputResult[0]) == 3) & (len(inputResult[0][0]) == 10) & (len(inputResult[0][2]) == 1), "inputResult: len: "+str(len(inputResult))+" [0]: "+str(len(inputResult[0]))+" [0][0]: "+str(len(inputResult[0][0]))+" [0][2]: "+str(len(inputResult[0][2]))
		

if __name__ == '__main__':
    unittest.main()