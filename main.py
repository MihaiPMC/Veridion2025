import requests
import subprocess

# Lista de arme cu id, nume și cost
weapons_data = {
    "1": {"text": "Feather", "cost": 1},
    "2": {"text": "Coal", "cost": 1},
    "3": {"text": "Pebble", "cost": 1},
    "4": {"text": "Leaf", "cost": 2},
    "5": {"text": "Paper", "cost": 2},
    "6": {"text": "Rock", "cost": 2},
    "7": {"text": "Water", "cost": 3},
    "8": {"text": "Twig", "cost": 3},
    "9": {"text": "Sword", "cost": 4},
    "10": {"text": "Shield", "cost": 4},
    "11": {"text": "Gun", "cost": 5},
    "12": {"text": "Flame", "cost": 5},
    "13": {"text": "Rope", "cost": 5},
    "14": {"text": "Disease", "cost": 6},
    "15": {"text": "Cure", "cost": 6},
    "16": {"text": "Bacteria", "cost": 6},
    "17": {"text": "Shadow", "cost": 7},
    "18": {"text": "Light", "cost": 7},
    "19": {"text": "Virus", "cost": 7},
    "20": {"text": "Sound", "cost": 8},
    "21": {"text": "Time", "cost": 8},
    "22": {"text": "Fate", "cost": 8},
    "23": {"text": "Earthquake", "cost": 9},
    "24": {"text": "Storm", "cost": 9},
    "25": {"text": "Vaccine", "cost": 9},
    "26": {"text": "Logic", "cost": 10},
    "27": {"text": "Gravity", "cost": 10},
    "28": {"text": "Robots", "cost": 10},
    "29": {"text": "Stone", "cost": 11},
    "30": {"text": "Echo", "cost": 11},
    "31": {"text": "Thunder", "cost": 12},
    "32": {"text": "Karma", "cost": 12},
    "33": {"text": "Wind", "cost": 13},
    "34": {"text": "Ice", "cost": 13},
    "35": {"text": "Sandstorm", "cost": 13},
    "36": {"text": "Laser", "cost": 14},
    "37": {"text": "Magma", "cost": 14},
    "38": {"text": "Peace", "cost": 14},
    "39": {"text": "Explosion", "cost": 15},
    "40": {"text": "War", "cost": 15},
    "41": {"text": "Enlightenment", "cost": 15},
    "42": {"text": "Nuclear Bomb", "cost": 16},
    "43": {"text": "Volcano", "cost": 16},
    "44": {"text": "Whale", "cost": 17},
    "45": {"text": "Earth", "cost": 17},
    "46": {"text": "Moon", "cost": 17},
    "47": {"text": "Star", "cost": 18},
    "48": {"text": "Tsunami", "cost": 18},
    "49": {"text": "Supernova", "cost": 19},
    "50": {"text": "Antimatter", "cost": 19},
    "51": {"text": "Plague", "cost": 20},
    "52": {"text": "Rebirth", "cost": 20},
    "53": {"text": "Tectonic Shift", "cost": 21},
    "54": {"text": "Gamma-Ray Burst", "cost": 22},
    "55": {"text": "Human Spirit", "cost": 23},
    "56": {"text": "Apocalyptic Meteor", "cost": 24},
    "57": {"text": "Earth's Core", "cost": 25},
    "58": {"text": "Neutron Star", "cost": 26},
    "59": {"text": "Supermassive Black Hole", "cost": 35},
    "60": {"text": "Entropy", "cost": 45}
}

# Această funcție folosește Ollama pentru a obține arma recomandată de AI.
def get_cheapest_weapon_from_ollama(word):
    prompt = f"""You are an assistant for a game similar to Rock, Paper, Scissors. You have the following list of weapons with their associated costs:
Feather (1), Coal (1), Pebble (1), Leaf (2), Paper (2), Rock (2), Water (3), Twig (3), Sword (4), Shield (4), Gun (5), Flame (5), Rope (5), Disease (6), Cure (6), Bacteria (6), Shadow (7), Light (7), Virus (7), Sound (8), Time (8), Fate (8), Earthquake (9), Storm (9), Vaccine (9), Logic (10), Gravity (10), Robots (10), Stone (11), Echo (11), Thunder (12), Karma (12), Wind (13), Ice (13), Sandstorm (13), Laser (14), Magma (14), Peace (14), Explosion (15), War (15), Enlightenment (15), Nuclear Bomb (16), Volcano (16), Whale (17), Earth (17), Moon (17), Star (18), Tsunami (18), Supernova (19), Antimatter (19), Plague (20), Rebirth (20), Tectonic Shift (21), Gamma-Ray Burst (22), Human Spirit (23), Apocalyptic Meteor (24), Earth's Core (25), Neutron Star (26), Supermassive Black Hole (35), Entropy (45).
When I give you a word, choose the weapon with the lowest cost that can beat that word according to the game rules. Be sure that the chosen weapon can beat the given word — it is obvious. For example, Wind beats Fire, Earthquake beats Town, Gun beats Lion, etc. Respond with exactly one word – the name of the weapon – and nothing else. Try to respond with the cheapest one.
Word: {word}"""

    # Folosim subprocess pentru a apela Ollama; asigură-te că modelul specificat este instalat pe Mac-ul tău.
    process = subprocess.Popen(
        ["ollama", "run", "gemma3:12b"],  # sau alt model disponibil în Ollama
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    output, err = process.communicate(input=prompt)

    chosen_weapon = output.strip()
    return chosen_weapon


def get_api_call():
    get_url = "http://172.18.4.158:8000/get-word"
    response = requests.get(get_url)
    if response.status_code == 200:
        data = response.json()
        return data["word"], data["round"]
    else:
        print("Eroare la obținerea cuvântului:", response.status_code)
        return None


def post_api_call(word_id, round_id):
    post_url = "http://172.18.4.158:8000/submit-word"
    data = {
        "player_id": "CRV_Coders",
        "word_id": word_id,
        "round_id": round_id
    }
    response = requests.post(post_url, json=data)
    if response.status_code == 200:
        print("Postare reușită")
    else:
        print("Eroare la postarea cuvântului:", response.status_code)

def main():

    getWord, roundID = get_api_call()

    print(getWord, roundID)

    # word = "Human"
    chosen_weapon_name = get_cheapest_weapon_from_ollama(getWord)
    # print(f"Ollama a ales arma: {chosen_weapon_name}")

    # Căutăm word_id corespunzător numelui primit de la AI (comparație case-insensitive)
    weapon_id = None
    for id, details in weapons_data.items():
        if details["text"].lower() == chosen_weapon_name.lower():
            weapon_id = id
            break
    if weapon_id is None:
        print("Nu s-a găsit o armă corespunzătoare de la Ollama.")
        return

    weapon_name = weapons_data[weapon_id]["text"]
    print(f"Chosen weapon: {weapon_name} (ID: {weapon_id})")

    # Postăm arma aleasă în API
    post_api_call(weapon_id, roundID)



if __name__ == "__main__":
    main()