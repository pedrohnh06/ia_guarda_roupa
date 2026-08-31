
import requests
try:
    resp = requests.post('http://localhost:8000/auth/register', json={'email': 'teste@teste.com', 'password': '123'})
    print('STATUS:', resp.status_code)
    print('BODY:', resp.text)
except Exception as e:
    print('ERROR:', e)