from hand import Hand

class EnemyAI:
    pass

class BasicAI(EnemyAI):
    @staticmethod
    def s_hit(hand: Hand):
        return hand.calculate_total() < 17
    
    