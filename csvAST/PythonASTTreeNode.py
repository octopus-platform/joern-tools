from CSVRowAccessors import CODE

class PythonASTTreeNode():
    def __init__(self, row):
        self.row = row
        self.children = []

    def appendChild(self, child):
        self.children.append(child)

    def applyFunc(self, f):
        self.row = f(self.row)
        for child in self.children:
            child.applyFunc(f)
    
    def __str__(self):
        retStr = '@+'
        if self.row != None:
            rowStr = str(self.row[CODE])
            rowStr = rowStr.replace('(', '\\(')
            rowStr = rowStr.replace(')', '\\)')
            retStr += rowStr
        for child in self.children:
            retStr += str(child)
        retStr += '+@'
        return retStr
