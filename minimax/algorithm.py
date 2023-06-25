import random
from copy import deepcopy

import pygame

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


def minimax(position, depth, max_player, for_player, game, alpha, beta):
    if depth == 0 or position.winner() is not None:
        return position.new_eval(), position

    moves = []
    best_eval = None
    lim_eval = float("-inf") if max_player == BLACK else float("inf")
    opponent = WHITE if max_player == BLACK else BLACK

    for move in get_all_moves(position, max_player, game):
        evaluation = minimax(move, depth - 1, opponent, for_player, game, alpha, beta)[0]
        lim_eval = max(lim_eval, evaluation) if max_player == BLACK else min(lim_eval, evaluation)

        if lim_eval == evaluation:
            if for_player == BLACK:
                if max_player == BLACK:
                    alpha = max(alpha, lim_eval)
                else:
                    beta = min(beta, lim_eval)
            else:
                if max_player == WHITE:
                    alpha = min(alpha, lim_eval)
                else:
                    beta = max(beta, lim_eval)

            if for_player == BLACK and beta <= alpha:
                break
            elif for_player == WHITE and beta >= alpha:
                break

            moves.append((move, lim_eval))
            best_eval = lim_eval

    best_moves = [m for m in moves if m[1] == best_eval]
    best_move = random.choice(best_moves)[0] if len(best_moves) > 0 else None

    return lim_eval, best_move


def simulate_move(piece, move, board, game, skip):
    board.move(piece, move[0], move[1])
    if skip:
        board.remove(skip)

    return board


def get_all_moves(board, color, game):
    moves = []
    for piece in board.get_all_pieces(color):
        valid_moves = board.get_valid_moves(piece)
        for move, skip in valid_moves.items():
            # draw_moves(game, board, piece)  # TODO: remove?
            temp_board = deepcopy(board)
            temp_piece = temp_board.get_piece(piece.row, piece.column)
            new_board = simulate_move(temp_piece, move, temp_board, game, skip)
            moves.append(new_board)

    return moves


def draw_moves(game, board, piece):
    valid_moves = board.get_valid_moves(piece)
    board.draw(game.win)
    pygame.draw.circle(game.win, (0, 255, 0), (piece.x, piece.y), 50, 5)
    game.draw_valid_moves(valid_moves.keys())
    pygame.display.update()
    # pygame.time.delay(100)
