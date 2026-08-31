import requests

BASE = 'http://localhost:8001'

# 1. Registrar usuario
r = requests.post(f'{BASE}/auth/register', json={'email': 'pedro@teste.com', 'password': 'senha123'})
print('REGISTER:', r.status_code, r.text)

# 2. Login
r = requests.post(f'{BASE}/auth/login', data={'username': 'pedro@teste.com', 'password': 'senha123'})
print('LOGIN:', r.status_code)
token = r.json()['access_token']
headers = {'Authorization': f'Bearer {token}'}

# 3. Cadastrar roupas variadas
roupas = [
    {'name': 'Camiseta Preta Basica', 'category': 'Superior', 'weather': 'Neutro', 'color': 'Neutro', 'style': 'Casual'},
    {'name': 'Camisa Social Branca', 'category': 'Superior', 'weather': 'Neutro', 'color': 'Neutro', 'style': 'Social'},
    {'name': 'Regata Estampada', 'category': 'Superior', 'weather': 'Calor', 'color': 'Estampada', 'style': 'Casual'},
    {'name': 'Blusa de Frio Cinza', 'category': 'Superior', 'weather': 'Frio', 'color': 'Neutro', 'style': 'Casual'},
    {'name': 'Calca Jeans', 'category': 'Inferior', 'weather': 'Neutro', 'color': 'Neutro', 'style': 'Casual'},
    {'name': 'Calca Social Preta', 'category': 'Inferior', 'weather': 'Neutro', 'color': 'Neutro', 'style': 'Social'},
    {'name': 'Bermuda Estampada', 'category': 'Inferior', 'weather': 'Calor', 'color': 'Estampada', 'style': 'Casual'},
    {'name': 'Short Esportivo', 'category': 'Inferior', 'weather': 'Calor', 'color': 'Primaria', 'style': 'Esportivo'},
    {'name': 'Tenis Branco', 'category': 'Calcado', 'weather': 'Neutro', 'color': 'Neutro', 'style': 'Casual'},
    {'name': 'Sapato Social', 'category': 'Calcado', 'weather': 'Neutro', 'color': 'Neutro', 'style': 'Social'},
    {'name': 'Bota Preta', 'category': 'Calcado', 'weather': 'Frio', 'color': 'Neutro', 'style': 'Casual'},
    {'name': 'Casaco Moletom', 'category': 'Cobertura', 'weather': 'Frio', 'color': 'Neutro', 'style': 'Casual'},
    {'name': 'Blazer Preto', 'category': 'Cobertura', 'weather': 'Frio', 'color': 'Neutro', 'style': 'Social'},
    {'name': 'Jaqueta Jeans', 'category': 'Cobertura', 'weather': 'Frio', 'color': 'Neutro', 'style': 'Casual'},
]

for roupa in roupas:
    r = requests.post(f'{BASE}/clothes/', json=roupa, headers=headers)
    print(f'  {roupa["name"]}: {r.status_code}')

print('\n--- TESTANDO RECOMENDACAO ---')
r = requests.get(f'{BASE}/clothes/recommend?city=Guarulhos', headers=headers)
print('RECOMMEND:', r.status_code)
if r.status_code == 200:
    for peca in r.json():
        print(f'  {peca["category"]}: {peca["name"]} ({peca["color"]}, {peca["style"]})')
else:
    print('ERRO:', r.text)