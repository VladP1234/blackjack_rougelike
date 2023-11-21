from enum import Enum, auto
from base import Base
from game_map import GameMap
from combat_manager import CombatManager
from merchant import MerchantManager
from deck import display_cards
from random import sample
import pygame
import pygame_gui
import sys

class GameState(Enum):
    BASE = auto()
    MAP = auto()
    COMBAT = auto()
    MERCHANT = auto()


class Game:
    def __init__(self, width=900, height=600, fps=60):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        self.gui_manager = pygame_gui.UIManager((width, height))
        self.clock = pygame.time.Clock()
        self.fps = fps
        self.running = True
        self.in_combat = False
        self.enemy = None
        self.state = GameState.BASE
        self.base = Base(self.gui_manager)
        self.game_map = GameMap(self.gui_manager)
        self.combat_manager = CombatManager(self.gui_manager)
        self.merchant_manager = MerchantManager(self.gui_manager, self.combat_manager.player)
        self.clock = pygame.time.Clock()

    def handle_events(self):
        for event in pygame.event.get():
            self.gui_manager.process_events(event)
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                # if event.key == pygame.K_ESCAPE:
                #     self.running = False
                if event.key == pygame.K_d:
                    display_cards(self.screen, sample(self.combat_manager.player.deck.cards, len(self.combat_manager.player.deck.cards)))
        if self.state == GameState.BASE:
            self.base.handle_events()
        elif self.state == GameState.MAP:
            self.game_map.handle_events()
        elif self.state == GameState.COMBAT:
            self.combat_manager.handle_events()
        elif self.state == GameState.MERCHANT:
            self.merchant_manager.handle_events()

    def update(self):
        self.gui_manager.update(time_delta=self.clock.tick(60)/1000.0)
        if self.state == GameState.BASE:
            self.base.update()
            if self.base.start_run:
                self.change_state(GameState.MAP)
                self.combat_manager.player.deck.cards = self.base.deck_selector.selected_deck
                self.game_map.reset()
                self.combat_manager.reset()
                # self.combat_manager = CombatManager(self.gui_manager)
                # self.merchant_manager = MerchantManager(self.gui_manager, self.combat_manager.player)
                # print("changed state to map")
        elif self.state == GameState.MAP:
            self.game_map.update()
            if self.game_map.go_to_combat:
                self.game_map.go_to_combat = False
                self.change_state(GameState.COMBAT)
                # print("entering combat")
            if self.game_map.go_to_merchant:
                self.game_map.go_to_merchant = False
                self.change_state(GameState.MERCHANT)
                # print("entering merchant")
            self.gui_manager.update(time_delta=self.clock.tick(60)/1000.0)
        elif self.state == GameState.COMBAT:
            self.combat_manager.update()
            # if self.combat_manager.effects:
            #     print("here")
            #     for effect in self.combat_manager.effects:
            #         effect(self)
            if self.combat_manager.leave_combat:
                if self.combat_manager.player.hp <= 0:
                    self.change_state(GameState.BASE)
                else:
                    self.game_map.go_to_next_level()
                    self.change_state(GameState.MAP)
        elif self.state == GameState.MERCHANT:
            self.merchant_manager.update()
            if self.merchant_manager.leave_merchant:
                self.game_map.go_to_next_level()
                self.change_state(GameState.MAP)
    
    def change_state(self, new_state: GameState):
        if new_state == GameState.BASE:
            self.base.show_ui()
            self.combat_manager.hide_ui()
        elif new_state == GameState.MAP:
            self.base.hide_ui()
            self.combat_manager.hide_ui()
            self.merchant_manager.hide_ui()
            self.game_map.show_ui()
        elif new_state == GameState.COMBAT:
            self.game_map.hide_ui()
            self.combat_manager.show_ui()
            self.combat_manager.enter_combat(self.game_map.current_level)
        elif new_state == GameState.MERCHANT:
            self.game_map.hide_ui()
            self.merchant_manager.show_ui()
            self.merchant_manager.enter_merchant(self.game_map.current_level, self.game_map.floor_num, self.gui_manager)
        self.state = new_state
    
    def draw(self):
        self.screen.fill((200, 200, 200))
        self.gui_manager.draw_ui(self.screen)
        if self.state == GameState.BASE:
            self.base.draw(self.screen)
        elif self.state == GameState.MAP:
            self.game_map.draw(self.screen)
        elif self.state == GameState.COMBAT:
            self.combat_manager.draw(self.screen)
        elif self.state == GameState.MERCHANT:
            self.merchant_manager.draw(self.screen)
        pygame.display.update()

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            pygame.display.flip()
            self.clock.tick(self.fps)

        pygame.quit()
        sys.exit()
