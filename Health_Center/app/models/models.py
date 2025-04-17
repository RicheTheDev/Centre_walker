from app import db
from datetime import datetime

# ----------------------------
# Utilisateur générique du système
# ----------------------------
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(50), nullable=False)  # 'admin', 'doctor', 'patient'
    type = db.Column(db.String(50))  # Pour l'héritage

    __mapper_args__ = {
        'polymorphic_identity': 'user',
        'polymorphic_on': type
    }

    consultations = db.relationship('Consultation', backref='doctor', lazy=True)

    def __repr__(self):
        return f"<User {self.username} - Role: {self.role}>"


# ----------------------------
# Patient (hérite de User)
# ----------------------------
class Patient(User):
    __tablename__ = 'patients'

    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    phone_number = db.Column(db.String(15), nullable=False)
    address = db.Column(db.String(200), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    consultations = db.relationship('Consultation', backref='patient', lazy=True)

    __mapper_args__ = {
        'polymorphic_identity': 'patient',
    }

    def __repr__(self):
        return f"<Patient {self.first_name} {self.last_name}>"


# ----------------------------
# Consultation médicale
# ----------------------------
class Consultation(db.Model):
    __tablename__ = 'consultations'

    id = db.Column(db.Integer, primary_key=True)
    consultation_date = db.Column(db.DateTime, default=datetime.utcnow)
    diagnosis = db.Column(db.String(255), nullable=False)
    treatment = db.Column(db.String(255), nullable=True)

    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return f"<Consultation #{self.id} - {self.consultation_date.strftime('%Y-%m-%d')}>"
