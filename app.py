from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector

app = Flask(__name__)
app.secret_key = 'secretkey'

#database connection 
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",  # leave blank for XAMPP unless you've set a password
        database="Honeypot"
    )

#Home route
@app.route('/')
def home():
    return redirect(url_for('login'))

#register route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        retype_password = request.form['retype-password']

        if password != retype_password:
            flash('Passwords do not match!')
            return redirect(url_for('register'))

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Username already exists!')
            return redirect(url_for('register'))

        hashed_password = generate_password_hash(password)

        new_user = User(
            firstname=firstname,
            lastname=lastname,
            email=email,
            username=username,
            password=hashed_password
        )
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful. Please login.')
        return redirect(url_for('login'))

    return render_template('Registration.html')


#login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            session['user'] = user.username
            return redirect(url_for('dashboard'))

        flash('Invalid credentials')
        return redirect(url_for('login'))

    return render_template('Login.html')

#dashboard route 
@app.route('/dashboard')
def dashboard():
    if 'user' in session:
        return render_template('Dashboard.html', user=session['user'])
    flash('Please login first.')
    return redirect(url_for('login'))

#logout route 
@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully.')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
