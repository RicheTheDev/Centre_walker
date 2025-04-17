from app import create_app, db, bcrypt
from app.models.models import User

app = create_app()

with app.app_context():
    db.create_all()
    print("✅ Base de données initialisée avec succès.")

    # Vérifie si un admin existe déjà
    existing_admin = User.query.filter_by(username="ASSOGBA Ulrich").first()

    if not existing_admin:
        hashed_password = bcrypt.generate_password_hash("Ulrich@2024").decode('utf-8')
        admin = User(
            username="ASSOGBA Ulrich",
            email="uassogba06@gmail.com",
            password=hashed_password,
            role="admin",
            type="user"  # Très important si tu utilises l’héritage
        )
        db.session.add(admin)
        db.session.commit()
        print("👑 Utilisateur admin créé avec succès.")
    else:
        print("⚠️ Utilisateur admin déjà existant.")