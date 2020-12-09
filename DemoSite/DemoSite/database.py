import sqlite3

class Database():
    _instance = None
    _connection = None

    @staticmethod
    def getInstance():
        if Database._instance == None:
            Database("database.db")
        
        return Database._instance

    def __init__(self, filename):
        
        if Database._instance == None:
            Database._instance = self
            self.connection = sqlite3.connect(filename)

            cursor = self.connection.cursor()

            cursor.execute('''CREATE TABLE IF NOT EXISTS users
                      (ID int NOT NULL,first_name text, last_name text, email text,  password text, class text, type text, PRIMARY KEY (ID))''')
            
            self.connection.commit()
        
        else:
            raise Exception("This class is a singleton!")

    
    def getConnection(self):
        return self.connection

database = Database.getInstance()

print(database.getConnection())