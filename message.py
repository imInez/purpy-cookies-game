from pygame import font as pyfont
class Message:

    def __init__(self, game, msg=None, below=0):
        """Initialize message attributes"""
        self.settings = game.settings
        self.screen=game.screen
        self.screen_rect = self.screen.get_rect()
        self.font = pyfont.SysFont(None, 38)
        self.below = below
        self.msg = msg

        # prep message
        self.prep(msg)

    def set_text(self, text):
        self.msg = text

    def put_below(self):
        if self.below> 0:
            self.msg_rect.y += self.below

    def prep(self, msg):
        """ Render message into an image and place it center it """
        self.msg_image = self.font.render(msg, True, (0, 0, 0), self.settings.bg_color, )
        self.msg_rect = self.msg_image.get_rect()
        self.msg_rect.centerx = self.screen_rect.centerx
        self.msg_rect.y = 70
        self.put_below()

    def blit(self):
        self.screen.blit(self.msg_image, self.msg_rect)


