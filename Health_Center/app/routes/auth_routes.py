from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db, bcrypt
from app.models.models import User
from app.models.models import Patient
from flask import session

auth_routes = Blueprint('auth_routes', __name__, template_folder='templates')



@auth_routes.route('/')
def home():
    return render_template('home.html')




@auth_routes.route('/register/doctor', methods=['GET', 'POST'])
def register_doctor():
    role = 'doctor'  # préchargé pour le formulaire

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

    return render_template('register.html', role=role)




@auth_routes.route('/register/nurse', methods=['GET', 'POST'])
def register_nurse():
    role = 'nurse'  # préchargé pour le formulaire

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

    return render_template('register.html', role=role)

from datetime import datetime






@auth_routes.route('/register/patient', methods=['GET', 'POST'])
def register_patient():
    role = 'patient' 

    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        date_of_birth = request.form['date_of_birth']
        gender = request.form['gender']
        phone_number = request.form['phone_number']
        address = request.form['address']

        # ✅ Convertir la date en objet datetime.date
        date_of_birth = datetime.strptime(date_of_birth, '%Y-%m-%d').date()

        hashed_pw = bcrypt.generate_password_hash(password).decode('utf-8')

        new_patient = Patient(
            username=username,
            email=email,
            password=hashed_pw,
            role=role,
            first_name=first_name,
            last_name=last_name,
            date_of_birth=date_of_birth,
            gender=gender,
            phone_number=phone_number,
            address=address
        )

        db.session.add(new_patient)
        db.session.commit()
        flash("Inscription du patient réussie. Vous pouvez maintenant vous connecter.", "success")
        return redirect(url_for('auth_routes.select'))

    return render_template('/patients/register_patient.html', role=role)




@auth_routes.route('/login/doctor', methods=['GET', 'POST'])
def login_doctor():
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





@auth_routes.route('/login/nurse', methods=['GET', 'POST'])
def login_nurse():
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






@auth_routes.route('/login/patient', methods=['GET', 'POST'])
def login_patient():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = Patient.query.filter_by(email=email).first()

        if user and bcrypt.check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['username'] = user.username
            session['role'] = user.role

            flash(f"Bienvenue {user.first_name} 👋", "success")
            return redirect(url_for('auth_routes.dashboard_patient'))

        else:
            flash("Email ou mot de passe incorrect", "danger")
            return redirect(url_for('auth_routes.login_patient'))

    return render_template('login.html', role='patient')




@auth_routes.route('/select')
def select():
    return render_template('role_selection.html')


@auth_routes.route('/PatientList')
def Listpatient():
    return render_template('patients/patientList.html')


@auth_routes.route('/logout')
def logout():
    session.clear()
    flash("Déconnexion réussie.", "success")
    return redirect(url_for('auth_routes.home'))




@auth_routes.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash("Veuillez vous connecter pour accéder au dashboard.", "danger")
        return redirect(url_for('auth_routes.login'))

    return render_template('dashboard.html', username=session.get('username'))






@auth_routes.route('/dashboard/patient')
def dashboard_patient():
    if 'user_id' not in session:
        flash("Veuillez vous connecter pour accéder au dashboard.", "danger")
        return redirect(url_for('auth_routes.login'))
    
    if session.get('role') != 'patient':
        flash("Accès non autorisé. Réservé aux patients.", "danger")
        return redirect(url_for('auth_routes.login')) 

    return render_template('patients/dashboard_patient.html', username=session.get('username'))
