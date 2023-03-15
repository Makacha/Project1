import copy
from abc import abstractmethod

from game.pieces.piece import Piece, CanPin


class Diagonal(Piece):

    def able_capture_diagonal(self, x: int, y: int, board, old=None, new=None):
        u, v = self.pos
        if x < u:
            x, u = u, x
            y, v = v, y
        if (u, v) == new:
            return False
        if x + y == u + v:
            for i in range(u + 1, x):
                j = x + y - i
                if (i, j) == old:
                    continue
                if board.at((i, j)) is not None or (i, j) == new:
                    return False
        elif x - y == u - v:
            for i in range(u + 1, x):
                j = i - x + y
                if (i, j) == old:
                    continue
                if board.at((i, j)) is not None or (i, j) == new:
                    return False
        else:
            return False
        return True

    def get_valid_des_in_diagonal(self, board):
        x, y = self.pos
        for i in range(1, 8):
            u = x + i
            v = y + i
            if board.out_of_board((u, v)):
                break
            other = board.at((u, v))
            if other is None:
                self.valid_des.append((u, v))
            elif other.color == self.color:
                break
            else:
                self.valid_des.append((u, v))
                break
        for i in range(-1, -8, -1):
            u = x + i
            v = y + i
            if board.out_of_board((u, v)):
                break
            other = board.at((u, v))
            if other is None:
                self.valid_des.append((u, v))
            elif other.color == self.color:
                break
            else:
                self.valid_des.append((u, v))
                break
        for i in range(1, 8):
            u = x + i
            v = y - i
            if board.out_of_board((u, v)):
                break
            other = board.at((u, v))
            if other is None:
                self.valid_des.append((u, v))
            elif other.color == self.color:
                break
            else:
                self.valid_des.append((u, v))
                break
        for i in range(1, 8):
            u = x - i
            v = y + i
            if board.out_of_board((u, v)):
                break
            other = board.at((u, v))
            if other is None:
                self.valid_des.append((u, v))
            elif other.color == self.color:
                break
            else:
                self.valid_des.append((u, v))
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
