import pygame
from RadioButton import RadioButton
from checkers.constants import GUI_WIDTH, GUI_HEIGHT, SQUARE_SIZE, BLACK, WHITE, LIGHT_BLUE
from checkers.game import Game
from minimax.algorithm import minimax

pygame.init()
FPS = 60
WIN = pygame.display.set_mode((GUI_WIDTH, GUI_HEIGHT))
pygame.display.set_caption('Warcaby')


def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col


def main():
    run = True
    clock = pygame.time.Clock()
    WIN.fill(LIGHT_BLUE)
    game = Game(WIN)
    bot_depth = 1

    ##### BOT TEXT #####
    font_bot = pygame.font.SysFont('Arial', 32, bold=True)
    bot_text = font_bot.render("Wybierz poziom przeciwnika:", True, BLACK)
    bot_textrect = bot_text.get_rect()
    bot_textrect.center = ((1000, 50))

    ##### BOT BUTTONS #####
    font_button = pygame.font.SysFont(None, 40)
    bot_buttons = [
        RadioButton(850, 90, 125, 40, font_button, "AI 1"),
        RadioButton(1025, 90, 125, 40, font_button, "AI 2"),
        RadioButton(850, 155, 125, 40, font_button, "AI 3"),
        RadioButton(1025, 155, 125, 40, font_button, "AI 4"),
        RadioButton(937, 220, 125, 40, font_button, "AI 5")
    ]
    for rb in bot_buttons:
        rb.set_radio_buttons(bot_buttons)
    bot_buttons[0].clicked = True
    group = pygame.sprite.Group(bot_buttons)

    ##### GAME LOOP #####
    while run:
        clock.tick(FPS)
        WIN.blit(bot_text, bot_textrect)

        if game.turn == BLACK:
            value, new_board = minimax(game.get_board(), bot_depth, BLACK, game)
            game.ai_move(new_board)
            print("Bot wykonał ruch z głębią = " + str(bot_depth))

        if game.winner() != None:
            print(game.winner())
            run = False

        event_list = pygame.event.get()
        for event in event_list:
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if pos[0] < 800:
                    row, col = get_row_col_from_mouse(pos)
                    game.select(row, col)

        if bot_buttons[0].checkClick():
            bot_depth = 1
        if bot_buttons[1].checkClick():
            bot_depth = 2
        if bot_buttons[2].checkClick():
            bot_depth = 3
        if bot_buttons[3].checkClick():
            bot_depth = 4
        if bot_buttons[4].checkClick():
            bot_depth = 5

        group.update(event_list)
        group.draw(WIN)
        pygame.display.flip()

        game.update()

    pygame.quit()


main()
