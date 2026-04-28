import pygame
import sys

from ui.board         import draw_board, draw_pieces
from ui.left_panel    import draw_left_panel
from ui.right_panel   import draw_right_panel
from ui.input_handler import handle_input
from ui.utils         import coord_to_square
from ui.assets_loader import load_images

from config import (
    WIDTH, HEIGHT, BG_COLOR,
    ROWS, COLS,
    SQUARE_SIZE, BOARD_LEFT_X, BOARD_TOP_Y, BOARD_HEIGHT,
)

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess Position Analyzer")

PIECE_IMAGES = load_images()

board = [[None] * COLS for _ in range(ROWS)]

dragging_piece = None
old_r, old_c   = None, None
turn           = "w"
analysis_result = None

piece_limits = {
    "wK": 1, "wQ": 1, "wR": 2, "wB": 2, "wN": 2, "wP": 8,
    "bK": 1, "bQ": 1, "bR": 2, "bB": 2, "bN": 2, "bP": 8,
}
piece_count = {k: 0 for k in piece_limits}
palette     = []

title_font = pygame.font.SysFont("Georgia", 24, bold=True)
clock      = pygame.time.Clock()


while True:
    screen.fill(BG_COLOR)

    # ===== TITLE =====
    title_surf = title_font.render("Chess Position Analyzer", True, (60, 30, 45))
    screen.blit(title_surf, (BOARD_LEFT_X, 22))

    mouse_pos = pygame.mouse.get_pos()
    events    = pygame.event.get()

    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # ===== BOARD =====
    draw_board(screen, BOARD_TOP_Y, BOARD_LEFT_X, SQUARE_SIZE)
    draw_pieces(screen, board, PIECE_IMAGES, BOARD_TOP_Y, BOARD_LEFT_X, SQUARE_SIZE)

    # ===== LEFT PANEL =====
    white_btn, black_btn, analyse_btn, palette = draw_left_panel(
    screen, PIECE_IMAGES, turn, SQUARE_SIZE
    )

    # ===== RIGHT PANEL =====
    draw_right_panel(
        screen, analysis_result,
        BOARD_LEFT_X, SQUARE_SIZE
    )

    # ===== STATE =====
    state = {
        "board":           board,
        "palette":         palette,
        "mouse_pos":       mouse_pos,
        "coord_to_square": lambda pos: coord_to_square(
            pos, BOARD_TOP_Y, BOARD_LEFT_X, BOARD_HEIGHT, SQUARE_SIZE
        ),
        "analysis_result": analysis_result,
        "piece_count":     piece_count,
        "piece_limits":    piece_limits,
        "turn":            turn,
        "white_btn":       white_btn,
        "black_btn":       black_btn,
        "analyse_btn":     analyse_btn,
        "dragging_piece":  dragging_piece,
        "old_r":           old_r,
        "old_c":           old_c,
    }

    # ===== INPUT =====
    dragging_piece, old_r, old_c, turn, analysis_result = handle_input(events, state)

    # ===== DRAG GHOST =====
    if dragging_piece and dragging_piece in PIECE_IMAGES:
        mx, my = mouse_pos
        screen.blit(
            PIECE_IMAGES[dragging_piece],
            (mx - SQUARE_SIZE // 2, my - SQUARE_SIZE // 2),
        )

    pygame.display.flip()
    clock.tick(60)