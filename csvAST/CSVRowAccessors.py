# TODO: adapt to output of subTree.py

NODE_ID = 0
LEVEL = 1
ROW_TYPE = 2
CODE = 3

def getCSVRowType(row):
    return row[ROW_TYPE]

def getCSVRowStartPos(row):
    return row[START_POS].split(':')

def getCSVRowEndPos(row):
    return row[END_POS].split(':')

def getCSVRowLevel(row):
    return row[LEVEL]

def getCSVRowCondition(row):
    return row[CONDITION]
