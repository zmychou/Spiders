#!/usr/bin/python

from Sqlite import Sqlite 
from Calculation import Calculation

class Analysis:

    def __init__(self, db):

        self.database = Sqlite(db)

    def getTotal(self):
        """ Get the total number of bike which group by tag """
        #tag = input('Input a tag:')
        rows = self.database.select(['Bikes'], ['count(id)', 'tag'], 'id group by tag')
        for row in rows:
            print(row)
    
    def getUnActiveBikes(self):
        pass
        
    def getActiveBikesNum(self):
        
        #cal = Calculation(sql=self.database)
        #col = cal.prepareToCal()
        col = 'col0318night2day'#cal.prepareToCal()
        print('Total bikes is ' + str(self.database.select(['Distances'], ['count(id)', col]).fetchone()[0]))
        print('Total not active bikes is ' + str(self.database.select(['Distances'], ['count(id)', col], col + '=0').fetchone()[0]))
        slice = []
        slice.append([self.database.select(['Distances'], ['count(id)', col], col + ' between 0 and 100').fetchone()[0], 0, 100])
        step = 250
        for i in range(100, 10000, step):
            slice.append([self.database.select(['Distances'], ['count(id)', col], col + ' between ' + str(i) + ' and ' + str(i + step)).fetchone()[0], i, i+ step])
        slice.append([self.database.select(['Distances'], ['count(id)', col], col + ' between 10000 and 30000').fetchone()[0], 10000, 30000])
        print(slice)
        print('Get slice done.....')
        return slice
            
    def getTypeShare(self):
    
        tag = input('Input a tag:')
        rows = self.database.select(['Bikes'], ['count(id)', 'tag'], 'tag=\'' + tag + '\'')
        total = rows.fetchone()[0]
        rows = self.database.select(['Bikes'], ['count(id)', 'tag'], 'tag=\'' + tag + '\' and bikeType=2')
        type2 = rows.fetchone()[0]
        type1 = total - type2
        print('Total is ' + str(total) + ', type2 is ' + str(type2))
        arr = [type1, type2, total]
        return arr

    def createPoints(self):
        """ Select bike's data from database and format to a file which will be used to assosiate with Baidu Javascript API 
        to generate the heat map 
        The formated data store in points.txt, visit http://lbsyun.baidu.com/index.php?title=jspopular for more details
        of heat map generating  """
        tag = input('Input a tag:')
        self.database.createView('Bikes', 'TmpBikes', ['id', 'region'], 'tag=\'' + tag + '\'')
        rows = self.database.select(['TmpBikes'], ['count(id)', 'region'], 'id group by region')
        txt = open('points.txt', 'w')
        for row in rows:
            rowParcel = row[1].split(',')
            txt.write('{"lng":' + rowParcel[1] + ',"lat":' + rowParcel[0] \
                    + ',"count":' + str(row[0]) + '},\n')
                    
        print('point.txt has been generated......')

analyser = Analysis('ShareBikes.db')
analyser.getActiveBikesNum()
