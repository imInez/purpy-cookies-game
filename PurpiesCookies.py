import sys
import random
import pygame
from settings import Settings
from statistics import Statistics
from scoreboard import Scoreboard
from purpy import Purpy
from cookie import Cookie
from button import Button
from message import Message


class PurpyCookies:
    """ Core class to manage game assets and behaviour """

    def __init__(self):
        """ Initiate the game and game resources """
        pygame.init()
        self.FPS_CLOCK = pygame.time.Clock()
        self.settings = Settings()
        self.stats = Statistics(self)
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        self.screen.fill(self.settings.bg_color)
        pygame.display.set_caption("Purpie's cookies!")
        self.scoreboard = Scoreboard(self)

        self.last_message = -1
        self.cookies_count = 0

        self.purpy = Purpy(self)
        self.cookies = pygame.sprite.Group()
        self.play_button = Button(self)
        self._create_cookies()

    def _check_play_button(self, mouse_pos):
        """ Check if mouse clicked on button and (re)start a game if so"""
        if self.play_button.rect.collidepoint(mouse_pos):
            self.stats.reset_stats()
            self.cookies.empty()
            self.scoreboard.prep_live_cookies()
            self.scoreboard.prep_score()
            self.scoreboard.prep_level()
            self.stats.start_game()

    def _create_single_cookie(self, cookies_per_row, row_number):
        """ Create a single cookie """
        cookie = Cookie(self)
        # place cookie in random place in a row
        cookie.rect.x = self.purpy.rect.width + cookie.rect.width * random.randint(0,cookies_per_row)
        cookie.rect.y = 4*cookie.rect.height * (-1*row_number)
        self.cookies.add(cookie)

    def _create_cookies(self):
        """ Create a pack of cookies """
        cookie = Cookie(self)
        # Check how many cookies could fit in a row and column
        cookies_per_row = (self.settings.screen_width - 2*self.purpy.rect.width) // cookie.rect.width
        cookies_per_column = self.settings.screen_height // cookie.rect.height
        # Create cookies rows
        for row in range(cookies_per_column):
            self._create_single_cookie(cookies_per_row, row)
        self.cookies_count = len(self.cookies.sprites())

    def _recreate_cookies(self):
        """ Recreate cookies bag when all previous are eaten/missed """
        if len(self.cookies.sprites()) <= self.cookies_count//2:
            self._create_cookies()
            self.stats.level += 1
            self.scoreboard.prep_level()
            self.stats.cookie_drop_speed += 0.5

    def _drop_cookies_row(self):
        for cookie in self.cookies.sprites():
            cookie.rect.y += self.stats.cookie_drop_speed

    def _dropped_cookie(self):
        """ Handle a cookie when it's dropped out of screen """
        for cookie in self.cookies.sprites():
            if cookie.rect.top > self.screen.get_rect().bottom:
                self.cookies_count -= 1
                self.stats.dropped_count += 1
                cookie.kill()
                self.stats.lifes_left -= 1
                self.scoreboard.prep_live_cookies()
            if self.stats.dropped_count > 3:
                self.stats.replay_after_drop = True
                self.final_score = self.stats.score
                self.stats.game_active = False

    def _eaten_cookie(self):
        """ Handle cookie and purpy collision - when purpy eats a cookie """
        if pygame.sprite.spritecollide(self.purpy, self.cookies, dokill=False,
                                       collided=pygame.sprite.collide_circle_ratio(0.5)):
            self.purpy.eating = True
            self.purpy.reset_run()
            self.cookies_count -= 1
            pygame.sprite.spritecollide(self.purpy, self.cookies, dokill=True)
            self.stats.score += 1
            self.scoreboard.prep_score()
            self.scoreboard.prep_level()

    def _update_cookies(self):
        """Update each cookie in cookies group"""
        if self.stats.game_active:
            self._recreate_cookies()
            self._drop_cookies_row()
            self._eaten_cookie()
            self._dropped_cookie()


    def _react_keyboard_keys(self, event_key, is_pressed):
        """React to certain key event """
        keys = {'right': pygame.K_RIGHT, 'left': pygame.K_LEFT, 'up': pygame.K_UP, 'down': pygame.K_DOWN,
                'run':pygame.K_SPACE, 'quit': pygame.K_q}

        if event_key == keys['right']:
            self.purpy.walking = is_pressed
            self.purpy.move_right = is_pressed
        elif event_key == keys['left']:
            self.purpy.walking = is_pressed
            self.purpy.move_left = is_pressed
        if event_key == keys['up']:
            self.purpy.move_up = is_pressed
        if event_key == keys['down']:
            self.purpy.move_down = is_pressed
        if event_key == keys['run']:
            self.purpy.running = is_pressed
            self.purpy.run = is_pressed
        if event_key == keys['quit']:
            sys.exit()

    def _check_events(self):
        """ Watch mouse and keyboard events """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYUP:
                self._react_keyboard_keys(event.key, False)
            elif event.type == pygame.KEYDOWN:
                self._react_keyboard_keys(event.key, True)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _quit_when_drown(self):
        """ Quit game when purpy goes down lower than the screen """
        if self.purpy.drown is True:
            sys.exit()

    def _update_screen(self):
        """ Update images on the screen, and flip to the new screen. """
        self.purpy.blitme()
        if self.stats.drowning_exit:
            for msg in self.purpy.drowning_messages:
                msg.blit()
        elif self.stats.game_active:
            self.cookies.draw(self.screen)
            self.scoreboard.draw_score()
        elif not self.stats.game_active:
            if self.stats.replay_after_drop == True:
                for msg in self.purpy.replaying_messages:
                    msg.blit()
                    score_value = Message(self, f"we only had {str(self.stats.score)} cookies ",50)
                    score_value.blit()
            else:
                for msg in self.purpy.welcome_messages:
                    msg.blit()
            self.play_button.blit()
        pygame.display.flip()

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self.screen.fill(self.settings.bg_color)
            self._update_cookies()
            self.purpy.update()
            self._quit_when_drown()
            self._check_events()
            self._update_screen()
            self.FPS_CLOCK.tick(self.settings.FPS)

if __name__ == '__main__':
    """ Make game instance and run the game """
    game = PurpyCookies()
    game.run_game()
