#!/usr/bin/env python2

from joerntools.shelltool.TraversalTool import TraversalTool

DESCRIPTION = """ Run an arbitrary gremlin traversal. """

if __name__ == '__main__':
    tool = TraversalTool(DESCRIPTION)
    tool.run()
