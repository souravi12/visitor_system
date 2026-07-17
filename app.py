from flask import Flask, render_template, request, redirect, url_for, session
import psycopg2
import base64
import os

app = Flask(__name__)
app.secret_key = '1234'  # change this before showing anyone

username = 'souravi'
password = '1234'


@app.template_filter('b64encode')
def b64encode_filter(data):
    return base64.b64encode(data).decode('utf-8') if data else ''


def get_db_connection():
    return psycopg2.connect(
        host=os.environ.get('SUPABASE_HOST'),
        dbname=os.environ.get('SUPABASE_DB'),
        user=os.environ.get('SUPABASE_USER'),
        password=os.environ.get('SUPABASE_PASSWORD'),
        port=os.environ.get('SUPABASE_PORT', '5432')
    )


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

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO visitors (emp_id, name, purpose, checkin, checkout, phone_no, date, photo) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
        (emp_id, name, purpose, checkin, checkout, phone_no, date, psycopg2.Binary(photo_blob) if photo_blob else None)
    )
    conn.commit()
    cur.close()
    conn.close()
    return redirect('/visitors')


@app.route('/visitors')
def show_visitors():
    if 'user' not in session:
        return redirect('/login')

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM visitors")
    data = cur.fetchall()

    cur.execute("SELECT COUNT(*) FROM visitors")
    total = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM visitors WHERE checkout IS NULL")
    inside = cur.fetchone()[0]

    cur.close()
    conn.close()

    return render_template(
        'visitors.html',
        visitors=data,
        total=total,
        inside=inside
    )


@app.route('/checkout/<int:visitor_id>', methods=['POST'])
def checkout_visitor(visitor_id):
    if 'user' not in session:
        return redirect('/login')

    checkout_time = request.form['checkout_time']

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE visitors SET checkout = %s WHERE id = %s",
        (checkout_time, visitor_id)
    )
    conn.commit()
    cur.close()
    conn.close()

    return redirect('/visitors')


if __name__ == '__main__':
    app.run(debug=True)