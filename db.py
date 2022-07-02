from sqlite3 import *
import os
from pathlib import Path

################################################################################################################################################
def get_akk(id,login,password,name):
    db = connect('akkountall/akkount.db')
    cur = db.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS user(
        id INT,
        login TEXT PRIMARY KEY,
        password TEXT,
        price1  INT,
        asses INT,
        status INT,
        first_name TEXT)''')
    db.commit()
    cur.execute(f'SELECT login FROM user WHERE login="{login}"')
    if cur.fetchone() == None:
        
        -
        db.commit()
        return True
    else:
        return False
        



    


def get_user():
    db = connect(f'akkountall/akkount.db')
    cur = db.cursor()
    cur.execute('SELECT status FROM user WHERE status=0 ')
    if cur.fetchone() == None:
        return False
    else:
        for  i in cur.execute(f'SELECT id,login,password FROM user WHERE status=0'):
            return i[0],i[1],i[2]


def get_price_asses(price1,asses,login,id):
    db = connect('akkountall/akkount.db')
    cur = db.cursor()
    cur.execute(f'UPDATE user SET status = 1 WHERE login = "{login}"')
    cur.execute(f'UPDATE user SET asses = {asses} WHERE login = "{login}"')
    cur.execute(f'UPDATE user SET price1 = {price1} WHERE login = "{login}"')
    db.commit()
    cur.close()
    db.close()
    db = connect('priceall/price.db')
    cur = db.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS users(
        id INT PRIMARY KEY,
        priceall INT,
        purchases INT,
        btc  TEXT)''')
    cur.execute(f'SELECT id FROM users WHERE id = {id}')
    if cur.fetchone() is None:
        cur.execute('INSERT INTO users VALUES(?,?,?,?)',(id,price1,1,'NONE'))
        db.commit()
    else:
        for i in cur.execute(f'SELECT priceall FROM users WHERE id = {id}'):
            balance = i[0]
        for i in cur.execute(f'SELECT purchases FROM users WHERE id = {id}'):
            pur = i[0]  
          
        cur.execute(f'UPDATE users SET priceall = {int(balance) + int(price1)} WHERE id = {id}')
        cur.execute(f'UPDATE users SET purchases = {int(pur)+ 1} WHERE id = {id}')
        
        db.commit()


def delete():
    if get_user() == False:
        pass
    else:
        login,password,id = get_user()
        db = connect(f'akkountall/akkount.db')
        cur = db.cursor()
        cur.execute(f'DELETE FROM user WHERE login = "{login}"')
        db.commit()


################################################################################################################################################


def get_treatment():
    tex = dict()
    db = connect(f'akkountall/akkount.db')
    cur = db.cursor()
    cur.execute('SELECT status FROM user WHERE status = 1 ')
    if cur.fetchone() is None:
        return tex
    else:
        for  b in cur.execute(f'SELECT login,password FROM user WHERE status=1'):
            login = b[0]
            password = b[1]
            tex.update({f'{login}':f'{password}'})
        return tex


def send_assept():
    db = connect(f'akkountall/akkount.db')
    cur = db.cursor()
    cur.execute('SELECT status FROM user WHERE status = 1 ')
    if cur.fetchone() is None:
        return False
    else:
        for  b in cur.execute(f'SELECT login,password,asses,price1 FROM user WHERE status=1'):
            login = b[0]
            password = b[1]
            asses = b[2]
            return  login,password,asses,b[3]


def get_treat():
    stat = 2
    db = connect(f'akkountall/akkount.db')
    cur = db.cursor()
    for  b in cur.execute(f'SELECT id,asses,login FROM user WHERE status=1'):
        id = b[0]
        asses = b[1]
        login = b[2]
        cur.execute(f'UPDATE user SET status = {stat} WHERE login = "{login}"')
        db.commit()
        return id, asses,login
    

    


def get_money(id):
    db = connect('priceall/price.db')
    cur = db.cursor()
    cur.execute(f'SELECT id FROM users WHERE id = {id}')
    if cur.fetchone() is None:
        return False
    else:
        for i in cur.execute(f'SELECT priceall FROM users WHERE id = {id}'):
            money = i[0]
        for i in cur.execute(f'SELECT purchases FROM users WHERE id = {id}'):
            pur= i[0]                

        return money,pur


def send_nick(id,name):
    db = connect('priceall/price.db')
    cur = db.cursor()
    cur.execute(f'UPDATE users SET btc = "{name}" WHERE id = {id}')
    db.commit()

def get_nickname(id):
    db = connect('priceall/price.db')
    cur = db.cursor()
    cur.execute(f'SELECT btc FROM users WHERE id = {id}')
    if cur.fetchone() == 'False':
        return False
    else:
        for i in cur.execute(f'SELECT btc FROM users WHERE id = {id}'):
            return i[0]


def get_user_assess_price1(login):
    db = connect(f'akkountall/akkount.db')
    cur = db.cursor()
    cur.execute('SELECT status FROM user WHERE status = 1 ')
    if cur.fetchone() is None:
        pass
    else:
        for  b in cur.execute(f'SELECT asses,price1 FROM user WHERE login="{login}"'):
            asses= b[0]
            price = b[1]
            return asses,price


def get_user1_price1(login,price):
    db = connect(f'akkountall/akkount.db')
    cur = db.cursor()
    cur.execute(f'UPDATE user SET price1 = {price} WHERE login = "{login}"')
    db.commit()


def get_status(login):
    db = connect(f'akkountall/akkount.db')
    cur = db.cursor()
    for i in cur.execute(f'SELECT id FROM user WHERE login = "{login}" '):
        return i[0]

def delete1(login):
    db = connect(f'akkountall/akkount.db')
    cur = db.cursor()  
    cur.execute(f'DELETE FROM user WHERE login = "{login}"')
    db.commit()


def get_user_id(log):
    login = log
    stat  = 2
    db = connect(f'akkountall/akkount.db')
    cur = db.cursor() 
    cur.execute(f'UPDATE user SET status = {stat} WHERE login = "{login}"')
    db.commit()
    for i in cur.execute(f'SELECT id,price1,asses FROM user WHERE login = "{login}" '):
        return i[0],i[1],i[2]


def get_btc_wallet(id):
    db = connect('priceall/price.db')
    cur = db.cursor()
    for i in cur.execute(f'SELECT btc FROM users WHERE id = {id}'):
        return i[0]


def get_user_id_btc(log):
    db = connect(f'akkountall/akkount.db')
    cur = db.cursor() 
    for i in cur.execute(f'SELECT id FROM user WHERE login = "{log}" '):
        return i[0]


def get_name():
    db = connect('akkountall/akkount.db')
    cur = db.cursor()
    for i in cur.execute('SELECT first_name FROM user WHERE status=0'):
        return i[0]


def get_name_after(login):
    db = connect('akkountall/akkount.db')
    cur = db.cursor()
    for i in cur.execute(f'SELECT first_name FROM user WHERE login="{login}"'):
        return i[0]


def get_purchases(id):
    db = connect('priceall/price.db')
    cur = db.cursor()
    try:
        for i in cur.execute(f'SELECT purchases FROM users WHERE id = {id} '):
            return i[0]
    except:
        return False


def get_purchases1(login):
    db = connect('akkountall/akkount.db')
    cur = db.cursor()
    for i in cur.execute(f'SELECT id FROM user WHERE login="{login}"'):
        id = i[0]

    cur.close()
    db.close()
    db = connect('priceall/price.db')
    cur = db.cursor()
    try:
        for i in cur.execute(f'SELECT purchases FROM users WHERE id = {id} '):
            return i[0]
    except:
        return False


    
def get_pur(id):
    db = connect('priceall/price.db')
    cur = db.cursor()
    try:
        for i in cur.execute(f'SELECT purchases,priceall FROM users WHERE id = {id} '):
            return i[0],i[1]
    except:
        return False


def get_treatment1():
    tex = dict()
    db = connect(f'akkountall/akkount.db')
    cur = db.cursor()
    cur.execute('SELECT status FROM user WHERE status = 2 ')
    if cur.fetchone() is None:
        return tex
    else:
        for  b in cur.execute(f'SELECT login,password FROM user WHERE status=2'):
            login = b[0]
            password = b[1]
            tex.update({f'{login}':f'{password}'})
        return tex


def get_user_price2(login):
    db = connect(f'akkountall/akkount.db')
    cur = db.cursor()
    cur.execute('SELECT status FROM user WHERE status = 1 ')
    for  b in cur.execute(f'SELECT price1 FROM user WHERE login="{login}"'):
        price = b[0]
        return price
