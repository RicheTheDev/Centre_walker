from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db, bcrypt
from app.models.models import User
from flask import session

auth_routes = Blueprint('auth_routes', __name__, template_folder='templates')


@auth_routes.route('/')
def home():
    return render_template('home.html')


@auth_routes.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        role = request.form['role'] 

        hashed_pw = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(username=username, email=email, password=hashed_pw, role=role)

        db.session.add(new_user)
        db.session.commit()
        flash("Inscription réussie, vous pouvez maintenant vous connecter.", "success")
        return redirect(url_for('auth_routes.login'))

    return render_template('register.html')



@auth_routes.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()

        if user and bcrypt.check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['username'] = user.username
            session['role'] = user.role
            flash(f"Bienvenue {user.username} 👋", "success")
            return redirect(url_for('auth_routes.dashboard'))
        else:
            flash("Email ou mot de passe incorrect", "danger")
            return redirect(url_for('auth_routes.login'))

    return render_template('login.html')

@auth_routes.route('/logout')
def logout():
    session.clear()
    flash("Déconnexion réussie.", "success")
    return redirect(url_for('auth_routes.login'))

@auth_routes.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash("Veuillez vous connecter pour accéder au dashboard.", "danger")
        return redirect(url_for('auth_routes.login'))

    return render_template('dashboard.html', username=session.get('username'))



