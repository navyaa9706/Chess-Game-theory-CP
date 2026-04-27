from engine.board_converter import board_to_fen
from engine.evaluation import evaluate_board
import chess
import time


def analyse_position_greedy(ui_board, turn):
    fen = board_to_fen(ui_board, turn)
    board = chess.Board(fen)

    best_move = None
    best_score = float("-inf") if turn == "w" else float("inf")

    nodes = 0
    start = time.time()

    for move in board.legal_moves:
        nodes += 1

        board.push(move)
        score = evaluate_board(board)
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

    print("\nGREEDY")
    print("Best Move:", best_move)
    print("Score:", best_score)
    print("Nodes:", nodes)
    print("Time:", round(total_time, 5), "sec")

    return best_move, best_score, nodes, total_time