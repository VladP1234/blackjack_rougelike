class StatusEffect:
    def __init__(self) -> None:
        pass
    def on_reveal(self, player):
        pass

    def on_turn_start(self, player):
        pass

    def on_turn_end(self, player):
        pass

    def on_remove(self, player):
        pass

class Bleeding(StatusEffect):
    def __init__(self, damage, duration) -> None:
        self.damage = damage
        self.duration = duration
    def on_reveal(self, player):
        stack_duration_damage(player, Bleeding, self)
    def on_turn_start(self, player):
        player.take_damage(self.damage)
        self.duration -= 1
        if self.duration == 0:
            player.remove_effect(self)

class Stun(StatusEffect):
    def __init__(self, duration) -> None:
        self.duration = duration
    def on_reveal(self, player):
        if player.stats.is_stunned:
            stack_duration(player, Stun, self)
        else:
            player.stats.is_stunned = True
    def on_turn_end(self, player):
        if self.duration == 0:
            player.remove_effect(self)
        self.duration -= 1

class Hex(StatusEffect):
    def __init__(self, damage) -> None:
        self.damage = damage
    def on_reveal(self, player):
        stack_duration(player, Hex, self)
    def on_turn_start(self, player):
        player.hp -= self.damage

class Poison(StatusEffect):
    def __init__(self, damage) -> None:
        self.damage = damage
    def on_reveal(self, player):
        stack_damage(player, Poison, self)
    def on_turn_start(self, player):
        if self.damage == 0:
            player.remove_effect(self)
        player.take_damage(self.damage)
        self.damage -= 1

from math import floor
class Burn(StatusEffect):
    def __init__(self, damage) -> None:
        self.damage = damage
    def on_reveal(self, player):
        stack_damage(player, Burn, self)
    def on_turn_start(self, player):
        if self.damage == 0:
            player.remove_effect(self)
        player.take_damage(self.damage)
        self.damage = floor(self.damage/2)

class Frostbite(StatusEffect):
    def __init__(self, damage, duration) -> None:
        self.damage = damage
        self.duration = duration
    def on_reveal(self, player):
        stack_damage(player, Frostbite, self)

class InstantArmour(StatusEffect):
    def __init__(self, armour_amount) -> None:
        self.armour_amount = armour_amount
    def on_reveal(self, player):
        player.stats.armour += self.armour_amount

class Blindness(StatusEffect):
    def __init__(self, duration) -> None:
        self.duration = duration
    def on_reveal(self, player):
        if player.stats.is_blind:
            stack_duration(player, Blindness, self)
        else:
            player.stats.is_blind = True
    def on_turn_end(self, player):
        if self.duration == 0:
            player.remove_effect(self)
            player.stats.is_blind = False
        self.duration -= 1


class InstantHeal(StatusEffect): 
    def __init__(self, heal_amount) -> None:
        self.heal_amount = heal_amount
    def on_reveal(self, player):
        if self.heal_amount > 0:
            player.heal(self.heal_amount)
        else:
            player.take_damage(self.heal_amount)

class InstantTempHp(StatusEffect):
    def __init__(self, hp_amount) -> None:
        self.hp_amount = hp_amount
    def on_reveal(self, player):
        player.stats.temp_hp += self.hp_amount

class Regen(StatusEffect):
    def __init__(self, heal_amount) -> None:
        self.damage = heal_amount
    def on_reveal(self, player):
        stack_damage(player, Regen, self)
    def on_turn_end(self, player):
        player.heal(self.heal_amount)
        self.damage -= 1
        if self.damage == 0:
            player.remove_effect(self)

class Vulnerable(StatusEffect):
    def __init__(self, duration) -> None:
        self.duration = duration
    def on_reveal(self, player):
        if player.stats.is_vulnerable:
            stack_duration(player, Vulnerable, self)
        else:
            player.stats.is_vulnerabe = True
    def on_turn_end(self, player):
        if self.duration == 0:
            player.remove_effect(self)
        self.duration -= 1


def stack_duration(player, class_type, class_to_stack):
    for status in player.status_effects:
        if isinstance(status, class_type):
            status.duration += class_to_stack.duration
            player.remove_effect(class_to_stack)

def stack_damage(player, class_type, class_to_stack):
    for status in player.status_effects:
        if isinstance(status, class_type):
            status.damage += class_to_stack.damage
            player.remove_effect(class_to_stack)

def stack_duration_damage(player, class_type, class_to_stack):
    for status in player.status_effects:
        if isinstance(status, class_type):
            status.damage += class_to_stack.damage
            status.duration += class_to_stack.duration
            player.remove_effect(class_to_stack)