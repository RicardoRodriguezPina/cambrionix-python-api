'''
Created on Apr 15, 2014

@author: eichhorn
'''
import serial
import re
import serialinterface
import cambrionixport
import threading
import time

class CambrionixException(Exception):
    pass

class Cambrionix(object):
    
    def __init__(self, device, autoUpdate=1.0):
        
        self._interface = serialinterface.SerialInterface(serial.Serial, device, 115200, 8, 'N', 1)
        self._ports = {}
        
        self.resetReboot()
        self.updatePorts()
        
        self._poller = None
        if autoUpdate is not None:
            self._poller = StatePoller(self, autoUpdate)
            self._poller.start()
        
        
    def close(self):
        # necessary?
        # self._interface.sendCommand('remote exit')
        if self._poller:
            self._poller.stop()
            
            # do we need to join it??
            #self._poller.join()
            
        self._interface.close()

    def health(self):
        return self._interface.sendCommand('health')
    
    def resetReboot(self):
        self._interface.sendCommand('crf')
    
    def sendBreak(self):
        """
        If the cambrionix is in a auto-log-state like  loge or logc, it won't respond until
        a break is sent (Ctrl-C). Call this function in this case
        """
        self._interface.sendCommand('\x03')
        
    
    def getProfiles(self):
        return self._interface.sendCommand('list_profiles', serialinterface.TableResponseHandler())
    
    def disableAllProfiles(self):
        profiles = self.getProfiles()
        
        for profile in profiles:
            self._interface.sendCommand('en_profile %s 0' % profile[0])
    
    def enableProfile(self, profileId):
        self._interface.sendCommand('en_profile %s 1' % str(profileId))
            
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


class StatePoller(threading.Thread):
    def __init__(self, cambrionix, interval=1.0):
        threading.Thread.__init__(self)
        
        self._interval = interval
        self._cambrionix = cambrionix
        
        self._stop = threading.Event()
        
    def run(self):
        while not self._stop.isSet():
            # print "updating cambrionix ports"
            self._cambrionix.updatePorts()
            time.sleep(self._interval)
            
    def stop(self):
        self._stop.set()
            
