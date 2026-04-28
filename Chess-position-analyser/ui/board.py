import pygame
from config import LIGHT_SQ, DARK_SQ, LABEL_COLOR


def draw_board(screen, BOARD_TOP_Y, BOARD_LEFT_X, SQUARE_SIZE):
    font = pygame.font.SysFont("Arial", 15)

    for row in range(8):
        for col in range(8):
            color = LIGHT_SQ if (row + col) % 2 == 0 else DARK_SQ

            x = BOARD_LEFT_X + col * SQUARE_SIZE
            y = BOARD_TOP_Y  + row * SQUARE_SIZE

            pygame.draw.rect(screen, color, (x, y, SQUARE_SIZE, SQUARE_SIZE))

            # rank numbers (8 → 1) on the left edge of column 0
            if col == 0:
                text = font.render(str(8 - row), True, LABEL_COLOR)
                screen.blit(text, (x - 22, y + SQUARE_SIZE // 2 - 8))

            # file letters (a → h) below row 7
            if row == 7:
                letter = chr(ord('a') + col)
                text = font.render(letter, True, LABEL_COLOR)
                screen.blit(text, (x + SQUARE_SIZE // 2 - 5, y + SQUARE_SIZE + 6))

def draw_pieces(screen, board, PIECE_IMAGES, BOARD_TOP_Y, BOARD_LEFT_X, SQUARE_SIZE):
    padding = 6  # thoda space square ke andar
    piece_size = SQUARE_SIZE - padding * 2

    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece:
                img = PIECE_IMAGES.get(piece)
                if img:
                    img_s = pygame.transform.smoothscale(img, (piece_size, piece_size))
                    x = BOARD_LEFT_X + col * SQUARE_SIZE + padding
                    y = BOARD_TOP_Y  + row * SQUARE_SIZE + padding
                    screen.blit(img_s, (x, y))
def draw_palette(screen, PIECE_IMAGES, BOARD_LEFT_X, BOARD_TOP_Y, SQUARE_SIZE):
    """
    Two rows of piece icons below the board.
    Returns list of (piece_key, pygame.Rect) for hit-testing.
    """
    palette = []

    white_pieces = ["wK", "wQ", "wR", "wB", "wN", "wP"]
    black_pieces = ["bK", "bQ", "bR", "bB", "bN", "bP"]

    BOARD_BOTTOM = BOARD_TOP_Y + 8 * SQUARE_SIZE
    ICON_SIZE    = 48
    H_GAP        = 14          # gap between icons
    ROW_GAP      = 10          # gap between white row and black row
    TOP_MARGIN   = 20          # space below board

    white_y = BOARD_BOTTOM + TOP_MARGIN
    black_y = white_y + ICON_SIZE + ROW_GAP

    for i, p in enumerate(white_pieces):
        x    = BOARD_LEFT_X + i * (ICON_SIZE + H_GAP)
        rect = pygame.Rect(x, white_y, ICON_SIZE, ICON_SIZE)
        palette.append((p, rect))
        img = PIECE_IMAGES.get(p)
        if img:
            screen.blit(img, (x, white_y))

    for i, p in enumerate(black_pieces):
        x    = BOARD_LEFT_X + i * (ICON_SIZE + H_GAP)
        rect = pygame.Rect(x, black_y, ICON_SIZE, ICON_SIZE)
        palette.append((p, rect))
        img = PIECE_IMAGES.get(p)
        if img:
            screen.blit(img, (x, black_y))

    return palette