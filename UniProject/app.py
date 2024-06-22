from flask import Flask, redirect, render_template, url_for, request, session, flash, get_flashed_messages

from flask_sqlalchemy import SQLAlchemy

from werkzeug.security import generate_password_hash, check_password_hash

import requests
from bs4 import BeautifulSoup
import time
import random
import sqlite3


#####
conn = sqlite3.connect('ComicsDatabase.sqlite')
conn.row_factory = sqlite3.Row
c = conn.cursor()

c.execute('''
    CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title VARCHAR(250),
        price FLOAT,
        status VARCHAR(100)
    )
''')

res = ''
page = 1
while page <= 5:
    url = f'https://parsek1.com/collections/all-comics?page={page}'
    page += 1

    response = requests.get(url)

    content = response.text
    soup = BeautifulSoup(content, 'html.parser')

    product_section = soup.find('div', class_='collection')
    comic_spec = product_section.find_all('li', class_='grid__item')

    for comic in comic_spec:
        # title
        info = comic.find('div', class_='card__content')
        title = info.a.text.strip()

        # price
        price_info = comic.find('span', class_='price-item price-item--regular')
        price = price_info.text.strip()

        # status
        bottom_left = comic.find('div', class_='card__badge bottom left')
        status = bottom_left.text.strip()
        if status != 'Sold out':
            status = 'In stock'

        c.execute("INSERT INTO books (title, price, status) VALUES (?, ?, ?)", (title, price, status))
        conn.commit()
    # time.sleep(random.randint(15, 20))

#####

app = Flask(__name__)
app.config['SECRET_KEY'] = 'agsad457ansk1'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ComicsDatabase.sqlite'
db = SQLAlchemy(app)

class user(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(80), unique=True, nullable=False)
    username = db.Column(db.String(80), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(80), nullable=False)

class books(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), nullable=False)

with app.app_context():
    db.create_all()

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/login', methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        global em
        email = request.form['email']
        pasw = request.form['password']

        if email == "" or pasw == "":
            flash('რომელიმე ველი ცარიელია', 'error')
        else:
            # pers_e = ""
            pers_p = False
            pers_e = user.query.filter_by(email = email).all()

            all_info = user.query.all()
            for i in all_info:
                if  check_password_hash(i.password, pasw) == True:
                    pers_p = True


            if pers_e and pers_p:
                em = email
                session['email'] = email
                return redirect('/home')
            else:
                flash('ელფოსტა ან პაროლი არასწორია', 'error')

    return render_template('login.html')

@app.route('/signup', methods = ['POST', 'GET'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        address = request.form['address']
        pasw = request.form['password']

        if email == "" or username == "" or pasw == "" or address == "":
            flash("რომელიმე ველი ცარიელია", 'error')
        else:
            flag = True
            all_info = user.query.all()
            for i in all_info:
                if i.email == email:
                    flag = False
                    break
            if flag == True:
                user1 = user(email = email, username = username, address = address, password = generate_password_hash(pasw))
                db.session.add(user1)
                db.session.commit()
                flash('თქვენ წარმატებით დარეგისტრირდით!')
            else:
                flash('მითითებული ელფოსტა უკვე გამოყენებულია', 'error')

    return render_template('signup.html')

@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect('/home')

@app.route('/profile')
def profile():
    name = ""
    addr = ""

    info = user.query.all()
    for i in info:
        if i.email == em:
            name = i.username
            addr = i.address

    return render_template('profile.html', name = name, email = em, address = addr)

@app.route('/parsek')
def parsek():
    return redirect('https://parsek1.com/')

@app.route('/testApi')
def testApi():

    all_comics = books.query.all()

    return render_template('testApi.html', all_comics=all_comics)

####
@app.errorhandler(404)
def page_not_found(error):
    return render_template('err.html'), 404


if __name__ == '__main__':
    app.run(debug=True)
