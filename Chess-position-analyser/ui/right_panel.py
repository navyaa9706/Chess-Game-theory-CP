import pygame

# ===== COLORS =====
BG_PANEL = (248, 236, 240)
CARD_BG = (255, 255, 255)
BORDER = (220, 190, 200)

TEXT_DARK = (60, 30, 45)
TEXT_MID = (120, 80, 95)
TEXT_LIGHT = (170, 130, 145)

ALGO_COLORS = {
    "greedy": (180, 110, 140),
    "minimax": (150, 90, 120),
    "alphabeta": (130, 70, 100),
}


# ===== HELPER =====
def format_move(move):
    move = str(move)
    if len(move) == 4:
        return f"{move[:2]} → {move[2:]}"
    return move


# ===== MAIN DRAW =====
def draw_right_panel(screen, analysis_result, BOARD_LEFT_X, SQUARE_SIZE):

    panel_x = BOARD_LEFT_X + 8 * SQUARE_SIZE + 50
    panel_y = 80
    panel_w = 300
    panel_h = 8 * SQUARE_SIZE

    # ===== PANEL BG =====
    pygame.draw.rect(screen, BG_PANEL, (panel_x, panel_y, panel_w, panel_h), border_radius=12)
    pygame.draw.rect(screen, BORDER, (panel_x, panel_y, panel_w, panel_h), 1, border_radius=12)

    # ===== FONTS =====
    title_font = pygame.font.SysFont("Georgia", 14, bold=True)
    text_font = pygame.font.SysFont("Arial", 12)
    move_font = pygame.font.SysFont("Arial", 18, bold=True)

    # ===== TITLE =====
    screen.blit(title_font.render("ANALYSIS", True, TEXT_MID),
                (panel_x + 15, panel_y + 10))

    pygame.draw.line(screen, BORDER,
                     (panel_x + 10, panel_y + 35),
                     (panel_x + panel_w - 10, panel_y + 35), 1)

    # ===== EMPTY STATE =====
    if not analysis_result:
        msg = text_font.render("Press Analyse", True, TEXT_LIGHT)
        screen.blit(msg,
                    (panel_x + panel_w // 2 - msg.get_width() // 2,
                     panel_y + panel_h // 2))
        return

    # ===== ALGO CARDS =====
    y = panel_y + 45

    for algo in ["greedy", "minimax", "alphabeta"]:

        data = analysis_result[algo]

        move = format_move(data["move"])
        score = data["score"]
        nodes = data["nodes"]
        time = f"{data['time']:.3f}"
        # CARD
        pygame.draw.rect(screen, CARD_BG,
                         (panel_x + 10, y, panel_w - 20, 70),
                         border_radius=10)

        pygame.draw.rect(screen, BORDER,
                         (panel_x + 10, y, panel_w - 20, 70),
                         1, border_radius=10)

        # HEADER
        screen.blit(text_font.render(algo.upper(), True, ALGO_COLORS[algo]),
                    (panel_x + 20, y + 5))

        # MOVE
        screen.blit(move_font.render(move, True, TEXT_DARK),
                    (panel_x + 20, y + 25))

        # STATS
        stats = f"S:{score}  N:{nodes}  T:{time}s"
        screen.blit(text_font.render(stats, True, TEXT_MID),
                    (panel_x + 20, y + 48))

        y += 80

    # ===== COMPARISON =====
    y += 5
    pygame.draw.line(screen, BORDER,
                     (panel_x + 10, y),
                     (panel_x + panel_w - 10, y), 1)

    y += 10

    max_nodes = max(a["nodes"] for a in analysis_result.values())
    max_time = max(a["time"] for a in analysis_result.values())

    for label, key, max_val in [
        ("Nodes", "nodes", max_nodes),
        ("Time", "time", max_time)
    ]:

        screen.blit(text_font.render(label, True, TEXT_LIGHT),
                    (panel_x + 15, y))
        y += 15

        for algo in ["greedy", "minimax", "alphabeta"]:

            val = analysis_result[algo][key]

            ratio = val / max_val if max_val else 0
            bar_width = int(150 * ratio)

            # LABEL
            screen.blit(text_font.render(algo[:5], True, TEXT_MID),
                        (panel_x + 15, y))

            # BAR
            pygame.draw.rect(screen, (230, 210, 220),
                             (panel_x + 80, y + 5, 150, 6),
                             border_radius=3)

            pygame.draw.rect(screen, ALGO_COLORS[algo],
                             (panel_x + 80, y + 5, bar_width, 6),
                             border_radius=3)

            # VALUE
            if key == "time":
                display_val = f"{val:.3f}"
            else:
                display_val = str(val)
            
            val_text = text_font.render(display_val, True, TEXT_MID)
            screen.blit(val_text,
                        (panel_x + panel_w - val_text.get_width() - 10, y))
            
            y += 18

        y += 5