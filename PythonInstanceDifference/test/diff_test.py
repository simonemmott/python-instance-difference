'''
Created on 16 Dec 2018

@author: simon
'''
import unittest
from entities_test import EntityA
from classUtil_test import ClassA, ClassB, ClassC
from utilities import classUtil
from difference import diff
import json



class Test(unittest.TestCase):

    def setUp(self):
        self.eA1 = EntityA(id=123, description='Entity A description', name='Entity A')
        self.eA2 = EntityA(id=123, name='Entity A2', description='Entity A2 description')

        self.fred = ClassA(name='Fred', description='caveman')
        self.barny = ClassA(name='Barny', description='caveman')
        self.bambam = ClassA(name='Bambam', description='cavechild')
        self.wilma = ClassA(name='Wilma', description='cavewoman')
        self.betty = ClassA(name='Betty', description='cavewoman')

        self.mrFred = ClassB(name='Fred', description='caveman', title='Mr')
        self.mrsWilma = ClassB(name='Wilma', description='cavewoman', title='Mrs')
        self.mrBarny = ClassB(name='Barny', description='caveman', title='Mr')
        self.mrsBetty = ClassB(name='Betty', description='cavewoman', title='Mrs')
        self.masterBambam = ClassB(name='Bambam', description='cavechild', title='Master')

        self.flintstones = ClassC(name='Flintstones', description='A family of cavemen', a=self.bambam, bs=[self.mrsWilma, self.mrFred])
        self.rubble = ClassC(name='Rubble', description='A family of cavemen', a=self.barny, bs=[self.mrsBetty, self.mrBarny])
        
    def tearDown(self):
        pass

    def test_compare_1(self):

        d = diff.compare(self.eA1, self.eA2)
        
        assert d.key == (123,)
        assert d.type_name == 'EntityA'
        assert len(d.diffs) == 2
        assert d.diffs['_description']['a'] == 'Entity A description'
        assert d.diffs['_description']['b'] == 'Entity A2 description'
        assert d.diffs['_name']['a'] == 'Entity A'
        assert d.diffs['_name']['b'] == 'Entity A2'
         
    def test_compare_2(self):
        
        d = diff.compare(self.barny, self.bambam)

        assert d.key == None
        assert d.type_name == 'ClassA'
        assert len(d.diffs) == 2
        assert d.diffs['_description']['a'] == 'caveman'
        assert d.diffs['_description']['b'] == 'cavechild'
        assert d.diffs['_name']['a'] == 'Barny'
        assert d.diffs['_name']['b'] == 'Bambam'
        
    def test_compare_3(self):
        
        d = diff.compare(self.flintstones, self.rubble)
        
        assert d.key == None
        assert d.type_name == 'ClassC'
        assert len(d.diffs) == 5
        assert d.diffs['_a._description']['a'] == 'cavechild'
        assert d.diffs['_a._description']['b'] == 'caveman'
        assert d.diffs['_a._name']['a'] == 'Bambam'
        assert d.diffs['_a._name']['b'] == 'Barny'
        assert d.diffs['_bs[0]._name']['a'] == 'Wilma'
        assert d.diffs['_bs[0]._name']['b'] == 'Betty'
        assert d.diffs['_bs[1]._name']['a'] == 'Fred'
        assert d.diffs['_bs[1]._name']['b'] == 'Barny'
        assert d.diffs['_name']['a'] == 'Flintstones'
        assert d.diffs['_name']['b'] == 'Rubble'
        
    def test_compare_4(self):
        
        fred = ClassB(name='Fred', description='caveman')
        
        d = diff.compare(self.mrFred, fred)
        
        assert d.key == None
        assert d.type_name == 'ClassB'
        assert len(d.diffs) == 1
        assert d.diffs['_title']['a'] == 'Mr'
        assert d.diffs['_title']['b'] == None
        
    def test_compare_5(self):
        
        fred = ClassB(name='Fred', description='caveman')
        fred2 = ClassB(name='Fred', description='caveman')
        
        d = diff.compare(fred, fred2)
        
        assert d.key == None
        assert d.type_name == 'ClassB'
        assert len(d.diffs) == 0
        
    def test_compare_6(self):
        
        flintstones = ClassC(name='Flintstones', description='A family of cavemen', bs=[self.mrsWilma, self.mrFred, self.bambam])
        
        d = diff.compare(self.flintstones, flintstones)

#        print(json.dumps(classUtil.to_dict(d), indent=4))
        
        assert d.key == None
        assert d.type_name == 'ClassC'
        assert len(d.diffs) == 2
        assert d.diffs['_a']['b'] == None
        assert d.diffs['_a']['format'] == 'JSON'
        assert json.loads(d.diffs['_a']['a'])['_description'] == 'cavechild'
        assert json.loads(d.diffs['_a']['a'])['_name'] == 'Bambam'
        assert d.diffs['_bs[2]']['a'] == None
        assert d.diffs['_bs[2]']['format'] == 'JSON'
        assert json.loads(d.diffs['_bs[2]']['b'])['_description'] == 'cavechild'
        assert json.loads(d.diffs['_bs[2]']['b'])['_name'] == 'Bambam'

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()