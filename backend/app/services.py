from app import models
import requests
# pyrefly: ignore [missing-import]
from sqlalchemy.orm import Session
import random

def get_weather(city: str):

    try:    
        response = requests.get(f"https://wttr.in/{city}?format=j1")
        data = response.json()
        temp_c = int(data["current_condition"][0]["temp_C"])
        if temp_c < 22:
            return "Frio"
        else: 
            return "Calor"
    except requests.exceptions.ConnectionError:
        return "Calor"
    except requests.exceptions.HTTPError as error:
        return "Calor"

def generate_outfit(
    user_id: int,
    city: str,
    db: Session
):
    categories = {
    "upper_list" : [],
    "lowwer_list": [],
    "footwar_list": [],
    "coverage_list": []
    }


    climate = get_weather(city)
    search_outfit = db.query(
        models.ClothingItem
        ).filter(
            models.ClothingItem.owner_id == user_id,
            models.ClothingItem.weather.in_([climate, "Neutro"])
            ).all()
    for part in search_outfit:
        if part.category == "Superior":
            categories["upper_list"].append(part)
        elif part.category == "Inferior":
            categories["lowwer_list"].append(part)
        elif part.category == "Calçado":
            categories["footwar_list"].append(part)
        elif part.category == "Cobertura":
            categories["coverage_list"].append(part)

    outfit_finaly = []
    for category_name, list_of_items in categories.items():
        if list_of_items:
            chosen_items = random.choice(list_of_items)
            outfit_finaly.append(chosen_items)
    
    return outfit_finaly
    

        

    

    