from player import Player
from deck import Deck, DefaultDecks
import pygame
import pygame_gui
from collections import namedtuple
from enum import Enum, auto
from level import Combat, Merchant
from utils import Text

Bleeding = namedtuple('BLEEDING', ['damage'])

class CombatState(Enum):
    FIGHT = auto()
    REWARD = auto()

class CombatManager:
    def __init__(self, UIManager: pygame_gui.UIManager) -> None:
        self.player = Player(Deck((100, 200), False), UIManager=UIManager)
        self.leave_combat = False
        self.state: CombatState = CombatState.FIGHT
        
        # Change this later to an import from a .json
        self.hit_button = pygame_gui.elements.UIButton(pygame.Rect((100, 400), (50, 50)), text="hit", manager=UIManager)
        self.e_hit_button = pygame_gui.elements.UIButton(pygame.Rect((650, 400), (50, 50)), text="hit", manager=UIManager)
        self.stand_button = pygame_gui.elements.UIButton(pygame.Rect((100, 500), (50, 50)), text="stand", manager=UIManager)
        self.e_stand_button = pygame_gui.elements.UIButton(pygame.Rect((650, 500), (50, 50)), text="stand", manager=UIManager)
        
        self.rewards_text = pygame_gui.elements.UITextBox(f"REWARDS!", pygame.Rect(300, 50, 200, 50), UIManager)
        self.gold_button = pygame_gui.elements.UIButton(pygame.Rect((350, 200), (100, 50)), text="50 gold", manager=UIManager)
        self.exit_combat_button = pygame_gui.elements.UIButton(pygame.Rect(300, 400, 200, 50), text="Back to Map", manager=UIManager, tool_tip_text="Once you leave, you can't return")

        self.ui = []
        self.ui.append(self.hit_button)
        self.ui.append(self.e_hit_button)
        self.ui.append(self.stand_button)
        self.ui.append(self.e_stand_button)
        self.ui.append(self.rewards_text)
        self.ui.append(self.gold_button)
        self.ui.append(self.exit_combat_button)
        
        self.combat_ui = []
        self.combat_ui.append(self.hit_button)
        self.combat_ui.append(self.e_hit_button)
        self.combat_ui.append(self.stand_button)
        self.combat_ui.append(self.e_stand_button)
        
        self.reward_ui = []
        self.reward_ui.append(self.rewards_text)
        self.reward_ui.append(self.gold_button)
        self.reward_ui.append(self.exit_combat_button)
        
        self.hide_ui()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.hit_button:
                    self.player.hit()
                elif event.ui_element == self.e_hit_button:
                    self.enemy.hit()
                elif event.ui_element == self.stand_button:
                    self.player.stand()
                elif event.ui_element == self.e_stand_button:
                    self.enemy.stand()
                elif event.ui_element == self.gold_button:
                    self.player.gain_gold(self.reward.gold)
                    self.gold_button.hide()
                elif event.ui_element == self.exit_combat_button:
                    self.leave_combat = True
    def update(self):
        if self.state == CombatState.FIGHT:
            if self.player.effect:
                self.player.effect(self)
                self.player.effect = None
            if self.player.standing and self.enemy.standing:
                self.player.resolve_status_effects()
                self.enemy.resolve_status_effects()
                player_total = self.player.hand.calculate_total()
                enemy_total = self.enemy.hand.calculate_total()
                if player_total == 21:
                    for card in self.player.hand.cards:
                        if card.on_blackjack_effect:
                            self.effects.append(card.on_blackjack_effect)
                if player_total > enemy_total:
                    if player_total <= 21:
                        self.player.deal_damage(self.enemy, player_total - enemy_total)
                    elif enemy_total <= 21:
                        self.enemy.deal_damage(self.player, enemy_total - 11)

                if enemy_total > player_total:
                    if enemy_total <= 21:
                        self.enemy.deal_damage(self.player, enemy_total - player_total)
                    elif player_total <= 21:
                        self.player.deal_damage(self.enemy, player_total - 11)
                self.player.standing = False
                self.enemy.standing = False
                self.player.reset()
                self.enemy.reset()
            if self.enemy.hp <= 0:
                self.change_state(CombatState.REWARD)
                self.player.deck.shuffle_deck()
            if self.player.hp <= 0:
                # End of game code
                pass

    def draw(self, screen: pygame.Surface):
        self.player.draw(screen)
        self.enemy.draw(screen)

    def hide_ui(self):
        for ui in self.ui:
            ui.visible = False
    def show_ui(self):
        for ui in self.ui:
            ui.visible = True
        self.change_state(CombatState.FIGHT)
    
    def hide_combat_ui(self):
        for ui in self.combat_ui:
            ui.visible = False
    def show_combat_ui(self):
        for ui in self.combat_ui:
            ui.visible = True

    def hide_reward_ui(self):
        for ui in self.reward_ui:
            ui.visible = False

    def show_reward_ui(self):
        for ui in self.reward_ui:
            ui.visible = True
    

    def change_state(self, new_state: CombatState):
        if new_state == CombatState.FIGHT:
            self.hide_reward_ui()
            self.show_combat_ui()
        elif new_state == CombatState.REWARD:
            self.show_reward_ui()
            self.hide_combat_ui()
        self.state = new_state

    def enter_combat(self, level: Combat):
        self.leave_combat = False
        self.player.deck.shuffle_deck()
        self.enemy = level.enemy
        self.reward = level.reward
        self.update_rewards()

    def update_rewards(self):
        self.gold_button.set_text(f"{self.reward.gold} gold")