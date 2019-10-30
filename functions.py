import os
import sqlite3


def get_path(directory, file):
    return os.path.join(directory, file)


def get_image(image):
    return get_path('images', image)


def get_homepage():
    con = sqlite3.connect('data.sql')
    cur = con.cursor()
    result = cur.execute("SELECT value FROM settings "
                         "WHERE name='homepage'").fetchone()
    return result[0]
