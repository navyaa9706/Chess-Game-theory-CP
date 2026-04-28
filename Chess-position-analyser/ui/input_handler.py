<<<<<<< HEAD
import pygame
import chess

from engine.analyse import analyse_position
from engine.evaluation import evaluate_board
from engine.board_converter import board_to_fen


def handle_input(events, state):

    board        = state["board"]            # 2D UI board
    palette      = state["palette"]
    coord_to_sq  = state["coord_to_square"]
    piece_count  = state["piece_count"]
    piece_limits = state["piece_limits"]

    dragging_piece = state["dragging_piece"]
    old_r          = state["old_r"]
    old_c          = state["old_c"]

    turn        = state["turn"]
    white_btn   = state["white_btn"]
    black_btn   = state["black_btn"]
    analyse_btn = state["analyse_btn"]

    analysis_result = state.get("analysis_result", None)

    for event in events:

        # ── MOUSE DOWN ─────────────────────────────────────
        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos

            # Switch turn
            if white_btn and white_btn.collidepoint(mx, my):
                turn = "w"
                continue

            if black_btn and black_btn.collidepoint(mx, my):
                turn = "b"
                continue

            # ── ANALYSE BUTTON ─────────────────────────────
            if analyse_btn and analyse_btn.collidepoint(mx, my):

                # Validate board (must have both kings)
                flat = [p for row in board for p in row]
                if "wK" not in flat or "bK" not in flat:
                    print("Invalid board: both kings required")
                    continue

                # Convert to chess.Board
                fen = board_to_fen(board)
                chess_board = chess.Board(fen)

                # Compute evaluation + analysis
                score = evaluate_board(chess_board)
                analysis = analyse_position(chess_board, turn)

                # Return both cleanly
                analysis_result = {
                    "score": score,
                    "result": analysis
                }
                continue

            # ── PICK FROM PALETTE ─────────────────────────
            picked = False
            for p, rect in palette:
                if rect.collidepoint(mx, my):
                    if piece_count[p] < piece_limits[p]:
                        dragging_piece = p
                        old_r, old_c   = None, None
                    else:
                        print(f"LIMIT REACHED for {p}")
                    picked = True
                    break

            if picked:
                continue

            # ── PICK FROM BOARD ───────────────────────────
            square = coord_to_sq((mx, my))
            if square:
                r, c = square
                if board[r][c] is not None:
                    dragging_piece = board[r][c]
                    old_r, old_c   = r, c
                    board[r][c]    = None

        # ── MOUSE UP ─────────────────────────────────────
        elif event.type == pygame.MOUSEBUTTONUP:

            if not dragging_piece:
                continue

            mx, my = event.pos
            square = coord_to_sq((mx, my))

            if square:
                r, c = square

                if board[r][c] is None:
                    board[r][c] = dragging_piece

                    # from palette
                    if old_r is None:
                        piece_count[dragging_piece] += 1

                else:
                    # occupied → revert
                    if old_r is not None:
                        board[old_r][old_c] = dragging_piece

            else:
                # dropped outside → delete if from board
                if old_r is not None:
                    piece_count[dragging_piece] = max(
                        0, piece_count[dragging_piece] - 1
                    )

            dragging_piece = None
            old_r, old_c   = None, None

    return dragging_piece, old_r, old_c, turn, analysis_result
=======
import pygame
from engine.analyse import analyse_position


def handle_input(events, state):

    board        = state["board"]
    palette      = state["palette"]
    coord_to_sq  = state["coord_to_square"]
    piece_count  = state["piece_count"]
    piece_limits = state["piece_limits"]

    dragging_piece = state["dragging_piece"]
    old_r          = state["old_r"]
    old_c          = state["old_c"]

    turn        = state["turn"]
    white_btn   = state["white_btn"]
    black_btn   = state["black_btn"]
    analyse_btn = state["analyse_btn"]

    # fallback if not present
    analysis_result = state.get("analysis_result", None)

    for event in events:

        # ── MOUSE DOWN ─────────────────────────────────────
        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos

            # ✅ TURN SELECT
            if white_btn and white_btn.collidepoint(mx, my):
                turn = "w"
                continue

            if black_btn and black_btn.collidepoint(mx, my):
                turn = "b"
                continue

            # ✅ ANALYSE BUTTON
            if analyse_btn and analyse_btn.collidepoint(mx, my):

                flat = [p for row in board for p in row]
                if "wK" not in flat or "bK" not in flat:
                    print("Invalid board: both kings required")
                    continue

                analysis_result = analyse_position(board, turn)
                continue

            # ✅ PALETTE PICK (FIXED — THIS WAS BROKEN)
            picked = False
            for p, rect in palette:
                if rect.collidepoint(mx, my):
                    if piece_count[p] < piece_limits[p]:
                        dragging_piece = p
                        old_r, old_c   = None, None
                    else:
                        print(f"LIMIT REACHED for {p}")
                    picked = True
                    break

            if picked:
                continue

            # ✅ BOARD PICK
            square = coord_to_sq((mx, my))
            if square:
                r, c = square
                if board[r][c] is not None:
                    dragging_piece = board[r][c]
                    old_r, old_c   = r, c
                    board[r][c]    = None

        # ── MOUSE UP ─────────────────────────────────────
        elif event.type == pygame.MOUSEBUTTONUP:

            if not dragging_piece:
                continue

            mx, my = event.pos
            square = coord_to_sq((mx, my))

            if square:
                r, c = square

                if board[r][c] is None:
                    board[r][c] = dragging_piece

                    # from palette
                    if old_r is None:
                        piece_count[dragging_piece] += 1

                else:
                    # occupied → revert
                    if old_r is not None:
                        board[old_r][old_c] = dragging_piece

            else:
                # dropped outside → delete if from board
                if old_r is not None:
                    piece_count[dragging_piece] = max(
                        0, piece_count[dragging_piece] - 1
                    )

            dragging_piece = None
            old_r, old_c   = None, None

    return dragging_piece, old_r, old_c, turn, analysis_result
>>>>>>> b2b86a5855560c379b5274914dc1441a1715e3ae
