from hand import Hand
from deck import Deck, DefaultDecks
from utils import make_text
from status_effect import *
import pygame
import pygame_gui

class Player:
    def __init__(self, deck: Deck, is_enemy: bool = False, UIManager = False) -> None:
        self.hand = Hand(is_enemy)
        self.deck = deck
        self.hp_blit_pos = (deck.pos[0], deck.pos[1]-100)
        self.hp = 10
        self.max_hp = 20
        self.standing = False

        if not is_enemy:
            self.hud = Hud(UIManager)
            self.gold = 0
            self.gain_gold(10000)
        
        self.stats = Stats()
        self.block = 0
        
        self.effect = None

        self.status_effects = []
    def draw(self, screen: pygame.Surface):
        self.deck.draw(screen)
        self.hand.draw(screen)
        screen.blit(make_text(f'{self.hp}', 20), self.hp_blit_pos)

    def display_effcts(self, screen: pygame.Surface):
        pass
    
    def hit(self):
        top_card = self.deck.draw_card()
        if top_card.on_reveal_effect:
            self.effect = top_card.on_reveal_effect
        self.hand.cards.append(top_card)
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
        self.status_effects.append(effect)
        if effect.has_on_reveal_effect:
            effect.on_reveal(self)
    
    def resolve_status_effects(self):
        for status in self.status_effects:
            status.on_turn_end(self)
    
    def remove_effect(self, effect):
        for s_effect in self.status_effects:
            if s_effect == effect:
                self.status_effects.remove(effect)

    def heal(self, heal_amount):
        self.hp = min(self.hp + heal_amount, self.max_hp)

    def deal_damage(self, enemy, damage_amount):
        flat_modifier = 0
        flat_modifier += self.stats.strength
        percent_modifier =  1
        percent_modifier += 0.25 if self.stats.is_raging else 0
        percent_modifier -= 0.25 if self.stats.is_weak else 0
        percent_modifier *= 1.5 if enemy.stats.is_vulnerable else 1

        enemy.take_damage((damage_amount + flat_modifier)*percent_modifier)

    def take_damage(self, damage_amount):
        self.block -= damage_amount
        if self.block < 0:
            self.hp += self.block
            self.block = 0

    def gain_block(self, block_amount):
        self.block += block_amount + self.stats.dexterity

class Hud: 
    def __init__(self, UIManager) -> None:
        self.gold = pygame_gui.elements.UITextBox(
            "0 gold", 
            pygame.Rect(600, 25, 100, 50),
            UIManager
        )
    def update_gold(self, total_gold: int | float):
        self.gold.html_text = f"{total_gold} gold"
        self.gold.rebuild()

class Stats():
    def __init__(self) -> None:
        self.strength = 0
        self.dexterity = 0
        self.is_weak = False
        self.is_vulnerable = False
        self.is_raging = False