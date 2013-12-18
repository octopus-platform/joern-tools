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
        
        
        self.argParser.add_argument('-a', '--attributes',
                                    nargs='+', type = str,
                                    help="""Attributes of interest""",
                                    default = [])

    # @Override
    def streamStart(self):
        self.j = JoernSteps()
        self.j.connectToDatabase()

    def outputRecord(self, record):
        id, node = record
        
        if type(node) == list:
            keys = self.args.attributes
            keyValPairs = [(keys[i] + ':' + str(node[i])) for i in range(len(keys))]
        else:
            keys = [k for k in node]
            keyValPairs = [str(k) + ':' + str(node[k]) for k in keys]
            keyValPairs.sort()
        
        keyValPairs = [k.replace('\t', '') for k in keyValPairs]
        
        self.output('%s\t%s\n' % (id, '\t'.join(keyValPairs)))

    # @Override
    def processLine(self, line):
        query = self._queryFromLine(line)

        if self.args.complete:
            query += '.transform{ [it.id, it]}'
        elif self.args.attributes != []:
            query += '.transform{ [it.id, ['
            for attr in self.args.attributes:
                query += 'it.%s,' % (attr)
            query = query[:-1]
            query += ']]}'
        else:
            query += '.transform{[it.id, []]}'
        
        y = self.j.runGremlinQuery(query)
        for x in y:
            self.outputRecord(x)

    # Override this
    def _queryFromLine(self, line):
        return ''
    
    
