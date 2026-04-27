import time
from engine.board_converter import board_to_fen
from engine.evaluation import evaluate_board
import chess

MAX_DEPTH = 4
nodes = 0


def analyse_position_iddfs(ui_board, turn):
    global nodes
    nodes = 0

    fen = board_to_fen(ui_board, turn)
    board = chess.Board(fen)

    best_move = None
    best_score = float("-inf") if turn == "w" else float("inf")

    start = time.time()

    for depth in range(1, MAX_DEPTH + 1):
        current_best_move = None
        current_best_score = float("-inf") if turn == "w" else float("inf")

        for move in board.legal_moves:
            board.push(move)

            score = minimax(board, depth - 1, False if turn == "w" else True)

            board.pop()

            if turn == "w":
                if score > current_best_score:
                    current_best_score = score
                    current_best_move = move
            else:
                if score < current_best_score:
                    current_best_score = score
                    current_best_move = move

        best_move = current_best_move
        best_score = current_best_score

    total_time = time.time() - start

    print("\nIDDFS")
    print("Best Move:", best_move)
    print("Score:", best_score)
    print("Nodes:", nodes)
    print("Time:", round(total_time, 5), "sec")

    return best_move, best_score, nodes, total_time


def minimax(board, depth, maximizing):
    global nodes
    nodes += 1

    if depth == 0 or board.is_game_over():
        return evaluate_board(board)

    moves = list(board.legal_moves)

    if maximizing:
        max_eval = float("-inf")
        for move in moves:
            board.push(move)
            eval = minimax(board, depth - 1, False)
            board.pop()
            max_eval = max(max_eval, eval)
        return max_eval
    else:
        min_eval = float("inf")
        for move in moves:
            board.push(move)
            eval = minimax(board, depth - 1, True)
            board.pop()
            min_eval = min(min_eval, eval)
        return min_eval
