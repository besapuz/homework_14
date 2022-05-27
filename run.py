import sqlite3

connect = sqlite3.connect('netflix.db')
cursor = connect.cursor()

sqlite_query = ("""
                SELECT 
                """)