'''
Created on Apr 15, 2014

@author: eichhorn
'''
import unittest
import cambrionix

class TestCambrionix(unittest.TestCase):
    
    def setUp(self):
        self.camb = cambrionix.Cambrionix('/dev/ttyUSB1')
        
    def tearDown(self):
        self.camb.close()
    
    def testHealth(self):
        self.camb.health()
        
    def testUpdatePorts(self):
        self.camb.updatePorts()
        
    def testGetConnectedPorts(self):
        self.camb.getConnectedPorts()

    def testGetProfiles(self):
        self.assertEquals(5, len(self.camb.getProfiles()))
        
    def testDisableEnableProfile(self):
        
        #enable one
        self.camb.enableProfile(4)
        self.assertFalse(all([prof[1] == 'enabled' for prof in self.camb.getProfiles()]))
        self.assertTrue(any([prof[1] == 'enabled' for prof in self.camb.getProfiles()]))
        
        # disable alle
        self.camb.disableAllProfiles()
        self.assertTrue(all([prof[1] == 'disabled' for prof in self.camb.getProfiles()]))
    
        
#         print camb._command('\x03')
#         print camb._command('beep 1000')
#         #camb.readForever()
#         
#         camb.updatePorts()
#         camb._command('crf')
#         print camb.getConnectedPorts()
#         
#         print camb._command('list_profiles')
#         #camb.disableAllProfiles()
#         print camb._command('list_profiles')
#         camb.updatePorts()
#         print camb.getConnectedPorts()
#         camb.enableAllProfiles()
#         print camb._command('list_profiles')
#         print camb.getConnectedPorts()
#         #print camb._command('mode c')
#         #print camb._command('loge 1')
#         print camb._command('system')
#         

def createDummyCambrionix():
    return cambrionix.Cambrionix(device='', serialFactory=lambda *args, **kwargs:None)
