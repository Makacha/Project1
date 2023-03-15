import sys
from typing import List

import pygame
from game.board import Board
from game.button import Button
from game.move import Move
from game.settings import BACKGROUND_PATH, PIECE_SIZE, COLOR
from game.text import Text


class Chess:
    width = 712
    height = 512
    board: Board
    move: Move = Move()
    history_move: List[Move] = []
    index_move: int = 0

    def __init__(self):
        self.pygame = pygame
        self.pygame.init()
        self.size = (self.width, self.height)
        self.window = pygame.display
        self.screen = self.window.set_mode(self.size)
        self.window.set_caption("Chess")
        self.clock = self.pygame.time.Clock()
        self.time_step = 0
        self.board = Board()
        self.turn = COLOR[0]
        bg_path = BACKGROUND_PATH + "board.png"
        self.background = pygame.image.load(bg_path)
        self.menu = Text("Menu", (612, 80), 56)
        self.menu.draw(self.screen)
        self.new_game_button = Button("New game", (537, 210), (150, 50))
        self.new_game_button.draw(self.screen)
        self.quit_button = Button("Quit", (537, 270), (150, 50))
        self.quit_button.draw(self.screen)
        self.black_win = Text("Black win", (258, 258), 72, (0, 0, 0), (181, 181, 181))
        self.white_win = Text("White win", (258, 258), 72, (255, 255, 255), (54, 54, 54))
        self.is_quit = False

    def run(self):
        # main game loop
        while not self.is_quit:
            # hold frame rate at 60 fps
            dt = self.clock.tick(60)
            self.time_step += 1
            # enumerate event
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)
                # sprite handle event
                self.handle(event)

            self.update(dt / 1000.)
            # re-draw screen
            self.draw(self.screen)

    def draw(self, screen):
        if not self.board.is_over():
            screen.blit(self.background, (0, 0))
            self.board.draw(screen)
        else:
            color = self.board.is_over()
            if color == COLOR[0]:
                self.white_win.draw(screen)
            else:
                self.black_win.draw(screen)
        self.window.flip()

    def update(self, dt):
        if self.index_move < len(self.history_move):
            self.board.move(self.history_move[self.index_move])
            self.index_move += 1
            self.turn = COLOR[self.index_move % 2]

    def handle(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            u, v = pygame.mouse.get_pos()
            y, x = (int(u / PIECE_SIZE), 7 - int(v / PIECE_SIZE))
            if self.board.out_of_board((x, y)):
                if self.new_game_button.is_clicked((u, v)):
                    self.board = Board()
                    self.turn = COLOR[0]
                    self.history_move = []
                    self.index_move = 0
                if self.quit_button.is_clicked((u, v)):
                    self.is_quit = True
            else:
                if (x, y) == self.board.target:
                    self.board.target = (-1, -1)
                elif self.board.at((x, y)) is not None and self.board.at((x, y)).color == self.turn:
                    self.board.target = (x, y)
                    self.move.cur = (x, y)
                else:
                    self.board.target = (-1, -1)
                    if self.move.cur and ((x, y) in self.board.at(self.move.cur).valid_des):
                        self.move.des = (x, y)
                        self.history_move.append(self.move)
                        self.move = Move()
