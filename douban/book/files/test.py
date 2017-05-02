
from CsvReader import CsvReader

def test():
    c = CsvReader('ttt.csv')
    sets = c.getOffset()
    print(sets)

test()
