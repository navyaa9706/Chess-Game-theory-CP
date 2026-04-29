import pygame
import os

#================= IMAGES =================
def load_images():
    piece_files = {
        "wP": "wp.png", "wR": "wr.png", "wN": "wn.png",
        "wB": "wb.png", "wQ": "wq.png", "wK": "wk.png",
        "bP": "bp.png", "bR": "br.png", "bN": "bn.png",
        "bB": "bb.png", "bQ": "bq.png", "bK": "bk.png"
    }

    images = {}

    for piece, filename in piece_files.items():
        path = os.path.join("assets/images", filename)
        if os.path.exists(path):
            images[piece] = pygame.image.load(path).convert_alpha()

    return images


# ================= PRESETS =================

def get_presets():
    return {
       "Mate in 1": [
        ["bR", None, None, None, None, "bR", "bK", None],  # 8
        ["bQ", None, None, None, None, "bP", None, "bP"],  # 7
        [None]*8,                                          # 6
        [None]*8,                                          # 5
        [None]*8,                                          # 4
        [None]*8,                                          # 3
        [None, "wB", None, None, None, "wP", None, None],  # 2
        [None, "wK", None, None, None, None, "wR", None],  # 1
        ],
        "Simple Trade": [
            [None]*8,
            [None]*8,
            [None]*8,
            [None,None,"bQ",None,None,None,None,None],
            [None,None,"wQ",None,None,None,None,None],
            [None]*8,
            [None]*8,
            [None]*8,
        ]
    }


def load_preset(board, piece_count, preset_board):

    # reset board
    for r in range(8):
        for c in range(8):
            board[r][c] = preset_board[r][c]

    # reset counts
    for k in piece_count:
        piece_count[k] = 0

    # recount
    for row in board:
        for p in row:
            if p:
                piece_count[p] += 1