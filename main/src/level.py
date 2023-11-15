from player import Player
from deck import Deck, DefaultDecks
from typing import Dict
from enemy_ai import BasicAI


class Reward:
    def __init__(self, gold) -> None:
        self.gold: int = gold
    
    def to_dict(self):
        return {"gold": self.gold}

    @classmethod
    def from_dict(cls, data):
        return cls(**data)

class Combat:
    def __init__(self, enemy: Player, reward: Reward) -> None:
        self.enemy: Player = enemy
        self.reward: Reward = reward
    
    def to_dict(self):
        return {"enemy": self.enemy.to_dict(), "reward": self.reward.to_dict()}

    @classmethod
    def from_dict(cls, data, UIManager):
        enemy = Player.from_dict(data["enemy"], UIManager)
        # print(enemy)
        reward = Reward.from_dict(data["reward"])
        return cls(enemy, reward)

class Merchant:
    def __init__(self) -> None:
        pass

default_deck = Deck((623, 200), True, DefaultDecks.Base)

floors: Dict[str, Dict[str, Combat|Merchant]] = {
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
    }
}
