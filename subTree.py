#!/usr/bin/env python2

from joern.all import JoernSteps
from PipeTool import PipeTool

DESCRIPTION = """Prints all nodes of the AST rooted at the node with
the given id."""

class SubTree(PipeTool):
    
    def __init__(self):
        PipeTool.__init__(self, DESCRIPTION)

    # @Override
    def streamStart(self):
        self.j = JoernSteps()
        self.j.connectToDatabase()

    # @Override
    def processLine(self, line):
        nodeId = int(line)
        
        query = """ g.v(%d).astNodeToSubNodes()
        .transform{ [it[0].id, it[1], it[0].type, it[0].code] }""" % (nodeId)

        y = self.j.runGremlinQuery(query)
        for x in y:
            print '%s\t%s\t%s\t%s' % tuple(x)

if __name__ == '__main__':
    tool = SubTree()
    tool.run()
