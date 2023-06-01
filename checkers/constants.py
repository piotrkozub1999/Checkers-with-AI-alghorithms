import pygame

GUI_WIDTH, GUI_HEIGHT = 1200, 800
WIDTH, HEIGHT = 800, 800
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH // COLS

RED = (200, 20, 20)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREY = (128, 128, 128)
LIGHT_BROWN = (233, 228, 212)
BROWN = (101, 67, 33)
LIGHT_BLUE = (230, 247, 255)
CROWN = pygame.transform.scale(pygame.image.load('assets/crown.png'), (44, 25))
MAX_MOVES = 5
