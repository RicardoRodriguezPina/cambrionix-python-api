'''
Created on Apr 16, 2014

@author: eichhorn
'''
import unittest
import cambrionix
import time


class CambrionixPortTest(unittest.TestCase):

    def setUp(self):
        self.camb = cambrionix.Cambrionix('/dev/ttyUSB0')
        
    def tearDown(self):
        self.camb.close()
        
    def testSetOnAndOff(self):
        #self.camb.disableAllProfiles()
        self.camb.enableProfile(1)
        
        port1 = self.camb.getPort(1)
        port1.setCharge()
        
        # sleep to make the updater poll
        for i in range(8):
            time.sleep(1)
            if port1.isOn():
                break
        else:
            self.fail('Failed to turn on port')
         
        # turn it off, sleep and check again
        port1.setOff()
        for i in range(8):
            time.sleep(1)
            if port1.isOff():
                break
        else:
            self.fail('Failed to turn off port')


