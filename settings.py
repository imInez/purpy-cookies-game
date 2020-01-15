import random
class Settings:
    " A class to store settings for game "

    def __init__(self):

        # screen settings
        self.screen_width = 1280
        self.screen_height = 800
        self.bg_color = (255,255,255)
        self.FPS = 30

        # starting values
        self.lifes = 3
        self.level = 0
        self.score = 0
        self.purpy_velocity = 30
        self.cookie_rows = 10
        self.cookie_drop_speed = 15
        self.dropped_cookies_limit = 3

    @staticmethod
    def get_random_speed(a,b):
        return random.uniform(a,b)

