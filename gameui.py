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
        self.transparent = (0, 0, 0, 0)

        # fonts
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 36)

        # Game Data
        self.notes = Note.get_notes()
        self.intervals = Interval.get_intervals()
        self.level = 1
        self.direction = 'asc'
        self.score = 0

        # UI state
        self.state = 'menu'



    def draw_button(self, x, y, width, height, text, active=False, bg_color=(255, 255, 255)):
        pygame.draw.rect(self.screen, bg_color, (x, y, width, height))
        text_surface = self.font_medium.render(text, True, self.color)
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
    
    def draw_menu_screen(self):
        self.screen.fill(self.background)

        #title
        title = self.font_large.render("Es Relative Pitch Trainer Setup", True, self.color)
        self.screen.blit(title, (self.width / 2 - title.get_width() / 2, 50))

        # Selected level 
        level_text = self.font_medium.render("Select Level (1-5): ", True, self.color)
        self.screen.blit(level_text, (self.width / 2 - level_text.get_width() / 2, 100))
        selected_level = self.font_medium.render(f"{self.level}", True, self.color)
        self.screen.blit(selected_level, (self.width / 2 - level_text.get_width() / 2 + 75, 150))

        # Level controls
        decrease = self.draw_button(self.width / 2 - 150, 130, 50, 50, '<', self.level > 1, self.transparent)
        increase = self.draw_button(self.width / 2 + 100, 130, 50, 50, '>', self.level < 5, self.transparent)

        # Direction
        asc_btn = self.draw_button(self.width / 2 - 200, 400, 100, 50, 'Ascending', self.direction == 'asc', self.choices)
        desc_btn = self.draw_button(self.width / 2 - 50, 400, 100, 50, 'Descending', self.direction == 'desc', self.choices)
        both_btn = self.draw_button(self.width / 2 + 100, 400, 100, 50, 'Both', self.direction == 'both', self.choices)

        # Start button
        start_btn = self.draw_button(self.width / 2 - 100, 500, 200, 50, 'Start', self.choices)

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
            if self.state == 'menu':
                self.draw_menu_screen()
            else:
                self.draw_game_screen()

            pygame.display.flip()
        pygame.quit()

if __name__ == "__main__":
    game = GameUI()
    game.run()