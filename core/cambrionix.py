'''
Created on Apr 15, 2014

@author: eichhorn
'''
import serial
import re
import serialinterface
import cambrionixport

class CambrionixException(Exception):
    pass

class Cambrionix(object):
    
    def __init__(self, device):
        
        self._interface = serialinterface.SerialInterface(serial.Serial, device, 115200, 8, 'N', 1)
        self._ports = {}
        
        self.updatePorts()
        
    def close(self):
        # necessary?
        # self._interface.sendCommand('remote exit')
        self._interface.close()

    def health(self):
        return self._interface.sendCommand('health')
    
    def sendBreak(self):
        """
        If the cambrionix is in a auto-log-state like  loge or logc, it won't respond until
        a break is sent (Ctrl-C). Call this function in this case
        """
        self._interface.sendCommand('\x03')
        
    
    def getProfiles(self):
        profileResponse = self._command('list_profiles')
        
        profiles = []
        for profile in re.split('[\r\n]+', profileResponse):
            m = self.profilesPattern.match(profile)
            if m:
                profiles.append(m.group(1))
            
        return profiles

    def disableAllProfiles(self):
        profiles = self.getProfiles()
        
        for profile in profiles:
            self._command('en_profile %s 0' % profile)
            
    def enableAllProfiles(self):
        profiles = self.getProfiles()
        
        for profile in profiles:
            self._command('en_profile %s 1' % profile)
            
    def updatePorts(self):
        stateResponse = self._interface.sendCommand('state', serialinterface.TableResponseHandler())
        
        if len(self._ports) != 0 and len(stateResponse) != len(self._ports):
            raise CambrionixException('Different number of ports between status polls. Not good.')
        
        try:
            for state in stateResponse:
                portId = int(state[0])
                
                if portId in self._ports:
                    self._ports[portId].update(state)
                else:
                    port = cambrionixport.Port(serialInterface=self._interface, portId=portId, state=state)
                    self._ports[portId] = port
        except Exception as e:
            print "Error parsing the response %s (%s)" % (stateResponse, str(e))
            
        if len(self._ports) == 0:
            raise CambrionixException('Could not read any ports. Something is seriously wrong.')
        
    def getConnectedPorts(self):
        return [port for port in self._ports.itervalues() if port.isConnected()]
    
    def getPort(self, portId):
        if portId not in self._ports:
            raise AttributeError('No cambrionixport available with ID %d' % int(portId))
        
        return self._ports[portId]


