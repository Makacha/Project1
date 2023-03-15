import pygame

from game import settings
from game.pieces.line import Line
from game.pieces.piece import CanPin


class Rook(Line, CanPin):
    status: int = 0

    def __init__(self, pos: (int, int), color):
        self.color = color
        img_path = settings.PIECES_IMAGE_PATH + color + "-rook.png"
        self.image = pygame.image.load(img_path)
        super().__init__(pos)

    def able_capture(self, x: int, y: int, board, old=None, new=None):
        return self.able_capture_line(x, y, board, old, new)

    def gen_valid_des(self, board):
        self.valid_des = []
        if self.is_pinned:
            return
        self.get_valid_des_in_line(board)
