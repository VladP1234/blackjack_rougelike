from card import Card, AltValueCard, heart_on_reveal
from typing import List, Dict
from enum import Enum, auto
import pygame
from json import load
from random import shuffle

class DefaultDecks(Enum):
    Base = auto()
    Sample1 = auto()

class Deck:
    def __init__(self, pos: (int, int), is_enemy, cards: List[Card|AltValueCard]|DefaultDecks = DefaultDecks.Sample1) -> None:
        if is_enemy:
            self.modifier = -1
        else:
            self.modifier = 1
        if type(cards) == DefaultDecks:
            # with open('decks.json', 'r') as decks_file:
            #     decks: Dict[str, str] = load(decks_file)
            match cards:
                case DefaultDecks.Base:
                    self.cards = [
                        AltValueCard(11, 'main/Sprites/Card_Back.png', 1, (pos[0] + 200 * self.modifier - 50 * self.modifier, pos[1])),
                        Card(2, 'main/Sprites/Cards/2_hearts.png',  (pos[0] + self.modifier * 150, pos[1])),
                        Card(3, 'main/Sprites/Cards/3_hearts.png',  (pos[0] + self.modifier * 150, pos[1])),
                        Card(4, 'main/Sprites/Cards/4_hearts.png',  (pos[0] + self.modifier * 150, pos[1])),
                        Card(5, 'main/Sprites/Cards/5_hearts.png',  (pos[0] + self.modifier * 150, pos[1])),
                        Card(6, 'main/Sprites/Cards/6_hearts.png',  (pos[0] + self.modifier * 150, pos[1])),
                        Card(7, 'main/Sprites/Cards/7_hearts.png',  (pos[0] + self.modifier * 150, pos[1])),
                        Card(8, 'main/Sprites/Cards/8_hearts.png',  (pos[0] + self.modifier * 150, pos[1])),
                        Card(9, 'main/Sprites/Cards/9_hearts.png',  (pos[0] + self.modifier * 150, pos[1])),
                        Card(10, 'main/Sprites/Cards/10_hearts.png', (pos[0] + self.modifier * 150, pos[1])),
                        Card(10, 'main/Sprites/Cards/10_hearts.png', (pos[0] + self.modifier * 150, pos[1])),
                        Card(10, 'main/Sprites/Cards/10_hearts.png', (pos[0] + self.modifier * 150, pos[1])),
                        Card(10, 'main/Sprites/Cards/10_hearts.png', (pos[0] + self.modifier * 150, pos[1])),
                    ]
                case DefaultDecks.Sample1:
                    self.cards = [
                        Card(10, 'main/Sprites/Card_Back.png', (pos[0] + 200 * self.modifier - 50 * self.modifier, pos[1])),
                        Card(10, 'main/Sprites/Card_Back.png', (pos[0] + 200 * self.modifier - 50 * self.modifier, pos[1])),
                        Card(10, 'main/Sprites/Card_Back.png', (pos[0] + 200 * self.modifier - 50 * self.modifier, pos[1])),
                    ]
        else:
            self.cards = cards
        self.pos = pos
        self.image = pygame.image.load('main/Sprites/Deck.png')
        self.image = pygame.transform.scale(self.image, (255/2, 381/2))
        self.discard_pile: List[Card | AltValueCard] = []

    def draw(self, screen: pygame.Surface):
        screen.blit(self.image, self.pos)
    def draw_card(self) -> Card:
        if len(self.cards) == 0:
            self.shuffle_deck()
        top_card = self.cards.pop(0)
        self.discard_pile.append(top_card)
        return top_card
    
    def shuffle_deck(self):
        while len(self.discard_pile) > 0:
            self.cards.append(self.discard_pile.pop())
        shuffle(self.cards)

# used GPT for this since I couldn't be bothered to build this QoL feature, hence the presense of comments
# At least I found out about enumerate which would have come in handy any time I used temporary counters
def display_cards(screen, cards: List[Card|AltValueCard]):
    running = True
    clock = pygame.time.Clock()
    y_scroll_offset = 150
    horizontal_spacing, vertical_spacing = 200, 250
    cards_per_row = 4

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False 
            if event.type == pygame.MOUSEWHEEL:
                y_scroll_offset += event.y * 30  # Scroll speed

        screen.fill((200, 200, 200))  # Clear screen with black background

        # Draw cards with the current scroll offset
        for i, card in enumerate(cards):
            row = i // cards_per_row
            col = i % cards_per_row
            x = col * horizontal_spacing - 200
            y = row * vertical_spacing - y_scroll_offset
            card.draw(screen, x, -y)

        pygame.display.flip()  # Update the screen with what we've drawn

        clock.tick(60)
    