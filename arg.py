#!/usr/bin/env python2

import sys
from joern.all import JoernSteps

def usage():
    print ('%s <callee> <argument>' % (sys.argv[0]))

if __name__ == '__main__':
    
    j = JoernSteps()
    j.connectToDatabase()

    if len(sys.argv) != 3:
        usage()
        sys.exit()

    query = """ getArgumentNTo("%s", "%d").code """ % (sys.argv[1], int(sys.argv[2]) - 1)
    
    y = j.runGremlinQuery(query)
    for x in y:
        print x
