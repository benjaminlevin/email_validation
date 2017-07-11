from flask import Flask, request, redirect, render_template, session, flash
from mysqlconnection import MySQLConnector
import re
app = Flask(__name__)
app.secret_key = 'ThisIsSecret'
mysql = MySQLConnector(app,'mydb')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    email = request.form['email']
    addressToVerify =request.form['email']
    match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', addressToVerify)
    if match == None:
        session['message'] = 'Email is not valid!'
        return redirect('/')
    elif " " in email:
        session['message'] = 'Email is not valid!'
        return redirect('/')
    elif "@" and "." in email:
        if len(email) > 8:
            print 'success'
            query = "INSERT INTO emails (email, created_at, updated_at) \
            VALUES (:email, NOW(), NOW())"
            data = {
                'email': request.form['email']
                }
            mysql.query_db(query, data)
            session['message'] = ''
            return redirect('/success')
        else:
            session['message'] = 'Email is not valid!'
            return redirect('/')

@app.route('/success')
def success():
    session['message'] = ''
    query = "SELECT * FROM emails"                         
    emails = mysql.query_db(query)   
    return render_template('success.html', all_emails=emails)

@app.route('/delete/<id>')
def delete(id):
    query = "DELETE FROM emails WHERE id = :id"
    data = {'id': id}
    mysql.query_db(query, data)
    return redirect('/')

app.run(debug=True)