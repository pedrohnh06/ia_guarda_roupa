import requests

BASE = 'http://localhost:8001'

# Login
r = requests.post(f'{BASE}/auth/login', data={'username': 'pedro@teste.com', 'password': 'senha123'})
token = r.json()['access_token']
headers = {'Authorization': f'Bearer {token}'}

# Testar clima
r2 = requests.get('https://wttr.in/Ushuaia?format=j1')
data = r2.json()
temp = data['current_condition'][0]['temp_C']
print(f'Temperatura em Ushuaia: {temp}C')

# Listar roupas do usuario
r3 = requests.get(f'{BASE}/clothes/', headers=headers)
print(f'\nRoupas cadastradas: {len(r3.json())}')
for roupa in r3.json():
    print(f'  [{roupa["category"]}] {roupa["name"]} - weather:{roupa["weather"]}, color:{roupa["color"]}')