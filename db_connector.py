import sqlite3

class database:

    def __init__(self):
        self.DBname = "database.db"

    def connect(self):
        conn = None
        try:
            conn = sqlite3.connect(self.DBname)
        except Exception as e:
            print(e)
        return conn
    
    def queryDB(self, command, params=[]):
        conn = self.connect()
        cur = conn.cursor()
        cur.execute(command,params)
        result = cur.fetchall()
        self.disconnect(conn)
        return result
    
    def updateDB(self,command, params=[]):
        conn = self.connect()
        cur = conn.cursor()
        cur.execute(command,params)
        conn.commit()
        result = cur.fetchall()
        self.disconnect(conn)
        return result
    
    def disconnect(self, conn):
        conn.close()
        