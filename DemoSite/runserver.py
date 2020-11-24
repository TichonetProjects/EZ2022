"""
This script runs the DemoSite application using a development server.
"""

from os import environ
from DemoSite import app
import sqlite3

def first_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print("Can connect to the server!")

        cursor = conn.cursor()

        cursor.execute('''CREATE TABLE IF NOT EXISTS users
                      (name text, email text, username text,  pass text)''')
        conn.commit()
    
        for row in cursor.execute('SELECT * FROM users ORDER BY name'):
            print(row)

        conn.close()
    
    finally:
        pass


if __name__ == '__main__':
    first_connection(r"database.db")
    HOST = environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT, debug=True)