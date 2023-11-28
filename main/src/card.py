import pygame
from typing import Dict, List
import json
from status_effect import *


class Effect:
    def __init__(self, effect_type, params, target) -> None:
        self.effect_type = effect_type
        self.params = params
        self.target = target


class Card:
    def __init__(
        self,
        value,
        image_path,
        pos,
        name=None,
        on_reveal_effect: Effect | None = None,
        on_blackjack_effect: Effect | None = None,
    ) -> None:
        self.value = value
        self.name = name
        self.image_path = image_path
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (255 / 2, 381 / 2))
        self.pos = pos
        self.on_reveal_effect_serialise = on_reveal_effect
        if on_reveal_effect:
            self.on_reveal_effect = (
                lambda cm: effect_on_reveal(
                    cm,
                    on_reveal_effect.effect_type(**on_reveal_effect.params),
                    on_reveal_effect.target,
                )
                if on_reveal_effect
                else None
            )
        else:
            self.on_reveal_effect = None
        self.on_blackjack_effect_serialise = on_blackjack_effect
        # TODO: Ask howse why the original didn't work
        # self.on_blackjack_effect = lambda cm: effect_on_reveal(cm, on_blackjack_effect.effect_type(**on_blackjack_effect.params), on_blackjack_effect.target) if on_blackjack_effect else None

        if on_blackjack_effect:
            self.on_blackjack_effect = (
                lambda cm: effect_on_reveal(
                    cm,
                    on_blackjack_effect.effect_type(**on_blackjack_effect.params),
                    on_blackjack_effect.target,
                )
                if on_blackjack_effect
                else None
            )
        else:
            self.on_blackjack_effect = None

    def draw(self, screen, x_offset, y_offset):
        screen.blit(self.image, (self.pos[0] + x_offset, self.pos[1] - y_offset))

    # Used GPT for this, made most other serialisation functions myself based on this
    def serialize(self):
        # Convert the card to a JSON-serializable dictionary
        return {
            "value": self.value,
            "name": self.name,
            "image_path": self.image_path,
            "pos": self.pos,
            # Serialize the effect by its class name and attributes
            "on_reveal_effect": self.on_reveal_effect_serialise.effect_type.__name__
            if self.on_reveal_effect
            else None,
            "on_reveal_effect_attrs": self.on_reveal_effect_serialise.params
            if self.on_reveal_effect
            else None,
            "on_reveal_effect_target": self.on_reveal_effect_serialise.target
            if self.on_reveal_effect
            else None,
            "on_blackjack_effect": self.on_blackjack_effect_serialise.effect_type.__name__
            if self.on_blackjack_effect
            else None,
            "on_blackjack_effect_attrs": self.on_blackjack_effect_serialise.params
            if self.on_blackjack_effect
            else None,
            "on_blackjack_effect_target": self.on_blackjack_effect_serialise.target
            if self.on_blackjack_effect
            else None,
        }

    @staticmethod
    def deserialize(card_data):
        # Import the status effects

        # Reconstruct the effects based on the stored data
        on_reveal_effect = None
        if card_data.get("on_reveal_effect"):
            effect_class = globals()[card_data["on_reveal_effect"]]
            effect_attrs = card_data["on_reveal_effect_attrs"]
            target = card_data["on_reveal_effect_target"]
            on_reveal_effect = Effect(effect_class, effect_attrs, target)

        on_blackjack_effect = None
        if card_data.get("on_blackjack_effect"):
            effect_class = globals()[card_data["on_blackjack_effect"]]
            effect_attrs = card_data["on_blackjack_effect_attrs"]
            target = card_data["on_blackjack_effect_target"]
            on_blackjack_effect = Effect(effect_class, effect_attrs, target)

        # Create the card object
        card = Card(
            card_data["value"],
            card_data["image_path"],
            tuple(card_data["pos"]),
            card_data.get("name"),
            on_reveal_effect=on_reveal_effect,
            on_blackjack_effect=on_blackjack_effect,
        )
        return card


class AltValueCard(Card):
    def __init__(
        self,
        value,
        image_path,
        alt_value,
        pos,
        name=None,
        on_reveal_effect=None,
        on_blackjack_effect=None,
    ) -> None:
        super().__init__(
            value, image_path, pos, name, on_reveal_effect, on_blackjack_effect
        )
        self.alt_value = alt_value

    def serialize(self):
        return_dict = super().serialize()
        return_dict["alt_value"] = self.alt_value
        return return_dict

    @staticmethod
    def deserialize(card_data):
        on_reveal_effect = None
        if card_data.get("on_reveal_effect"):
            effect_class = globals()[card_data["on_reveal_effect"]]
            effect_attrs = card_data["on_reveal_effect_attrs"]
            target = card_data["on_reveal_effect_target"]
            on_reveal_effect = Effect(effect_class, effect_attrs, target)

        on_blackjack_effect = None
        if card_data.get("on_blackjack_effect"):
            effect_class = globals()[card_data["on_blackjack_effect"]]
            effect_attrs = card_data["on_blackjack_effect_attrs"]
            target = card_data["on_blackjack_effect_target"]
            on_blackjack_effect = Effect(effect_class, effect_attrs, target)

        card = AltValueCard(
            card_data["value"],
            card_data["image_path"],
            card_data["alt_value"],
            tuple(card_data["pos"]),
            card_data.get("name"),
            on_reveal_effect=on_reveal_effect,
            on_blackjack_effect=on_blackjack_effect,
        )
        return card


def heart_on_reveal(combat_manager, heal_amount):
    combat_manager.player.hp += heal_amount


def effect_on_reveal(combat_manager, effect, target):
    if target == "player":
        combat_manager.player.affect(effect)
    if target == "enemy":
        combat_manager.enemy.affect(effect)


# merch44
# with open('merchant_cards.json', 'r') as f:
#     merchant_cards_data = json.load(f)

# merchant_cards_new = {int(floor): [Card.deserialize(card_data) for card_data in cards] for floor, cards in merchant_cards_data.items()}

# for card in merchant_cards_new[1]:
#     print(card.on_reveal_effect_serialise)
