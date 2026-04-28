import pygame
import sys

from ui.board         import draw_board, draw_pieces
from ui.left_panel    import draw_left_panel
from ui.right_panel   import draw_right_panel
from ui.input_handler import handle_input
from ui.utils         import coord_to_square
from ui.assets_loader import load_images, get_presets
from ui.eval_bar      import EvalBar

from config import (
    WIDTH, HEIGHT, BG_COLOR,
    ROWS, COLS,
    SQUARE_SIZE, BOARD_LEFT_X, BOARD_TOP_Y, BOARD_HEIGHT,
)

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess Position Analyzer")

PIECE_IMAGES = load_images()

# ===== PRESETS =====
PRESETS = get_presets()
selected_preset = None
dropdown_open = False

# ===== GAME STATE =====
board = [[None] * COLS for _ in range(ROWS)]

dragging_piece = None
old_r, old_c   = None, None
turn           = "w"

analysis_result = None
eval_score = 0

# ===== PIECE LIMITS =====
piece_limits = {
    "wK": 1, "wQ": 1, "wR": 2, "wB": 2, "wN": 2, "wP": 8,
    "bK": 1, "bQ": 1, "bR": 2, "bB": 2, "bN": 2, "bP": 8,
}
piece_count = {k: 0 for k in piece_limits}
palette     = []

# ===== UI =====
title_font = pygame.font.SysFont("Georgia", 24, bold=True)
clock      = pygame.time.Clock()

eval_bar = EvalBar(
    x=BOARD_LEFT_X + 8 * SQUARE_SIZE + 5,
    y=BOARD_TOP_Y,
    width=20,
    height=BOARD_HEIGHT
)

# ================= MAIN LOOP =================
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
    white_btn, black_btn, analyse_btn, palette, dropdown_rect, option_rects = draw_left_panel(
        screen,
        PIECE_IMAGES,
        turn,
        SQUARE_SIZE,
        PRESETS,
        selected_preset,
        dropdown_open
    )

    # ===== RIGHT PANEL =====
    draw_right_panel(
        screen,
        analysis_result,
        BOARD_LEFT_X,
        SQUARE_SIZE
    )

    # ===== EVAL BAR =====
    eval_bar.draw(screen)

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

        # ===== PRESET STATE =====
        "presets": PRESETS,
        "selected_preset": selected_preset,
        "dropdown_open": dropdown_open,
        "dropdown_rect": dropdown_rect,
        "option_rects": option_rects,
    }

    # ===== INPUT =====
    (
        dragging_piece,
        old_r,
        old_c,
        turn,
        raw_result,
        selected_preset,
        dropdown_open
    ) = handle_input(events, state)

    # ===== PROCESS ANALYSIS RESULT =====
    if isinstance(raw_result, dict):
        # pick ONE algo score for eval bar (use alphabeta)
        if "alphabeta" in raw_result:
            eval_score = raw_result["alphabeta"]["score"]
        analysis_result = raw_result

    # ===== UPDATE EVAL BAR =====
    eval_bar.update(eval_score)

    # ===== DRAG GHOST =====
    if dragging_piece and dragging_piece in PIECE_IMAGES:
        mx, my = mouse_pos
        screen.blit(
            PIECE_IMAGES[dragging_piece],
            (mx - SQUARE_SIZE // 2, my - SQUARE_SIZE // 2),
        )

    pygame.display.flip()
    clock.tick(60)