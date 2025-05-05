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
		if corticalLayer == 3:
			print("corticalLayer: ", corticalLayer)
		for i in range(numberOfPyramidalsToAdd):
			for j, column in enumerate(self.columns):
				print("Threshold: ", threshold)
				column.addPyramidalToLayer(corticalLayer, threshold, inputs[j], source)

	def addInterneuronToLayerWithThreshold(self, corticalLayer, numberOfInterneuronsToAdd, threshold):
		for i in range(numberOfInterneuronsToAdd):
			for column in self.columns:
				column.addInterneuronToLayerWithThreshold(corticalLayer, threshold, len(self.columns))
				column.getLayer(corticalLayer).interneuronsActivity.append(0)

	def presentInputsInOneTimeslotToCorticalArea(self, excitatoryInputs, recordingManagementInputs, multipleSource = False):
		# First: present inputs to each column and collect outputs

		# with open("brain.txt", "a") as log_file:
		# 	log_file.write(f"Excitatory Inputs: {excitatoryInputs}\n")
		# 	log_file.write(f"Recording Management Inputs: {recordingManagementInputs}\n")
		# 	log_file.write(f"Multiple Source: {multipleSource}\n")
		# print("recordingManagementInputs: ", recordingManagementInputs)

		self.currentOutputs = []    
		for i, column in enumerate(self.columns):
			output = column.presentInputs(excitatoryInputs, recordingManagementInputs[i], multipleSource)
			self.currentOutputs.append(output)

		# Second: collect layer one outputs from all columns
		layerOneOutputs = []
		# print("self.currentOutputs: ", self.cur/rentOutputs)
		# print("self.columns: ", self.columns)
		# print("self.columns[0].layerOneInterneurons: ", self.columns[0].getLayer(1).interneuronsActivity)
		for columnOutput in self.currentOutputs:
			layerOneOutputs.append(columnOutput[0])


		# Third: update each column's layer one interneurons with outputs from all columns
		for column in self.columns:
			column.updateInterneuronActivityForLayerWithCurrentOutputs(1, layerOneOutputs)

		# Fourth: collect layer two outputs from all columns
		layerTwoOutputs = []
		for columnOutput in self.currentOutputs:
			layerTwoOutputs.append(columnOutput[1])

		# Fifth: update each column's layer two interneurons with outputs from all columns
		for column in self.columns:
			column.updateInterneuronActivityForLayerWithCurrentOutputs(2, layerTwoOutputs)

		return self.currentOutputs
		
	def sleep(self):
		# sleep is not currently implemented on column so this actually does nothing. There are notes on 
		# CorticalColumn.py CorticalColumn >> sleep for what an implementation would look like from Andrew (RJT)
		for column in self.columns:
			column.sleep()

	
