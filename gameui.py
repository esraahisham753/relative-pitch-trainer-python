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
        self.background = (255, 221, 171, 255)
        self.color = (0, 0, 0)
        self.choices = (63, 125, 88, 255)
        self.blue = (0, 100, 255, 255)
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
        self.game = None
        self.active_choice = ''

        # UI state
        self.state = 'menu'

        # UI components
        self.menu = {}



    def draw_button(self, x, y, width, height, text, active=False, bg_color=(255, 255, 255, 0)):
        text_surface = self.font_medium.render(text, True, self.color)
        text_rect = text_surface.get_rect()
        btn_width = text_surface.get_width() + width
        text_rect.center = (btn_width / 2, height / 2)
        button_surface = pygame.Surface((btn_width, height), pygame.SRCALPHA)
        pygame.draw.rect(button_surface, bg_color, (0, 0, btn_width, height))
        button_surface.blit(text_surface, text_rect)
        self.screen.blit(button_surface, (x, y))
        return pygame.Rect(x, y, btn_width, height)
    
    def draw_game_screen(self):
        self.screen.fill(self.background)

        # title
        title = self.font_large.render("Es Relative Pitch Trainer", True, self.color)
        self.screen.blit(title, (self.width / 2 - title.get_width() / 2, 50)) 

        # score
        score = self.font_medium.render(f"Score: {self.score}", True, self.color)
        self.screen.blit(score, (20, 20))

        # render questions
        question = self.game.generate_question()
        for i, choice in enumerate(question.choices):
            self.draw_button(50 + (i * 250), 200, 50, 30, choice, self.active_choice == choice, self.choices)

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
        self.screen.blit(selected_level, (self.width / 2 - level_text.get_width() / 2 + 100, 150))

        # Level controls
        decrease = self.draw_button(self.width / 2 - 150, 135, 20, 50, '<', self.level > 1, self.transparent)
        increase = self.draw_button(self.width / 2 + 100, 135, 20, 50, '>', self.level < 5, self.transparent)

        # Direction
        asc_bg = self.blue if self.direction == 'asc' else self.choices
        asc_btn = self.draw_button(self.width / 2 - 200, 300, 20, 50, 'Ascending', self.direction == 'asc', asc_bg)
        desc_bg = self.blue if self.direction == 'desc' else self.choices
        desc_btn = self.draw_button(self.width / 2 - 50, 300, 20, 50, 'Descending', self.direction == 'desc', desc_bg)
        both_bg = self.blue if self.direction == 'both' else self.choices
        both_btn = self.draw_button(self.width / 2 + 115, 300, 20, 50, 'Both', self.direction == 'both', both_bg)

        # Start button
        start_btn = self.draw_button(self.width / 2 - 50, 400, 20, 50, 'Start', False, self.choices)

        # assign components to menu dict
        self.menu['level'] = (decrease, increase)
        self.menu['direction'] = (asc_btn, desc_btn, both_btn)
        self.menu['start'] = start_btn


    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if self.state == 'menu':
                        if self.menu['level'][0].collidepoint(mouse_pos):
                            self.level = max(1, self.level - 1)
                        elif self.menu['level'][1].collidepoint(mouse_pos):
                            self.level = min(5, self.level + 1)
                        elif self.menu['direction'][0].collidepoint(mouse_pos):
                            self.direction = 'asc'
                        elif self.menu['direction'][1].collidepoint(mouse_pos):
                            self.direction = 'desc'
                        elif self.menu['direction'][2].collidepoint(mouse_pos):
                            self.direction = 'both'
                        elif self.menu['start'].collidepoint(mouse_pos):
                            self.state = 'game'
                            self.game = Relative_Pitch_Trainer(10, self.level, self.direction, 0, self.intervals, self.notes)

                
            if self.state == 'menu':
                self.draw_menu_screen()
            else:
                self.draw_game_screen()

            pygame.display.flip()
        pygame.quit()

if __name__ == "__main__":
    game = GameUI()
    game.run()