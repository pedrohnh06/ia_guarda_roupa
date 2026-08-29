from app.database import SessionLocal
from app.models import User
from app.security import verify_password

db = SessionLocal()
users = db.query(User).all()
for u in users:
    print(f'Email: {u.email}')
    print(f'Hash: {u.hashed_password}')
    print('Password verify (123456):', verify_password('123456', u.hashed_password))
    print('Password verify (senha123):', verify_password('senha123', u.hashed_password))