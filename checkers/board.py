import pygame

from .constants import BLACK, ROWS, SQUARE_SIZE, COLS, WHITE, BROWN, LIGHT_BROWN
from .piece import Piece


class Board:
    def __init__(self):
        self.board = []
        self.white_left = 12
        self.black_left = 12
        self.white_queens = 0
        self.black_queens = 0
        self.create_board()
        # self.weights = [
        #     [4, 1, 2, 1, 1, 2, 1, 4],
        #     [1, 4, 3, 2, 2, 3, 4, 1],
        #     [2, 3, 4, 3, 3, 4, 3, 2],
        #     [1, 2, 3, 4, 4, 3, 2, 1],
        #     [1, 2, 3, 4, 4, 3, 2, 1],
        #     [2, 3, 4, 3, 3, 4, 3, 2],
        #     [1, 4, 3, 2, 2, 3, 4, 1],
        #     [4, 1, 2, 1, 1, 2, 1, 4]
        # ]

    @staticmethod
    def draw_squares(win):
        for row in range(ROWS):
            for col in range(row % 2, COLS, 2):
                pygame.draw.rect(win, LIGHT_BROWN, (row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
        for row in range(ROWS):
            for col in range((row + 1) % 2, COLS, 2):
                pygame.draw.rect(win, BROWN, (row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    # def evaluate(self):
    #     return self.black_left - self.white_left + (self.black_queens * 0.5 - self.white_queens * 0.5)

    # def evaluate(self):
    #
    #     score = self.black_left - self.white_left + (self.black_queens * 0.5 - self.white_queens * 0.5)
    #     for i in range(len(self.board)):
    #         for j in range(len(self.board[i])):
    #             if self.board[i][j] != 0:
    #                 if self.board[i][j].getColor() == BLACK:  # jeżeli jest to pionek bota
    #                     score += self.weights[i][j]
    #                 elif self.board[i][j].getColor() == WHITE:  # jeżeli jest to pionek przeciwnika
    #                     score -= self.weights[i][j]
    #     print(score)
    #     return score

    def evaluate(self):
        piece_connectivity = 0
        piece_advancement = 0
        piece_mobility = 0
        central_control = 0
        king_safety = 0

        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j] != 0:
                    if self.board[i][j].getColor() == WHITE:
                        if i < 5 and not self.board[i][j].queen:
                            piece_advancement -= (5 - i)
                        piece_mobility -= len(self.get_valid_moves(self.board[i][j]))
                        if self.board[i][j].queen:
                            king_safety -= 10
                            king_safety += abs(i - len(self.board) // 2)
                            king_safety += min(i, len(self.board) - 1 - i)

                            threat_lvl = self.count_threatening_squares(i, j, BLACK)
                            king_safety += threat_lvl

                        piece_connectivity -= self.get_piece_connectivity(i, j, WHITE)

                    elif self.board[i][j].getColor() == BLACK:
                        if i > 4 and not self.board[i][j].queen:
                            piece_advancement += (i - 4)
                        piece_mobility += len(self.get_valid_moves(self.board[i][j]))

                        if self.board[i][j].queen:
                            king_safety += 10
                            king_safety -= abs(i - len(self.board) // 2)
                            king_safety -= min(i, len(self.board) - 1 - i)

                            threat_lvl = self.count_threatening_squares(i, j, WHITE)
                            king_safety -= threat_lvl

                        piece_connectivity += self.get_piece_connectivity(i, j, BLACK)

        score = self.black_left - self.white_left + \
                2 * (self.black_queens - self.white_queens) + \
                0.2 * piece_advancement + \
                0.2 * piece_mobility + \
                0.1 * king_safety + \
                0.1 * piece_connectivity

        return round(score, 1)

    def get_all_pieces(self, color):
        pieces = []
        for row in self.board:
            for piece in row:
                if piece != 0 and piece.color == color:
                    pieces.append(piece)
        return pieces

    def move(self, piece, row, column):
        self.board[piece.row][piece.column], self.board[row][column] = \
            self.board[row][column], self.board[piece.row][piece.column]
        piece.move(row, column)

        if row == ROWS - 1 or row == 0:
            piece.make_queen()
            if piece.color == BLACK:
                self.black_queens += 1
            else:
                self.white_queens += 1

    def get_piece(self, row, column):
        return self.board[row][column]

    def create_board(self):
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                if col % 2 == ((row + 1) % 2):
                    if row < 3:
                        self.board[row].append(Piece(row, col, BLACK))
                    elif row > 4:
                        self.board[row].append(Piece(row, col, WHITE))
                    else:
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)

    def draw(self, win):
        self.draw_squares(win)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(win)

    def remove(self, pieces):
        for piece in pieces:
            self.board[piece.row][piece.column] = 0
            if piece != 0:
                if piece.color == WHITE:
                    self.white_left -= 1
                else:
                    self.black_left -= 1

    def winner(self):
        if self.white_left <= 0:
            return BLACK
        elif self.black_left <= 0:
            return WHITE

        return None

    def get_valid_moves(self, piece):
        moves = {}
        left = piece.column - 1
        right = piece.column + 1
        row = piece.row

        if piece.color == WHITE or piece.queen:
            moves.update(self._traverse_left(row - 1, max(row - 3, -1), -1, piece.color, left))
            moves.update(self._traverse_right(row - 1, max(row - 3, -1), -1, piece.color, right))

        if piece.color == BLACK or piece.queen:
            moves.update(self._traverse_left(row + 1, min(row + 3, ROWS), 1, piece.color, left))
            moves.update(self._traverse_right(row + 1, min(row + 3, ROWS), 1, piece.color, right))

        return moves

    def _traverse_left(self, start, stop, step, color, left, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if left < 0:
                break

            current = self.board[r][left]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, left)] = last + skipped
                else:
                    moves[(r, left)] = last

                if last:
                    if step == -1:
                        row = max(r - 3, 0)
                    else:
                        row = min(r + 3, ROWS)
                    moves.update(self._traverse_left(r + step, row, step, color, left - 1, skipped=last))
                    moves.update(self._traverse_right(r + step, row, step, color, left + 1, skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]

            left -= 1

        return moves

    def _traverse_right(self, start, stop, step, color, right, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if right >= COLS:
                break

            current = self.board[r][right]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, right)] = last + skipped
                else:
                    moves[(r, right)] = last

                if last:
                    if step == -1:
                        row = max(r - 3, 0)
                    else:
                        row = min(r + 3, ROWS)
                    moves.update(self._traverse_left(r + step, row, step, color, right - 1, skipped=last))
                    moves.update(self._traverse_right(r + step, row, step, color, right + 1, skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]

            right += 1

        return moves

    def pieces_left(self):
        return self.black_left + self.white_left

    def count_threatening_squares(self, r, c, threatening_colour):
        opponent_sq = 0
        adj_sq = [(r - 1, c - 1), (r - 1, c + 1), (r + 1, c - 1), (r + 1, c + 1)]
        for sqr, sqc in adj_sq:
            if 0 <= sqr < len(self.board) and 0 <= sqc < len(self.board[sqr]):
                if self.board[sqr][sqc] != 0:
                    if self.board[sqr][sqc].getColor() == threatening_colour:
                        opponent_sq += 1
        return opponent_sq

    def get_piece_connectivity(self, r, c, colour):
        piece_connectivity = 0
        central_region = (2, 2, len(self.board) - 3, len(self.board) - 3)
        adj_sq = [(r - 1, c - 1), (r - 1, c + 1), (r + 1, c - 1), (r + 1, c + 1)]
        for sqr, sqc in adj_sq:
            if (central_region[0] <= sqr <= central_region[0] + central_region[2] and
                    central_region[1] <= sqc <= central_region[1] + central_region[3]):
                if self.board[sqr][sqc] != 0:
                    if self.board[sqr][sqc].getColor() == colour:
                        piece_connectivity += 1

            if 0 <= sqr < len(self.board) and 0 <= sqc < len(self.board[sqr]):
                if self.board[sqr][sqc] != 0:
                    if self.board[sqr][sqc].getColor() == colour:
                        piece_connectivity += 1
        return piece_connectivity
