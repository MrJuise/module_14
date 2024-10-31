import sqlite3


def initiate_db():
    conn = sqlite3.connect("products.db")
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Products(
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    price INTEGER NOT NULL)
    ''')
    conn.commit()
    conn.close()

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

