import pygame
import pygame_gui
from utils import make_text
from card import Card, AltValueCard
from json import load
from deck import Deck


class Arrow:
    def __init__(self) -> None:
        self.arrow1 = pygame.transform.scale(
            pygame.image.load("main/Sprites/Base/casino_arrow_1.png"), (200, 200)
        )
        self.arrow2 = pygame.transform.scale(
            pygame.image.load("main/Sprites/Base/casino_arrow_2.png"), (200, 200)
        )
        self.active_arrow = 1
        self.arrow_delay = 0

    def draw(self, screen: pygame.Surface):
        # makes arrow flash
        if self.arrow_delay < 10:
            self.arrow_delay += 1

        if self.active_arrow == 1:
            screen.blit(self.arrow1, (575, 200))
            if self.arrow_delay == 10:
                self.active_arrow = 2
                self.arrow_delay = 0
        elif self.active_arrow == 2:
            screen.blit(self.arrow2, (575, 200))
            if self.arrow_delay == 10:
                self.active_arrow = 1
                self.arrow_delay = 0


class DeckSelector:
    def __init__(self, UIManager: pygame_gui.UIManager) -> None:
        self.selected_deck: Deck | None = None
        with open("starter_decks.json") as f:
            self.decks = {}
            for name, card_list in load(f).items():
                deck = []
                for card_data in card_list:
                    card_type = Card
                    if "alt_value" in card_data:
                        card_type = AltValueCard
                    deck.append(card_type.deserialize(card_data))
                self.decks[name] = deck

            # self.decks = {name : [Card.deserialize(card_data) for card_data in card_list] for name, card_list in load(f).items()}
        self.buttons = []

        button_layout = {
            "Hearts": (50, 100),
            "Clubs": (200, 100),
            "Diamonds": (350, 100),
            "Spades": (500, 100),
            "Alties": (650, 100),
        }
        # generates buttons which allows the player to select a starting deck
        for deck_type, position in button_layout.items():
            button = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(position, (100, 50)),
                text=deck_type.capitalize(),
                manager=UIManager,
            )
            self.buttons.append((button, deck_type))
        self.title_text = make_text("Pick a starting deck", 50)
        self.hide_ui()

    def handle_events(self, event):
        for button, deck_type in self.buttons:
            if (
                event.type == pygame.USEREVENT
                and event.user_type == pygame_gui.UI_BUTTON_PRESSED
            ):
                if event.ui_element == button:
                    self.selected_deck = self.decks[deck_type]
                    self.hide_ui()
                    break

    def update(self):
        pass

    def draw(self, screen: pygame.Surface):
        screen.blit(self.title_text, (300, 50))

    def hide_ui(self):
        for button, _ in self.buttons:
            button.hide()

    def show_ui(self):
        for button, _ in self.buttons:
            button.show()


# main class of the file, all other classes "report" to it
class Base:
    def __init__(self, UIManager) -> None:
        self.arrow = Arrow()
        self.ui = []
        self.start_run_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((575, 200), (190, 190)),
            text="",
            manager=UIManager,
        )
        self.ui.append(self.start_run_button)
        self.start_run = False
        self.deck_selector = DeckSelector(UIManager)
        self.selecting_decks = False

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.start_run_button:
                    self.selecting_decks = True
                    self.deck_selector.show_ui()
                    self.hide_ui()
            self.deck_selector.handle_events(event)

    def update(self):
        if self.selecting_decks:
            self.deck_selector.update()
        if self.deck_selector.selected_deck:
            self.start_run = True

    def hide_ui(self):
        self.start_run = False
        for ui in self.ui:
            ui.visible = False

    def show_ui(self):
        self.start_run = False
        self.selecting_decks = False
        self.selecting_decks = False
        self.deck_selector.selected_deck = None
        for ui in self.ui:
            ui.visible = True

    def draw(self, screen: pygame.Surface):
        if self.selecting_decks:
            self.deck_selector.draw(screen)
        else:
            self.arrow.draw(screen)
