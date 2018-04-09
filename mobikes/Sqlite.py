#/usr/bin/env python3

import sqlite3

class Sqlite:

    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.cursor = self.conn.cursor()
        
    def createTable(self, tableName, cols, primaryKeys = []):
        clause = 'CREATE TABLE IF NOT EXISTS ' + tableName + '('
        for col in cols:
            clause += col + ','
        if len(primaryKeys) > 0:
            clause += 'PRIMARY KEY('
            for key in primaryKeys:
                clause += key + ','
        clause = clause.rstrip(',')
        clause += '))'
        self.cursor.execute(clause)

    def alterTable(self, table, col):
        clause = 'ALTER TABLE ' + table + ' ADD COLUMN ' + col + ' INTEGER'
        self.cursor.execute(clause)
    
    def createView(self,table, view, cols, selection=None):
        clause = "CREATE TEMP VIEW " + view + " ("
        for col in cols:
            clause += col + ','
        clause = clause.rstrip(',')
        clause += ') AS SELECT '
        for col in cols:
            clause += col + ','
        clause = clause.rstrip(',')
        clause += ' from ' + table
        if selection is not None:
            clause += ' WHERE ' +selection
        self.cursor.execute(clause)

            
    def insert(self, table, cols, values, commit=True):
        """ Construct the sql clause and then execute it """
        
        clause = 'INSERT INTO ' + table + ' ('
        
        for col in cols:
            clause += col + ',' 
        clause = clause.rstrip(',')
        clause += ') VALUES ('
        for value in values:
            clause += str(value) + ','
        clause = clause.rstrip(',')
        clause += ')'
        self.cursor.execute(clause)
        
        if commit is True:
            self.conn.commit()
            
        print(clause)

    def select(self, table, projection, selection = None, args = None):
        
        clause = "SELECT "
        for proj in projection:
            clause += proj + ','
        
        clause = clause.rstrip(',')
        clause += ' FROM '
        for t in table:
            clause += t + ','
        clause = clause.rstrip(',') 
        if selection is not None:
            clause += ' WHERE ' + selection
 #           return self.cursor.execute(clause , args)
 #       else :
 
        #print(clause)
        cur = self.conn.cursor()
        return cur.execute(clause)
        
    def update(self, table, colVal,selection, commit=True):
        """ Construct the sql clause and then execute it """
        
        clause = 'UPDATE ' + table + ' SET '
        
        for col in colVal:
            clause += col[0] + '=' + col[1]
        clause = clause.rstrip(',')
        clause += ' WHERE ' + selection
        self.cursor.execute(clause)
        
        if commit is True:
            self.conn.commit()
            
            
    def close(self):
        
        self.conn.close()
