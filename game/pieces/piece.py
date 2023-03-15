from abc import ABC, abstractmethod

import pygame
from game import settings


class Piece(ABC, pygame.sprite.Sprite):
    pos: (int, int)
    image = None
    valid_des: [(int, int)] = []
    color: str
    is_pinned: bool = False

    def __init__(self, pos: (int, int)):
        super(Piece, self).__init__()
        self.pos = pos
        pass

    def move(self, des: (int, int)):
        self.pos = des

    def check_move(self, des: (int, int)):
        return 1 if des in self.valid_des else 0, des

    @abstractmethod
    def gen_valid_des(self, board):
        pass

    @abstractmethod
    def able_capture(self, x: int, y: int, board):
        pass

    def draw(self, screen):
        x, y = self.pos
        x = (7 - x) * 64
        y = y * 64
        screen.blit(self.image, (y, x))

    def show_target(self, board, screen):
        self.gen_valid_des(board)
        for u, v in self.valid_des:
            x = (7 - u) * 64
            y = v * 64
            if board.at((u, v)) is None:
                screen.blit(settings.CANDIDATE_MOVE_IMAGE, (y, x))
            else:
                screen.blit(settings.CANDIDATE_MOVE_CAPTURE_IMAGE, (y, x))


class CanPin(Piece):

    @abstractmethod
    def able_capture(self, x: int, y: int, board, old=None, new=None):
        pass
