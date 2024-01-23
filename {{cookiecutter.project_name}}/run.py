# app/app.py

from app import create_app
from app.models.user import db

app = create_app()
# Check if tables exist, if not, create them
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
