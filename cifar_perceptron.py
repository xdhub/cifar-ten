from PIL import Image
import numpy as np
import glob
import csv
from pybrain.utilities           import percentError
from pybrain.tools.shortcuts     import buildNetwork
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.structure.modules   import SoftmaxLayer
from pybrain.datasets import ClassificationDataSet

#USE LOCAL PATH
folder = '~/train/'
imgList = glob.glob(folder+'*.png')

#CREATE ARRAYS TO USE
img_array = []
data_array =[]
merge_array=[]

#OPEN LABELED DATA FILE AND PUT INTO ARRAY, USE LOCAL PATH
datafile = open('~/train/trainLabels (1).csv', 'r')
datareader = csv.reader(datafile)

for row in datareader:
    data_array.append(row)
    
data_array =np.array(data_array)

#OPEN, FLATTEN, AND LOAD IMAGE DATA INTO AN ARRAY
for img in  imgList:
    openImg = Image.open(img)
    converted_img = openImg.convert('RGB')
    ndarr = np.array(converted_img)
    ndarr = ndarr.flatten()
    img_array.append(ndarr)
    
img_array = np.array(img_array)
merge_array=zip(img_array, data_array) 

#SET UP DATA SET
ds = ClassificationDataSet(3072, class_labels=['frog','truck','deer','automobile','bird','horse','ship','cat','dog','airplane'])   

for i,k in merge_array:
    ds.appendLinked(i,k)

# CREATE TEST AND TRAINING SETS  
tstdata, trndata = ds.splitWithProportion( 0.25 )
trndata._convertToOneOfMany()
tstdata._convertToOneOfMany()

#SET UP NEURAL NET
fnn = buildNetwork(trndata.indim, 6, 10, outclass=SoftmaxLayer)
trainer = BackpropTrainer( fnn, dataset=trndata, momentum=0.1, verbose=True, weightdecay=0.01)

#TRAIN THE MODEL AND OUTPUT ERROR RATE
for i in range(20):
    trainer.trainEpochs( 1 )
trnresult = percentError( trainer.testOnClassData(),
                              trndata['class'] )
tstresult = percentError( trainer.testOnClassData(
           dataset=tstdata ), tstdata['class'] )

print "epoch: %4d" % trainer.totalepochs, \
          "  train error: %5.2f%%" % trnresult, \
          "  test error: %5.2f%%" % tstresult





