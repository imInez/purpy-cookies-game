from pygame import image as pyimage
from pygame.sprite import Sprite

class Cookie(Sprite):
    """A class to handle single cookie from a cookie bag"""
    def __init__(self, game):
        """ Initalize cookie and set it's position """
        super().__init__()

        self.game = game
        self.settings = game.settings

        self.screen = game.screen
        self.screen_rect = game.screen.get_rect()

        # Load the image for a cookie
        self.image = pyimage.load('images/cookie1.bmp')
        self.rect = self.image.get_rect()

        # Set starting position and speed
        self.rect.x = 0
        self.rect.y = 0
        self.cookie_velocity = 0





