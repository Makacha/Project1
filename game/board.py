from typing import Optional, Type

from game.settings import BACKGROUND_PATH, PIECES_KEY, COLOR
from game.move import Move
from game.pieces import Piece, King, Pawn, Queen


class Board:
    pieces = []
    target: (int, int) = (-1, -1)
    last_active: Piece = None
    winner: str = None

    def __init__(self):
        f = open(BACKGROUND_PATH + "board.data", "r")
        self.pieces = []
        for i in range(8):
            r = f.readline()
            self.pieces.append([])
            for j in range(8):
                c = r[j]
                if PIECES_KEY.get(c):
                    self.pieces[i].append(PIECES_KEY[c]((i, j), "white" if i <= 2 else "black"))
                else:
                    self.pieces[i].append(None)

    def at(self, pos: (int, int)) -> Optional[Piece]:
        x, y = pos
        return self.pieces[x][y]

    def assign(self, pos: (int, int), piece: Piece):
        x, y = pos
        if isinstance(piece, Pawn):
            if (piece.color == COLOR[0] and x == 7) or (piece.color == COLOR[0] and x == 7):
                piece = Queen(piece.pos, piece.color)
        self.pieces[x][y] = piece
        piece.move(pos)

    def remove(self, pos: (int, int), captured=False):
        x, y = pos
        if captured and isinstance(self.pieces[x][y], King):
            if self.pieces[x][y].color == COLOR[0]:
                self.winner = COLOR[1]
            else:
                self.winner = COLOR[0]
        self.pieces[x][y] = None

    def out_of_board(self, pos: (int, int)):
        x, y = pos
        return not (0 <= x < 8 and 0 <= y < 8)

    def is_over(self):
        if self.winner:
            return self.winner
        return False

    def get_king(self, color):
        for i in range(0, 8):
            for j in range(0, 8):
                if self.pieces[i][j] and isinstance(self.pieces[i][j], King) and self.pieces[i][j].color == color:
                    return i, j

    def move(self, move: Move):
        current_piece = self.at(move.cur)
        if current_piece is None:
            return

        if self.out_of_board(move.des):
            return
        current_piece.gen_valid_des(self)
        check_move, arg = current_piece.check_move(move.des)
        if check_move == 0:
            return
        self.last_active = current_piece
        if check_move == 1:
            self.remove(move.cur)
            self.remove(arg, True)
            self.assign(move.des, current_piece)
        else:
            r_pos, r_des = arg
            r_piece = self.at(r_pos)
            self.remove(r_pos)
            self.remove(move.cur)
            self.assign(r_des, r_piece)
            self.assign(move.des, current_piece)

    def draw(self, screen):
        for i in range(8):
            for j in range(8):
                if self.pieces[i][j]:
                    self.pieces[i][j].draw(screen)
        x, y = self.target
        if not self.out_of_board((x, y)) and self.at((x, y)):
            self.pieces[x][y].show_target(self, screen)
