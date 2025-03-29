from time import sleep

import requests
import subprocess
import time

NUM_ROUNDS = 5

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
get_url = "http://172.18.4.158:8000/get-word"
post_url = "http://172.18.4.158:8000/submit-word"
status_url = "http://172.18.4.158:8000/status"


def get_cheapest_weapon_from_ollama(word):
    prompt = f"""Word: {word}"""

    # Folosim subprocess pentru a apela Ollama; asigură-te că modelul specificat este instalat pe Mac-ul tău.
    process = subprocess.Popen(
        ["ollama", "run", "Mymodel"],  # sau alt model disponibil în Ollama
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    output, err = process.communicate(input=prompt)

    chosen_weapon = output.strip()
    return chosen_weapon

def get_api_call():
    response = requests.get(get_url)
    if response.status_code == 200:
        data = response.json()
        return data["word"], data["round"]
    else:
        print("Eroare la obținerea cuvântului:", response.status_code)
        return None


def post_api_call(word_id, round_id):
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


def play_game(player_id):
    for round_id in range(1, NUM_ROUNDS + 1):
        round_num = -1
        while round_num != round_id:
            response = requests.get(get_url)

            # print(response.json())
            sys_word = response.json()["word"]
            round_num = response.json()["round"]

            sleep(1)

        if round_id > 1:
            status = requests.get(status_url)
            print(status.json())

        chosen_word = get_cheapest_weapon_from_ollama(sys_word)
        print("Player", player_id, "Round:", round_num, "System word:", sys_word, "Chosen word:", chosen_word)

        word_id = 54
        for id, details in weapons_data.items():
            if details["text"].lower() == chosen_word.lower():
                word_id = int(id)
                break

        if word_id is None:
            word_id = int(54)

        if int(word_id) >= 59 or word_id is None:
            word_id = int(1)

        data = {
            "player_id": player_id,
            "word_id": word_id,
            "round_id": round_num
        }

        response = requests.post(post_url, json=data)
        print(response.json())

def play_from_console():
    while True:
        word = input("Introdu cuvântul: ")
        if word.lower() == "exit":
            break


        chosen_word = get_cheapest_weapon_from_ollama(word)
        print("Cuvântul ales:", chosen_word)
        word_id = 54
        for id, details in weapons_data.items():
            if details["text"].lower() == chosen_word.lower():
                word_id = int(id)
                break

        if word_id is None:
            word_id = int(54)

        if int(word_id) >= 59 or word_id is None:
            word_id = int(1)


        print(word_id)




if __name__ == "__main__":

    # Play the game
    play_game("ilDJONfOzl")

    # play_from_console();