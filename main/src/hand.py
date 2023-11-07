import pygame
from card import Card, AltValueCard
from typing import List
from utils import make_text

class Hand:
    def __init__(self, is_enemy) -> None:
        self.cards: List[Card|AltValueCard] = []
        self.total = 0
        if is_enemy:
            self.modifier = -1
        else:
            self.modifier = 1
    def add_card(self, card):
        self.cards.append(card)
    def draw(self, screen: pygame.Surface):
        # screen.blit(make_text(f'{len(self.cards)}', 12), (400 + 200*-self.modifier, 100))
        offset = 0
        for card in self.cards:
            offset += 5*self.modifier
            card.draw(screen, offset, abs(offset))
        self.total = make_text(str(self.calculate_total()), 24)
        if self.modifier == 1:
            screen.blit(self.total, (150, 150))
        if self.modifier == -1:
            screen.blit(self.total, (650, 150))
    def calculate_total(self) -> int:
        total = 0
        for card in self.cards:
            total += card.value
        
        return total
        alt_value_cards: List[AltValueCard] = []
        
        # TODO: implement over 21 alt value stuff

        # if total > 21:
        #     for card in self.cards:
        #         if type(card) == AltValueCard:
        #             alt_value_cards.append(card)
        # for card in alt_value_cards:
        #     if card.alt_value == total -
