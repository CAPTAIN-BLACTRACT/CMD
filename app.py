import os
from flask import Flask, request, render_template, jsonify
from compensation_logic import calculate_compensation
from flask import    redirect, session, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename


app = Flask(__name__)
app.secret_key = "your_secret_key_here"  # use something secure!
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120))
    gender = db.Column(db.String(20))
    profile_picture = db.Column(db.String(200)) 



UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    return render_template('profile.html', user=user)

@app.route('/update_profile', methods=['POST'])
def update_profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user = User.query.get(session['user_id'])

    user.username = request.form['username']
    user.gender = request.form['gender']
    user.email = request.form['email']

    if 'profile_picture' in request.files:
        picture = request.files['profile_picture']
        if picture.filename != '':
            filename = secure_filename(picture.filename)
            picture_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            picture.save(picture_path)
            user.profile_picture = filename

    db.session.commit()
    flash('Profile updated successfully!', 'success')
    return redirect(url_for('profile'))




@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'], method='pbkdf2:sha256')
        
        # Check if the user already exists
        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'error')
            return redirect(url_for('register'))
        
        # Create new user
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful!', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        
        # Check if user exists and password matches
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id  # Store user ID in the session
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        flash('Invalid credentials, please try again.', 'error')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)  # Remove the user from the session
    flash('Logged out successfully!', 'success')
    return redirect(url_for('login'))


@app.route('/')
def home():
    if 'user_id' not in session:
        return redirect(url_for('login'))  # Redirect to login if the user is not logged in
    return render_template('index.html')


@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.json
    result = calculate_compensation(data)
    return jsonify({'compensation': result})



if __name__ == '__main__':
    app.run(debug=True)
