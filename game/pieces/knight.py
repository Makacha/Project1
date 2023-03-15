import copy

import pygame

from game import settings
from game.pieces import Piece
from game.pieces.piece import CanPin


class Knight(Piece):

    row = [-2, -2, -1, 1, 2, 2, 1, -1]
    col = [-1, 1, 2, 2, 1, -1, -2, -2]

    def __init__(self, pos, color):
        self.color = color
        img_path = settings.PIECES_IMAGE_PATH + color + "-knight.png"
        self.image = pygame.image.load(img_path)
        super().__init__(pos)

    def able_capture(self, x: int, y: int, board):
        u, v = self.pos
        for i in range(0, 8):
            if x - u == self.row[i] and y - v == self.col[i]:
                return True
        return False

    def gen_valid_des(self, board):
        self.valid_des = []
        if self.is_pinned:
            return
        x, y = self.pos
        for i in range(8):
            u = self.row[i] + x
            v = self.col[i] + y
            if not board.out_of_board((u, v)):
                other = board.at((u, v))
                if other is None or other.color != self.color:
                    self.valid_des.append((u, v))

        temp = copy.deepcopy(self.valid_des)
        for u, v in self.valid_des:
            kx, ky = board.get_king(self.color)
            flag = False
            for i in range(0, 8):
                if flag:
                    break
                for j in range(0, 8):
                    if flag:
                        break
                    other = board.at((i, j))
                    if other and other.color != self.color and isinstance(other, CanPin):
                        if other.able_capture(kx, ky, board, (x, y), (u, v)):
                            flag = True
                            temp.remove((u, v))
        self.valid_des = temp
