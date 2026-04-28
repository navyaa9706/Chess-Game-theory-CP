from engine.board_converter import board_to_fen
from engine.evaluation import evaluate_board
import chess
from engine.ordering import order_moves
import time

DEPTH = 3
nodes = 0

def analyse_position_alphabeta(ui_board, turn):
    global nodes
    nodes = 0

    fen = board_to_fen(ui_board, turn)
    board = chess.Board(fen)

    best_move = None
    best_score = float("-inf") if turn == "w" else float("inf")

    start = time.time()

    for move in board.legal_moves:
        board.push(move)

        score = alphabeta(
            board,
            DEPTH - 1,
            float("-inf"),
            float("inf"),
            False if turn == "w" else True
        )

        board.pop()

        if turn == "w":
            if score > best_score:
                best_score = score
                best_move = move
        else:
            if score < best_score:
                best_score = score
                best_move = move

    total_time = time.time() - start

    print("\nALPHA-BETA")
    print("Best Move:", best_move)
    print("Score:", best_score)
    print("Nodes:", nodes)
    print("Time:", round(total_time, 5), "sec")

    return best_move, best_score, nodes, total_time


def alphabeta(board, depth, alpha, beta, maximizing):
    global nodes
    nodes += 1

    if depth == 0 or board.is_game_over():
        return evaluate_board(board)

    moves = list(board.legal_moves)

    if maximizing:
        max_eval = float("-inf")

        for move in moves:
            board.push(move)
            eval = alphabeta(board, depth - 1, alpha, beta, False)
            board.pop()

            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)

            if beta <= alpha:
                break

        return max_eval

    else:
        min_eval = float("inf")

        for move in moves:
            board.push(move)
            eval = alphabeta(board, depth - 1, alpha, beta, True)
            board.pop()

            min_eval = min(min_eval, eval)
            beta = min(beta, eval)

            if beta <= alpha:
                break

        return min_eval