import pygame
import pyautogui

from RadioButton import RadioButton
from checkers.constants import GUI_WIDTH, GUI_HEIGHT, SQUARE_SIZE, BLACK, LIGHT_BLUE, WHITE
from checkers.game import Game
from minimax.algorithm import minimax


pygame.init()
FPS = 60
WIN = pygame.display.set_mode((GUI_WIDTH, GUI_HEIGHT))
pygame.display.set_caption('Checkers')


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
    bot_text = font_text.render("Choose the level of black", True, BLACK)
    bot_textrect = bot_text.get_rect()
    bot_textrect.center = (1000, 50)

    ##### BOT BUTTONS #####
    font_button = pygame.font.SysFont(None, 38)
    bot_buttons = [
        RadioButton(850, 90, 125, 40, font_button, "AI 1"),
        RadioButton(1025, 90, 125, 40, font_button, "AI 2"),
        RadioButton(850, 155, 125, 40, font_button, "AI 3"),
        RadioButton(1025, 155, 125, 40, font_button, "AI 4"),
        RadioButton(937, 220, 125, 40, font_button, "AI 5")
    ]

    ##### HINT TEXT #####
    hint_text = font_text.render("Choose the level of white (hint)", True, BLACK)
    hint_textrect = hint_text.get_rect()
    hint_textrect.center = (1000, 320)

    ##### HINT BUTTONS #####
    hint_buttons = [
        RadioButton(850, 360, 125, 40, font_button, "NO AI"),
        RadioButton(1025, 360, 125, 40, font_button, "AI 1"),
        RadioButton(850, 425, 125, 40, font_button, "AI 2"),
        RadioButton(1025, 425, 125, 40, font_button, "AI 3"),
        RadioButton(850, 490, 125, 40, font_button, "AI 4"),
        RadioButton(1025, 490, 125, 40, font_button, "AI 5")
    ]

    ##### AI TEXT #####
    ai_text = font_text.render("Select a game mode", True, BLACK)
    ai_textrect = ai_text.get_rect()
    ai_textrect.center = (1000, 600)

    ##### AI Game Box #####
    ai_buttons = [RadioButton(885, 640, 230, 40, font_button, "Game against AI"),
                  RadioButton(885, 705, 230, 40, font_button, "AI Simulation")]

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
            print("BLACK Bot wykonał ruch z głębią = " + str(bot_depth))
            game.last_move = BLACK

        if game.turn == WHITE:
            if hint_depth != 0:
                if ai_game:
                    value, new_board = minimax(game.get_board(), hint_depth, WHITE, game, True)
                    game.ai_move(new_board)
                    print("WHITE Bot wykonał ruch z głębią = " + str(bot_depth))

                elif not hint_active:
                    hint_active = True
                    if game.winner() is None and not game.hint:
                        value, new_board = minimax(game.get_board(), hint_depth, WHITE, game, True)
                        game.get_hint(new_board)
                    print(f"Wygenerowano podpowiedź z głębią = {hint_depth}")

            game.last_move = WHITE

        if game.winner() is not None:
            winner = "White" if game.winner() == WHITE else "Black"
            # print(f"{winner} has won the game!")
            pyautogui.alert(f"{winner} has won the game!")
            run = False

        event_list = pygame.event.get()
        for event in event_list:
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN and not ai_game:
                pos = pygame.mouse.get_pos()
                if pos[0] < 800:
                    row, col = get_row_col_from_mouse(pos)
                    game.select(row, col)
                    game.last_move = WHITE
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
                pyautogui.alert("Choose the level of WHITE first!")
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
                pyautogui.alert("The game end in a draw!")
                run = False

    pygame.quit()


main()
