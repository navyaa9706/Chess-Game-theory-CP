import pygame

def draw_left_panel(screen, PIECE_IMAGES, turn, SQUARE_SIZE):

    panel_x = 40
    panel_y = 80
    panel_w = 160
    panel_h = 8 * SQUARE_SIZE   # increased so nothing gets cut

    # ===== BACKGROUND =====
    pygame.draw.rect(screen, (255,255,255), (panel_x-10, panel_y-10, panel_w, panel_h), border_radius=12)

    font = pygame.font.SysFont("Arial", 14, bold=True)
    text_font = pygame.font.SysFont("Arial", 14)

    def draw_section(title, y):
        txt = font.render(title, True, (90,50,60))
        screen.blit(txt, (panel_x, y))
        return y + 25

    def draw_piece_grid(pieces, start_y):
        rects = []
        size = 42
        gap = 10

        for i, p in enumerate(pieces):
            x = panel_x + (i % 2) * (size + gap)
            y = start_y + (i // 2) * (size + gap)

            rect = pygame.Rect(x, y, size, size)
            pygame.draw.rect(screen, (245,235,240), rect, border_radius=8)

            img = pygame.transform.smoothscale(PIECE_IMAGES[p], (size-8, size-8))
            screen.blit(img, (x+4, y+4))

            rects.append((p, rect))

        # ✅ CORRECT ROW CALCULATION
        rows = (len(pieces) + 1) // 2
        new_y = start_y + rows * (size + gap)

        return rects, new_y

    y = panel_y

    # ===== WHITE =====
    y = draw_section("WHITE", y)
    white_rects, y = draw_piece_grid(["wK","wQ","wR","wB","wN","wP"], y)

    y += 10

    # ===== BLACK =====
    y = draw_section("BLACK", y)
    black_rects, y = draw_piece_grid(["bK","bQ","bR","bB","bN","bP"], y)

    y += 15   # tighter spacing (no ugly gap)

    # ===== TURN =====
    y = draw_section("TURN", y)

    white_btn = pygame.Rect(panel_x, y, 120, 40)
    black_btn = pygame.Rect(panel_x, y+50, 120, 40)

    w_color = (220,220,255) if turn == "w" else (240,240,240)
    b_color = (220,220,255) if turn == "b" else (240,240,240)

    pygame.draw.rect(screen, w_color, white_btn, border_radius=10)
    pygame.draw.rect(screen, b_color, black_btn, border_radius=10)

    pygame.draw.rect(screen, (120,100,110), white_btn, 2, border_radius=10)
    pygame.draw.rect(screen, (120,100,110), black_btn, 2, border_radius=10)

    screen.blit(text_font.render("White", True, (0,0,0)), (white_btn.x+35, white_btn.y+10))
    screen.blit(text_font.render("Black", True, (0,0,0)), (black_btn.x+35, black_btn.y+10))

    y += 105

    # ===== ANALYSE BUTTON =====
    analyse_btn = pygame.Rect(panel_x, y, 120, 45)

    pygame.draw.rect(screen, (180,150,170), analyse_btn, border_radius=10)
    pygame.draw.rect(screen, (120,100,110), analyse_btn, 2, border_radius=10)

    screen.blit(text_font.render("Analyse", True, (255,255,255)),
                (analyse_btn.x+28, analyse_btn.y+12))

    palette = white_rects + black_rects

    return white_btn, black_btn, analyse_btn, palette