import pygame


class Text:
    def __init__(self, pos: pygame.Rect, text_surf: pygame.Surface) -> None:
        self.pos = pos
        self.text_surf = text_surf
        self.visible = True

    def draw(self, screen: pygame.Surface):
        if self.visible:
            screen.blit(self.text_surf, self.pos)


def make_text(text: str, font_size: int, color: tuple = (0, 0, 0)) -> pygame.Surface:
    font = pygame.font.Font(None, font_size)
    text_surface = font.render(text, True, color)
    return text_surface


# floor1 = Level(Player((623, 200), True))

# serialise()

# AltValueCard(11, 'main/Sprites/Card_Back.png', 1, (pos[0] + 200 * self.modifier - 50 * self.modifier, pos[1])),
#             Card(2, 'main/Sprites/Card_Back.png', (pos[0] + 200 * self.modifier - 50 * self.modifier, pos[1])),
#             Card(3, 'main/Sprites/Card_Back.png', (pos[0] + 200 * self.modifier - 50 * self.modifier, pos[1])),
#             Card(4, 'main/Sprites/Card_Back.png', (pos[0] + 200 * self.modifier - 50 * self.modifier, pos[1])),
#             Card(5, 'main/Sprites/Card_Back.png', (pos[0] + 200 * self.modifier - 50 * self.modifier, pos[1])),
#             Card(6, 'main/Sprites/Card_Back.png', (pos[0] + 200 * self.modifier - 50 * self.modifier, pos[1])),
#             Card(7, 'main/Sprites/Card_Back.png', (pos[0] + 200 * self.modifier - 50 * self.modifier, pos[1])),
#             Card(8, 'main/Sprites/Card_Back.png', (pos[0] + 200 * self.modifier - 50 * self.modifier, pos[1])),
#             Card(9, 'main/Sprites/Card_Back.png', (pos[0] + 200 * self.modifier - 50 * self.modifier, pos[1])),
#             Card(10, 'main/Sprites/Card_Back.png', (pos[0] + 200 * self.modifier - 50 * self.modifier, pos[1])),
#             Card(10, 'main/Sprites/Card_Back.png', (pos[0] + 200 * self.modifier - 50 * self.modifier, pos[1])),
#             Card(10, 'main/Sprites/Card_Back.png', (pos[0] + 200 * self.modifier - 50 * self.modifier, pos[1])),
#             Card(10, 'main/Sprites/Card_Back.png', (pos[0] + 200 * self.modifier - 50 * self.modifier, pos[1])),
