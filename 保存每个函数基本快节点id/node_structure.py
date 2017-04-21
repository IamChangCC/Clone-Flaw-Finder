#!/usr/bin/env python2
import string


########################################################################
class node:
    """"""

    #----------------------------------------------------------------------
    def __init__(self,ID=None,CODE=None,TYPE=None,FUNCTIONID=None):
        """Constructor"""
        self.id=ID
        self.type=TYPE
        self.CODE=CODE
        self.functionId=FUNCTIONID
        self.inE=[]
        self.outE=[]
        
    
    
    