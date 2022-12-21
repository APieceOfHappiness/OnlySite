# my sql template

import sqlite3

db = sqlite3.connect('./cur/databases/users.db')

cur = db.cursor()
cur.execute("DROP TABLE IF EXISTS saved_forms")
cur.execute("""CREATE TABLE saved_forms(
    login TEXT,
    sex TEXT,
    date TEXT,
    profile TEXT,
    truth TEXT,
    coffee BOOL,
    not_coffee BOOL,
    addition_info TEXT
)""")
# cur.execute("DROP TABLE IF EXISTS users")
# cur.execute("""CREATE TABLE users(
#     login TEXT,
#     password TEXT
# )""")
# cur.execute("INSERT INTO users VALUES('Not Igor', '12321')")
# cur.execute("SELECT * FROM users")
# print(cur.fetchall())
db.commit()
db.close()
#
# db = sqlite3.connect('users.db')
# cur = db.cursor()
#
# cur.execute(""" CREATE TABLE IF NOT EXISTS users (
#     login TEXT,
#     password_1 TEXT,
#     password_2 TEXT
# )""")
#
# # name = "'Igor'"
# cur.execute('DELETE FROM users WHERE rowid > 3')
#
# cur.execute("SELECT * FROM users WHERE login=?", ['Igor'])
# print(cur.fetchall())
#
#
# db.commit()
#
# db.close()