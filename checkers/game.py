import pygame

from checkers.board import Board
from .constants import RED, WHITE, SQUARE_SIZE, BLACK, MAX_MOVES


class Game:
    def __init__(self, win):
        self.win = win
        self.selected = None
        self.board = Board()
        self.turn = WHITE
        self.valid_moves = {}
        self.hint = None
        self.moves = 0
        self.pieces_num = 24
        self.draw = False
        self.last_move = None

    def update(self):
        self.board.draw(self.win)
        self.draw_valid_moves(self.valid_moves)
        self.draw = self.draw_check()
        if self.hint is not None:
            pygame.draw.circle(self.win, (0, 255, 0), (self.hint[0].x, self.hint[0].y), 50, 5)
            pygame.draw.circle(self.win, (0, 255, 0),
                               (self.hint[1][1] * SQUARE_SIZE + SQUARE_SIZE // 2,
                                self.hint[1][0] * SQUARE_SIZE + SQUARE_SIZE // 2), 15)

        pygame.display.update()
        return self.draw

    def winner(self):
        w_blocked, b_blocked = True, True
        for p in self.board.get_all_pieces(WHITE):
            if self.board.get_valid_moves(p):
                w_blocked = False

        for p in self.board.get_all_pieces(BLACK):
            if self.board.get_valid_moves(p):
                b_blocked = False

        if w_blocked and b_blocked:
            return self.last_move

        if w_blocked:
            return BLACK
        if b_blocked:
            return WHITE

        return self.board.winner()

    def draw_check(self):
        if self.pieces_num != self.board.pieces_left():
            self.moves = 0
            self.pieces_num = self.board.pieces_left()

        if self.moves >= MAX_MOVES:
            return True
        else:
            return False

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
            self.moves += 1
            # print(f"Liczba ruchów bez bicia: {self.moves}")

    def get_board(self):
        return self.board

    def ai_move(self, board):
        if board:
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
