from flask import Flask, render_template, request, redirect, url_for,session
from flask_mysqldb import MySQL
import cv2
import base64


app = Flask(__name__)
app.secret_key ='1234' #anypass

username = 'souravi'
password = '1234'


@app.template_filter('b64encode')
def b64encode_filter(data):
    return base64.b64encode(data).decode('utf-8')

@app.route('/')
def home ():
 return redirect('/login')

@app.route('/login', methods=['GET' , 'POST'])
def login():
    
    if request.method == 'POST':
        
        enter_username = request.form['username']
        enter_password = request.form['password']


        if enter_username == username and enter_password == password:
            session['user'] = enter_username
            return redirect('/index')
                     
        else:
            return 'Invalid credentials. <a href="/login">Try again</a>'
                 
    else:
        return render_template('login.html')
    
                 
@app.route('/index')     
def index():
    if 'user' in session:
        return  render_template('index.html' , user=session['user'])
    else:
        return redirect('/login')
    
@app.route('/logout')
def logout():
         session.pop('user' , None)
         return redirect('/login')

                                    
                 

# MySQL Config
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'MyNewPass'  # Replace with your real password
app.config['MYSQL_DB'] = 'visitor_db'

mysql = MySQL(app)
  

# Route to handle form submission
@app.route('/add', methods=['POST'])
def add_visitor():

    photo_data = request.form['photo']
    if photo_data:
        header, encoded = photo_data.split(",", 1)
        photo_blob = base64.b64decode(encoded)
    else:
        photo_blob = None

    if request.method == 'POST':
        
        name = request.form['name']
        emp_id = request.form['emp_id']
        purpose = request.form['purpose']
        checkin = request.form['checkin']
        checkout = request.form['checkout']
        phone_no = request.form['phone_no']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO visitors (emp_id, name, purpose, checkin, checkout,phone_no,photo) VALUES (%s, %s, %s, %s, %s,%s,%s)",
            (emp_id, name, purpose, checkin, checkout,phone_no,photo_blob))

        mysql.connection.commit()
        cur.close()
        return redirect('/visitors')

# Route to show the list of visitors

@app.route('/visitors')
def show_visitors():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM visitors")
    data = cur.fetchall()
    cur.close()
    return render_template('visitors.html', visitors=data)

if __name__ == '__main__':
    app.run(debug=True)
