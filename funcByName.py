#!/usr/bin/env python2

import sys, os
from joern.all import JoernSteps

def usage():
    print ('%s <lucene-query>' % (sys.argv[0]))

if __name__ == '__main__':

    j = JoernSteps()
    j.connectToDatabase()
    
    for line in sys.stdin:
        luceneQuery = line.rstrip()
        cmd = "queryNodeIndex('functionName:%s')" % (luceneQuery)
        cmd += """
        .sideEffect{ name = it.functionName; loc = it.location; }
        .functionToFile().sideEffect{fname = it.filepath }
        .transform{ [name,fname, loc] }
        """
    
        y = j.runGremlinQuery(cmd)
        for x in y:
            print '%s\t%s:%s' % tuple(x)
