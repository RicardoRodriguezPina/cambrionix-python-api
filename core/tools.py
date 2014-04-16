'''
Created on Apr 16, 2014

@author: eichhorn
'''


from functools import wraps
import threading

def synchronized(func):
    func.lock = threading.Lock()
    @wraps(func)
    def _synchronizer(self, *args, **kwargs):
        with func.lock:
            return func(self, *args, **kwargs)
        
    return _synchronizer
