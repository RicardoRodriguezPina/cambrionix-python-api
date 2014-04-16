'''
Created on Apr 16, 2014

@author: eichhorn
'''
import serialinterface
import cambrionix

class Port(object):
    
    portModeConstants = {'O': 'off',
                 'S': 'sync',
                 'B': 'biased',
                 'I': 'idle',
                 'P': 'profiling',
                 'C': 'charging',
                 'F': 'finished',
                 'A': 'attached',
                 'D': 'detached',
                 'T': 'theft',
                 'E': 'errors',
                 'R': 'rebooted',
                 'r': 'vbus_reset'
                 }

    
    def __init__(self, serialInterface, portId, state, autoupdate=True):
        
        self._interface = serialInterface
        self.portId = portId
        self.current = 0
        self.flags = set()
        self.uptime = 0
        self.energy = 0
        
        self._autoupdate = autoupdate
        
        self.update(state)
        
    def isConnected(self):
        return 'attached' in self.flags
      
    def __repr__(self):
        return str(self)
    
    def __str__(self):
        return 'Port %s (%s), flags=%s, up for %d seconds, energy %f wh' % (self.portId,
                                                                            self.current,
                                                                            ','.join(self.flags),
                                                                            self.uptime,
                                                                            self.energy)
        
    def selfUpdate(self):
        response = self._interface.sendCommand('state %d' % self.portId, serialinterface.TableResponseHandler())
        if not len(response) == 1:
            raise cambrionix.CambrionixException('requesting state for one port should return only one port. Got %s' % response)
        
        self.update(response[0])
        
    
    def _doAutoupdate(self):
        if not self._autoupdate:
            return
        
        self.selfUpdate()
        
    def update(self, state):
        print "updating port %d to state %s" % (self.portId, str(state))
        if len(state) != 7:
            raise cambrionix.CambrionixException('Port state is expected to have 7 values. Got %s' % state)
        
        self.current = int(state[1])
        self.flags.clear()
        for (constant, flag) in self.portModeConstants.iteritems():
            if constant in state[2]:
                self.flags.add(flag)
        self.uptime = int(state[4])
        self.energy = float(state[6])
        
    def isOff(self):
        return 'off' in self.flags
    
    def isCharge(self):
        return 'charging' in self.flags
        
    def _setMode(self, mode):
        response = self._interface.sendCommand('mode %s %d' % (mode, self.portId))
        if response.strip() != '':
            raise cambrionix.CambrionixException('Could not set port (%s)' % response)
        self._doAutoupdate()
        
    def setCharge(self):
        self._setMode('c')
        
    def setOff(self):
        self._setMode('o')
        
