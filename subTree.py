#!/usr/bin/env python2

from joern.all import JoernSteps
from PipeTool import PipeTool

DESCRIPTION = """Prints all nodes of the AST rooted at the node with
the given id. Output format is rootNodeId TAB nodeId TAB level."""

OUTPUT_CSV = 'csv'
OUTPUT_PICKLE= 'pickle'
OUTPUT_FORMATS = [OUTPUT_CSV, OUTPUT_PICKLE]

class SubTree(PipeTool):
    
    def __init__(self):
        PipeTool.__init__(self, DESCRIPTION)
    
    def _outputCSV(self, dbResult, rootNodeId):
        out = ''
        for z in dbResult:
            id = z[0]
            x = z[1]
            # rootNodeId nodeId depth
            out += '%s\t%s\t%s\t' % (rootNodeId, id, x[1])
    
            for k in x[0]:
                attrKey = str(k)
                attrVal = x[0][k]
                attrVal = str(attrVal).replace('\t', ' ')
                out += '%s:%s\t' % (attrKey, attrVal)
            out = out[:-1] + '\n'

            self.output(out)

    # @Override
    def streamStart(self):
        self.j = JoernSteps()
        self.j.connectToDatabase()

    # @Override
    def processLine(self, line):
        nodeId = int(line)
        
        query = """g.v(%d).astNodeToSubNodes().transform{ [it[0].id, it] }""" % (nodeId)
        dbResult = self.j.runGremlinQuery(query)
        self._outputCSV(dbResult, nodeId)
    
    
if __name__ == '__main__':
    tool = SubTree()
    tool.run()
