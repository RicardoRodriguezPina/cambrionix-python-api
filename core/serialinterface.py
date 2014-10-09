'''
Created on Apr 16, 2014

@author: eichhorn
'''
import serial
import time
import tools
import logging

log = logging.getLogger('cambrionix.SerialInterface')

class ResponseHandler(object):
    def __init__(self, ignoreEmptyLines=True):
        self.ignoreEmptyLines = ignoreEmptyLines

class RawResponseHandler(ResponseHandler):
    """
    Handles a response by simply returning it as a string.
    """
    
    def __call__(self, response):
        return str(response)

class MapResponseHandler(ResponseHandler):
    """
    Assumes a key-value response, which is 
    transformed into a python dict.
    
    For example:
    keyA: valueA
    keyB: valueB
    would be transformed to
    {'keyA':'valueA', 'keyB':'value'B}
    """
    def __call__(self, response):
        parsedResponse = {}

        for line in response.splitlines():
            
            line = line.strip()
            if len(line) == 0 and self.ignoreEmptyLines:
                continue
            
            keyvalue = line.split(':')
            if len(keyvalue) != 2:
                log.error("error retrieving list response for line \n" + line)
                continue
            key = keyvalue[0].strip()
            value = keyvalue[1].strip()
            if key in parsedResponse:
                log.warn("found key %s at least twice for response" % key)
            
            parsedResponse[key] = value
        return parsedResponse


class TableResponseHandler(ResponseHandler):
    """
    Assumes a list-like response, splitting each line by a separator (,).
    A warning is printed for all lines whose column number differs from the rest.
    """
    def __call__(self, response):
        parsedResponse = []
        cols = None
        for line in response.splitlines():
            line = line.strip()
            if len(line) == 0 and self.ignoreEmptyLines:
                continue
            parsedLine = line.split(',')
            if cols is None:
                cols = len(parsedLine)
                
            if len(parsedLine) != cols:
                log.warn("line %s has a different number of cols than the others" % line)
            
            parsedResponse.append(map(lambda x:x.strip(), parsedLine))
        return parsedResponse

class SerialInterfaceException(Exception):
    pass


class SerialInterface(object):
    """
    Provides a higher-level interface for the serial cambrionixport.
    
    For test purposes, the serial factory can be replaced by 
    other functions/classes that produce mocked serial interfaces.
    """
    def __init__(self, serialFactory, *args, **kwargs):
        
        if 'timeout' not in kwargs:
            kwargs['timeout'] = 2
            
        self._ignoreFirstLine = False
        
        self._readTimeout = float(kwargs['timeout'])
        
        # for each command to retrieve a respond, we'll wait just one second
        self._serial = serialFactory(*args, **kwargs)
        
    def getReadTimeout(self):
        return self._readTimeout
        
    def setIgnoreFirstLine(self, ignore):
        self._ignoreFirstLine = ignore
        
    def close(self):
        if not self._serial.closed:
            self._serial.close()
        
    @tools.synchronized
    def sendCommand(self, command, responseHandler=RawResponseHandler(), removeEcho=True, sendSuffix='\r\n', responseTerminator='>>'):
        """
        Main interface of the serial interface.
        A command is sent to the interface, with the default suffix \r\n appended.
        The response is read until the responseTerminator appears.
        
        The response is than handed to the responesHandler, which transforms as necessary.
        Existing response handlers are RawResponseHandler, TableResponseHandler, MapResponseHandler
        """
        
        commandToWrite = command
        # append suffix, if not there already
        if not commandToWrite.endswith(sendSuffix):
            commandToWrite += sendSuffix
        
        self._serial.write(commandToWrite)
        # first the response byte by byte
        response = []
        while len(response) < len(responseTerminator) or ''.join(response[-len(responseTerminator):]) != responseTerminator:
            result = self._serial.read(1)
            if len(result) > 0:
                response.append(result)
            
            if (time.time() - start) > self._readTimeout:
                log.debug('Timeout: response so far: ' + ''.join(response))
                raise SerialInterfaceException('Could not get a response within %f seconds.' % self._readTimeout)
            
        # join it into a string
        response = ''.join(response[:-2])
        
        response = response.strip()
        
        if removeEcho:
            if response.startswith(command):
                response = response[len(command):].strip()
        return responseHandler(response)
        
        
