class Hyperparameters(object):
    def __init__(self, learningRate=0.13, numberEpochs=10, batchSize=600, patience = 5000, patienceIncrease = 2, improvementThreshold = 0.995):
        self.learningRate = learningRate
        self.numberEpochs = numberEpochs
        self.batchSize = batchSize
        self.patience = patience
        self.patienceIncrease = patienceIncrease
        self.improvementThreshold = improvementThreshold

class HyperparametersMLP(Hyperparameters):
    def __init__(self, learningRate=0.13, numberEpochs=10, L1Reg=0.00, L2Reg=0.0001, batchSize=600, patience = 5000, patienceIncrease = 2, improvementThreshold = 0.995, nHidden1 = 5000):
        Hyperparameters.__init__(self, learningRate, numberEpochs, batchSize, patience, patienceIncrease, improvementThreshold)
        self.L1Reg = L1Reg
        self.L2Reg = L2Reg
        self.nHidden1 = nHidden1
        
