"""
This script runs the DemoSite application using a development server.
"""

from os import environ
from EzrahotSite import app
import sqlite3

if __name__ == '__main__':
    HOST = environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT, debug=True)
