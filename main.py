from flask import Flask, render_template, redirect, request,session
import mysql.connector
import os
import pandas as pd

app=Flask(__name__)
app.secret_key=os.urandom(24)

conn=mysql.connector.connect(host="remotemysql.com",user="3Bqv6hLogw",password="wGwACLhVwh",database="3Bqv6hLogw")
cursor=conn.cursor()

@app.route('/')
def login():
    return render_template('login.html')


@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/home')
def home():
    if 'user_id' in session:
        return render_template('home.html')
    else:
        return redirect('/')

@app.route('/loginvalidation',methods=['POST'])
def loginvalidation():
    email=request.form.get('email')
    password=request.form.get('password')

    cursor.execute("""SELECT * FROM `users` WHERE  `email` LIKE '{}' AND `password` LIKE '{}'"""
                   .format(email,password))
    users=cursor.fetchall()
    if len(users)>0:
        session['user_id']=users[0][0]
        return redirect('/home')
    else:
        return redirect('/')

@app.route('/add_user',methods=['POST'])
def add_user():
    name=request.form.get('uname')
    email=request.form.get('uemail')
    password=request.form.get('upassword')

    cursor.execute("""SELECT * FROM `users` WHERE  `email` LIKE '{}'"""
                   .format(email))
    users = cursor.fetchall()
    if len(users)!=0:
        return redirect('/invalid')

    cursor.execute("""INSERT INTO `users` (`user_id`,`name`,`email`,`password`) VALUES 
    (NULL,'{}','{}','{}')""".format(name,email,password))
    conn.commit()

    cursor.execute("""SELECT * FROM `users` WHERE  `email` LIKE '{}'"""
                   .format(email))
    users = cursor.fetchall()
    session['user_id'] = users[0][0]
    return redirect('/home')

@app.route('/logout')
def logout():
    session.pop('user_id')
    return redirect('/')

@app.route('/invalid')
def invalid():
    return render_template('already_member.html')

@app.route('/data',methods=['POST'])
def data():
    if request.method=='post':
        file=request.form['upload-file']
        data=pd.read_excel(file)
        return render_template('home.html', data=data.to_html())


if __name__ == "__main__":
    app.run(debug=True)
