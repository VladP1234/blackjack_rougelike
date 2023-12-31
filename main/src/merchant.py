from level import Merchant
from card import Card, AltValueCard
from typing import Dict, List
import pygame
import pygame_gui
from random import sample, randint
from player import Player
from re import findall
from utils import make_text
import json


class MerchantManager:
    def __init__(self, UIManager: pygame_gui.UIManager, player: Player) -> None:
        self.leave_merchant = False
        self.cards: Dict[pygame_gui.elements.UIButton, Card | AltValueCard] = {}
        self.ui = []
        self.leave_merchant_button = pygame_gui.elements.UIButton(
            pygame.Rect(500, 525, 200, 50),
            text="Back to Map",
            manager=UIManager,
            tool_tip_text="Once you leave, you can't return",
        )
        self.ui.append(self.leave_merchant_button)
        self.bought_cards: List[Card | AltValueCard] = []

        self.player = player

        self.attempt_counter = 0
        self.warning_message = None
        self.warning_message_timer = None

        self.hide_ui()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element in self.cards:
                    clicked_button = None
                    for button, card in self.cards.items():
                        if event.ui_element == button:
                            cost = int(findall(r"\d+", button.tool_tip_text)[0])
                            if self.player.gold >= cost:
                                card.pos = (250, 200)
                                self.player.deck.cards.append(card)
                                clicked_button = button
                                button.kill()
                                self.player.gain_gold(-cost)
                            else:
                                self.attempt_counter += 1
                                if self.attempt_counter > 10:
                                    self.display_warning_message()

                    if clicked_button:
                        del self.cards[clicked_button]
                elif event.ui_element == self.leave_merchant_button:
                    self.leave_merchant = True

    def update(self):
        pass

    def draw(self, screen: pygame.Surface):
        for button, card in self.cards.items():
            card.draw(
                screen, button.relative_rect.left + 10, -5 - button.relative_rect.top
            )
        if self.warning_message:
            # Calculate the position for the text to be centered on the screen
            screen_center_x = screen.get_width() // 2
            screen_center_y = screen.get_height() // 2
            message_rect = self.warning_message.get_rect(
                center=(screen_center_x, screen_center_y)
            )

            screen.blit(self.warning_message, message_rect.topleft)
            if pygame.time.get_ticks() - self.warning_message_timer > 3000:  # 3 seconds
                self.warning_message = None
                self.attempt_counter = 5

    def hide_ui(self):
        for ui in self.ui:
            ui.visible = False
        for button in self.cards:
            button.kill()
        self.cards = {}

    def show_ui(self):
        for ui in self.ui:
            ui.visible = True

    def enter_merchant(self, level: Merchant, floor, UIManager: pygame_gui.UIManager):
        self.leave_merchant = False
        self.generate_cards(floor, UIManager)

    def generate_cards(self, floor: int, UIManager: pygame_gui.UIManager):
        card_num = 0
        y_mod = 0
        x_mod = -200
        for card in sample(self.get_merchant_cards(floor), k=6):
            card_num += 1
            x_mod += 200
            if card_num == 5:
                x_mod = 0
                y_mod += 250
            button = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(25 + x_mod, 100 + y_mod, 150, 200),
                text=f"{card.name}",
                manager=UIManager,
                tool_tip_text=f"{randint(50, 200)} gold",
            )
            self.cards[button] = card

    @staticmethod
    def get_merchant_cards(floor):
        # Read in the JSON file
        with open("expanded_merchant_cards_v2.json", "r") as f:
            merchant_cards_data = json.load(f)

        merchant_cards_new = {
            int(floor): [Card.deserialize(card_data) for card_data in cards]
            for floor, cards in merchant_cards_data.items()
        }

        return merchant_cards_new[floor]

    # Code generated by GPT because I didn't want to spend much time on this joke
    def display_warning_message(self):
        self.warning_message = make_text(
            "This is not a charity", 74, (255, 0, 0)
        )  # Large red text
        self.warning_message_timer = (
            pygame.time.get_ticks()
        )  # Record the time when the message is displayed
