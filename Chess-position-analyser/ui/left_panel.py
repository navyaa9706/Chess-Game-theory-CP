import pygame

def draw_left_panel(screen, PIECE_IMAGES, turn, SQUARE_SIZE,
                   presets, selected_preset, dropdown_open):

    panel_x = 40
    panel_y = 80
    panel_w = 160
    panel_h = 8 * SQUARE_SIZE

    pygame.draw.rect(screen, (255,255,255),
                     (panel_x-10, panel_y-10, panel_w, panel_h),
                     border_radius=12)

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

        rows = (len(pieces) + 1) // 2
        return rects, start_y + rows * (size + gap)

    y = panel_y

    # ===== WHITE =====
    y = draw_section("WHITE", y)
    white_rects, y = draw_piece_grid(["wK","wQ","wR","wB","wN","wP"], y)

    y += 10

    # ===== BLACK =====
    y = draw_section("BLACK", y)
    black_rects, y = draw_piece_grid(["bK","bQ","bR","bB","bN","bP"], y)

    y += 15

    # ===== TURN =====
    y = draw_section("TURN", y)

    radius = 10

    white_center = (panel_x + 20, y + 12)
    black_center = (panel_x + 90, y + 12)

    pygame.draw.circle(screen, (120,100,110), white_center, radius, 2)
    pygame.draw.circle(screen, (120,100,110), black_center, radius, 2)

    if turn == "w":
        pygame.draw.circle(screen, (120,100,110), white_center, radius-4)
    else:
        pygame.draw.circle(screen, (120,100,110), black_center, radius-4)

    screen.blit(text_font.render("W", True, (0,0,0)),
                (white_center[0] + 12, white_center[1] - 8))
    screen.blit(text_font.render("B", True, (0,0,0)),
                (black_center[0] + 12, black_center[1] - 8))

    white_btn = pygame.Rect(white_center[0]-radius, white_center[1]-radius, radius*2, radius*2)
    black_btn = pygame.Rect(black_center[0]-radius, black_center[1]-radius, radius*2, radius*2)

    y += 30

    # ===== ANALYSE BUTTON =====
    analyse_btn = pygame.Rect(panel_x, y, 120, 45)

    pygame.draw.rect(screen, (180,150,170), analyse_btn, border_radius=10)
    pygame.draw.rect(screen, (120,100,110), analyse_btn, 2, border_radius=10)

    screen.blit(text_font.render("Analyse", True, (255,255,255)),
                (analyse_btn.x+28, analyse_btn.y+12))

    y += 60

    # ===== PRESET DROPDOWN =====
    y = draw_section("PRESET", y)

    box_w = 120
    box_h = 30

    dropdown_rect = pygame.Rect(panel_x, y, box_w, box_h)

    pygame.draw.rect(screen, (240,240,240), dropdown_rect, border_radius=8)
    pygame.draw.rect(screen, (120,100,110), dropdown_rect, 2, border_radius=8)

    label = selected_preset if selected_preset else "Select"
    screen.blit(text_font.render(label, True, (0,0,0)),
                (dropdown_rect.x + 10, dropdown_rect.y + 6))

    pygame.draw.polygon(screen, (0,0,0), [
        (dropdown_rect.right - 15, dropdown_rect.y + 10),
        (dropdown_rect.right - 5, dropdown_rect.y + 10),
        (dropdown_rect.right - 10, dropdown_rect.y + 18)
    ])

    option_rects = []

    if dropdown_open:
        for i, key in enumerate(presets.keys()):
            rect = pygame.Rect(panel_x,
                               y + (i + 1) * box_h,
                               box_w,
                               box_h)

            pygame.draw.rect(screen, (255,255,255), rect, border_radius=6)
            pygame.draw.rect(screen, (120,100,110), rect, 1, border_radius=6)

            screen.blit(text_font.render(key, True, (0,0,0)),
                        (rect.x + 10, rect.y + 6))

            option_rects.append((key, rect))

    y += box_h + 10

    # ===== FIXED MISSING VARIABLE =====
    palette = white_rects + black_rects

    return white_btn, black_btn, analyse_btn, palette, dropdown_rect, option_rects