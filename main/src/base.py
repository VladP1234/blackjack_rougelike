import pygame
import pygame_gui

class Arrow:
    def __init__(self) -> None:
        self.arrow1 = pygame.transform.scale(pygame.image.load('main/Sprites/Base/casino_arrow_1.png'), (200, 200))
        self.arrow2 = pygame.transform.scale(pygame.image.load('main/Sprites/Base/casino_arrow_2.png'), (200, 200))
        self.active_arrow = 1
        self.arrow_delay = 0

    def draw(self, screen: pygame.Surface):
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


class Base:
    def __init__(self, UIManager) -> None:
        self.arrow = Arrow()
        self.ui = []
        self.start_run_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((575, 200), (190, 190)), text="", manager=UIManager)
        self.ui.append(self.start_run_button)
        self.start_run = False

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.start_run_button:
                    self.start_run = True
    def update(self):
        pass
    def hide_ui(self):
        self.start_run = False
        for ui in self.ui:
            ui.visible = False
    def show_ui(self):
        for ui in self.ui:
            ui.visible = True

    def draw(self, screen: pygame.Surface):
        self.arrow.draw(screen)
