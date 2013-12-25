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

    # @Override
    def processLine(self, line):
        query = self._queryFromLine(line)
        query += self._outputTransformTerm()

        y = self.j.runGremlinQuery(query)
        for x in y:
            self.outputRecord(x)

    def _outputTransformTerm(self):
        """
        Calculate the output transformation term based on command line
        options.
        """
        if self.args.complete:
            return '.transform{ [it.id, it]}'
        elif self.args.attributes != []:
            term = '.transform{ [it.id, ['
            for attr in self.args.attributes:
                term += 'it.%s,' % (attr)
            term = term[:-1]
            term += ']]}'
            return term
        else:
            return '.transform{[it.id, []]}'

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

    # Override this
    def _queryFromLine(self, line):
        return ''
    
