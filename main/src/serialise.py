from deck import Deck, DefaultDecks
from json import dump
from typing import Dict
from level import Combat, Merchant, Reward
from player import Player
from enemy_ai import BasicAI


def obj_to_json(obj):
    return obj.to_json()


def serialise(obj, file_name):
    with open(file_name, "w") as file:
        dump(obj, file, default=obj_to_json)


default_deck = Deck((623, 200), True, DefaultDecks.Base)

floors: Dict[str, Dict[str, Combat | Merchant]] = {
    "1": {
        "1": Merchant(),
        "2A": Combat(Player(default_deck, True, enemy_ai=BasicAI()), Reward(100)),
        "2B": Combat(Player(default_deck, True, enemy_ai=BasicAI()), Reward(100)),
        "3A": Combat(Player(default_deck, True, enemy_ai=BasicAI()), Reward(100)),
        "3B": Combat(Player(default_deck, True, enemy_ai=BasicAI()), Reward(100)),
        "4": Merchant(),
        "5A": Combat(Player(default_deck, True, enemy_ai=BasicAI()), Reward(100)),
        "5B": Combat(Player(default_deck, True, enemy_ai=BasicAI()), Reward(100)),
        "6A": Combat(Player(default_deck, True, enemy_ai=BasicAI()), Reward(100)),
        "6B": Combat(Player(default_deck, True, enemy_ai=BasicAI()), Reward(100)),
        "7": Merchant(),
    },
    "2": {
        "1": Combat(Player(default_deck, True, enemy_ai=BasicAI()), Reward(50)),
        "2A": Combat(Player(default_deck, True, enemy_ai=BasicAI()), Reward(100)),
        "2B": Combat(Player(default_deck, True, enemy_ai=BasicAI()), Reward(100)),
        "3A": Combat(Player(default_deck, True, enemy_ai=BasicAI()), Reward(100)),
        "3B": Combat(Player(default_deck, True, enemy_ai=BasicAI()), Reward(100)),
        "4": Merchant(),
        "5A": Combat(Player(default_deck, True, enemy_ai=BasicAI()), Reward(100)),
        "5B": Combat(Player(default_deck, True, enemy_ai=BasicAI()), Reward(100)),
        "6A": Combat(Player(default_deck, True, enemy_ai=BasicAI()), Reward(100)),
        "6B": Combat(Player(default_deck, True, enemy_ai=BasicAI()), Reward(100)),
        "7": Merchant(),
    },
    "3": {
        "1": Combat(Player(default_deck, True, enemy_ai=BasicAI()), Reward(50)),
        "2A": Combat(Player(default_deck, True, enemy_ai=BasicAI()), Reward(100)),
        "2B": Combat(Player(default_deck, True, enemy_ai=BasicAI()), Reward(100)),
        "3A": Combat(Player(default_deck, True, enemy_ai=BasicAI()), Reward(100)),
        "3B": Combat(Player(default_deck, True, enemy_ai=BasicAI()), Reward(100)),
        "4": Merchant(),
        "5A": Combat(Player(default_deck, True, enemy_ai=BasicAI()), Reward(100)),
        "5B": Combat(Player(default_deck, True, enemy_ai=BasicAI()), Reward(100)),
        "6A": Combat(Player(default_deck, True, enemy_ai=BasicAI()), Reward(100)),
        "6B": Combat(Player(default_deck, True, enemy_ai=BasicAI()), Reward(100)),
        "7": Merchant(),
    },
}

import json


def dict_to_json(data, file_name):
    serialized_data = {}
    for floor_num, floor in data.items():
        floor_data = {}
        for key, value in floor.items():
            if isinstance(value, Combat):
                floor_data[key] = value.to_dict()
            elif isinstance(value, Merchant):
                floor_data[key] = "Merchant"
            else:
                floor_data[key] = value
        serialized_data[floor_num] = floor_data

    with open(file_name, "w") as file:
        json.dump(serialized_data, file, indent=4)


def json_to_dict(file_name, UIManager):
    with open(file_name, "r") as file:
        serialized_data = json.load(file)

    deserialized_data = {}
    for floor_num, floor in serialized_data.items():
        current_floor = {}

        for level_num, level in floor.items():
            if level == "Merchant":
                current_floor[level_num] = Merchant()
            else:
                # print(Combat.from_dict(level, UIManager).enemy)
                current_floor[level_num] = Combat.from_dict(level, UIManager)
            # if 'type' in value and value['type'] == 'Combat':
            #     deserialized_data[key] = Combat.from_dict(value)
            # elif 'type' in value and value['type'] == 'Merchant':
            #     deserialized_data[key] = Merchant()
            # else:
            #     deserialized_data[key] = value
        deserialized_data[floor_num] = current_floor
    return deserialized_data


# from pprint import pprint
# dict_to_json(floors, "floors.json")
# pprint(json_to_dict("floors.json"))
