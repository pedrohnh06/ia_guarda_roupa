import requests

BASE_URL = "http://localhost:8000"

def login(
    email: str,
    password: str
):
    response = requests.post(
        f"{BASE_URL}/auth/login",
        data = {"username": email, "password": password}
    )   
    return response.json()

def register(
    email: str,
    password: str
):
    response = requests.post(
        f"{BASE_URL}/auth/register",
        json = {"email": email, "password": password}
    )
    return response.json()

def get_recommendation(
    token: str,
    city: str
):
    response = requests.get(
        f"{BASE_URL}/clothes/recommend?city={city}",
        headers={"Authorization": f"Bearer {token}"}
    )
    return response.json()

def get_clothes(token: str):
    response = requests.get(
        f"{BASE_URL}/clothes/",
        headers={"Authorization": f"Bearer {token}"}
    )
    return response.json()

def create_clothing(token: str, clothing_data: dict):
    response = requests.post(
        f"{BASE_URL}/clothes/",
        json=clothing_data,
        headers={"Authorization": f"Bearer {token}"}
    )
    return response.json()

def update_settings(token: str, temp_threshold: int):
    response = requests.put(
        f"{BASE_URL}/auth/settings",
        json={"temp_threshold": temp_threshold},
        headers={"Authorization": f"Bearer {token}"}
    )
    return response.json()

def upload_image(token: str, file_bytes: bytes, filename: str):
    response = requests.post(
        f"{BASE_URL}/clothes/upload",
        files={"file": (filename, file_bytes, "image/jpeg")},
        headers={"Authorization": f"Bearer {token}"}
    )
    return response.json()
def update_clothing(token: str, item_id: int, clothing_data: dict):
    response = requests.patch(
        f"{BASE_URL}/clothes/{item_id}",
        json=clothing_data,
        headers={"Authorization": f"Bearer {token}"}
    )
    return response.json()
def delete_clothing(token: str, item_id: int):
    response = requests.delete(
        f"{BASE_URL}/clothes/{item_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    return response.json()