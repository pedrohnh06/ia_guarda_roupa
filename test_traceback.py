from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

try:
    response = client.post('/auth/register', json={'email': 'teste_fastapi@teste.com', 'password': '123'})
    print(response.status_code)
    print(response.json())
except Exception as e:
    import traceback
    traceback.print_exc()