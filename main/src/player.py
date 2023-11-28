from hand import Hand
from enemy_ai import EnemyAI, BasicAI, CheatAI
from deck import Deck, DefaultDecks
from utils import make_text
from status_effect import *
from typing import Dict
import pygame
import pygame_gui


class Stats:
    def __init__(self) -> None:
        self.strength = 0
        self.dexterity = 0
        self.armour = 0
        self.temp_hp = 0
        self.is_blind = False
        self.is_weak = False
        self.is_vulnerable = False
        self.is_raging = False
        self.is_stunned = False

    def reset(self):
        self.strength = 0
        self.dexterity = 0
        self.armour = 0
        self.temp_hp = 0
        self.is_blind = False
        self.is_weak = False
        self.is_vulnerable = False
        self.is_raging = False
        self.is_stunned = False

    def to_dict(self) -> Dict:
        return {
            "strength": self.strength,
            "dexterity": self.dexterity,
            "armour": self.armour,
            "temp_hp": self.temp_hp,
            "is_blind": self.is_blind,
            "is_weak": self.is_weak,
            "is_vulnerable": self.is_vulnerable,
            "is_raging": self.is_raging,
            "is_stunned": self.is_stunned,
        }

    @classmethod
    def from_dict(cls, attributes_dict):
        return cls(
            strength=attributes_dict["strength"],
            dexterity=attributes_dict["dexterity"],
            armour=attributes_dict["armour"],
            temp_hp=attributes_dict["temp_hp"],
            is_blind=attributes_dict["is_blind"],
            is_weak=attributes_dict["is_weak"],
            is_vulnerable=attributes_dict["is_vulnerable"],
            is_raging=attributes_dict["is_raging"],
            is_stunned=attributes_dict["is_stunned"],
        )


class Player:
    def __init__(
        self,
        deck: Deck,
        is_enemy: bool = False,
        UIManager=None,
        enemy_ai: EnemyAI | None = None,
        stats: Stats = None,
    ) -> None:
        self.hand = Hand(is_enemy)
        self.deck = deck
        self.hp_blit_pos = (deck.pos[0], deck.pos[1] - 100)
        self.hp = 10
        self.max_hp = 20
        self.standing = False
        self.is_enemy = is_enemy

        if not is_enemy:
            self.hud = Hud(UIManager)
            self.gold = 0
        else:
            self.ai = enemy_ai

        self.stats = stats or Stats()

        self.block = 0

        self.effect = None

        self.status_effects = []

    def to_dict(self) -> Dict:
        return {
            "is_enemy": self.is_enemy,
            "deck": self.deck.to_dict(),
            "hp": self.hp,
            "max_hp": self.max_hp,
            "ai": type(self.ai).__name__,
            "stats": self.stats.to_dict(),
        }

    @classmethod
    def from_dict(cls, data, UIManager):
        return_class = cls(
            Deck.from_dict(data["deck"]),
            is_enemy=data["is_enemy"],
            UIManager=UIManager,
            enemy_ai=globals()[data["ai"]](),
        )
        return_class.hp = data["hp"]
        return_class.max_hp = data["max_hp"]
        return return_class

    def draw(self, screen: pygame.Surface, icon_dict):
        if self.hand.calculate_total() >= 21:
            self.standing = True
        self.deck.draw(screen)
        self.hand.draw(screen)
        self.display_hp(screen)
        screen.blit(make_text(f"{self.hp}", 20), self.hp_blit_pos)
        self.display_effcts(screen, icon_dict)

    # Used GPT for this, made a health bar a 100 times before, no need for me to make it 101 tiei
    def display_hp(self, screen: pygame.Surface):
        BAR_WIDTH = 120
        BAR_HEIGHT = 10

        # Calculate the width of the foreground health bar
        health_ratio = self.hp / self.max_hp
        foreground_width = BAR_WIDTH * health_ratio

        # Create the background rectangle (red)
        background_rect = pygame.Rect(
            (self.deck.pos[0], self.deck.pos[1] + 190), (BAR_WIDTH, BAR_HEIGHT)
        )
        pygame.draw.rect(screen, (255, 0, 0), background_rect)  # Red

        # Create the foreground rectangle (green)
        foreground_rect = pygame.Rect(
            (self.deck.pos[0], self.deck.pos[1] + 190), (foreground_width, BAR_HEIGHT)
        )
        pygame.draw.rect(screen, (0, 255, 0), foreground_rect)  # Green

        temp_hp_rect = pygame.Rect(
            (self.deck.pos[0], self.deck.pos[1] + 190),
            (BAR_WIDTH * self.stats.temp_hp / self.max_hp, BAR_HEIGHT),
        )
        pygame.draw.rect(screen, (255, 255, 0), temp_hp_rect)
        if self.stats.temp_hp > 0:
            screen.blit(
                make_text(str(self.stats.temp_hp), 28),
                (self.deck.pos[0], self.deck.pos[1] + 210),
            )

    def display_effcts(
        self, screen: pygame.Surface, icon_dict: Dict[str, pygame.Surface]
    ):
        offset = 1 if self.is_enemy else -1
        for counter, effect in enumerate(self.status_effects):
            # print(type(effect), self.is_enemy)
            if isinstance(effect, Blindness):
                screen.blit(
                    icon_dict["Blindness"], (390 + 365 * offset, counter * 100 + 50)
                )
                screen.blit(
                    make_text(str(effect.duration), 40, color=(200, 0, 0)),
                    (415 + 340 * offset, counter * 100 + 90),
                )
            if isinstance(effect, Bleeding):
                screen.blit(
                    icon_dict["Bleeding"], (390 + 365 * offset, counter * 100 + 50)
                )
                screen.blit(
                    make_text(str(effect.duration), 40, color=(0, 0, 0)),
                    (415 + 340 * offset, counter * 100 + 90),
                )
                screen.blit(
                    make_text(str(effect.damage), 40, color=(0, 0, 0)),
                    (460 + 340 * offset, counter * 100 + 90),
                )

    def hit(self):
        if not self.standing:
            top_card = self.deck.draw_card()
            if top_card.on_reveal_effect:
                self.effect = top_card.on_reveal_effect
            self.hand.cards.append(top_card)
            if self.stats.is_stunned:
                if len(self.hand.cards) >= 2:
                    self.stand()

    def stand(self):
        self.standing = True

    def reset(self):
        # while len(self.hand.cards) > 0:
        self.hand.cards = []

    def gain_gold(self, gold: int | float):
        self.gold += gold
        self.hud.update_gold(self.gold)

    # Status effect code
    def affect(self, effect: StatusEffect):
        effect.on_reveal(self)
        if not effect.dupe:
            self.status_effects.append(effect)

    def turn_end_status(self):
        for status in self.status_effects:
            status.on_turn_end(self)

    def turn_start_status(self):
        for status in self.status_effects:
            status.on_turn_start(self)

    def remove_effect(self, effect):
        for s_effect in self.status_effects:
            if s_effect == effect:
                self.status_effects.remove(effect)

    def heal(self, heal_amount):
        self.hp = min(self.hp + heal_amount, self.max_hp)

    def deal_damage(self, enemy, damage_amount):
        flat_modifier = 0
        flat_modifier += self.stats.strength
        for effect in self.status_effects:
            if isinstance(effect, Frostbite):
                flat_modifier -= effect.damage
        percent_modifier = 1
        percent_modifier += 0.25 if self.stats.is_raging else 0
        percent_modifier -= 0.25 if self.stats.is_weak else 0
        percent_modifier *= 1.5 if enemy.stats.is_vulnerable else 1
        if self.stats.is_blind:
            percent_modifier = 0
        enemy.take_damage((damage_amount + flat_modifier) * percent_modifier)

    def take_damage(self, damage_amount):
        damage_amount -= self.stats.armour
        if damage_amount > 0:
            self.block -= damage_amount
            if self.block < 0:
                self.stats.temp_hp += self.block
                self.block = 0
                if self.stats.temp_hp < 0:
                    self.hp += self.stats.temp_hp
                    self.stats.temp_hp = 0

    def gain_block(self, block_amount):
        self.block += block_amount + self.stats.dexterity


class Hud:
    def __init__(self, UIManager) -> None:
        self.gold = pygame_gui.elements.UITextBox(
            "0 gold", pygame.Rect(700, 25, 100, 50), UIManager
        )

    def update_gold(self, total_gold: int | float):
        self.gold.html_text = f"{total_gold} gold"
        self.gold.rebuild()
