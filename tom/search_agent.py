import math
import random

import chess


class SearchAgent(object):

    def __init__(self, time_limit=5):
        """Setup the Search Agent"""
        self.time_limit = time_limit
        self.name = "Chess Engine"
        self.author = "S. Vanneste"

    def random_move(self, board: chess.Board):
        return random.sample(list(board.legal_moves), 1)[0]

    def random_with_first_level_search(self, board: chess.Board):
        moves = list(board.legal_moves)

        best_move = random.sample(moves, 1)[0]
        best_move_value = 0

        for move in moves:
            board.push(move)
            if board.is_checkmate():
                move_value = 100
                if move_value > best_move_value:
                    best_move = move
            board.pop()

            if board.is_into_check(move):
                move_value = 90
                if move_value > best_move_value:
                    best_move = move

            if board.is_capture(move):
                move_value = 80
                if move_value > best_move_value:
                    best_move = move

            if board.is_castling(move):
                move_value = 70
                if move_value > best_move_value:
                    best_move = move

        return best_move

    def ab_minimax_r(self, board):
        moves = list(board.legal_moves)

        best_move = random.sample(moves, 1)[0]
        best_move_value = -math.inf

        for move in moves:
            board.push(move)
            move_value = max(best_move_value, self.ab_minimax(False, 2, board, -math.inf, math.inf))
            board.pop()
            if move_value > best_move_value:
                best_move_value = move_value
                best_move = move
        return best_move

    def ab_minimax(self, maxTurn, maxDepth, board, alpha, beta):
        moves = board.legal_moves
        if maxDepth == 0:
            return -self.utility(board)
        if maxTurn:
            value = -math.inf
            for move in moves:
                board.push(move)
                value = max(value, self.ab_minimax(not maxTurn, maxDepth - 1, board, alpha, beta))
                board.pop()
                alpha = max(alpha, value)
                if beta <= alpha:
                    return value
            return value
        else:
            value = math.inf
            for move in moves:
                board.push(move)
                value = min(value, self.ab_minimax(not maxTurn, maxDepth - 1, board, alpha, beta))
                board.pop()
                beta = min(beta, value)
                if beta <= alpha:
                    return value
            return value

    def utility(self, board):
        u = 0
        for i in range(0, 64):
            piece = board.piece_at(i)
            if piece is not None:
                color = piece.color
                if color is board.turn:
                    u = u + self.getPieceValue(str(board.piece_at(i))) + self.getPosValue(str(board.piece_at(i)), i,
                                                                                          color)
                else:
                    u = u - (self.getPieceValue(str(board.piece_at(i))) + self.getPosValue(str(board.piece_at(i)), i,
                                                                                           color))
        return u

    def getPieceValue(self, piece):
        u = 0
        if piece == 'P' or piece == 'p':
            u = 100
        elif piece == "N" or piece == 'n':
            u = 300
        elif piece == "B" or piece == 'b':
            u = 300
        elif piece == "R" or piece == 'r':
            u = 500
        elif piece == "Q" or piece == 'q':
            u = 900
        elif piece == "K" or piece == 'k':
            u = 9000
        return u

    def getPosValue(self, piece, i, color):
        u = 0
        pawn_table = [0, 0, 0, 0, 0, 0, 0, 0,
                      50, 50, 50, 50, 50, 50, 50, 50,
                      10, 10, 20, 30, 30, 20, 10, 10,
                      5, 5, 10, 25, 25, 10, 5, 5,
                      0, 0, 0, 20, 20, 0, 0, 0,
                      5, -5, -10, 0, 0, -10, -5, 5,
                      5, 10, 10, -20, -20, 10, 10, 5,
                      0, 0, 0, 0, 0, 0, 0, 0]
        knight_table = [-50, -40, -30, -30, -30, -30, -40, -50,
                        -40, -20, 0, 0, 0, 0, -20, -40,
                        -30, 0, 10, 15, 15, 10, 0, -30,
                        -30, 5, 15, 20, 20, 15, 5, -30,
                        -30, 0, 15, 20, 20, 15, 0, -30,
                        -30, 5, 10, 15, 15, 10, 5, -30,
                        -40, -20, 0, 5, 5, 0, -20, -40,
                        -50, -40, -30, -30, -30, -30, -40, -50]
        bishop_table = [-20, -10, -10, -10, -10, -10, -10, -20,
                        -10, 0, 0, 0, 0, 0, 0, -10,
                        -10, 0, 5, 10, 10, 5, 0, -10,
                        -10, 5, 5, 10, 10, 5, 5, -10,
                        -10, 0, 10, 10, 10, 10, 0, -10,
                        -10, 10, 10, 10, 10, 10, 10, -10,
                        -10, 5, 0, 0, 0, 0, 5, -10,
                        -20, -10, -10, -10, -10, -10, -10, -20]
        rook_table = [0, 0, 0, 0, 0, 0, 0, 0,
                      5, 10, 10, 10, 10, 10, 10, 5,
                      -5, 0, 0, 0, 0, 0, 0, -5,
                      -5, 0, 0, 0, 0, 0, 0, -5,
                      -5, 0, 0, 0, 0, 0, 0, -5,
                      -5, 0, 0, 0, 0, 0, 0, -5,
                      -5, 0, 0, 0, 0, 0, 0, -5,
                      0, 0, 0, 5, 5, 0, 0, 0]
        queen_table = [-20, -10, -10, -5, -5, -10, -10, -20,
                       -10, 0, 0, 0, 0, 0, 0, -10,
                       -10, 0, 5, 5, 5, 5, 0, -10,
                       -5, 0, 5, 5, 5, 5, 0, -5,
                       0, 0, 5, 5, 5, 5, 0, -5,
                       -10, 5, 5, 5, 5, 5, 0, -10,
                       -10, 0, 5, 0, 0, 0, 0, -10,
                       -20, -10, -10, -5, -5, -10, -10, -20]
        king_table = [-30, -40, -40, -50, -50, -40, -40, -30,
                      -30, -40, -40, -50, -50, -40, -40, -30,
                      -30, -40, -40, -50, -50, -40, -40, -30,
                      -30, -40, -40, -50, -50, -40, -40, -30,
                      -20, -30, -30, -40, -40, -30, -30, -20,
                      -10, -20, -20, -20, -20, -20, -20, -10,
                      20, 20, 0, 0, 0, 0, 20, 20,
                      20, 30, 10, 0, 0, 10, 30, 20]
        if piece == 'P' or piece == 'p':
            if color:
                u = pawn_table[i]
            else:
                u = pawn_table[63 - i]
        elif piece == "N" or piece == 'n':
            if color:
                u = knight_table[i]
            else:
                u = knight_table[63 - i]
        elif piece == "B" or piece == 'b':
            if color:
                u = bishop_table[i]
            else:
                u = bishop_table[63 - i]
        elif piece == "R" or piece == 'r':
            if color:
                u = rook_table[i]
            else:
                u = rook_table[63 - i]
        elif piece == "Q" or piece == 'q':
            if color:
                u = queen_table[i]
            else:
                u = queen_table[63 - i]
        elif piece == "K" or piece == 'k':
            if color:
                u = king_table[i]
            else:
                u = king_table[63 - i]
        return u
