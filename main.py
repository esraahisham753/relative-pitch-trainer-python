import pygame
from music import Note, Interval, Relative_Pitch_Trainer

class GameUI:
    def __init__(self):
        pygame.init()

        # Screen dimensions
        self.width = 1200
        self.hight = 700
        
        try:
            self.background_image = pygame.image.load('background.jpg')
        except pygame.error:
            self.background_image = None
        
        self.overlay_color = (237, 242, 247, 200)
        self.screen = pygame.display.set_mode((self.width, self.hight), pygame.RESIZABLE)
        pygame.display.set_caption("Es Relative Pitch Trainer")
        info = pygame.display.Info()
        self.width = info.current_w
        self.hight = info.current_h
        self.background = (237, 242, 247, 255)
        self.color = (45, 55, 72)
        self.choices = (66, 153, 255, 255)
        self.blue = (49, 130, 206, 255)
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
        self.num_questions = 10
        self.active_choice = ''
        self.active_qustion = {}

        # UI state
        self.state = 'menu'
        self.play = False
        self.first_render = True
        self.cur_question = 1
        self.input_active = False
        self.input_text = '10'
        # UI components
        self.menu = {}
        self.choices_btns = []


    def draw_background(self):
        if self.background_image:
            scaled_bg = pygame.transform.scale(self.background_image, (self.width, self.hight))
            self.screen.blit(scaled_bg, (0, 0))
        else:
            self.screen.fill(self.background)
        
        # Create a semi-transparent overlay
        overlay = pygame.Surface((self.width, self.hight), pygame.SRCALPHA)
        overlay.fill(self.overlay_color)
        self.screen.blit(overlay, (0, 0))

    def draw_button(self, x, y, width, height, text, active=False, bg_color=(255, 255, 255, 0)):
        text_surface = self.font_medium.render(text, True, self.color)
        text_rect = text_surface.get_rect()
        btn_width = width
        text_rect.center = (btn_width / 2, height / 2)
        button_surface = pygame.Surface((btn_width, height), pygame.SRCALPHA)
        pygame.draw.rect(button_surface, bg_color, (0, 0, btn_width, height), border_radius=5)
        button_surface.blit(text_surface, text_rect)
        self.screen.blit(button_surface, (x, y))
        return pygame.Rect(x, y, btn_width, height)
    
    def draw_game_screen(self):
        self.draw_background()

        # title
        title = self.font_large.render("Es Relative Pitch Trainer", True, self.color)
        self.screen.blit(title, (self.width / 2 - title.get_width() / 2, 50)) 

        # score
        score = self.font_medium.render(f"Score: {self.score}", True, self.color)
        self.screen.blit(score, (20, 20))

        # render questions
        for i, choice in enumerate(self.active_question.choices):
            bg_color = self.blue if self.active_choice == choice else self.choices
            choice_btn = self.draw_button(self.width / 2 - 150, 200 + (i * 70), 300, 50, choice, self.active_choice == choice, bg_color)
            self.choices_btns.append(choice_btn)

        return  []
    
    def draw_menu_screen(self):
        self.draw_background()

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
        asc_btn = self.draw_button(self.width / 2 - 200, 300, 140, 50, 'Ascending', self.direction == 'asc', asc_bg)
        desc_bg = self.blue if self.direction == 'desc' else self.choices
        desc_btn = self.draw_button(self.width / 2 - 50, 300, 140, 50, 'Descending', self.direction == 'desc', desc_bg)
        both_bg = self.blue if self.direction == 'both' else self.choices
        both_btn = self.draw_button(self.width / 2 + 115, 300, 140, 50, 'Both', self.direction == 'both', both_bg)

        # num questions
        num_questions_text = self.font_medium.render("Number of Questions: ", True, self.color)
        self.screen.blit(num_questions_text, (self.width / 2 - num_questions_text.get_width() / 2, 400))
        input_box = pygame.Rect(self.width / 2 + 150, 390, 100, 50)
        input_color = self.blue if self.input_active else self.choices
        pygame.draw.rect(self.screen, input_color, input_box, border_radius=5)
        input_surface = self.font_medium.render(self.input_text, True, self.color)
        input_rect = input_surface.get_rect(center=input_box.center)
        self.screen.blit(input_surface, input_rect)
        self.menu['input_box'] = input_box

        # Start button
        start_btn = self.draw_button(self.width / 2 - 50, 500, 140, 50, 'Start', False, self.choices)

        # assign components to menu dict
        self.menu['level'] = (decrease, increase)
        self.menu['direction'] = (asc_btn, desc_btn, both_btn)
        self.menu['start'] = start_btn

    def draw_result_screen(self):
        self.draw_background()

        # title
        if self.cur_question < self.game.num_questions:
            text = 'Correct!' if self.active_question.check_answer(self.active_choice) else 'Incorrect!'
            title = self.font_large.render(text, True, self.color)
            current_interval = f"{self.active_question.interval.first_note.note} to {self.active_question.interval.second_note.note} is {self.active_question.interval.name}"
            current_interval_text = self.font_medium.render(current_interval, True, self.color)
            self.screen.blit(title, (self.width / 2 - title.get_width() / 2, 50))
            self.screen.blit(current_interval_text, (self.width / 2 - current_interval_text.get_width() / 2, 150))
            question_track = self.font_medium.render(f"Question {self.cur_question}/{self.game.num_questions}", True, self.color)
            self.screen.blit(question_track, (self.width / 2 - question_track.get_width() / 2, 250))
            next_btn = self.draw_button(self.width / 2 - 150, 300, 300, 50, 'Next', False, self.choices)
            self.menu['next'] = next_btn
        else:
            final_score = self.font_large.render(f"Final Score: {self.score}/{self.game.num_questions}", True, self.color)
            self.screen.blit(final_score, (self.width / 2 - final_score.get_width() / 2, 50))
            self.menu['play_again'] = self.draw_button(self.width / 2 - 150, 300, 300, 50, 'Play Again', False, self.choices)

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_f:
                        if self.screen.get_flags() & pygame.RESIZABLE:
                            self.screen = pygame.display.set_mode((1200, 700))
                            self.width = 1200
                            self.hight = 700
                        else:
                            info = pygame.display.Info()
                            self.width = info.current_w
                            self.hight = info.current_h - 40
                            self.screen = pygame.display.set_mode((self.width, self.hight), pygame.RESIZABLE)
                if event.type == pygame.VIDEORESIZE:
                    self.width, self.hight = event.w, event.h
                    self.screen = pygame.display.set_mode((self.width, self.hight), pygame.RESIZABLE)
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
                        elif self.menu['input_box'].collidepoint(mouse_pos):
                            self.input_active = True
                            self.input_text = ''
                        elif self.menu['start'].collidepoint(mouse_pos):
                            self.state = 'game'
                            self.game = Relative_Pitch_Trainer(self.num_questions, self.level, self.direction, 0, self.intervals, self.notes)
                            self.active_question = self.game.generate_question()
                            self.play = True
                    elif self.state == 'game':
                        for i, choice in enumerate(self.choices_btns):
                            if choice.collidepoint(mouse_pos):
                                self.active_choice = self.active_question.choices[i]
                                if self.active_question.check_answer(self.active_question.choices[i]):
                                    self.score += 1
                                self.state = 'result'
                                break
                    elif self.state == 'result':
                        if self.cur_question < self.game.num_questions:
                            if self.menu['next'].collidepoint(mouse_pos):
                                self.active_question = self.game.generate_question()
                                self.cur_question += 1
                                self.active_choice = ''
                                self.state = 'game'
                                self.first_render = True
                                self.play = True
                                self.choices_btns = []
                        else:
                            if self.menu['play_again'].collidepoint(mouse_pos):
                                self.state = 'menu'
                                self.score = 0
                                self.cur_question = 1
                                self.active_choice = ''
                                self.choices_btns = []
                                self.game = None
                                self.active_question = {}
                                self.play = False
                                self.first_render = True
                                self.menu = {}
                
                if event.type == pygame.KEYDOWN and self.input_active:
                    if event.key == pygame.K_RETURN:
                        self.input_active = False
                    elif event.key == pygame.K_BACKSPACE:
                        self.input_text = self.input_text[:-1]
                    else:
                        if event.unicode.isnumeric() and len(self.input_text) < 4:
                            self.input_text += event.unicode
                    
                    try:
                        num = int(self.input_text)
                        self.num_questions = max(1, min(num, 100))
                        self.input_text = str(self.num_questions)
                    except ValueError:
                        self.input_text = '10'
                        self.num_questions = 10

            if self.state == 'menu':
                self.draw_menu_screen()
            elif self.state == 'result':
                self.draw_result_screen()
            else:
                self.draw_game_screen()
                if self.play and not self.first_render:
                    self.active_question.play_interval()
                    self.play = False
                self.first_render = False

            pygame.display.flip()
        pygame.quit()

if __name__ == "__main__":
    game = GameUI()
    game.run()