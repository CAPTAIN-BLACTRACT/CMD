from app import app, db
from app import User  # make sure User is imported too

with app.app_context():
    db.create_all()
