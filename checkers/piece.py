import pygame

from .constants import SQUARE_SIZE, CROWN, GREY


class Piece:
    PADDING = 15
    OUTLINE = 2

    def __init__(self, row, column, color):
        self.row = row
        self.column = column
        self.color = color
        self.queen = False
        self.x = 0
        self.y = 0
        self.claculate_position()

    def claculate_position(self):
        self.x = SQUARE_SIZE * self.column + SQUARE_SIZE // 2
        self.y = SQUARE_SIZE * self.row + SQUARE_SIZE // 2

    def make_queen(self):
        self.queen = True

    def draw(self, win):
        radius = SQUARE_SIZE // 2 - self.PADDING
        pygame.draw.circle(win, GREY, (self.x, self.y), radius + self.OUTLINE)
        pygame.draw.circle(win, self.color, (self.x, self.y), radius)
        if self.queen:
            win.blit(CROWN, (self.x - CROWN.get_width() // 2, self.y - CROWN.get_height() // 2))

    def move(self, row, column):
        self.row = row
        self.column = column
        self.claculate_position()

    def getColor(self):
        return self.color

    def __repr__(self):
        return str(self.color)
