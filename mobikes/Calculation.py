#!/usr/bin/env python3

import sqlite3
from Sqlite import Sqlite
import math


class Calculation:

    def __init__(self, db=None, sql=None):
    
        # The radius of Earth,with the unit of meter
        self.R = 6371004      
        self.PI = 3.14 
        if sql is not None:
            self.database = sql
        else :
            self.database = Sqlite(db)
    
    def calcDistance(self, lat1, lng1, lat2, lng2):
        latA = 90 - lat1
        latB = 90 - lat2
        c = math.sin(latA) * math.sin(latB) * math.cos(lng1 - lng2) \
            + math.cos(latA) * math.cos(latB)   
        if c > 1:
            c = 1;
        d = self.R * math.acos(c) * self.PI / 180
        return d
        
    def doCalculate(self, table, colName,tag1, tag2):
        tag = tag1#str(input('Input the origin tag:'))
        rows = self.database.select(['Bikes'], ['id', 'lng', 'lat'], 'tag=\'' + tag + '\'')
        tag = tag2#str(input('Input the dest tag:'))
        print('Calculating.......')
        for row in rows:
            r = self.database.select(['Bikes'], ['lng', 'lat'], 'tag=\'' + tag + '\' and id=' + row[0])
            try:
                rr = r.fetchone()
                res = self.calcDistance(row[2], row[1], rr[1], rr[0])
                res = int(res)
                self.database.update(table, [[colName, str(res)]], 'id=' + row[0],False)
                print('Restore '+row[0]+ ' move distance ' + str(res))
            except TypeError as e:
                print(e)
        self.database.conn.commit()
        print('Data has ready........')
        
    def prepareToCal(self):

        tableName = 'Distances'
        self.database.createTable(tableName, ['id'], ['id'])
        tag1 = input('Input the first tag you want to fecth:')
        tag2 = input('Input the second tag you want to fecth:')
        tags = [tag1, tag2]
        for tag in tags:
#            print(self.database.select(['Bikes'], ['count(id)', 'tag'], 'tag=\'' + tag + '\'').fetchone()[0])

            print('Selecting data specifid by ' + tag)
            rows = self.database.select(['Bikes'], ['id'], 'tag=\'' + tag + '\'')
            for row in rows:
                try:
                    self.database.insert(tableName, ['id'], [row[0]],False)
                except Exception as e:
                    pass
                    #print(e)
        self.database.conn.commit()
        col = str(input('Input the column name you want to insert:'))
        try:
            self.database.alterTable(tableName, str(col))
        except Exception as e:
            print(e)
        self.doCalculate(tableName, col, tag1, tag2)
        return col
        
if __name__=='__main__':
    cal = Calculation('ShareBikes.db')
    cal.prepareToCal()
