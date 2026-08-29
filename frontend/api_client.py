import requests

BASE_URL = "http://localhost:8001"

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