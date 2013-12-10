
import argparse

def parseLocationString(values):
    x = values.split(':')
    for i in range(1,len(x)):
        x[i] = int(x[i])
    return x

class ParseLocationString(argparse.Action):
    
    def __call__(self, parser, namespace, values, option_string=None):
        
        try:
            parsedLine = parseLocationString(values)
            (filename, startLine, stopLine, startIndex, stopIndex) = parsedLine
        except ValueError:
            parser.error("invalid location string")
        
        setattr(namespace, 'filename', filename)
        setattr(namespace, 'location', '%d:%d:%d:%d' % tuple(parsedLine[1:]) )
        setattr(namespace, 'startLine', startLine)
        setattr(namespace, 'stopLine', stopLine)
        setattr(namespace, 'startIndex', startIndex)
        setattr(namespace, 'stopIndex', stopIndex)
        
