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
        cur.execute("CREATE TABLE Pages(id INTEGER PRIMARY KEY AUTOINCREMENT, "
                    "url STRING, count INT);")
        cur.execute("CREATE TABLE settings(name STRING, value STRING);")
        cur.execute('''INSERT INTO settings(name,value) 
                       VALUES("homepage","https://google.com"), 
                       ("collect statistic", "true")''')
        con.commit()

        cur.close()
        con.close()


def statistic(browser):
    """Change the database. Counts how many times a site has been visited."""
    con = sqlite3.connect('database.sql')
    cur = con.cursor()

    url = browser.url().toString()
    url = url.replace('www.', '').split('?')[0]

    result = cur.execute("SELECT COUNT(1), id FROM Pages WHERE url = ?",
                         (url,)).fetchone()

    if result[0] == 0:
        cur.execute("INSERT INTO Pages('url', 'count') VALUES(?, 1)",
                    (url,))
        con.commit()
    else:
        result = cur.execute("SELECT id, count FROM Pages WHERE url = ?",
                             (url,)).fetchone()
        page_id, count = result
        cur.execute("UPDATE Pages SET count = ? WHERE id = ?",
                    (count + 1, page_id))
        con.commit()

    cur.close()
    con.close()


def change_homepage(url):
    con = sqlite3.connect('database.sql')
    cur = con.cursor()

    cur.execute("UPDATE settings SET value = ? WHERE name = 'homepage'", (url,))
    con.commit()

    cur.close()
    con.close()


def change_variable(state):
    con = sqlite3.connect('database.sql')
    cur = con.cursor()

    cur.execute("UPDATE settings SET value = ? "
                "WHERE name = 'collect statistic'", (state,))
    con.commit()

    cur.close()
    con.close()


def clear_statistic():
    con = sqlite3.connect('database.sql')
    cur = con.cursor()

    cur.execute("DROP TABLE IF EXISTS Pages")
    cur.execute("CREATE TABLE Pages(id INTEGER PRIMARY KEY AUTOINCREMENT, "
                "url STRING, count INT);")
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

    cur.close()
    con.close()

    return result[0]


def get_variable():
    con = sqlite3.connect('database.sql')
    cur = con.cursor()

    result = cur.execute("SELECT value FROM settings "
                         "WHERE name = 'collect statistic'").fetchone()

    return True if result[0].lower() == 'true' else False


create_database()
