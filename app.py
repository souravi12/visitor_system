import pymysql
pymysql.install_as_MySQLdb()

from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import base64

app = Flask(__name__)
app.secret_key = '1234'  # change this before showing anyone

username = 'souravi'
password = '1234'


@app.template_filter('b64encode')
def b64encode_filter(data):
    return base64.b64encode(data).decode('utf-8')


@app.route('/')
def home():
    return redirect('/login')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        enter_username = request.form['username']
        enter_password = request.form['password']

        if enter_username == username and enter_password == password:
            session['user'] = enter_username
            return redirect('/index')
        else:
            error = 'Invalid username or password'
            return render_template('login.html', error=error)

    return render_template('login.html')


@app.route('/index')
def index():
    if 'user' in session:
        return render_template('index.html', user=session['user'])
    else:
        return redirect('/login')


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/login')


# MySQL Config
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Koyel'
app.config['MYSQL_DB'] = 'visitor_db'

mysql = MySQL(app)


@app.route('/add', methods=['POST'])
def add_visitor():
    if 'user' not in session:
        return redirect('/login')

    photo_data = request.form['photo']
    if photo_data:
        header, encoded = photo_data.split(",", 1)
        photo_blob = base64.b64decode(encoded)
    else:
        photo_blob = None

    name = request.form['name']
    emp_id = request.form['emp_id']
    purpose = request.form['purpose']
    checkin = request.form['checkin']
    checkout = request.form['checkout']
    if checkout == "":
        checkout = None
    phone_no = request.form['phone_no']
    date = request.form['date']

    cur = mysql.connection.cursor()
    cur.execute(
        "INSERT INTO visitors (emp_id, name, purpose, checkin, checkout, phone_no, date, photo) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
        (emp_id, name, purpose, checkin, checkout, phone_no, date, photo_blob)
    )
    mysql.connection.commit()
    cur.close()
    return redirect('/visitors')


@app.route('/visitors')
def show_visitors():
    if 'user' not in session:
        return redirect('/login')

    cur = mysql.connection.cursor()

    cur.execute("SELECT * FROM visitors")
    data = cur.fetchall()

    cur.execute("SELECT COUNT(*) FROM visitors")
    total = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM visitors WHERE checkout IS NULL OR checkout = '' OR checkout = '00:00:00'")
    inside = cur.fetchone()[0]

    cur.close()

    return render_template(
        'visitors.html',
        visitors=data,
        total=total,
        inside=inside
    )


# ── NEW: checkout route ──────────────────────────────────────────────────────
@app.route('/checkout/<int:visitor_id>', methods=['POST'])
def checkout_visitor(visitor_id):
    if 'user' not in session:
        return redirect('/login')

    checkout_time = request.form['checkout_time']

    cur = mysql.connection.cursor()
    cur.execute(
        "UPDATE visitors SET checkout = %s WHERE id = %s",
        (checkout_time, visitor_id)
    )
    mysql.connection.commit()
    cur.close()

    return redirect('/visitors')
# ─────────────────────────────────────────────────────────────────────────────


if __name__ == '__main__':
    app.run(debug=True)