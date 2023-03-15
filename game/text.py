import pygame


class Text:

    def __init__(self, text: str, center: (int, int), size=28, color=None, bg=None):
        font = pygame.font.SysFont('Corbel', size)
        self.center = center
        if color:
            self.text = font.render(text, True, color, bg)
        else:
            self.text = font.render(text, True, (255, 255, 255))

    def draw(self, screen):
        rect = self.text.get_rect()
        rect.center = self.center
        screen.blit(self.text, rect)
