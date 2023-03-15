import pygame

from game.settings import BUTTON_COLOR


class Button:
    pos: (int, int)
    size: (int, int)

    def __init__(self, text: str, pos: (int, int), size: (int, int)):
        font = pygame.font.SysFont('Corbel', 28)
        self.pos = pos
        self.size = size
        self.text = font.render(text, True, (255, 255, 255))

    def is_clicked(self, pos: (int, int)):
        x1, y1 = self.pos
        x, y = pos
        x2, y2 = self.size
        x2 += x1
        y2 += y1
        return x1 <= x <= x2 and y1 <= y <= y2

    def draw(self, screen):
        pygame.draw.rect(screen, BUTTON_COLOR, pygame.Rect(self.pos, self.size), 3, 4)
        rect = self.text.get_rect()
        x, y = self.pos
        w, h = self.size
        rect.center = (x + w / 2, y + h / 2)
        screen.blit(self.text, rect)
