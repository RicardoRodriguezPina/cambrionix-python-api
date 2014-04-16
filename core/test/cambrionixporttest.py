'''
Created on Apr 16, 2014

@author: eichhorn
'''
import unittest
import cambrionix


class CambrionixPortTest(unittest.TestCase):

    def setUp(self):
        self.camb = cambrionix.Cambrionix('/dev/ttyUSB1')
        
    def tearDown(self):
        self.camb.close()
        
    def testSetSyncAndOff(self):
        port1 = self.camb.getPort(1)
        port1.setCharge()
        self.assertTrue(port1.isCharge())
        
        #port1.setOff()
        #self.assertTrue(port1.isOff())


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
