#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from __future__ import division
import os
from joern.all import JoernSteps
from joerntools.shelltool.ChunkStartTool import ChunkStartTool
from collections import Counter
from embedder.Writer import Writer 
import get_all_functions

CHUNK_SIZE = 512
NEO4J_URL ='http://localhost:7474/db/data/'
FILE_PATH = '/home/chucky/chucky/similar_detector/tmp_folder'
EDGE_TYPES = ['IS_PARENT_DIR_OF','DECLARES','IS_AST_PARENT','FLOW_TO','USE','POST_DOM','CONTROLS','IS_FUNCTION_OF_AST','IS_FUNCTIO_OF_CFG','IS_FILE_OF','DEF','REACHES','IS_CLASS_OF','FUNCTION_CALL','IS_ARG']
########################################################################
class method_3():
    """this method takes different features into one vector, but the different place in vector is specified."""
    '''[0:the return type of the function,
        1:the number of the parameters
        2~20:the num of different property type nodes
        21~30:the num of different leble edges
        31~40:the num of different kinds of API functions
        41~45:the num of different kinds of node types,like Callee]'''

    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        self.JS = JoernSteps()
        self.JS.setGraphDbURL(NEO4J_URL)
        self.JS.connectToDatabase() 
        self.return_type_dataDir = os.path.join(FILE_PATH, 'return_type_data') 
        self.parameter_dataDir = os.path.join(FILE_PATH, 'parameter_data') 
        self.edge_dataDir = os.path.join(FILE_PATH, 'edge_data') 
        self.node_type_dataDir = os.path.join(FILE_PATH, 'node_type_data')
        self.all_return_type=[]
        self.all_node_type=[]
        self.FUNCTION_LIST = {}       
        self.get_function_list(ChunkStartTool)
        self.get_all_return_type()
    
    #----------------------------------------------------------------------
    '''def chunks(self, l, n):
        for i in xrange(0, len(l), n):
            yield l[i:i+n]
            """"""
     '''       
    """take all the function name and functionId into a dict"""    
    def get_function_list(self,ChunkStartTool):
        '''query_get_all_functions="""queryNodeIndex('type:Function AND name:%s').id"""
        '''
        list_function = get_all_functions.ListFuncs(ChunkStartTool)#ListFuncs()
        list_function.run()
        self.FUNCTION_LIST=list_function.ALL_FUNCTIONS
    
    
    #----------------------------------------------------------------------
    def return_type(self,function_id):
        """get the return_type of current function"""
        query_return_type = """queryNodeIndex('functionId:%s AND type:ReturnType').code"""%function_id#transform{[it.id]}.toList()
        return_type_code_u = self.JS.runGremlinQuery(query_return_type)   
        return_type_code=[]
        for type_code in return_type_code_u:
            return_type_code.append(type_code.encode("utf-8") )
        return return_type_code       
        
        
    #----------------------------------------------------------------------
    def get_all_return_type(self):
        """get the return_type of all functions"""
        for function_id in self.FUNCTION_LIST.iterkeys():#self.chunks(self.FUNCTION_LIST.keys(), CHUNK_SIZE):
            for current_return_type in self.return_type(function_id):
                if current_return_type not in self.all_return_type:
                    self.all_return_type.append(current_return_type)
        
    
    #----------------------------------------------------------------------
    def get_parameter_type(self,function_id):
        """get the num of specified function parameters"""
        query_parameter_type = """queryNodeIndex('functionId:%s AND type:ParameterType').code.toList()"""%function_id
        parameter_list = self.JS.runGremlinQuery(query_parameter_type) 
        return parameter_list  
    
    #----------------------------------------------------------------------
    def get_different_edge_num(self,function_id):
        """get the num of different type edges in the specified function"""
        query_edge_num="""queryNodeIndex('functionId:%s').outE.label"""%function_id
        edge_label=self.JS.runGremlinQuery(query_edge_num) 
        total_num=len(edge_label)
        edge_label_dic_standard={}
        edge_label_dic=dict((a.encode("utf-8"),edge_label.count(a)) for a in edge_label)
        for key in edge_label_dic.iterkeys():
            edge_label_dic_standard[key]=float(edge_label_dic[key]/total_num)
        #edge_label.count()
        return edge_label_dic_standard
     
    #----------------------------------------------------------------------
    def get_all_types(self):
        """get the types of all nodes"""
        for function_id in self.FUNCTION_LIST.iterkeys():#self.chunks(self.FUNCTION_LIST.keys(), CHUNK_SIZE):
            query_node_type = """queryNodeIndex('functionId:%s').type"""%function_id
            node_types = self.JS.runGremlinQuery(query_node_type)
            for current_node_type in node_types:
                if current_node_type.encode("utf-8") not in self.all_node_type:
                    self.all_node_type.append(current_node_type.encode("utf-8"))   
        print "ok"
        
    #----------------------------------------------------------------------
    def get_different_type_num(self,function_id):
        """get the num of different node types in the specified function"""
        query_type_num="""queryNodeIndex('functionId:%s').type"""%function_id
        type_label=self.JS.runGremlinQuery(query_type_num) 
        total_num=len(type_label)
        type_dic_standard={}
        type_dic=dict((a.encode("utf-8"),type_label.count(a)) for a in type_label)
        for key in type_dic.iterkeys():
            type_dic_standard[key]=float(type_dic[key]/total_num)
                #edge_label.count()
        return type_dic_standard        
        
    def output_return_type(self):
        return_type_writer=Writer()
        return_type_writer.setOutputDirectory(self.return_type_dataDir)
        return_type_writer.run()
        for function_id in self.FUNCTION_LIST.iterkeys():
            symbols= self.return_type(function_id)
            return_type_writer._writeDataPoints(function_id, symbols)
        return_type_writer._finalizeOutputDirectory()
    #----------------------------------------------------------------------
    def output_parameter_type(self):
        """"""
        return_type_writer=Writer()
        return_type_writer.setOutputDirectory(self.parameter_dataDir)
        return_type_writer.run()
        for function_id in self.FUNCTION_LIST.iterkeys():
            symbols= self.get_parameter_type(function_id)
            return_type_writer._writeDataPoints(function_id, symbols)
        return_type_writer._finalizeOutputDirectory()  
        
    #----------------------------------------------------------------------
    def output_edge_type(self):
        """"""
        return_type_writer=Writer()
        return_type_writer.setOutputDirectory(self.edge_dataDir)
        return_type_writer.run()
        for function_id in self.FUNCTION_LIST.iterkeys():
            symbols= self.get_different_edge_num(function_id)
            return_type_writer._writeDataPoints(function_id, symbols)
        return_type_writer._finalizeOutputDirectory()        
        
        #for function_id in self.FUNCTION_LIST.iterkeys():#self.chunks(self.FUNCTION_LIST.keys(), CHUNK_SIZE):
            
        #    current_function_paras=self.get_different_type_num(function_id)
        #    print function_id
        #self.get_all_types() 
        #----------------------------------------------------------------------
    def output_node_type(self):
        """"""
        return_type_writer=Writer()
        return_type_writer.setOutputDirectory(self.node_type_dataDir)
        return_type_writer.run()
        for function_id in self.FUNCTION_LIST.iterkeys():
            symbols= self.get_different_type_num(function_id)
            return_type_writer._writeDataPoints(function_id, symbols)
        return_type_writer._finalizeOutputDirectory()      
    def execute(self):
        self.output_return_type()
        self.output_parameter_type()
        self.output_edge_type() 
        self.output_node_type()
if __name__ == '__main__':
    method_3().execute()         
    print "ok"


#提取所有边和各类操作的个数，第2列：各类变量的个数；……第N列：用到各类API函数的个数，还应包括函数输入输出、数据结构是否相似、逻辑流程、）