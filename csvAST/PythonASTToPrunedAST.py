from csvAST.PythonASTTreeNode import PythonASTTreeNode
from csvAST.PythonASTProcessor import PythonASTProcessor

PRUNED = 'pruned'
prunedRow = [PRUNED, '(*)', '(*)', '(*)', '']

class PythonASTToPrunedAST(PythonASTProcessor):
    def __init__(self):
        PythonASTProcessor.__init__(self)
        self.nodeTypesOfInterest = []
        self.keepNodesOfInterest = False

    def nodeHandler(self, node):
        self.prunedTree = self._pruneTree(node)
        return False

    def _pruneTree(self, node):
        return self._prune(node)
    
    def _prune(self, node):
        if self._mustPruneNode(node):
            r = prunedRow
        else:
            r = node.row
        
        newRootNode = PythonASTTreeNode(r)
        self.addPrunedChildren(node, newRootNode)
        return newRootNode
    
    def addPrunedChildren(self, node, root):
        for child in node.children:
            self._attachPruned(child, root)

    def _attachPruned(self, node, root):

        if self._mustPruneNode(node):
            self._pruneNode(node, root)
        else:
            newNode = PythonASTTreeNode(node.row)
            self.addPrunedChildren(node, newNode)
            root.appendChild(newNode)

    def _mustPruneNode(self, node):
        nodeType = node.row[0]
        if (len(self.nodeTypesOfInterest) == 0): return False
        if self.keepNodesOfInterest and (nodeType in self.nodeTypesOfInterest): return False
        if (not self.keepNodesOfInterest) and (not(nodeType in self.nodeTypesOfInterest)): return False
        return True

    def getPrunedTree(self):
        return self.prunedTree
