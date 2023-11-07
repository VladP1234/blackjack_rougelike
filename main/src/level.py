from player import Player
from deck import Deck, DefaultDecks
from typing import Dict


class Reward:
    def __init__(self, gold) -> None:
        self.gold: int = gold

class Combat:
    def __init__(self, enemy: Player, reward: Reward) -> None:
        self.enemy: Player = enemy
        self.reward: Reward = reward
    # def to_json(self):
    #     return {"enemy": self.enemy.to_json, "reward": self.reward.to_json}

class Merchant:
    def __init__(self) -> None:
        pass

default_deck = Deck((623, 200), True, DefaultDecks.Base)

floors: Dict[str, Dict[str, Combat|Merchant]] = {
    "1": {
    "1": Merchant(),
    "2A": Combat(Player(default_deck, True), Reward(100)),
    "2B": Combat(Player(default_deck, True), Reward(100)),
    "3A": Combat(Player(default_deck, True), Reward(100)),
    "3B": Combat(Player(default_deck, True), Reward(100)),
    "4": Merchant(),
    "5A": Combat(Player(default_deck, True), Reward(100)),
    "5B": Combat(Player(default_deck, True), Reward(100)),
    "6A": Combat(Player(default_deck, True), Reward(100)),
    "6B": Combat(Player(default_deck, True), Reward(100)),
    "7": Merchant(),
    },
    "2": {
    "1": Combat(Player(default_deck, True), Reward(50)),
    "2A": Combat(Player(default_deck, True), Reward(100)),
    "2B": Combat(Player(default_deck, True), Reward(100)),
    "3A": Combat(Player(default_deck, True), Reward(100)),
    "3B": Combat(Player(default_deck, True), Reward(100)),
    "4": Merchant(),
    "5A": Combat(Player(default_deck, True), Reward(100)),
    "5B": Combat(Player(default_deck, True), Reward(100)),
    "6A": Combat(Player(default_deck, True), Reward(100)),
    "6B": Combat(Player(default_deck, True), Reward(100)),
    "7": Merchant(),
    },
    "3": {
    "1": Combat(Player(default_deck, True), Reward(50)),
    "2A": Combat(Player(default_deck, True), Reward(100)),
    "2B": Combat(Player(default_deck, True), Reward(100)),
    "3A": Combat(Player(default_deck, True), Reward(100)),
    "3B": Combat(Player(default_deck, True), Reward(100)),
    "4": Merchant(),
    "5A": Combat(Player(default_deck, True), Reward(100)),
    "5B": Combat(Player(default_deck, True), Reward(100)),
    "6A": Combat(Player(default_deck, True), Reward(100)),
    "6B": Combat(Player(default_deck, True), Reward(100)),
    "7": Merchant(),
    }
}
