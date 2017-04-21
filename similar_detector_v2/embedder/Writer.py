#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import os

########################################################################
class Writer(object):
    """"""

    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        #self.directory = self.setOutputDirectory(directory)
        #self.dataDir
        #self.tocFilename      
       
    #----------------------------------------------------------------------
    def setOutputDirectory(self, directory):
        self.outputDirectory = directory  
    def _finalizeOutputDirectory(self):
        self.toc.close()    
    def _initializeOutputDirectory(self):
        """"""
        directory = self.outputDirectory
        if os.path.exists(directory):
            raise
        self.dataDir = os.path.join(directory, 'data') 
        self.tocFilename = os.path.join(directory, 'TOC') 
        os.makedirs(self.dataDir)
        self.toc = file(self.tocFilename, 'w')
        
        self.curDatapoint = 0        
    def _writeDataPoints(self,function_id,symbols):
        #for (funcId, symbols) in functions:
        self.toc.write("%d\n" % (function_id))
        self._addDataPoint(symbols)
        
    def _addDataPoint(self, symbols):
        datapointFilename = os.path.join(self.dataDir, str(self.curDatapoint))
        f = file(datapointFilename, 'w')
        if type(symbols)==list:
            f.writelines([x + "\n" for x in symbols])
        elif type(symbols)==dict:    
            for x in symbols.iterkeys():
                content=x + ":"+str(symbols[x])+"\n"
                f.writelines(content)
        f.close()
        self.curDatapoint += 1            
    #----------------------------------------------------------------------
    def run(self):
        try: 
            # Will throw error if output directory already exists
            self._initializeOutputDirectory()
        except:
            return
        #self._connectToDatabase()
        #functions = self._getAPISymbolsFromDatabase()
        #self._writeDataPoints(functions)
        #self._finalizeOutputDirectory()
        #self._embed()
    def _embed(self):
        # self.embedder = SallyBasedEmbedder()
        self.embedder = Embedder()
        self.embedder.embed(self.outputDirectory)       
        
    
    