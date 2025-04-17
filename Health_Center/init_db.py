from app import create_app, db
from app.models import models 

app = create_app()

with app.app_context():
    db.create_all()
    print("✅ Base de données initialisée avec succès.")
