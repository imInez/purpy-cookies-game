from pygame import font as pyfont, image as pyimage

class Button:

    def __init__(self, game):
        """Initialize the button attributes"""
        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()

        # Set button's properties
        self.image = pyimage.load('images/play_button.bmp')
        self.rect = self.image.get_rect()
        self.rect.center = self.screen_rect.center

    def blit(self):
        self.screen.blit(self.image, self.rect)