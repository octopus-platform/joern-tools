from csvAST.CSVProcessor import CSVProcessor
from csvAST.CSVRowAccessors import getCSVRowLevel
from csvAST.PythonASTTreeNode import PythonASTTreeNode

"""
A CSVProcessor which converts an AST in CSV format to an internal
python representation allowing transformations to be performed.
"""

class CSVToPythonAST(CSVProcessor):
    def __init__(self):
        CSVProcessor.__init__(self)
        
        self.rootNode = PythonASTTreeNode(None)
        self.parentStack = []
        self.previousNode = self.rootNode
        
        self.defaultHandler = self.handleNode
    
    def handleNode(self, row):
        
        newNode = PythonASTTreeNode(row)
        
        # code below fails if level ever
        # increases by more than one at once
        level = int(getCSVRowLevel(row))
        if level > len(self.parentStack) - 1:
            # moved down one level, push previous node
            self.parentStack.append(self.previousNode)
        elif level < len(self.parentStack) -1:
            while(level < len(self.parentStack) - 1):
                self.parentStack.pop()
        else:
            # stayed on a level, no need to adjust parentStack
            pass
                
        parentNode = self.parentStack[-1]
        parentNode.appendChild(newNode)
        
        self.previousNode = newNode
    
    def getResult(self):
        return self.rootNode
    
def pythonASTFromDbResult(dbResult):
    csvRows = (_csvRow(z) for z in dbResult)
    return pythonASTFromCSV(csvRows)

def pythonASTFromCSV(csvRows):
    converter = CSVToPythonAST()
    converter.processCSVRows(csvRows)
    return converter.getResult()

def _csvRow(z):
    nodeId = z[0]
    x = z[1]
    if x[0]['operator'] == None:
        return '%s\t%s\t%s\t%s' % (nodeId, x[1], x[0]['type'], x[0]['code']) 
    else:
        return '%s\t%s\t%s\t%s' % (nodeId, x[1], x[0]['type'], x[0]['operator'])
        
