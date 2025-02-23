from flask import Flask, request, jsonify, render_template
import mysql.connector
import os

app = Flask(__name__)

# MySQL connection settings
DB_HOST = 'maglev.proxy.rlwy.net'
DB_USER = 'root'
DB_PASSWORD = 'CfijXJamefkpUSuRogjOQmSypuKjNMkk'
DB_NAME = 'railway'
DB_PORT = 22632

# Connect to MySQL
def get_db_connection():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        port=DB_PORT
    )

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/place_order', methods=['POST'])
def place_order():
    try:
        data = request.json
        name = data.get('name')
        email = data.get('email')
        product = data.get('product')
        quantity = data.get('quantity')

        if not all([name, email, product, quantity]):
            return jsonify({"error": "All fields are required"}), 400

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO orders (name, email, product, quantity) VALUES (%s, %s, %s, %s)",
                       (name, email, product, quantity))
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"message": "Order placed successfully!"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
