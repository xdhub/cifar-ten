import DBNClassifier
import random
import dataset
from hyperparameter import HyperparametersDBN

def learningrate():
    return 0.001 * (10 ** (random.randint(0, 6) / 2.0))

def epochs():
    return 5 + int(abs(random.normalvariate(0, 15)))

def layersize():
    return 100 + int(abs(random.normalvariate(900, 2000)))

def twoLayers():
    return [layersize(), layersize()]

def threeLayers():
    return [layersize(), layersize(), layersize()]

def fourLayers():
    return [layersize(), layersize(), layersize(), layersize()]

def hyper():
    p = random.random()
    nHidden = None
    if p < 0.5:
        nHidden = twoLayers()
    elif p < 0.9:
        nHidden = threeLayers()
    else:
        nHidden = fourLayers()
    print 'Layers: ', nHidden
    
    pretrainingEpochs=epochs()
    pretrainingLearningRate=learningrate()
    print 'Pretraining epochs: ', pretrainingEpochs
    print 'Pretraining learning rate: ', pretrainingLearningRate

    learningRate=learningrate()
    numberEpochs=epochs()
    print 'Fine tuning epochs: ', numberEpochs
    print 'Fine tuning learning rate: ', learningRate
    
    return HyperparametersDBN(learningRate=learningRate, 
        numberEpochs=numberEpochs,
        pretrainingEpochs=pretrainingEpochs, 
        pretrainingLearningRate=pretrainingLearningRate,
        nHidden=nHidden)
    
if __name__ == '__main__':
    DBNClassifier.test_DBN(dataset.Mnist(), hyper())

