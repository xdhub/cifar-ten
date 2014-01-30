# To change this template, choose Tools | Templates
# and open the template in the editor.

import math
import mathutils
import bpy

# this should be 180 in degrees or pi in radians
halfCircleAngle = math.pi

def parseLine(line):
   vstr = line.split(",")
   v = [0.0]*len(vstr)
   for i in range(0, len(vstr)):
      v[i] = float(vstr[i])
   return v

def parseMatrix(rows):
   matrix = list()
   for row in rows:
      matrix.append(parseLine(row))

   return matrix

def createMatrix(rows):
   return mathutils.Matrix(parseMatrix(rows))

def readFile(fileName):
   file = open(fileName)
   matrices = list()

   while True:
      rows = list()
      
      for i in range(0, 3):
         line = file.readline()
         if not line: break
         rows.append(line)
      
      if len(rows) < 3: break
         
      matrices.append(createMatrix(rows))

   file.close()
   return matrices

#def getTestData():
#    return readFile("/home/kmo/study/motion/testData01.csv")

def norm(x):
   total = 0.0
   for a in x:
      total += abs(a) ** 2
   return math.sqrt(total)

# assume x and y are two iterable objects of the same length
def vectorDiff(x, y):
   z = list(x)
   for i in range(0, len(x)):
      z[i] = x[i]-y[i]
   return z

# assume x and y are two iterable objects of the same length
def distance(x, y):
   return norm(vectorDiff(x, y))

# assume two real numbers are the same if within this distance
def epsilon():
   return 1.0e-10

# test whether two numbers are identical
def sameVector(x, y):
   return distance(x, y) < epsilon()

# find the base top
def getBaseTop():
   return bpy.data.objects["xBasicTop"]

# find the second top
def getSecondTop():
   return bpy.data.objects["xSecondTop"]

# set rotation of object using a matrix
def setRotation(object, matrix):
   object.rotation_euler = matrix.to_euler()

# animate two tops using given datafile, this version is implemented with euler angles
def animateTops(matrices, frameSteps = 1):
   # to avoid discontinuities in motion when angle changes from 360 to 0 or back
   # keep track of total angle by adding a phase which is a multilple of 360

   # phases for base top in order x,y,z
   phase1 = [0,0,0]

   # phases for second top in order x,y,z
   phase2 = [0,0,0]

   base = getBaseTop()
   second = getSecondTop()

   # need to set rotation modes for Euler angles
   base.rotation_mode = 'XYZ'
   second.rotation_mode = 'XYZ'

   #matrices = getTestData()
   numberOfKeyFrames = len(matrices)/2

   # initialize with the first matrices in the list
   base.rotation_euler = matrices[0].to_euler()
   base.keyframe_insert(data_path="rotation_euler", frame=1)
   second.rotation_euler = matrices[1].to_euler()
   second.keyframe_insert(data_path="rotation_euler", frame=1)

   # now set keyframes from the rest of the matrices
   for i in range(1, int(numberOfKeyFrames)):
      frameNumber = 1 + i*frameSteps

      # rotate the base top and create a keyframe
#      base.rotation_euler = matrices[2*i].to_euler()
      base.rotation_euler = updateEuler(phase1, matrices[2*i-2], matrices[2*i])
      base.keyframe_insert(data_path="rotation_euler", frame=frameNumber)

      # rotate the second top and create a keyframe
#      second.rotation_euler = matrices[2*i + 1].to_euler()
      second.rotation_euler = updateEuler(phase2, matrices[2*i-1], matrices[2*i+1])
      second.keyframe_insert(data_path="rotation_euler", frame=frameNumber)

def updateEuler(phases, oldMatrix, newMatrix):
   oldEuler = oldMatrix.to_euler()
   newEuler = newMatrix.to_euler()

   # test whether any of the Euler angles change by more than 180 degrees
   phases[0] += updateAngle(oldEuler.x, newEuler.x)
   phases[1] += updateAngle(oldEuler.y, newEuler.y)
   phases[2] += updateAngle(oldEuler.z, newEuler.z)

   # correct the phase of newEuler angles
   newEuler.x += phases[0]*halfCircleAngle*2
   newEuler.y += phases[1]*halfCircleAngle*2
   newEuler.z += phases[2]*halfCircleAngle*2

   return newEuler

minArc = halfCircleAngle * 0.75

def updateAngle(oldAngle, newAngle):
#   return 0
   p = 0
   d = oldAngle - newAngle
   if abs(d) > minArc:
      if d > 0:
         p = 1
      else:
         p = -1
   return p

def animateTopsQ(matrices, frameSteps=1):
   base = getBaseTop()
   second = getSecondTop()
   numberOfKeyFrames = len(matrices)/2

   # need to set rotation modes for quaternions
   base.rotation_mode = 'QUATERNION'
   second.rotation_mode = 'QUATERNION'

   # now set keyframes from the rest of the matrices
   for i in range(0, int(numberOfKeyFrames)):
      frameNumber = 1 + i*frameSteps

      # rotate the base top and create a keyframe
      base.rotation_quaternion = matrices[2*i].to_quaternion()
      base.keyframe_insert(data_path="rotation_quaternion", frame=frameNumber)

      # rotate the second top and create a keyframe
      second.rotation_quaternion = matrices[2*i + 1].to_quaternion()
      second.keyframe_insert(data_path="rotation_quaternion", frame=frameNumber)

# this does not work well
def animateTopsM(matrices, frameSteps=1):
   base = getBaseTop()
   second = getSecondTop()

   # need to set rotation modes for Euler angles
   base.rotation_mode = 'XYZ'
   second.rotation_mode = 'XYZ'

   numberOfKeyFrames = len(matrices)/2

   # now set keyframes from the matrices
   for i in range(0, int(numberOfKeyFrames)):
      frameNumber = 1 + i*frameSteps

      # rotate the base top and create a keyframe
      base.matrix_basis = matrices[2*i].to_4x4()
      base.keyframe_insert(data_path="rotation_euler", frame=frameNumber)

      # rotate the second top and create a keyframe
      second.matrix_basis = matrices[2*i + 1].to_4x4()
      second.keyframe_insert(data_path="rotation_euler", frame=frameNumber)
