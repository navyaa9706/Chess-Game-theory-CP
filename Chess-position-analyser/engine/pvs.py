import time
from engine.board_converter import board_to_fen
from engine.evaluation import evaluate_board
import chess

DEPTH = 4
nodes = 0


def analyse_position_pvs(ui_board, turn):
    global nodes
    nodes = 0

    fen = board_to_fen(ui_board, turn)
    board = chess.Board(fen)

    best_move = None
    best_score = float("-inf")

    start = time.time()

    for move in board.legal_moves:
        board.push(move)

        score = -pvs(board, DEPTH - 1, float("-inf"), float("inf"))

        board.pop()

        if score > best_score:
            best_score = score
            best_move = move

    total_time = time.time() - start

    return best_move, best_score, nodes, total_time


def pvs(board, depth, alpha, beta):
    global nodes
    nodes += 1

    if depth == 0 or board.is_game_over():
        return evaluate_board(board)

    first = True

    for move in board.legal_moves:
        board.push(move)

        if first:
            score = -pvs(board, depth - 1, -beta, -alpha)
        else:
            score = -pvs(board, depth - 1, -alpha - 1, -alpha)

            if score > alpha:
                score = -pvs(board, depth - 1, -beta, -alpha)

        board.pop()

        alpha = max(alpha, score)

        if alpha >= beta:
            break

        first = False

    return alpha