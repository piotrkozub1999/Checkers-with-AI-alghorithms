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
    ai_game = False
    font_text = pygame.font.SysFont('Arial', 30)

    ##### BOT TEXT #####
    bot_text = font_text.render("Wybierz poziom czarnych:", True, BLACK)
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
    hint_text = font_text.render("Wybierz poziom podpowiedzi:", True, BLACK)
    hint_textrect = hint_text.get_rect()
    hint_textrect.center = (1000, 300)

    ##### HINT BUTTONS #####
    hint_buttons = [
        RadioButton(850, 340, 125, 40, font_button, "NO AI"),
        RadioButton(1025, 340, 125, 40, font_button, "AI 1"),
        RadioButton(850, 405, 125, 40, font_button, "AI 2"),
        RadioButton(1025, 405, 125, 40, font_button, "AI 3"),
        RadioButton(850, 470, 125, 40, font_button, "AI 4"),
        RadioButton(1025, 470, 125, 40, font_button, "AI 5")
    ]

    ##### AI TEXT #####
    ai_text = font_text.render("Wybierz tryb:", True, BLACK)
    ai_textrect = ai_text.get_rect()
    ai_textrect.center = (1000, 600)

    ##### AI Game Box #####
    ai_buttons = [RadioButton(900, 640, 200, 40, font_button, "Game with AI"),
                  RadioButton(900, 705, 200, 40, font_button, "Only AI Game")]

    for rb in bot_buttons:
        rb.set_radio_buttons(bot_buttons)

    for hb in hint_buttons:
        hb.set_radio_buttons(hint_buttons)

    for ab in ai_buttons:
        ab.set_radio_buttons(ai_buttons)

    bot_buttons[0].clicked = True
    group = pygame.sprite.Group(bot_buttons)

    hint_buttons[0].clicked = True
    group_h = pygame.sprite.Group(hint_buttons)

    ai_buttons[0].clicked = True
    group_ai = pygame.sprite.Group(ai_buttons)
    i = 0
    ##### GAME LOOP #####
    while run:
        clock.tick(FPS)

        WIN.blit(bot_text, bot_textrect)
        WIN.blit(hint_text, hint_textrect)
        WIN.blit(ai_text, ai_textrect)

        if game.turn == BLACK:
            hint_active = False
            game.hint = None
            value, new_board = minimax(game.get_board(), bot_depth, BLACK, game)
            game.ai_move(new_board)
            print("Bot wykonał ruch z głębią = " + str(bot_depth))

        if game.turn == WHITE and hint_depth != 0 and not hint_active:
            hint_active = True
            value, new_board = minimax(game.get_board(), hint_depth, WHITE, game, True)
            if game.winner() is None:
                game.get_hint(new_board)
            print(f"Wygenerowano podpowiedź z głębią = {hint_depth}")

        if game.winner() is not None:
            winner = "WHITE" if game.winner() == WHITE else "BLACK"
            print(f"{winner} has won the game!")
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
                else:
                    game.selected = None
                    game.valid_moves = {}

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
            game.hint = None
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

        if ai_buttons[0].checkClick():
            ai_game = False

        if ai_buttons[1].checkClick():
            if hint_buttons[0].clicked:
                print("Wybierz poziom białych")
                ai_buttons[1].clicked = False
                ai_buttons[0].clicked = True
            else:
                ai_game = True

        group.update(event_list)
        group.draw(WIN)

        group_h.update(event_list)
        group_h.draw(WIN)

        group_ai.update(event_list)
        group_ai.draw(WIN)

        pygame.display.flip()

        if run:
            # game.draw_check()
            draw = game.update()
            if draw:
                print("REMIS")
                run = False

    pygame.quit()


main()
