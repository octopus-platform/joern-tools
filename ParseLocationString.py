
import argparse

class ParseLocationString(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        
        try:
            (filename,startLine,stopLine,startIndex,stopIndex) = values.split(':')
            startLine = int(startLine)
            stopLine = int(stopLine)
            startIndex = int(startIndex)
            stopIndex = int(stopIndex)
        except ValueError:
            parser.error("invalid location string")
        
        setattr(namespace, 'filename', filename)
        setattr(namespace, 'location', '%d:%d:%d:%d' % (startLine, stopLine, startIndex, stopIndex))
        setattr(namespace, 'startLine', startLine)
        setattr(namespace, 'stopLine', stopLine)
        setattr(namespace, 'startIndex', startIndex)
        setattr(namespace, 'stopIndex', stopIndex)
        
