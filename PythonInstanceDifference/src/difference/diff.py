'''
Created on 16 Dec 2018

@author: simon
'''
from entities import entities
from utilities import classUtil, typeUtil
import json, itertools

class Diff(object):
    
    type_name = None
    key = None
    diffs = {}
    
    def __init__(self, **kw):
        self.type_name = kw.get('typeName', self.type_name)
        if kw.get('type'):
            self.type_name = kw.get('type').__name__
        self.key = kw.get('key', self.key)
        self.diffs = {}
        
    def register(self, path, a, b, **kw):
        if kw.get('format'):
            self.diffs[path] = {'a': a, 'b': b, 'format': kw.get('format')}
        else:
            self.diffs[path] = {'a': a, 'b': b}
        
def compare(a, b, **kw):
    
    key = entities.get_pk(a) if entities.is_entity(type(a)) else None
    diff = kw.get('diff', Diff(type=type(a),key=key))
    path = kw.get('path', '')
        
    if not typeUtil.is_instance(a) or not typeUtil.is_instance(b):
        raise ValueError('Only able to compare class instances')
    if (a == None or b == None) and not (a == None and b == None):
        if a == None:
            diff.register(path, None, json.dumps(classUtil.to_dict(b)), format='JSON')
        else:
            diff.register(path, json.dumps(classUtil.to_dict(a)), None, format='JSON')
        return diff
    if type(a) != type(b):
        raise ValueError('Only able to compare instances of the same type')

    path = path+'.' if path != '' else path
    
    for attr in classUtil.get_attributes(type(a)):
        aVal = getattr(a, attr)
        bVal = getattr(b, attr)
        
        if (aVal == None and bVal == None) or aVal == bVal:
            pass
        else:
            
            if type(aVal) != type(bVal):
                if aVal == None:
                    if typeUtil.is_primitive(bVal):
                        diff.register(path+attr, None, bVal)
                    else:
                        diff.register(path+attr, None, json.dumps(classUtil.to_dict(bVal)), format='JSON')
                elif bVal == None:
                    if typeUtil.is_primitive(aVal):
                        diff.register(path+attr, aVal, None)
                    else:
                        diff.register(path+attr, json.dumps(classUtil.to_dict(aVal)), None, format='JSON')
                else:
                    diff.register(path+attr, json.dumps(classUtil.to_dict(aVal)), json.dumps(classUtil.to_dict(bVal)), format='JSON')
            else:
                if typeUtil.is_primitive(aVal):
                    diff.register(path+attr, aVal, bVal)
                elif typeUtil.is_collection(aVal):
                    if len(aVal) < len(bVal):
                        for index in range(len(bVal)):
                            bLst = bVal[index]
                            if index < len(aVal):
                                aLst = aVal[index]
                            else:
                                aLst = None
                            compare(aLst, bLst, diff=diff, path=path+attr+'['+str(index)+']')
                             
                    elif len(aVal) == len(bVal):
                        for index in range(len(aVal)):
                            compare(aVal[index], bVal[index], diff=diff, path=path+attr+'['+str(index)+']') 
                    else:
                        for index in range(len(aVal)):
                            aLst = aVal[index]
                            if index < len(bVal):
                                bLst = bVal[index]
                            else:
                                bLst = None
                            compare(aLst, bLst, diff=diff, path=path+attr+'['+index+']')
                elif typeUtil.is_map(aVal):
                    diff.register(path+attr, json.dumps(aVal), json.dumps(bVal), format='JSON')
                elif typeUtil.is_instance(aVal):
                    compare(aVal, bVal, diff=diff, path=path+attr)
                else:
                    raise TypeError('The listed value: %s has an unexpected type: %s' % (aVal, type(aVal)))
            
            

    return diff
    
        