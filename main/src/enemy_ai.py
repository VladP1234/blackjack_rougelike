from hand import Hand
from deck import Deck
from card import Card, AltValueCard


class EnemyAI:
    pass


class BasicAI(EnemyAI):
    @staticmethod
    def s_hit(hand: Hand, _):
        return hand.calculate_total() < 17


class AgressiveAI(EnemyAI):
    @staticmethod
    def s_hit(hand: Hand, _):
        return hand.calculate_total() < 18


class HyperAgressive(EnemyAI):
    @staticmethod
    def s_hit(hand: Hand, _):
        return hand.calculate_total() < 20


class PassiveAI(EnemyAI):
    @staticmethod
    def s_hit(hand: Hand, _):
        return hand.calculate_total() < 16


class HyperPassiveAI(EnemyAI):
    @staticmethod
    def s_hit(hand: Hand, _):
        return hand.calculate_total() < 14


class CheatAI(EnemyAI):
    @staticmethod
    def s_hit(hand: Hand, deck: Deck):
        if len(deck.cards) == 0:
            deck.shuffle_deck()
        if isinstance(deck.cards[0], AltValueCard):
            if hand.calculate_total() + deck.cards[0].value <= 21:
                return True
            else:
                if hand.calculate_total() + deck.cards[0].alt_value <= 21:
                    return True
                else:
                    return False
        else:
            return hand.calculate_total() + deck.cards[0].value <= 21
