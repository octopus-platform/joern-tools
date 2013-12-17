#!/usr/bin/env python2

import sys, os
from PipeTool import PipeTool
from joern.all import JoernSteps

class LookupTool(PipeTool):
    
    def __init__(self, DESCRIPTION):
        PipeTool.__init__(self, DESCRIPTION)

        self.argParser.add_argument('-c', '--complete',
                                    action='store_true',
                                    default=False,
                                    help = """ Output the complete
                                    node, not just its ID.""")
                                     
    # @Override
    def streamStart(self):
        self.j = JoernSteps()
        self.j.connectToDatabase()

    def outputRecord(self, record):
        id, node = record
        keys = [k for k in node]
        keys.sort()
        keyValPairs = [str(k) + ':' + str(node[k]) for k in keys]
        self.output('%s\t%s\n' % (id, '\t'.join(keyValPairs)))

    # @Override
    def processLine(self, line):
        query = self._queryFromLine(line)

        if self.args.complete:
            query += '.transform{ [it.id, it]}'
        else:
            query += '.transform{[it.id, []]}'
        
        y = self.j.runGremlinQuery(query)
        for x in y:
            self.outputRecord(x)

    # Override this
    def _queryFromLine(self, line):
        return ''
    
    
