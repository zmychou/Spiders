
from urllib.request import urlopen
import csv

class CsvReader:

    def readOffset(self):
        '''get offset from each row'''
        for row in self.reader:
            urlStr = row[0].split('/')
            print(urlStr[len(urlStr) - 2])
            self.offset.add(urlStr[len(urlStr) - 2])
            self.lastOne = row[0]

    def debug(self):
        print('zmychou debug'+self.offset.pop())

        
    def __init__(self, fileName):
        '''doc here'''
        csvFile = open(fileName, 'rt')
        self.reader = csv.reader(csvFile)
        self.author = 'zmychou'
        self.offset = set()
        self.lastOne = 'zmychou'
        self.readOffset()
    
    def getOffset(self):
        return self.offset

    def getLastOne(self):
        return self.lastOne


