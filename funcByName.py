#!/usr/bin/env python2

from py2neo import neo4j, gremlin
import sys, os
from joern.all import JoernSteps

def usage():
    print ('%s <lucene-query>' % (sys.argv[0]))

if __name__ == '__main__':

    j = JoernSteps()
    
    if len(sys.argv) == 2:
        luceneQuery = sys.argv[1]
        cmd = "queryNodeIndex('functionName:%s')" % (luceneQuery)
    else:
        usage()
        sys.exit()

    cmd += """
    .sideEffect{ name = it.functionName; loc = it.location; }
    .functionToFile().sideEffect{fname = it.filepath }
    .transform{ [name,fname, loc] }.toList()
    """
    
    y = j.executeGremlinCmd(cmd)
    for x in y:
        print '%s,%s,%s' % tuple(x)
