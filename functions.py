import os
import sqlite3


def create_database():
    path = os.getcwd()
    files_in_path = os.listdir(path)

    if 'database.sql' not in files_in_path:
        with open('database.sql', mode='w', encoding='utf-8') as file:
            pass

        con = sqlite3.connect('database.sql')
        cur = con.cursor()
        cur.execute("CREATE TABLE Pages(id INT, url STRING, count INT);")
        cur.execute("CREATE TABLE settings(name STRING, value STRING);")
        cur.execute('''INSERT INTO settings(name,value) 
                       VALUES("homepage","https://www.google.com")''')
        con.commit()

        cur.close()
        con.close()


def get_path(directory, file):
    return os.path.join(directory, file)


def get_image(image):
    return get_path('images', image)


def get_homepage():
    con = sqlite3.connect('database.sql')
    cur = con.cursor()
    result = cur.execute("SELECT value FROM settings "
                         "WHERE name='homepage'").fetchone()
    return result[0]


create_database()
