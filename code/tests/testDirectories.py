import os
import cifarDirectories

class TestDirectories():

    def setUp(self):
        self.y = 1

    def testDirectories(self):
        self.assertTrue(os.path.exists(cifarDirectories.base()))
        self.assertTrue(os.path.exists(cifarDirectories.code()))
        self.assertTrue(os.path.exists(cifarDirectories.data()))
        self.assertTrue(os.path.exists(cifarDirectories.cifarKaggle()))
        self.assertTrue(os.path.exists(cifarDirectories.demos()))
        self.assertTrue(os.path.exists(cifarDirectories.DeepLearningTutorials()))
        self.assertTrue(os.path.exists(cifarDirectories.DeepLearningTutorialsCode()))

