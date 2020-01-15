from pygame import font as pyfont
from cookie import Cookie
from pygame.sprite import Group

class Scoreboard:
    """A class to keep and display score for a game"""

    def __init__(self, game):
        """ Initiate te score and it's rect"""
        self.game = game
        self.settings = game.settings
        self.stats = game.stats

        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()

        # text (font) settings
        self.text_color = (0, 0, 0)
        self.font = pyfont.SysFont(None, 30)

        self.prep_score()
        self.prep_level()
        self.prep_live_cookies()

    def prep_score(self):
        """ Render score text into image"""
        score_text = 'cookies: ' + str(self.stats.score)
        self.score_image = self.font.render(score_text, True, self.text_color, self.settings.bg_color)

        # display
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 30
        self.score_rect.top = 50

    def prep_level(self):
        """Render level tect into image"""
        level_text = 'cookies pack: ' + str(self.stats.level)
        self.level_image = self.font.render(level_text, True, self.text_color, self.settings.bg_color)

        #display
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.screen_rect.right - 30
        self.level_rect.top = 100

    def prep_live_cookies(self):
        """Show how many cookies were dropped"""
        self.cookies_live = Group()
        for live in range(self.stats.lifes_left):
            cookie = Cookie(self.game)
            cookie.rect.y = 10
            cookie.rect.x = 10 + live * cookie.rect.width

            self.cookies_live.add(cookie)

    def draw_score(self):
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.cookies_live.draw(self.screen)

