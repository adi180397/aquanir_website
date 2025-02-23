from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# Database connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="aquanir"
)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/order', methods=['POST'])
def order():
    product = request.form['product']
    quantity = request.form['quantity']
    distributor = request.form['distributor']

    cursor = db.cursor()
    cursor.execute("INSERT INTO orders (product, quantity, distributor) VALUES (%s, %s, %s)", (product, quantity, distributor))
    db.commit()
    cursor.close()
    return redirect(url_for('home'))
