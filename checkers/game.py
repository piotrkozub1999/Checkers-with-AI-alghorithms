import pygame

from checkers.board import Board
from .constants import RED, WHITE, SQUARE_SIZE, BLACK


class Game:
    def __init__(self, win):
        self.win = win
        self.selected = None
        self.board = Board()
        self.turn = WHITE
        self.valid_moves = {}
        self.hint = None

    def update(self):
        self.board.draw(self.win)
        self.draw_valid_moves(self.valid_moves)
        if self.hint is not None:
            pygame.draw.circle(self.win, (0, 255, 0), (self.hint[0].x, self.hint[0].y), 50, 5)
            pygame.draw.circle(self.win, (0, 255, 0),
                               (self.hint[1][1] * SQUARE_SIZE + SQUARE_SIZE // 2,
                                self.hint[1][0] * SQUARE_SIZE + SQUARE_SIZE // 2), 15)

        pygame.display.update()

    def winner(self):
        blocked = True

        for p in self.board.get_all_pieces(self.turn):
            if self.board.get_valid_moves(p):
                blocked = False

        if blocked:
            return WHITE if self.turn == BLACK else WHITE

        return self.board.winner()

    def reset(self):
        self._init()

    def select(self, row, column):
        if self.selected:
            result = self._move(row, column)
            if not result:
                self.selected = None
                self.select(row, column)
        piece = self.board.get_piece(row, column)

        if piece != 0 and piece.color == self.turn:
            self.selected = piece
            self.valid_moves = self.board.get_valid_moves(piece)
            return True

        elif piece == 0:
            self.selected = None
            self.valid_moves = {}

        return False

    def _move(self, row, column):
        piece = self.board.get_piece(row, column)
        if self.selected and piece == 0 and (row, column) in self.valid_moves:
            self.board.move(self.selected, row, column)
            skipped = self.valid_moves[(row, column)]
            if skipped:
                self.board.remove(skipped)
            self.change_turn()
        else:
            return False

        return True

    def draw_valid_moves(self, moves):
        for move in moves:
            row, column = move
            pygame.draw.circle(self.win, RED,
                               (column * SQUARE_SIZE + SQUARE_SIZE // 2,
                                row * SQUARE_SIZE + SQUARE_SIZE // 2), 15)

    def change_turn(self):
        self.valid_moves = {}
        if self.turn == WHITE:
            self.turn = BLACK
        else:
            self.turn = WHITE

    def get_board(self):
        return self.board

    def ai_move(self, board):
        self.board = board
        self.change_turn()

    def get_hint(self, board):
        state = self.board
        move = board

        for i, row in enumerate(state.board):
            for j, sq in enumerate(row):
                if state.board[i][j] != 0 and move.board[i][j] == 0 and state.board[i][j].color == WHITE:
                    chosen_piece = sq

                elif state.board[i][j] == 0 and move.board[i][j] != 0 and move.board[i][j].color == WHITE:
                    target = (i, j)

        self.hint = (chosen_piece, target)
