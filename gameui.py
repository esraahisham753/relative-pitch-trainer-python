import pygame
from main import Note, Interval, Question, Relative_Pitch_Trainer

class GameUI:
    def __init__(self):
        pygame.init()

        # Screen dimensions

        self.width = 1200
        self.hight = 700
        self.screen = pygame.display.set_mode((self.width, self.hight))
        pygame.display.set_caption("Es Relative Pitch Trainer")
        self.background = (255, 221, 171)
        self.color = (0, 0, 0)
        self.choices = (63, 125, 88)
        self.blue = (0, 100, 255)

        # fonts
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 36)

        # Game Data
        self.notes = Note.get_notes()
        self.intervals = Interval.get_intervals()
        self.game = Relative_Pitch_Trainer(10, 1, 'both', 0, self.intervals, self.notes)
        self.score = 0



    def draw_button(self, x, y, width, height, text, active=False):
        color = self.choices if active else self.blue
        pygame.draw.rect(self.screen, color, (x, y, width, height))
        text_surface = self.font_medium.render(text, True, self.choices)
        text_rect = text_surface.get_rect()
        text_rect.center = (x + width / 2, y + height / 2)
        self.screen.blit(text_surface, text_rect)
        return pygame.Rect(x, y, width, height)
    
    def draw_game_screen(self):
        self.screen.fill(self.background)

        # title
        title = self.font_large.render("Es Relative Pitch Trainer", True, self.color)
        self.screen.blit(title, (self.width / 2 - title.get_width() / 2, 50)) 

        # score
        score = self.font_medium.render(f"Score: {self.score}", True, self.color)
        self.screen.blit(score, (20, 20))

        

        return  []

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            self.screen.fill(self.background)
            self.draw_game_screen()
            pygame.display.flip()
        pygame.quit()

if __name__ == "__main__":
    game = GameUI()
    game.run()