# To change this template, choose Tools | Templates
# and open the template in the editor.

import sys
sys.path.append("scripts")
import math, mathutils
import unittest, motion01

class  MotionTestCase(unittest.TestCase):
   #def setUp(self):
   #    self.foo = Motion()
   #

   #def tearDown(self):
   #    self.foo.dispose()
   #    self.foo = None

   def test_motion(self):
      #assert x != y;
      #self.assertEqual(x, y, "Msg");
      assert(True)
      # self.fail("TODO: Write test")

   # get a vector like object from a string
#   def tRead(self, line):
#      return motion01.parseCVSLine(line)

   # test parsing lines from comma separated file
   def testReadCVSLine(self):
      assert(motion01.sameVector(motion01.parseLine("0"), [0]))
      assert(motion01.sameVector(motion01.parseLine("0,0"), [0, 0]))
      assert(motion01.sameVector(motion01.parseLine("0,0,0"), [0, 0, 0]))
      assert(motion01.sameVector(motion01.parseLine("1.0, 2.0, 3.0"), [1, 2, 3]))

   def testDistance(self):
      # first some basic test of vector difference function
      assert(motion01.vectorDiff((0, 0), (0, 0)) == [0, 0])
      assert(motion01.vectorDiff((1, 2), (1, 2)) == [0, 0])
      assert(motion01.vectorDiff((1, 3), (1, 2)) == [0, 1])
      assert(motion01.vectorDiff((1, 2), (1, 3)) == [0, -1])

      # test whether vectors are the same
      assert(motion01.sameVector((0, 0), (1.0e-20, 0)))
      assert(not(motion01.sameVector((0, 0), (1, 0))))

      # now test the actual distance function
      assert(motion01.distance((0, 0), (0, 0)) == 0)
      assert(motion01.sameVector((1, 1), (1.0, 1.0 + 1.0e-20)))

   # test that the norm funtion works
   # note, there should be something like this already
   def testNorm(self):
      assert(motion01.norm((0, 0)) == 0.0)
      assert(motion01.norm((1, 1)) == math.sqrt(2))

   def testReadCVSMatrix(self):
      assert(motion01.parseMatrix(("0,0", "1,1")) == [[0, 0], [1, 1]])
      assert(motion01.parseMatrix(("1,0", "0,1")) == [[1, 0], [0, 1]])

   def testCreateMatrix(self):
      assert(motion01.createMatrix(("0,0", "1,1")) == mathutils.Matrix(((0.0, 0.0), (1.0, 1.0))))

   def testUpdateAngle(self):
      assert(motion01.updateAngle(0, 0) == 0)
      assert(motion01.updateAngle(motion01.halfCircleAngle*2, 0) == 1)
      assert(motion01.updateAngle(0, motion01.halfCircleAngle*2) == -1)
      assert(motion01.updateAngle(motion01.halfCircleAngle*0.5, motion01.halfCircleAngle*0.48) == 0)
      assert(motion01.updateAngle(0, motion01.halfCircleAngle*0.01) == 0)
      assert(motion01.updateAngle(0, motion01.halfCircleAngle*.25) == 0)
      assert(motion01.updateAngle(motion01.halfCircleAngle*0.48, motion01.halfCircleAngle*0.6) == 0)
      assert(motion01.updateAngle(motion01.halfCircleAngle*1.8, motion01.halfCircleAngle*0.2) == 1)
      assert(motion01.updateAngle(motion01.halfCircleAngle*0.5, motion01.halfCircleAngle*0.45) == 0)
      assert(motion01.updateAngle(motion01.halfCircleAngle*0.1, motion01.halfCircleAngle*1.9) == -1)
      assert(motion01.updateAngle(motion01.halfCircleAngle*0.49, motion01.halfCircleAngle*1.5) == -1)
   
#   def testUpdateEuler(self):
#      m1 = mathutils.Matrix(((-0.922680675983429, -0.0017084265127778053, 0.3855611979961395), (0.34100502729415894, -0.47028523683547974, 0.813970148563385), (0.17993313074111938, 0.8825128078460693, 0.4345056712627411)))
#      m2 = mathutils.Matrix(((-0.9238386154174805, 0.003333335043862462, 0.3827677071094513), (0.3361676037311554, -0.47117069363594055, 0.8154689073562622), (0.18306715786457062, 0.8820357322692871, 0.4341651201248169)))
#      print(m1)
#      print(m2)
      
#      p = [0,0,0]
#      eu = motion01.updateEuler(p, m1, m2)
#      print(p)
#      print(eu)
#      assert(p == [0, 0, -1])

#if __name__ == '__main__':
#   unittest.main()

suite = unittest.TestLoader().loadTestsFromTestCase(MotionTestCase)
#suite.addTest(unittest.TestLoader().loadTestsFromTestCase(WidgetTestCase))

unittest.TextTestRunner(verbosity=2).run(suite)

matrices = motion01.readFile("tops.csv")
motion01.animateTopsM(matrices, frameSteps=1)


