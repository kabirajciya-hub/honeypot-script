from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Simulated in-memory user database
users = {}

@app.route('/')
def home():
    return redirect(url_for('Login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        if email in users and users[email]['password'] == password:
            session['user'] = users[email]['username']
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password')
            return redirect(url_for('login'))

    return render_template('Login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['retype-password']

        if password != confirm_password:
            flash('Passwords do not match!')
            return redirect(url_for('register'))

        users[email] = {
            'firstname': firstname,
            'lastname': lastname,
            'username': username,
            'password': password
        }

        flash('Registered successfully! Please login.')
        return redirect(url_for('login'))

    return render_template('Registration.html')

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        flash('Please login first.')
        return redirect(url_for('login'))

    return render_template('Dashboard.html', user=session['user'])

@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('Logged out successfully!')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
