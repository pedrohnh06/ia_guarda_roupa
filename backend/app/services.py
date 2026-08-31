from app import models
import requests
# pyrefly: ignore [missing-import]
from sqlalchemy.orm import Session
from itertools import product, combinations

def get_weather(
    city: str,
    threshold: int
):

    try:    
        response = requests.get(f"https://wttr.in/{city}?format=j1")
        data = response.json()
        temp_c = int(data["current_condition"][0]["temp_C"])
        if temp_c < threshold:
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
    threshold: int,
    db: Session
):
    categories = {
    "upper_list" : [],
    "lowwer_list": [],
    "footwar_list": [],
    "coverage_list": []
    }


    climate = get_weather(city, threshold)
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
        elif part.category == "Calcado":
            categories["footwar_list"].append(part)
        elif part.category == "Cobertura":
            categories["coverage_list"].append(part)

    all_outfits = list(product(
        categories["upper_list"],
        categories["lowwer_list"],
        categories["footwar_list"],
        categories["coverage_list"]
        ))
    
    outfit_and_score = []
    for look in all_outfits:
        score = rate_the_look(look)
        outfit_and_score.append({"look": look, "score": score})
    
    outfit_and_score.sort(key=lambda x: x["score"], reverse=True)
    if not outfit_and_score:
        return[]

    return list(outfit_and_score[0]["look"])
    
def rate_the_look(
    outfit: tuple
):

    score = 0
    for part1, part2 in combinations(outfit, 2):
        if part1.style == part2.style:
            score += 3
        if part1.color == "Estampada" and part2.color == "Estampada":
            score -= 10
        if part1.usage_penalty >= 3 and part2.usage_penalty >= 3:
            score -= 5
        if part1.color == "Neutro" and part2.color == "Neutro":
            score += 5
    
    return score

