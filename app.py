from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_order', methods=['POST'])
def add_order():
    client_id = request.form['client_id']
    product = request.form['product']
    quantity = request.form['quantity']
    order_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    status = "En attente"

    conn = get_db_connection()
    conn.execute('INSERT INTO orders (client_id, product, quantity, order_date, status) VALUES (?, ?, ?, ?, ?)',
                 (client_id, product, quantity, order_date, status))
    conn.commit()
    conn.close()
    return redirect(url_for('orders'))

@app.route('/orders')
def orders():
    conn = get_db_connection()
    orders = conn.execute('SELECT * FROM orders').fetchall()
    conn.close()
    return render_template('orders.html', orders=orders)

@app.route('/update_status/<int:id>', methods=['POST'])
def update_status(id):
    new_status = request.form['status']
    conn = get_db_connection()
    conn.execute('UPDATE orders SET status = ? WHERE id = ?', (new_status, id))
    conn.commit()
    conn.close()
    return redirect(url_for('orders'))

@app.route('/delete_order/<int:id>')
def delete_order(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM orders WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('orders'))

if __name__ == '__main__':
    app.run(debug=True)