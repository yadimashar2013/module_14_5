import sqlite3


def initiate_db():
    connection = sqlite3.connect('initiate.db')
    cursor = connection.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users(
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    price INTEGER NOT N
    );
    ''')
    texts = [
        'Cохранить молодость кожи и здоровье глаз.',
        'Необходим для нормальной работы нервной, сердечно-сосудистой систем.',
        'Необходим для поддержания жизнедеятельности.',
        'Необходим для поддержки здоровья костей и иммунной системы организма.'
    ]
    produkts = ['Витамин А', 'Витамин В', 'Витамин С', 'Витамин D']
    prices = ['100', '200', '300', '400']


    cursor.execute('INSERT INTO Products(title, description, price) VALUES (?, ?, ?)',
                   (f'{produkts[0]}', f'{texts[0]}', f'{prices[0]}'))
    cursor.execute('INSERT INTO Products(title, description, price) VALUES (?, ?, ?)',
                   (f'{produkts[1]}', f'{texts[1]}', f'{prices[1]}'))
    cursor.execute('INSERT INTO Products(title, description, price) VALUES (?, ?, ?)',
                   (f'{produkts[2]}', f'{texts[2]}', f'{prices[2]}'))
    cursor.execute('INSERT INTO Products(title, description, price) VALUES (?, ?, ?)',
                   (f'{produkts[3]}', f'{texts[3]}', f'{prices[3]}'))
    connection.commit()
    connection.close()


def get_all_products():
    connection = sqlite3.connect('initiate.db')
    cursor = connection.cursor()
    cursor.execute('SELECT title FROM Products')
    title_list = cursor.fetchall()
    cursor.execute('SELECT description FROM Products')
    descriptions_list = cursor.fetchall()
    cursor.execute('SELECT price FROM Products')
    prices_list = cursor.fetchall()
    return [title_list, descriptions_list, prices_list]

connection = sqlite3.connect('initiate_Users.db')
cursor = connection.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS Users(
id INTEGER PRIMARY KEY,
username TEXT NOT NULL,
email TEXT NOT NULL,
age INTEGER NOT NULL,
balance INTEGER NOT NULL
);
''')


def is_included(username):
    connection = sqlite3.connect('initiate_Users.db')
    cursor = connection.cursor()
    s = cursor.execute('SELECT username FROM Users').fetchall()
    connection.commit()
    return (username,) in s


def add_user(username, email, age):
    connection = sqlite3.connect('initiate_Users.db')
    cursor = connection.cursor()
    cursor.execute(f'INSERT INTO Users (username, email, age, balance) VALUES("{username}", "{email}", "{age}", 1000)')
    connection.commit()


connection.commit()
connection.close()


