import os

import pygame

from game.pieces import Queen, Rook, Bishop, Pawn, Knight, King

BACKGROUND_PATH = os.path.dirname(os.path.abspath(__file__)) + "\\..\\res\\background\\"

PIECES_IMAGE_PATH = os.path.dirname(os.path.abspath(__file__)) + "\\..\\res\\pieces\\"

CANDIDATE_MOVE_IMAGE_PATH = os.path.dirname(os.path.abspath(__file__)) + "\\..\\res\\other\\"

CANDIDATE_MOVE_IMAGE = pygame.image.load(CANDIDATE_MOVE_IMAGE_PATH + "candidate.png")
CANDIDATE_MOVE_CAPTURE_IMAGE = pygame.image.load(CANDIDATE_MOVE_IMAGE_PATH + "candidate-capture.png")

PIECE_SIZE = 64

COLOR = ["white", "black"]

BUTTON_COLOR = (100, 100, 100)

PIECES_KEY = {
    "P": Pawn,
    "N": Knight,
    "R": Rook,
    "B": Bishop,
    "Q": Queen,
    "K": King
}


