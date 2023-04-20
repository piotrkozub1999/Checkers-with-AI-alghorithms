import pygame

from checkers.constants import GUI_WIDTH, GUI_HEIGHT, SQUARE_SIZE, BLACK, WHITE
from checkers.game import Game
from minimax.algorithm import minimax
pygame.init()
FPS = 60
font = pygame.font.SysFont('Arial', 40, bold=True)

WIN = pygame.display.set_mode((GUI_WIDTH, GUI_HEIGHT))
pygame.display.set_caption('Warcaby')

class Button():

    def __init__(self, x, y, width, height, buttonText='Button', onclickFunction=None, onePress=False):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.onclickFunction = onclickFunction
        self.onePress = onePress

        self.fillColors = {
            'normal': '#ffffff',
            'hover': '#666666',
            'pressed': '#333333',
        }

        self.buttonSurface = pygame.Surface((self.width, self.height))
        self.buttonRect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.buttonSurf = font.render(buttonText, True, (20, 20, 20))

        self.alreadyPressed = False


    def process(self):
        mousePos = pygame.mouse.get_pos()

        self.buttonSurface.fill(self.fillColors['normal'])
        if self.buttonRect.collidepoint(mousePos):
            self.buttonSurface.fill(self.fillColors['hover'])

            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                self.buttonSurface.fill(self.fillColors['pressed'])

                if self.onePress:
                    self.onclickFunction()

                elif not self.alreadyPressed:
                    self.onclickFunction()
                    self.alreadyPressed = True

            else:
                self.alreadyPressed = False

        self.buttonSurface.blit(self.buttonSurf, [
            self.buttonRect.width / 2 - self.buttonSurf.get_rect().width / 2,
            self.buttonRect.height / 2 - self.buttonSurf.get_rect().height / 2
        ])
        WIN.blit(self.buttonSurface, self.buttonRect)


def myFunction(value):
    print('MinMax depth = ' + str(value))


def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col


def main():
    run = True
    clock = pygame.time.Clock()
    WIN.fill(WHITE)
    game = Game(WIN)
    objects = []
    DEPTH = 2
    Button1 = Button(1080, 70, 100, 50, '1', myFunction(1))
    Button2 = Button(1080, 140, 100, 50, '2', myFunction(2), True)
    objects.append(Button1)
    objects.append(Button2)
    while run:
        clock.tick(FPS)

        if game.turn == BLACK:
            value, new_board = minimax(game.get_board(), DEPTH, BLACK, game)
            game.ai_move(new_board)
        for object in objects:
            object.process()
        pygame.display.flip()
        if game.winner() != None:
            print(game.winner())
            run = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if pos[0] < 800:
                    row, col = get_row_col_from_mouse(pos)
                    game.select(row, col)

        game.update()

    pygame.quit()


main()
