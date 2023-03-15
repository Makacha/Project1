import copy

import pygame

from game import settings
from game.pieces import Piece
from game.pieces.piece import CanPin


class Pawn(Piece):
    status: int = 0
    real_des: dict = {}

    def __init__(self, pos, color):
        self.color = color
        img_path = settings.PIECES_IMAGE_PATH + color + "-pawn.png"
        self.image = pygame.image.load(img_path)
        super().__init__(pos)

    def move(self, des: (int, int)):
        self.status += 1
        super().move(des)

    def check_move(self, des: (int, int)):
        if des in self.valid_des:
            return 1, self.real_des[str(des)]
        else:
            return 0, des

    def able_capture(self, x: int, y: int, board):
        u, v = self.pos
        if self.color == "white":
            if x == u + 1 and abs(v - y) == 1:
                return True
        else:
            if x == u - 1 and abs(v - y) == 1:
                return True
        return False

    def gen_valid_des(self, board):
        self.valid_des = []
        self.real_des.clear()
        if self.is_pinned:
            return
        x, y = self.pos
        if self.color == "white":
            if self.status == 0:
                for i in range(x + 1, x + 3):
                    if board.at((i, y)) is not None:
                        break
                    self.valid_des.append((i, y))
                    self.real_des[str((i, y))] = (i, y)
            else:
                if board.at((x + 1, y)) is None:
                    self.valid_des.append((x + 1, y))
                    self.real_des[str((x + 1, y))] = (x + 1, y)
            left = board.at((x + 1, y - 1)) if y > 0 else None
            right = board.at((x + 1, y + 1)) if y < 7 else None
            if left and left.color != self.color:
                self.valid_des.append((x + 1, y - 1))
                self.real_des[str((x + 1, y - 1))] = (x + 1, y - 1)
            if right and right.color != self.color:
                self.valid_des.append((x + 1, y + 1))
                self.real_des[str((x + 1, y + 1))] = (x + 1, y + 1)

            left = board.at((x, y - 1)) if y > 0 else None
            right = board.at((x, y + 1)) if y < 7 else None
            if left and isinstance(left, Pawn) and left.color != self.color \
                    and board.last_active == left and left.status == 1:
                self.valid_des.append((x + 1, y - 1))
                self.real_des[str((x + 1, y - 1))] = (x, y - 1)
            if right and isinstance(right, Pawn) and right.color != self.color \
                    and board.last_active == right and right.status == 1:
                self.valid_des.append((x + 1, y + 1))
                self.real_des[str((x + 1, y + 1))] = (x, y + 1)

        else:
            if self.status == 0:
                for i in range(x - 1, x - 3, - 1):
                    if board.at((i, y)) is not None:
                        break
                    self.valid_des.append((i, y))
                    self.real_des[str((i, y))] = (i, y)
            else:
                if board.at((x - 1, y)) is None:
                    self.valid_des.append((x - 1, y))
                    self.real_des[str((x - 1, y))] = (x - 1, y)
            left = board.at((x - 1, y - 1)) if y > 0 else None
            right = board.at((x - 1, y + 1)) if y < 7 else None
            if left and left.color != self.color:
                self.valid_des.append((x - 1, y - 1))
                self.real_des[str((x - 1, y - 1))] = (x - 1, y - 1)
            if right and right.color != self.color:
                self.valid_des.append((x - 1, y + 1))
                self.real_des[str((x - 1, y + 1))] = (x - 1, y + 1)
            left = board.at((x, y - 1)) if y > 0 else None
            right = board.at((x, y + 1)) if y < 7 else None
            if left and isinstance(left, Pawn) and left.color != self.color \
                    and board.last_active == left and left.status == 1:
                self.valid_des.append((x - 1, y - 1))
                self.real_des[str((x - 1, y - 1))] = (x, y - 1)
            if right and isinstance(right, Pawn) and right.color != self.color \
                    and board.last_active == right and right.status == 1:
                self.valid_des.append((x - 1, y + 1))
                self.real_des[str((x - 1, y + 1))] = (x, y + 1)

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
                            self.real_des.pop(str((u, v)))
        self.valid_des = temp
