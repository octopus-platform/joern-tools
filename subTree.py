#!/usr/bin/env python2

from joern.all import JoernSteps
from PipeTool import PipeTool

from csvAST.CSVToPythonAST import CSVToPythonAST

DESCRIPTION = """Prints all nodes of the AST rooted at the node with
the given id. The default output format is a CSV format similar to
that used of CodeSensor."""

class SubTree(PipeTool):
    
    def __init__(self):
        PipeTool.__init__(self, DESCRIPTION)

        self.argParser.add_argument('-s', '--sexpr',
            action='store_true', help="""return an s-expression for the
            sub tree, not CSV rows.""")

    # @Override
    def streamStart(self):
        self.j = JoernSteps()
        self.j.connectToDatabase()

    # @Override
    def processLine(self, line):
        nodeId = int(line)
        
        query = """g.v(%d).astNodeToSubNodes().transform{ [it[0].id, it] }""" % (nodeId)

        dbResult = self.j.runGremlinQuery(query)
        if self.args.sexpr:
            self._outputSExpressions(dbResult)
        else:
            self._outputAllNodes(dbResult)

    def _outputAllNodes(self, dbResult):
        for z in dbResult:
            nodeId = z[0]
            x = z[1]
            print '%s\t%s\t%s\t%s' % (nodeId, x[1], x[0]['type'], x[0]['code'])

    def _outputSExpressions(self, dbResult):
        csvRows = (self._csvRow(z) for z in dbResult)
        converter = CSVToPythonAST()
        converter.processCSVRows(csvRows)
        print converter.getResult()
    
    def _csvRow(self, z):
        nodeId = z[0]
        x = z[1]
        if x[0]['operator'] == None:
            return '%s\t%s\t%s\t%s' % (nodeId, x[1], x[0]['type'], x[0]['code']) 
        else:
            return '%s\t%s\t%s\t%s' % (nodeId, x[1], x[0]['type'], x[0]['operator'])
        

if __name__ == '__main__':
    tool = SubTree()
    tool.run()
