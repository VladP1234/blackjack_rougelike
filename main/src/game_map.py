from utils import make_text
from deck import Deck
from level import Combat, Merchant
from typing import Dict
from serialise import json_to_dict
import pygame
import pygame_gui


class GameMap:
    def __init__(self, UIManager) -> None:
        self.ui = []
        self.go_to_combat = False
        self.go_to_merchant = False
        self.floor_num = 1
        self.buttons: Dict[pygame_gui.elements.UIButton, Combat|Merchant] = {}
        self.current_floor = self.load_floor(self.floor_num, UIManager)
        self.current_level = self.buttons[list(self.buttons.keys())[0]]
        self.floor_texts = {
            1: make_text("Floor 1", 54),
            2: make_text("Floor 2", 54),
            3: make_text("Floor 3", 54) 
        }
        self.UIManager = UIManager
        
        # self.combat1_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((100, 200), (190, 190)), text="", manager=UIManager)
        # self.ui.append(self.combat1_button)
        
        self.hide_ui()

    def load_floor(self, floor_num: int, UIManager) -> Dict[str, Combat|Merchant]:
        floors = json_to_dict("floors.json", UIManager)
        # print(floors)
        floor: Dict[str, Combat | Merchant] = floors[str(floor_num)]
        self.buttons = {}
        for level_id, level in floor.items():
            y_mod = 0
            if level_id.isdigit():
                level_num = int(level_id)
            else:
                level_num = int(level_id[0])
                if level_id[1] == "A":
                    y_mod = -75
                elif level_id[1] == "B":
                    y_mod = 75
            button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(100 * level_num - 50, 200 + y_mod, 50, 50), text=f"{level_id}", manager=UIManager)
            if level_num != 1:
                button.disable()
            self.buttons[button] = level
            self.current_level_num = 1

        return floor

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                self.hide_ui()
                if event.ui_element in self.buttons:
                    self.current_level = None
                    for button, level in self.buttons.items():
                        if event.ui_element == button:
                            self.current_level = level
                            # print(self.current_level)
                        if type(self.current_level) == Merchant:
                            self.go_to_merchant = True
                            break
                        elif type(self.current_level) == Combat:
                            self.go_to_combat = True
                            break

    def draw(self, screen: pygame.Surface):
        screen.blit(self.floor_texts[self.floor_num], (350, 50))
    
    def update(self):
        pass

    def hide_ui(self):
        self.go_to_combat = False
        for ui in self.ui:
            ui.visible = False
        for button in self.buttons:
            button.visible = False
    def show_ui(self):
        for ui in self.ui:
            ui.visible = True
        for button in self.buttons:
            button.visible = True
    def go_to_next_level(self):
        self.current_level_num += 1
        if self.current_level_num == 8:
            self.current_level_num = 0
            self.floor_num += 1
            self.current_floor = self.load_floor(self.floor_num, self.UIManager)
        for button in self.buttons:
            if button.text[0] == str(self.current_level_num):
                button.enable()
            else:
                button.disable()