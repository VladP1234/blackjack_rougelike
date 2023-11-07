from deck import Deck, DefaultDecks
from json import dump
from typing import Dict
from level import Combat, Merchant, Reward
from player import Player

def obj_to_json(obj):
    return obj.to_json()

def serialise(obj, file_name):
    with open(file_name, 'w') as file:
        dump(obj, file, default=obj_to_json)

default_deck = Deck((623, 200), True, DefaultDecks.Base)

levels: Dict[str, Combat|Merchant] = {
    "1": Combat(Player(default_deck, True), Reward(50)),
    "2A": Combat(Player(default_deck, True), Reward(100)),
    "2B": Combat(Player(default_deck, True), Reward(100)),
    "3A": Combat(Player(default_deck, True), Reward(100)),
    "3B": Combat(Player(default_deck, True), Reward(100)),
    "4": Merchant,
    "5A": Combat(Player(default_deck, True), Reward(100)),
    "5B": Combat(Player(default_deck, True), Reward(100)),
    "6A": Combat(Player(default_deck, True), Reward(100)),
    "6B": Combat(Player(default_deck, True), Reward(100)),
    "7": Merchant,
}

serialise(levels, "floors.json")