#!/usr/bin/env python2

from joern.all import JoernSteps
from PipeTool import PipeTool

from csvAST.CSVToPythonAST import pythonASTFromDbResult
import pickle

DESCRIPTION = """Prints all nodes of the AST rooted at the node with
the given id. The default output format is a CSV format similar to
that used by CodeSensor."""

OUTPUT_CSV = 'csv'
OUTPUT_PICKLE= 'pickle'
OUTPUT_FORMATS = [OUTPUT_CSV, OUTPUT_PICKLE]

class SubTree(PipeTool):
    
    def __init__(self):
        PipeTool.__init__(self, DESCRIPTION)

        self.argParser.add_argument('-O', '--output-format', choices = OUTPUT_FORMATS,
                                    action='store', help="""The output
                                    format to use""",
                                    default = OUTPUT_CSV)
    
        self._initOutputHandlers()

    def _initOutputHandlers(self):
        self.outputHandler = dict()
        self.outputHandler[OUTPUT_CSV] = self._outputCSV
        self.outputHandler[OUTPUT_PICKLE] = self._outputPickle
    
    def _outputCSV(self, dbResult, rootNodeId):
        for z in dbResult:
            id = z[0]
            x = z[1]
            # rootNodeId, nodeId, depth, type, code
            code = x[0]['code'].replace('\t', ' ')
            self.output('%s\t%s\t%s\t%s\t%s\n' % (rootNodeId, id, x[1], x[0]['type'], x[0]['code']))
            
    def _outputPickle(self, dbResult, nodeId):
        pythonAST = pythonASTFromDbResult(dbResult)
        pickle.dump(pythonAST, self.args.out, protocol=2)
        
    # @Override
    def streamStart(self):
        self.j = JoernSteps()
        self.j.connectToDatabase()

    # @Override
    def processLine(self, line):
        nodeId = int(line)
        
        query = """g.v(%d).astNodeToSubNodes().transform{ [it[0].id, it] }""" % (nodeId)

        dbResult = self.j.runGremlinQuery(query)
        
        self.outputHandler[self.args.output_format](dbResult, nodeId)
    
    
if __name__ == '__main__':
    tool = SubTree()
    tool.run()
