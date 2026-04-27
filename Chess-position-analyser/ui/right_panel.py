import pygame

# ── THEME (MATCHES YOUR UI) ──────────────────────────────
BG_PANEL      = (248, 236, 240)
CARD_BG       = (255, 255, 255, 160)
CARD_BORDER   = (220, 190, 200)

ALGO_COLORS = {
    "greedy": {
        "header": (235, 210, 220),
        "accent": (130, 70, 90),
        "badge":  (220, 180, 200),
        "bar":    (180, 110, 140),
        "label":  "Fast",
    },
    "minimax": {
        "header": (240, 220, 230),
        "accent": (110, 60, 80),
        "badge":  (225, 190, 210),
        "bar":    (170, 100, 130),
        "label":  "Deep",
    },
    "alphabeta": {
        "header": (245, 225, 235),
        "accent": (100, 50, 70),
        "badge":  (230, 200, 215),
        "bar":    (160, 90, 120),
        "label":  "Optimized",
    },
}

TEXT_DARK   = (60, 30, 45)
TEXT_MID    = (120, 80, 95)
TEXT_LIGHT  = (170, 130, 145)
DIVIDER_COL = (230, 200, 210)
BAR_TRACK   = (235, 215, 220)


# ── HELPERS ──────────────────────────────────────────────
def _fmt_move(raw):
    raw = str(raw)
    if len(raw) == 4:
        return f"{raw[:2]} → {raw[2:]}"
    return raw


def _rounded_rect(w, h, color, r):
    surf = pygame.Surface((w, h), pygame.SRCALPHA)
    pygame.draw.rect(surf, color, (0, 0, w, h), border_radius=r)
    return surf


# ── MAIN DRAW FUNCTION ───────────────────────────────────
def draw_right_panel(screen, analysis_result, BOARD_LEFT_X, SQUARE_SIZE):

    panel_x = BOARD_LEFT_X + 8 * SQUARE_SIZE + 40
    panel_y = 80
    panel_w = 300
    panel_h = 8 * SQUARE_SIZE   # EXACT BOARD HEIGHT

    # ===== PANEL BG =====
    bg = _rounded_rect(panel_w, panel_h, (*BG_PANEL, 240), 12)
    screen.blit(bg, (panel_x, panel_y))

    pygame.draw.rect(screen, DIVIDER_COL,
                     (panel_x, panel_y, panel_w, panel_h),
                     1, border_radius=12)

    # ===== FONTS =====
    f_title = pygame.font.SysFont("Georgia", 14, bold=True)
    f_algo  = pygame.font.SysFont("Arial", 11, bold=True)
    f_move  = pygame.font.SysFont("Segoe UI Symbol", 20, bold=True)
    f_text  = pygame.font.SysFont("Arial", 11)
    # ===== HEADER =====
    screen.blit(f_title.render("ANALYSIS", True, TEXT_MID),
                (panel_x + 15, panel_y + 10))

    pygame.draw.line(screen, DIVIDER_COL,
                     (panel_x + 10, panel_y + 35),
                     (panel_x + panel_w - 10, panel_y + 35), 1)

    # ===== EMPTY STATE =====
    if not analysis_result:
        msg = f_text.render("Place pieces and press Analyse", True, TEXT_LIGHT)
        screen.blit(msg,
                    (panel_x + panel_w//2 - msg.get_width()//2,
                     panel_y + panel_h//2))
        return

    # ===== CARDS =====
    y = panel_y + 45

    for algo in ["greedy", "minimax", "alphabeta"]:
        data  = analysis_result[algo]
        theme = ALGO_COLORS[algo]

        move  = _fmt_move(data["move"])
        score = data["score"]
        nodes = data["nodes"]
        time  = round(data["time"], 4)

        # card
        card = _rounded_rect(panel_w-20, 80, (255,255,255,140), 10)
        screen.blit(card, (panel_x+10, y))

        pygame.draw.rect(screen, CARD_BORDER,
                         (panel_x+10, y, panel_w-20, 80),
                         1, border_radius=10)

        # header strip
        pygame.draw.rect(screen, theme["header"],
                         (panel_x+10, y, panel_w-20, 25),
                         border_top_left_radius=10,
                         border_top_right_radius=10)

        screen.blit(f_algo.render(algo.upper(), True, theme["accent"]),
                    (panel_x+20, y+5))

        screen.blit(f_text.render(theme["label"], True, theme["accent"]),
                    (panel_x+panel_w-80, y+5))

        # move
        screen.blit(f_move.render(move, True, theme["accent"]),
                    (panel_x+20, y+30))

        # stats
        stats = f"Score: {score}   Nodes: {nodes}   Time: {time}s"
        screen.blit(f_text.render(stats, True, TEXT_DARK),
                    (panel_x+20, y+55))

        y += 90

    # ===== COMPARISON BARS =====
    y += 5
    pygame.draw.line(screen, DIVIDER_COL,
                     (panel_x+10, y),
                     (panel_x+panel_w-10, y), 1)

    y += 10

    max_nodes = max(a["nodes"] for a in analysis_result.values())
    max_time  = max(a["time"] for a in analysis_result.values())

    for label, key, max_val in [
        ("Nodes", "nodes", max_nodes),
        ("Time", "time", max_time)
    ]:
        screen.blit(f_text.render(label, True, TEXT_LIGHT),
                    (panel_x+15, y))
        y += 15

        for algo in ["greedy","minimax","alphabeta"]:
            val   = analysis_result[algo][key]
            theme = ALGO_COLORS[algo]

            ratio = val / max_val if max_val else 0

            pygame.draw.rect(screen, BAR_TRACK,
                             (panel_x+80, y+5, 160, 6),
                             border_radius=3)

            pygame.draw.rect(screen, theme["bar"],
                             (panel_x+80, y+5, int((panel_w - 140) * ratio), 6),
                             border_radius=3)

            screen.blit(f_text.render(algo[:5], True, TEXT_MID),
                        (panel_x+15, y))

            val_text = f_text.render(str(val), True, TEXT_MID)
            screen.blit(val_text,
                        (panel_x + panel_w - val_text.get_width() - 10, y))
            
            y += 18

        y += 5