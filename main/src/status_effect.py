class StatusEffect:
    def __init__(self, has_on_reveal_effect=False) -> None:
        self.has_on_reveal_effect = has_on_reveal_effect
    def on_reveal(self, player):
        pass

    def on_turn_start(self, player):
        pass

    def on_turn_end(self, player):
        pass

    def on_remove(self, player):
        pass

class InstantArmour(StatusEffect):
    def __init__(self, armour_amount) -> None:
        super().__init__(True)
        self.armour_amount = armour_amount
    def on_reveal(self, player):
        player.stats.armour += self.armour_amount

class Blindness(StatusEffect):
    def __init__(self, duration) -> None:
        super().__init__(True)
        self.duration = duration
    def on_reveal(self, player):
        if player.stats.is_blind:
            for status in player.status_effects:
                if isinstance(status, Blindness):
                    status.duration += self.duration
                    player.remove_effect(self)
        else:
            player.stats.is_blind = True
    def on_turn_end(self, player):
        if self.duration == 0:
            player.remove_effect(self)
        self.duration -= 1

class InstantHeal(StatusEffect):
    def __init__(self, heal_amount) -> None:
        super().__init__(True)
        self.heal_amount = heal_amount
    def on_reveal(self, player):
        player.heal(self.heal_amount)

class Regen(StatusEffect):
    def __init__(self, heal_amount) -> None:
        super().__init__()
        self.heal_amount = heal_amount
    def on_turn_end(self, player):
        player.heal(self.heal_amount)
        self.heal_amount -= 1
        if self.heal_amount == 0:
            player.remove_effect(self)

class Vulnerable(StatusEffect):
    def __init__(self, duration) -> None:
        super().__init__(True)
        self.duration = duration
    def on_reveal(self, player):
        if player.stats.is_vulnerable:
            for status in player.status_effects:
                if isinstance(status, Vulnerable):
                    status.duration += self.duration
                    player.remove_effect(self)
        else:
            player.stats.is_vulnerabe = True
    def on_turn_end(self, player):
        if self.duration == 0:
            player.remove_effect(self)
        self.duration -= 1
