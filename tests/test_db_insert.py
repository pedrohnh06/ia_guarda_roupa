from backend.app.database import SessionLocal
from backend.app.models import User
from backend.app.security import get_password_hash

db = SessionLocal()
try:
    hash_str = get_password_hash('senha123')
    print('Hash gerado:', hash_str)
    new_user = User(email='meuteste@teste.com', hashed_password=hash_str)
    db.add(new_user)
    db.commit()
    print('Usuario criado com sucesso')
except Exception as e:
    import traceback
    traceback.print_exc()