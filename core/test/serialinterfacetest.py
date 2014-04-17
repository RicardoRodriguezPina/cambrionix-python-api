'''
Created on Apr 16, 2014

@author: eichhorn
'''
import unittest
import serialinterface


class TestResponseHandlers(unittest.TestCase):
    def testRawResponseHandler(self):
        self.assertEquals('abc', serialinterface.RawResponseHandler()('abc'))
        
    def testTableResponseHandler(self):
        self.assertEquals([['a', 'b', 'c'], ['1', '2', '3']], serialinterface.TableResponseHandler()("""a, b, c
        1 , 2, 3"""))

    def testListResponseHandler(self):
        self.assertEquals({'keyA':'valueA', 'keyB':'valueB'}, serialinterface.MapResponseHandler()("""keyA:valueA
        keyB : valueB"""))
