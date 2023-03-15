import copy
from abc import abstractmethod

from game.pieces.piece import Piece, CanPin


class Line(Piece):

    def able_capture_line(self, x: int, y: int, board, old=None, new=None):
        u, v = self.pos
        if (u, v) == new:
            return False
        if x == u:
            if y < v:
                v, y = y, v
            for j in range(v + 1, y):
                i = x
                if (i, j) == old:
                    continue
                if board.at((i, j)) is not None or (i, j) == new:
                    return False
        elif y == v:
            if x < u:
                u, x = x, u
            for i in range(u + 1, x):
                j = y
                if (i, j) == old:
                    continue
                if board.at((i, j)) is not None or (i, j) == new:
                    return False
        else:
            return False
        return True

    def get_valid_des_in_line(self, board):
        x, y = self.pos
        for i in range(x + 1, 8):
            other = board.at((i, y))
            if other is None:
                self.valid_des.append((i, y))
            elif other.color == self.color:
                break
            else:
                self.valid_des.append((i, y))
                break
        for i in range(x - 1, -1, -1):
            other = board.at((i, y))
            if other is None:
                self.valid_des.append((i, y))
            elif other.color == self.color:
                break
            else:
                self.valid_des.append((i, y))
                break
        for i in range(y + 1, 8):
            other = board.at((x, i))
            if other is None:
                self.valid_des.append((x, i))
            elif other.color == self.color:
                break
            else:
                self.valid_des.append((x, i))
                break
        for i in range(y - 1, -1, -1):
            other = board.at((x, i))
            if other is None:
                self.valid_des.append((x, i))
            elif other.color == self.color:
                break
            else:
                self.valid_des.append((x, i))
                break
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

    @abstractmethod
    def gen_valid_des(self, board):
        pass
