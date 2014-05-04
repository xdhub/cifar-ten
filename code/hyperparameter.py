class Hyperparameters(object):
    def __init__(self, learningRate=0.13, numberEpochs=1000, batchSize=600, patience = 5000, patienceIncrease = 2, improvementThreshold = 0.995):
        self.learningRate = learningRate
        self.numberEpochs = numberEpochs
        self.batchSize = batchSize
        self.patience = patience
        self.patienceIncrease = patienceIncrease
        self.improvementThreshold = improvementThreshold

class HyperparametersMLP(Hyperparameters):
    def __init__(self, learningRate=0.13, numberEpochs=1000, L1Reg=0.00, L2Reg=0.0001, batchSize=600, patience = 5000, patienceIncrease = 2, improvementThreshold = 0.995, nHidden1 = 5000):
        Hyperparameters.__init__(self, learningRate, numberEpochs, batchSize, patience, patienceIncrease, improvementThreshold)
        self.L1Reg = L1Reg
        self.L2Reg = L2Reg
        self.nHidden1 = nHidden1

class HyperparametersDBN(Hyperparameters):
    def __init__(self, learningRate=0.1, numberEpochs=1000, batchSize=10, patience = 5000, patienceIncrease = 2, improvementThreshold = 0.995, pretrainingEpochs = 100, pretrainingLearningRate=0.01, k=1, nHidden=[1000, 1000]):
        Hyperparameters.__init__(self, learningRate, numberEpochs, batchSize, patience, patienceIncrease, improvementThreshold)
        self.pretrainingEpochs = pretrainingEpochs
        self.pretrainingLearningRate = pretrainingLearningRate
        self.k = k
        self.nHidden = nHidden

