import pygame
import pygame_gui
from pygame_gui.elements import UIButton

# Custom Button Class
class CustomButton(UIButton):
    def __init__(self, relative_rect, text, manager):
        super().__init__(relative_rect, text, manager)
        
    def update(self, time_delta):
        super().update(time_delta)
        # Custom update code here

    def process_event(self, event):
        super().process_event(event)
        # Custom event handling code here
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self:
                    print("Custom button clicked!")

# Initialize Pygame
pygame.init()

# Window setup
pygame.display.set_caption('Custom Element Example')
window_surface = pygame.display.set_mode((800, 600))

# GUI Manager
manager = pygame_gui.UIManager((800, 600))

# Create Custom Button
custom_button = CustomButton(pygame.Rect((350, 275), (100, 50)), 'Click Me', manager)

# Main Loop
clock = pygame.time.Clock()
is_running = True

while is_running:
    time_delta = clock.tick(60) / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

        manager.process_events(event)

    manager.update(time_delta)

    window_surface.fill((0, 0, 0))
    manager.draw_ui(window_surface)

    pygame.display.update()
