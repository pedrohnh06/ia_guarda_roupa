import requests
try:
    resp = requests.post('http://localhost:8000/auth/register', json={'email': 'teste3@teste.com', 'password': 'senha123'})
    print('STATUS REGISTER:', resp.status_code)
    print('BODY:', resp.text)
except Exception as e:
    print('ERROR:', e)