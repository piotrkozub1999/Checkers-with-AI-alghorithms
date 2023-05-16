import pygame

from RadioButton import RadioButton
from checkers.constants import GUI_WIDTH, GUI_HEIGHT, SQUARE_SIZE, BLACK, LIGHT_BLUE, WHITE
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
    hint_depth = 0
    hint_active = False

    ##### BOT TEXT #####
    font_bot = pygame.font.SysFont('Arial', 26, bold=True)
    bot_text = font_bot.render("Wybierz poziom przeciwnika:", True, BLACK)
    bot_textrect = bot_text.get_rect()
    bot_textrect.center = (1000, 50)

    ##### BOT BUTTONS #####
    font_button = pygame.font.SysFont(None, 40)
    bot_buttons = [
        RadioButton(850, 90, 125, 40, font_button, "AI 1"),
        RadioButton(1025, 90, 125, 40, font_button, "AI 2"),
        RadioButton(850, 155, 125, 40, font_button, "AI 3"),
        RadioButton(1025, 155, 125, 40, font_button, "AI 4"),
        RadioButton(937, 220, 125, 40, font_button, "AI 5")
    ]

    ##### HINT TEXT #####
    font_hint = pygame.font.SysFont('Arial', 26, bold=True)
    hint_text = font_hint.render("Wybierz poziom podpowiedzi:", True, BLACK)
    hint_textrect = hint_text.get_rect()
    hint_textrect.center = (1000, 550)

    ##### HINT BUTTONS #####
    hint_buttons = [
        RadioButton(850, 590, 125, 40, font_button, "NO HINT"),
        RadioButton(1025, 590, 125, 40, font_button, "HINT 1"),
        RadioButton(850, 655, 125, 40, font_button, "HINT 2"),
        RadioButton(1025, 655, 125, 40, font_button, "HINT 3"),
        RadioButton(850, 720, 125, 40, font_button, "HINT 4"),
        RadioButton(1025, 720, 125, 40, font_button, "HINT 5")
    ]

    for rb in bot_buttons:
        rb.set_radio_buttons(bot_buttons)

    for hb in hint_buttons:
        hb.set_radio_buttons(hint_buttons)

    bot_buttons[0].clicked = True
    group = pygame.sprite.Group(bot_buttons)

    hint_buttons[0].clicked = True
    group_h = pygame.sprite.Group(hint_buttons)

    ##### GAME LOOP #####
    while run:
        clock.tick(FPS)

        WIN.blit(bot_text, bot_textrect)
        WIN.blit(hint_text, hint_textrect)

        if game.turn == BLACK:
            hint_active = False
            value, new_board = minimax(game.get_board(), bot_depth, BLACK, game)
            game.ai_move(new_board)
            print("Bot wykonał ruch z głębią = " + str(bot_depth))

        if game.turn == WHITE and hint_depth != 0 and not hint_active:
            hint_active = True
            value, new_board = minimax(game.get_board(), hint_depth, WHITE, game)
            print(f"Wygenerowano podpowiedź z głębią = {hint_depth}")

        if game.winner() is not None:
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

        if hint_buttons[0].checkClick():
            hint_depth = 0
        if hint_buttons[1].checkClick():
            hint_depth = 1
        if hint_buttons[2].checkClick():
            hint_depth = 2
        if hint_buttons[3].checkClick():
            hint_depth = 3
        if hint_buttons[4].checkClick():
            hint_depth = 4
        if hint_buttons[5].checkClick():
            hint_depth = 5

        group.update(event_list)
        group.draw(WIN)

        group_h.update(event_list)
        group_h.draw(WIN)

        pygame.display.flip()

        game.update()

    pygame.quit()


main()
