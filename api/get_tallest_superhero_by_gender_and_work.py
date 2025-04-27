import requests
import json

API_URL = "https://akabab.github.io/superhero-api/api/all.json"

def height_in_cm(superhero_height):
    if not superhero_height:
        return 0
    superhero_height = superhero_height.lower()
    parts = superhero_height.split()
    try:
        value = float(parts[0])
        if 'meters' in superhero_height:
            return value * 100
        else:
            return value
    except (ValueError, IndexError):
        return 0
    

def tallest_superhero(gender: str, work: bool, url: str = API_URL) -> dict:
    if not isinstance(gender, str):
        return json.dumps({
            "status": "400 Bad requests",
            "message": "Parameter 'gender' was wrong type"
        })
    
    if not isinstance(work, bool):
        return json.dumps({
            "status": "400 Bad requests",
            "message": "Parameter 'work' was wrong type"
        })
    
    response = requests.get(url)
    superheroes = response.json()

    if not isinstance(superheroes, list):
        return json.dumps({
            "status": "400 Bad requests",
            "message": "Incorrect URL!"
        })
        

    filtered_superheroes = [
        superhero for superhero in superheroes 
        if superhero.get('appearance', {}).get('gender') == gender 
        and ((superhero.get('work', {}).get('occupation') not in ['-', None, 'None']) == work)
    ]

    if not filtered_superheroes:
        not_info_tallest_superhero = {
            "status": "404 Not found",
            "message": "Superhero with given parameters was not found"
        }
        not_info_tallest_superhero_json = json.dumps(not_info_tallest_superhero)
        return not_info_tallest_superhero_json
    
    max_height = -1
    tallest_superhero = None
    for hero in filtered_superheroes:
        height_str = hero.get('appearance', {}).get('height', [0, '0'])[1]
        height_cm = height_in_cm(height_str)
        if height_cm > max_height:
            max_height = height_cm
            tallest_superhero = hero

    info_tallest_superhero = {
        "status": "200 OK",
        "id": tallest_superhero['id'],
        "name": tallest_superhero['name'],
        "height": tallest_superhero['appearance']['height'][1]
    }
    info_tallest_superhero_json = json.dumps(info_tallest_superhero)
    return info_tallest_superhero_json

