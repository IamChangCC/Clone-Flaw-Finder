#!/usr/bin/env python2

from joerntools.shelltool.ChunkStartTool import ChunkStartTool
import string


DESCRIPTION = """Create a list of all functions of the code base. The
first field is the function's name, the second field is the id of the
corresponding node in the database, and the third is the file it is
contained in"""

class ListFuncs(ChunkStartTool):

    def __init__(self, DESCRIPTION):
        ChunkStartTool.__init__(self, DESCRIPTION)
        self.ALL_FUNCTIONS={}

        self.argParser.add_argument('-p', '--pattern',
                                    action = 'store', type=str,
                                    default ="*")
        


    def _constructIdQuery(self):
        return """
            queryNodeIndex('type:Function AND name:%s').id
            """ % (self.args.pattern)

    def _constructQueryForChunk(self, chunk):
        return """idListToNodes(%s).transform{ it.name + "\t" + it.id  }""" % (chunk)

    def _handleChunkResult(self, res, chunk):
        for x in res:
            #print x
            x = x.encode("utf-8")
            index = x.index("\t")#(self, "\t")
            key = x[index+1:]
            name = x[:index]
            self.ALL_FUNCTIONS[key]=name


if __name__ == '__main__':
    tool = ListFuncs(DESCRIPTION)
    tool.run()