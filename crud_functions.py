import sqlite3

def initiate_db():
    conn = sqlite3.connect("products.db")
    curs = conn.cursor()
    curs.execute('''
    CREATE TABLE IF NOT EXISTS Products(
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    price INTEGER NOT NULL)
    ''')
    conn.commit()
    conn.close()
    connect = sqlite3.connect("Users.db")
    cursor = connect.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users(
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL,
    email TEXT NOT NULL,
    age INTEGER NOT NULL,
    balance INTEGER NOT NULL) 
    ''')
    connect.commit()
    connect.close()

def user_add(username, email, age):
    conn = sqlite3.connect("Users.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Users (username, email, age, balance) VALUES (?, ?, ?, ?)",
                   (username, email, age, 1000,))
    conn.commit()
    conn.close()

def is_included(username):
    with sqlite3.connect("Users.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM Users WHERE username = ?", (username, ))
        count = cursor.fetchone()[0]
        return count > 0

def get_all_products():
    with sqlite3.connect("products.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Products")
        products = cursor.fetchall()
    return products

def insert_prod():
    conn = sqlite3.connect("products.db")
    cursor = conn.cursor()
    for i in range(1, 5):
        cursor.execute("INSERT INTO Products (title, description, price) VALUES (?, ?, ?)",
                       (f"Продукт {i}", f"Описание {i}", i * 100))
    conn.commit()
    conn.close()



