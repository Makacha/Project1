import pygame

from game import settings
from game.pieces import Piece, Rook


class King(Piece):
    status: int = 0
    real_des: dict = {}

    row = [-1, 0, 1, 1, 1, 0, -1, -1]
    col = [-1, -1, -1, 0, 1, 1, 1, 0]

    def __init__(self, pos: (int, int), color):
        self.color = color
        img_path = settings.PIECES_IMAGE_PATH + color + "-king.png"
        self.image = pygame.image.load(img_path)
        super().__init__(pos)

    def check_move(self, des: (int, int)):
        if des in self.valid_des:
            if self.real_des.get(str(des)):
                x, y, v = self.real_des[str(des)]
                return 2, ((x, y), (x, v))
            return 1, des
        else:
            return 0, des

    def able_capture(self, x: int, y: int, board):
        u, v = self.pos
        for i in range(0, 8):
            if x - u == self.row[i] and y - v == self.col[i]:
                return True
        return False
    
    def check(self, x: int, y: int, board):
        for i in range(0, 8):
            for j in range(0, 8):
                if (i, j) == (x, y):
                    continue
                other = board.at((i, j))
                if other and other.color != self.color and other.able_capture(x, y, board):
                    return False
        return True
                
    def gen_valid_des(self, board):
        self.valid_des = []
        self.real_des.clear()
        x, y = self.pos
        if self.status == 0:
            left_rook = board.at((x, 0))
            for i in range(1, y):
                if board.at((x, i)):
                    left_rook = None
            if isinstance(left_rook, Rook) and left_rook.status == 0:
                self.valid_des.append((x, 2))
                self.real_des[str((x, 2))] = (x, 0, 3)
            right_rook = board.at((x, 7))
            for i in range(y + 1, 7):
                if board.at((x, i)):
                    right_rook = None
            if isinstance(right_rook, Rook) and right_rook.status == 0:
                self.valid_des.append((x, 6))
                self.real_des[str((x, 6))] = (x, 7, 5)

        for i in range(8):
            u = self.row[i] + x
            v = self.col[i] + y
            if not board.out_of_board((u, v)):
                other = board.at((u, v))
                if self.check(u, v, board) and (other is None or other.color != self.color):
                    self.valid_des.append((u, v))
