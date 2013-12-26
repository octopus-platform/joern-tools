#!/usr/bin/env python2

from joerntools.shelltool.JoernTool import JoernTool
import pygraphviz as pgv

DESCRIPTION = """Retrieve the AST rooted at the node with the given
id. The default output format is graphviz's 'dot'.
"""

class SubTree(JoernTool):
    
    def __init__(self):
        JoernTool.__init__(self, DESCRIPTION)
    
    # @Override
    def processLine(self, line):
        nodeId = int(line)
        
        nodes = self._getASTNodes(nodeId)
        edges = self._getASTEdges(nodeId)
        
        G = self._createDotGraph(nodes, edges)
        self._outputGraph(G, line)
    
    def _getASTNodes(self, nodeId):
        query = """g.v(%d).functionToASTRoot()
        .astNodeToSubNodes()
        """% (nodeId)
        
        return self._runGremlinQuery(query)
    
    def _getASTEdges(self, nodeId):
        query = """g.v(%d).functionToASTRoot()
        .astNodeToSubNodes().outE('IS_AST_PARENT')
        """% (nodeId)
        
        return self._runGremlinQuery(query)

    def _createDotGraph(self, nodes, edges):
        G = pgv.AGraph()
        
        for n in nodes:
            nodeId = n._id
            G.add_node(nodeId)
            node = G.get_node(nodeId)
            node.attr['label'] = self._attributesAsString(n)
    
        for e in edges:
            startNode = e.start_node._id
            endNode = e.end_node._id
            G.add_edge(startNode, endNode)
            
        return G
    
    def _attributesAsString(self, n):
        return '\n'.join( [k + ':' + str(n[k]).replace('\n',' ') for k in n])
    
    def _outputGraph(self, G, line):
        self.output('//' + line + '\n')
        self.output(str(G) + '\n')

    
if __name__ == '__main__':
    tool = SubTree()
    tool.run()
