import pygame

class EvalBar:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.score = 0

    def update(self, score):
        self.score = score

    def draw(self, screen):
        max_eval = 10
        score = max(-max_eval, min(max_eval, self.score))

        # Convert to ratio
        ratio = (score + max_eval) / (2 * max_eval)

        white_height = int(self.rect.height * ratio)
        black_height = self.rect.height - white_height

        # --- Black (top) ---
        pygame.draw.rect(
            screen,
            (60, 60, 60),
            (self.rect.x, self.rect.y, self.rect.width, black_height)
        )

        # --- White (bottom) ---
        pygame.draw.rect(
            screen,
            (240, 240, 240),
            (
                self.rect.x,
                self.rect.y + black_height,
                self.rect.width,
                white_height
            )
        )

        # Border
        pygame.draw.rect(screen, (0, 0, 0), self.rect, 2)

        # Score text
        font = pygame.font.SysFont(None, 22)
        display_score = round(score, 2)

        text_color = (255, 255, 255) if score < 0 else (0, 0, 0)
        text = font.render(str(display_score), True, text_color)

        text_rect = text.get_rect(center=self.rect.center)
        screen.blit(text, text_rect)
