# a Cortical Column is an arrangement of Neurons in a cortical area.  Typically neurons that are arranged in a column 
# share the same receptive field and neurons that fire together represent different properties off the same input event. (RJT)

from PyramidalNeuron import *
import random

class CorticalColumn:
	def __init__(self):
		self.layers = [CorticalLayer(1), CorticalLayer(2), CorticalLayer(3)]

	def getLayer(self, index):
		# Answer the layer with the coorespondiing index
		for layer in self.layers:
			if layer.index == index:
				return layer
		return None
	
	def addPyramidalToLayer(self, corticalLayer, threshold = CorticalBasalDendriteThreshold, inputs={}, \
						 source = None):
		config = self.configForLayer(corticalLayer, threshold, inputs, source)
		# this is as far down as the corticalLayer information is pushed. From here down everything is specific 
		# to the layer presened here.  The nurons, dendrites, and branches do not have a concept of cortical 
		# layer (RJT)
		assert threshold != None
		neuron = PyramidalNeuron(config['numOfBasilDendriteBranches'], config['dendriteThreshold'], \
						   config['numOfInputs'], config['inputs'], config['source'], config['managementInputs'], config['excitatoryInputWeight'])
		
		if corticalLayer == 3: # basal dendrite threshold is set to the global threshold
			neuron.basalDendrite.changeThreshold(CorticalLayerThreeBasalDendriteThreshold)

		self.getLayer(corticalLayer).pyramidalNeurons.append(neuron)
		for i in range(config['numOfProximalInputs']):
			# i is zero based so connections start at 0 (RJT)
			neuron.basalDendrite.addInputAndWeightForSource(i,config['proximalInputWeight'])

	def addInterneuronToLayerWithThreshold(self, corticalLayer, threshold, columnNumber): 
		# Adds and initializes an interneuron to layer of a column instance  (said layer two which was incorrect RJT)

		# sources is really number of columns but the initialize is no longer necessary in our Python translation (RJT)

		# EACH INTERNEURON HAS NumberOfInputsToLayerOneInterneuronsFromEachOtherColumn INPUTS FROM RANDOMLY SELECTED 
		# PYRAMIDALS IN EACH COLUMN EXCEPT ITS OWN AND NumberOfInputsToLayerOneInterneuronsFromOwnColumn INPUTS FROM 
		# RANDOMLY SELECTED PYRAMIDALS IN ITS OWN COLUMN

		config = self.configForLayer(corticalLayer, threshold, list(range(PyramidalsPerColumnLayerOne)))
		# print("NumberOfColumns: ", NumberOfColumns)
		neuron = InhibitoryInterneuron(threshold, NumberOfColumns=NumberOfColumns)
		self.getLayer(corticalLayer).interneurons.append(neuron)

		for column in range(NumberOfColumns):
			if column == columnNumber:
				for connection in range(config['interNuronConnectoiosToOwnColumn']):
					neuron.addInputAndWeightForSource(random.choice(config['inputs']), \
										LayerOneInterneuronInputSynapticStrengths, column)
			else:
				for connection in range(config['interNuronConnectionsFromEach']):
					neuron.addInputAndWeightForSource(random.choice(config['inputs']), \
									    LayerOneInterneuronInputSynapticStrengths, column)

	def changeBranchThresholdsForLayer(self, corticalLayer, newBranchThreshold):
		for neuron in self.getLayer(corticalLayer).pyramidalNeurons:
			neuron.changeBasilDendriteThresholds(newBranchThreshold)

	def reduceSynapticWeights(self, proportion):
		# This method reduces all the synaptic weights on all the branches of the 
		# apical dendrites of all the neurons in all layers"
		for layer in self.layers:
			layer.reduceSynapticWeights(self, proportion)
	
	def sleep(self):
		#this methdod does nothing, the notes below may be an indication of what was intended
	
		# ADD NEW BRANCHES TO layerOne PYRAMIDAL NEURONS

		# ADD NEW BRANCHES TO layerTwo PYRAMIDAL NEURONS

		# ADD NEW BRANCHES TO layerThree PYRAMIDAL NEURONS
		pass  # no op (do nohing)



	def configureB(self, layerOneBiasedInputPopulation):
		# this method apears to not be used in smalltalk.  layerOneBiasedInputPopulation is not defined anywhere (RJT)
		assert False, "method not called on orginal Smalltalk. the input is not defined anywhere, if you want to use this remove this assert"
		inputs = layerOneBiasedInputPopulation
		for corticalLayer in range(1,4):
			# the first layer has 20 banches and 15 values from layerOneBiaasedInputPopulation
			# the next two layers have 10 branches and 10 inputs whcih are random numbers from 1 to 50 inclusive
			branchesAndInputs = [{"branches":20,"inputs":15},{"branches":10,"inputs":10},{"brnaches":10,"inputs":10}]
			for neuron in self.getLayer(corticalLayer).pyramidalNeurons:
				for branchNumber in range(branchesAndInputs[corticalLayer-1][branches]):
					branch = neuron.addDendriteBranch()
					for inputNumber in range(branchesAndInputs[cortialLayer -1][inputs]):
						branch.addExcitatoryInput(random.choice(inputs))
					# only cortical layer1 uses the layerOneBiasedInputPopulation, Layer 2 and 3 use random numbers from 1 to 50 inclusive (RJT)
					inputs = range(1,51)

	def presentInputs(self, conditionDefiningInputs, managementInputs, multipleSource=False):
		# Reset all activity lists
		for layer_num in range(1, 4):
			self.getLayer(layer_num).pyramidalActivity = []
		# Process each layer separately, similar to Smalltalk
		layer1_outputs = []
		layer1 = self.getLayer(1)
		for neuron in layer1.pyramidalNeurons:
			interneuron_activity = layer1.interneuronsActivity.copy() if layer1.interneuronsActivity else []
			# print("conditionDefiningInputs: ", conditionDefiningInputs)
			# print("interneuron_activity: ", interneuron_activity)
			# print("multipleSource: ", multipleSource)
			output = neuron.presentInputs(conditionDefiningInputs, interneuron_activity, multipleSource)
			layer1_outputs.append(output)
		layer1.pyramidalActivity = layer1_outputs
		
		layer2_outputs = []
		layer2 = self.getLayer(2)
		for neuron in layer2.pyramidalNeurons:
			interneuron_activity = layer2.interneuronsActivity.copy() if layer2.interneuronsActivity else []
			output = neuron.presentInputs(layer1_outputs, interneuron_activity)
			layer2_outputs.append(output)
		layer2.pyramidalActivity = layer2_outputs

		
		layer3_outputs = []
		layer3 = self.getLayer(3)
		for neuron in layer3.pyramidalNeurons:
			output = neuron.presentInputs(layer2_outputs, [], False, managementInputs)
			layer3_outputs.append(output)
		layer3.pyramidalActivity = layer3_outputs

		# Return structure matching Smalltalk
		column_activity = [layer1_outputs, layer2_outputs, layer3_outputs]
		return column_activity

	def updateInterneuronActivityForLayer(self, corticalLayerNumber):
		corticalLayer = self.getLayer(corticalLayerNumber)
		for interNeuron, pryamidalActivity in zip(corticalLayer.interneurons, corticalLayer.pyramidalActivity):
			corticalLayer.interneuronsActivity.append(interNeuron.presentInputsFromMultipleSources(pryamidalActivity,[], True, []))
	
	def updateInterneuronActivityForLayerWithCurrentOutputs(self, corticalLayerNumber, currentOutputs):
		corticalLayer = self.getLayer(corticalLayerNumber)
		corticalLayer.interneuronsActivity = []  # Reset activity list
		# print("currentOutputs: ", currentOutputs)
		for i, interneuron in enumerate(corticalLayer.interneurons):
			# Following the Smalltalk implementation where each interneuron processes inputs from multiple sources
			activity = interneuron.presentInputsFromMultipleSources(currentOutputs, [], True, [])  # True for multipleSource
			corticalLayer.interneuronsActivity.append(activity)

	def updateInterneuronActivityInternalConnectivityOnly(self, corticalLayerNumber):
		corticalLayer = self.getLayer(corticalLayerNumber)
		for interNeuron, pryamidalActivity in zip(corticalLayer.interneurons, corticalLayer.pyramidalActivity):
			corticalLayer.interneuronsActivity.append(interNeuron.presentInputsFromMultipleSources(pryamidalActivity,[], False, []))
	
	def configForLayer(self, corticalLayer, threshold, inputs, source=None):
		if corticalLayer == 1:
			return self.layerOnePyramidalConfiguration(threshold, inputs, source)
		elif corticalLayer == 2:
			return self.layerTwoPyramidalConfiguration(threshold)
		elif corticalLayer == 3:
			return self.layerThreePyramidalConfiguration(threshold)
		else:
			assert False, "CortiicalColumn.py CorticalLayer >> configForLayer corticalLayer: "+ corticalLayer+" not supported"

	#the following configurations come from Smalltalk Brain >> configureFirstArea
	def layerOnePyramidalConfiguration(self, threshold, inputs, source):
		pyramidalConfig = {}
		pyramidalConfig['numOfInputs'] = NumberOfConditionDefiningInputsPerCorticalLayerOneBranch
		pyramidalConfig['numOfBasilDendriteBranches'] = NumberOfBranchesPerLayerOnePyramidal
		pyramidalConfig['numOfProximalInputs'] = NumberOfLayerOneInterneurons
		pyramidalConfig['proximalInputWeight'] = LayerOneInterneuronOutputSynapticStrengths
		pyramidalConfig['dendriteThreshold'] = threshold 
		pyramidalConfig['inputs'] = inputs 
		pyramidalConfig['source'] = source
		pyramidalConfig['managementInputs'] = 0
		pyramidalConfig['interNuronConnectionsFromEach'] = NumberOfInputsToLayerOneInterneuronsFromEachOtherColumn
		pyramidalConfig['interNuronConnectoiosToOwnColumn'] = NumberOfInputsToLayerOneInterneuronsFromOwnColumn
		pyramidalConfig['excitatoryInputWeight'] = None

		return pyramidalConfig

	def layerTwoPyramidalConfiguration(self, threshold, inputs = []):
		pyramidalConfig = {}
		pyramidalConfig['numOfInputs'] = NumberOfConditionDefiningInputsPerCorticalLayerTwoBranch
		pyramidalConfig['numOfBasilDendriteBranches'] = NumberOfBranchesPerLayerTwoPyramidal
		pyramidalConfig['numOfProximalInputs'] = NumberOfLayerTwoInterneurons
		pyramidalConfig['proximalInputWeight'] = LayerTwoInterneuronOutputSynapticStrengths
		pyramidalConfig['dendriteThreshold'] = threshold
		# should we adapt to the starting at 1 in smalltalk or adopt to the starting at 0 in Python
		# lets adpot 0 index start from Python (RJT)
		pyramidalConfig['inputs'] = list(range(PyramidalsPerColumnLayerOne))
		pyramidalConfig['source'] = None
		pyramidalConfig['managementInputs'] = 0
		pyramidalConfig['interNuronConnectionsFromEach'] = NumberOfInputsToLayerTwoInterneuronsFromEachOtherColumn
		pyramidalConfig['interNuronConnectoiosToOwnColumn'] = NumberOfInputsToLayerTwoInterneuronsFromOwnColumn
		pyramidalConfig['excitatoryInputWeight'] = None

		return pyramidalConfig
		 
	def layerThreePyramidalConfiguration(self, threshold, inputs=[]):
		pyramidalConfig = {}
		pyramidalConfig['numOfInputs'] = NumberOfConditionDefiningInputsPerCorticalLayerThreeBranch 
		pyramidalConfig['numOfBasilDendriteBranches'] = NumberOfBranchesPerLayerThreePyramidal
		pyramidalConfig['numOfProximalInputs'] = 0
		pyramidalConfig['proximalInputWeight'] = 0
		pyramidalConfig['dendriteThreshold'] = threshold
		pyramidalConfig['inputs'] = list(range(PyramidalsPerColumnLayerTwo))
		pyramidalConfig['source'] = None
		pyramidalConfig['managementInputs'] = NumberOfConditionRecordingOutputsFromBlackBoxHippocampus
		pyramidalConfig['interNuronConnectionsFromEach'] = 0
		pyramidalConfig['interNuronConnectoiosToOwnColumn'] = 0
		pyramidalConfig['excitatoryInputWeight'] = InitialLayerThreeSynapticWeight
		return pyramidalConfig

# a Cortical Layer is organization of neurons that has different connections and attributes, typically in the human brain there are 6 layers
class CorticalLayer:
	def __init__(self, index):
		self.index = index
		self.pyramidalNeurons = []
		self.pyramidalActivity = []
		self.interneurons = []
		self.interneuronsActivity = []

	def reduceSynapticWeights(self, proportion):
		# This method reduces all the synaptic weights on all the branches 
		# of the apical dendrites of all the neurons in all layers"  
		# 
		# The above comment says apical dendrites, but the downstream 
		# methods only change basilDendrites.  (RJT)
		for neuron in self.pyramidalNeurons:
			neuron.reduceSynapticWeights(proportion)
	
	def updateLayerOneInterneuronActivity(self):
		for neuron in self.interneurons:
			neuron.presentInputs(self, self.interneuronsActivity, [], True)

	