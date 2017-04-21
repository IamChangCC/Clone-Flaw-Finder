#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from joern.all import JoernSteps
from collections import Counter
from joerntools.shelltool.ChunkStartTool import ChunkStartTool
import get_all_functions
#from node_strcture import node
#from edge_structure import edge

NEO4J_URL ='http://localhost:7474/db/data/'
PARAMETER = 'Parameter'
VARIABLE = 'Variable'
CALLEE = 'Callee'

########################################################################
class get_basic_blocks():
    """"""

    #----------------------------------------------------------------------
    def __init__(self,):
        """Constructor"""
        self.JS = JoernSteps()
        self.JS.setGraphDbURL(NEO4J_URL)
        self.JS.connectToDatabase()        
        self.get_function_list(ChunkStartTool)
        self.FUNCTION_LIST = {}
        self.BASIC_BLOCK_LIST = {}
        
        
        
    """take all the function name and functionId into a dict"""    
    def get_function_list(self,ChunkStartTool):
        '''query_get_all_functions="""
            queryNodeIndex('type:Function AND name:%s').id
            """
        '''
        list_function = get_all_functions.ListFuncs(ChunkStartTool)#ListFuncs()
        list_function.run()
        self.FUNCTION_LIST=list_function.ALL_FUNCTIONS
    
    """given a functionId , this can get the graph of the function """
    '''def get_subgraph(functionid):
        query_get_function_graph="""
                   queryNodeIndex('functionId:%s').outE
                    """%functionid        
        #query=""" queryNodeIndex('type:Function AND name:%s').id"""
        function_graphEdges = self.JS.runGremlinQuery(query_get_function_graph)
        return function_graph
    '''
    """given a functionId , this can get the control flow graph of the function"""
    def get_cfg_graph(self,functionid):
        query_get_cfg_graph="""queryNodeIndex('functionId:%s').outE
        .filter{it.label=="CONTROLS"||it.label=="POST_DOM"}
        .transform{[it.outV.id,it.id,it.label,it.inV.id]}.toList()"""%functionid    
        function_cfg_graph = self.JS.runGremlinQuery(query_get_cfg_graph)
        return function_cfg_graph        
    
    """given a functionId , this can get the ENTRY node id of the function"""
    def get_ENTRY_node(self,functionid): 
        query_from_entry = """queryNodeIndex('functionId:%s AND type:CFGEntryNode').id"""%functionid#transform{[it.id]}.toList()
        id_entry = self.JS.runGremlinQuery(query_from_entry)    
        return id_entry[0]
    
    
    """given a nodeId , this can get the code of the node ,result is utf string"""
    def get_code(self,node_id):
        query_get_code="""g.v(%s).getProperty("code")"""%node_id  
        query_result = self.JS.runGremlinQuery(query_get_code)
        return query_result.encode('utf-8')  
    
    
    
    """given a nodeId , this can get the type of the node ,result is utf string"""
    def get_type(self,node_id):
        query_get_code="""g.v(%s).getProperty("type")"""%node_id  
        query_result = self.JS.runGremlinQuery(query_get_code)
        return query_result                
    
    """given a nodeId , this can get the nodes that be controled ,result are ids"""
    def get_control_nodes(self,node_id):
        query_get_control_code="""g.v(%s).out("CONTROLS").id"""%node_id  
        query_result = self.JS.runGremlinQuery(query_get_control_code)
        control_node_list=[]
        for r in query_result:
            control_node_list.append(r)        
        return control_node_list                    
        
    """given a nodeId , this can get the nodes that POST_DOM ,result are ids"""
    def get_POST_DOM_nodes(self,node_id):
        query_get_POST_DOM_code="""g.v(%s).out("POST_DOM").id"""%node_id  
        query_result = self.JS.runGremlinQuery(query_get_POST_DOM_code)
        POST_DOM_node_list=[]
        for r in query_result:
            POST_DOM_node_list.append(r)   
        if len(POST_DOM_node_list)<1:
            return []    
        return POST_DOM_node_list[0]

    """given a nodeId , this can get the nodes that DOM ,result are ids"""
    def get_DOM_nodes(self,node_id):
        query_get_POST_DOM_code="""g.v(%s).in("POST_DOM").id"""%node_id  
        query_result = self.JS.runGremlinQuery(query_get_POST_DOM_code)
        POST_DOM_node_list=[]
        for r in query_result:
            POST_DOM_node_list.append(r)
        if len(POST_DOM_node_list)<1:
            return []
        return POST_DOM_node_list[0]

    """check the node not in the two_demission list"""
    def check_in_or_not(self,node,BBs):
        in_BBS=False
        max_i=len(BBs)
        for eachNum in range(max_i):
            if node in BBs[eachNum]:
                in_BBS = True
        return in_BBS    

    def Dom_list_sort(self,node_list):
        BBs_sorted=[]
        BBs=[]
        for node in node_list:
            if not self.check_in_or_not(node, BBs):
                BBs_sorted=[]
                BBs_sorted.append(node)
                last_node=node#get_DOM_nodes(node)
                next_node=node#get_POST_DOM_nodes(node)
                while self.get_DOM_nodes(last_node) in node_list:
                    BBs_sorted.insert(BBs_sorted.index(last_node), self.get_DOM_nodes(last_node))
                    last_node=self.get_DOM_nodes(last_node)
                while self.get_POST_DOM_nodes(next_node) in node_list:
                    BBs_sorted.append(self.get_POST_DOM_nodes(next_node))
                    next_node=self.get_POST_DOM_nodes(next_node)
                BBs.append(BBs_sorted)
        '''for node_list in BBs:
            for node in node_list:
                if self.get_type(self.get_POST_DOM_nodes(node))== "Parameter":
                    node_list.remove(node)'''         
        for sub_node_list in BBs:
            list_tmp=[]
            for node in sub_node_list:            
                if self.get_type(node)!= "Parameter":
                    list_tmp.append(node) 
            BBs.remove(sub_node_list)
            BBs.append(list_tmp)        
        return BBs  
    '''given a node, return the basic blocks of it'''
    def get_BBs_of_node(self,node_id):
        current_control_ids=self.get_control_nodes(node_id)
        if len(current_control_ids)==0:
            return []
        else: 
            return self.Dom_list_sort(current_control_ids)
        
    
    '''get the basic blocks of the function'''
    def function_basic_blocks(self,functionid):
        basic_block_ids=[]#store the basic blocks node id
        queue=[]#put the FIFO node
        entry_id=self.get_ENTRY_node(functionid)
        queue.append(entry_id)
        function_BB_code=[]
        while len(queue)>0:
            control_nodes=self.get_control_nodes(queue[0])
            queue.remove(queue[0])
            if len(control_nodes)>0:
                queue=queue+control_nodes
                basic_block_ids=basic_block_ids+self.Dom_list_sort(control_nodes)
        #return basic_block_ids#if do this, we can get the basic block node ids
        '''Do this can let us get the basic block code.'''
        for node_list_ids in basic_block_ids:
            node_list_codes=[]
            for node_id in node_list_ids:
                node_list_codes.append(self.get_code(node_id))
            function_BB_code.append(node_list_codes)
        return function_BB_code
        #self.get_BBs_of_node(entry_id)
                    
        
        
    def execute(self):
        #for etem in self.function_basic_blocks(54):
        #    print etem[:]
        #Project_BBs={}
        self.get_function_list(ChunkStartTool)
        for etem in self.FUNCTION_LIST.iterkeys():        
            #self.get_cfg_graph(functionid)
            self.BASIC_BLOCK_LIST[etem]=self.function_basic_blocks(etem)
        print "ok"
        
        
if __name__ == '__main__':
    get_basic_blocks().execute()
    #get_basic_blocks().function_basic_blocks(54)
