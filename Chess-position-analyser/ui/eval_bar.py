import pygame


class EvalBar:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.score = 0

        self.font = pygame.font.SysFont("Arial", 16, bold=True)

    def update(self, score):
        self.score = score

    def draw(self, screen):
        max_eval = 10   # clamp range
        score = max(-max_eval, min(max_eval, self.score))

        # convert score → ratio (0 to 1)
        ratio = (score + max_eval) / (2 * max_eval)

        white_height = int(self.rect.height * ratio)
        black_height = self.rect.height - white_height

        # ===== DRAW BLACK (TOP) =====
        pygame.draw.rect(
            screen,
            (50, 50, 50),
            (self.rect.x, self.rect.y, self.rect.width, black_height),
            border_radius=6
        )

        # ===== DRAW WHITE (BOTTOM) =====
        pygame.draw.rect(
            screen,
            (245, 245, 245),
            (
                self.rect.x,
                self.rect.y + black_height,
                self.rect.width,
                white_height
            ),
            border_radius=6
        )

        # ===== BORDER =====
        pygame.draw.rect(screen, (120, 90, 100), self.rect, 2, border_radius=6)

        # ===== SCORE TEXT =====
        display_score = round(score, 2)

        # text color depends on dominance
        if score > 0:
            text_color = (0, 0, 0)      # white side → black text
        else:
            text_color = (255, 255, 255)  # black side → white text

        text = self.font.render(str(display_score), True, text_color)

        text_rect = text.get_rect(center=self.rect.center)
        screen.blit(text, text_rect)