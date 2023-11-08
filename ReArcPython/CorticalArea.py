# A CorticalArea is a collection of Cortical Columns that represent a sensory area 

from CorticalColumn import *

class CorticalArea:
	def __init__(self):
		self.columns = [] 
		self.currentOutputs = []

	def addColumnQty(self, numberOfColumns):
		for i in range(numberOfColumns):
			self.columns.append(CorticalColumn())

	def addPyramidalToLayerQtyThreshold(self, corticalLayer, numberOfPyramidalsToAdd, \
										threshold = CorticalBasalDendriteThreshold, inputs={}, source=None):
		for i in range(numberOfPyramidalsToAdd):
			for i, column in enumerate(self.columns):
				column.addPyramidalToLayer(corticalLayer, threshold, inputs[i], source)

	def addInterneuronToLayerWithThreshold(self, corticalLayer, numberOfInterneuronsToAdd, threshold):
		for i in range(numberOfInterneuronsToAdd):
			for column in self.columns:
				column.addInterneuronToLayerWithThreshold(corticalLayer, threshold, len(self.columns))

	def presentInputsInOneTimeslotToCorticalArea(self, excitatoryInputs, recordingManagementInputs, multipleSource = False):
		# Sensory action potentials from one timeslot are presented to each column in turn, generating an 
		# OrderedCollection containing output action potentials from each column. These OrderedCollections 
		# are collected into the OrderedCollection columnOutputs which is returned by the method.

		# Hence in structure, columnOutputs contains 40 OrderedCollections, one for each column. Each of these 
		# 40 OrderedCollections contains 3 OrderedCollections, one for each layer. These 3 OrderedCollections 
		# contain an element for each pyramidal neuron, indicating whether (1) or not (0) it generated an action 
		# potential in the timeslot.
		
		self.currentOutputs = []	
		for column in self.columns:
			output = column.presentInputs(excitatoryInputs, recordingManagementInputs, False)
			self.currentOutputs.append(output)
			# Why this is possible? PyramidalActivy is added to the cortialLayer instead of collected in a layer collection 
			# on the column. It is now possible to get that activy from presentInputs above directly from the CorticalLayer 
			# and process it (RJT)
			column.updateInterneuronActivityForLayer(1)
			column.updateInterneuronActivityForLayer(2)
			# We actually have 3 layers currently implemented but this layer is not called in Smalltalk. (RJT)
			# column.updateInterneuronActivityForLayer(3)

		return self.currentOutputs
		
	def sleep(self):
		# sleep is not currently implemented on column so this actually does nothing. There are notes on 
		# CorticalColumn.py CorticalColumn >> sleep for what an implementation would look like from Andrew (RJT)
		for column in self.columns:
			column.sleep()

	
