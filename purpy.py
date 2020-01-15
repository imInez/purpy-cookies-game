from pygame import image as pyimage, time as pytime, transform as pytransform
from message import Message


class Purpy:
    """ a class to manage Purpy """
    def __init__(self, game):
        """ Initialize purpy and set it's position """
        self.name = 'Purpy'
        self.screen = game.screen
        self.screen_rect = game.screen.get_rect()
        self.settings = game.settings
        self.stats = game.stats
        self.game = game

        # Load Purpy's image and get it's rect
        self.load_images()
        self.image = self.standing_frames[0]
        self.rect = self.image.get_rect()
        self.rect.midbottom = self.screen_rect.midbottom

        # Set movement flags
        self.move_right = False
        self.move_left = False
        self.move_up = False
        self.move_down = False
        self.drown = False
        self.run = False
        self.acc = 1

        # set flags for animations
        self.walking = False
        self.jumping = False
        self.running = False
        self.eating = False
        self.current_frame = 0
        self.last_update = 0
        self.drowning_exit = False

        # prepare messages
        self.welcome_messages =[Message(self.game, "Hi, I'm Purpy"),
                                Message(self.game, "and I can't help but always eat all cookies in a pack..", 50),
                                Message(self.game, "want to help me catch them?", 100)]

        self.drowning_messages = [Message(self.game, f"ok. bye.", 300)]

        self.replaying_messages = [Message(self.game, "you know this isn't exactly helpful"),
                                   Message(self.game, "try again and try to use space :)", 200)]

    def load_images(self):
        """Load all images for purpy's behaviour """
        self.image_smile = pyimage.load('images/purpy/purpy.bmp')
        self.image_sad = pyimage.load('images/purpy/purpy_sad.bmp')
        self.image_eats = pyimage.load('images/purpy/purpy_eats.bmp')
        self.image_eats_ear = pyimage.load('images/purpy/purpy_eats_ear.bmp')
        self.image_ear = pyimage.load('images/purpy/purpy_left_ear.bmp')
        self.image_eyes1 = pyimage.load('images/purpy/purpy_close_eyes1.bmp')
        self.image_eyes2 = pyimage.load('images/purpy/purpy_close_eyes2.bmp')
        self.image_eyes3 = pyimage.load('images/purpy/purpy_close_eyes3.bmp')
        self.image_turn = pyimage.load('images/purpy/purpy_turn_left.bmp')
        self.image_walk = pyimage.load('images/purpy/purpy_walk_left.bmp')

        # frames for animations
        self.standing_frames = [self.image_smile, self.image_eyes1, self.image_eyes2, self.image_eyes3]
        self.ear_frames = [self.image_smile, self.image_ear, self.image_ear, self.image_smile,
                           self.image_ear, self.image_ear, self.image_smile]
        self.eating_frames = [self.image_smile, self.image_eats, self.image_eats, self.image_eats,
                              self.image_eats, self.image_eats_ear,  self.image_smile, self.image_ear]
        self.walk_frames_left = [self.image_turn, self.image_walk, self.image_walk, self.image_walk, self.image_walk,
                                 self.image_walk]
        self.walk_frames_right = [pytransform.flip(frame, True, False) for frame in self.walk_frames_left]

    def set_image(self, image):
        """Set image for purpy"""
        self.image = image

    def _animation(self, frames, now, delay = None):
        self.current_frame = (self.current_frame + 1) % len(frames)
        self.image = frames[self.current_frame]
        if delay:
            if self.current_frame == delay:
                pytime.delay(100)
        if self.current_frame == 0:
            self.last_update = now

    def animate(self):
        """Animate purpy's behaviour"""
        now = pytime.get_ticks()
        if self.eating:
            self.walking = False
            if now - self.last_update > 200:
                self._animation(self.eating_frames, now)
                if self.last_update == now:
                    self.eating = False
        if self.walking:
            self.eating = False
            if now - self.last_update > 200:
                if self.move_right:
                    self._animation(self.walk_frames_right, now)
                elif self.move_left:
                    self._animation(self.walk_frames_left, now)
        if self.running:
            if now - self.last_update > 100:
                if self.move_right:
                    self._animation(self.walk_frames_right, now)
                else:
                    self._animation(self.walk_frames_left, now)
        if not self.walking and not self.jumping and not self.running and not self.eating:
            self.set_image(self.image_smile)
            if now - self.last_update > 2000:
                self._animation(self.standing_frames, now)

    def update_face_drowns(self):
        if self.rect.bottom > self.screen_rect.bottom:
            self.set_image(self.image_sad)

    def drowning(self):
        self.stats.game_active = False
        self.stats.drowning_exit = True
        if self.rect.top > self.screen_rect.bottom:
            self.drown = True

    def coming_up(self):
        self.stats.drowning_exit = False
        if self.stats.score > 0:
            self.stats.game_active = True
        else:
            self.stats.game_active = False

    def reset_run(self):
        self.settings.purpy_velocity = 30

    def update_position(self, speed):
        """Update Purpy's position based on movement flag"""
        if self.move_right and self.rect.right < self.screen_rect.right:
            self.rect.x += speed
            self.walking = True
        if self.move_left and self.rect.left > self.screen_rect.left:
            self.rect.x -= speed
            self.walking = True
        if self.move_up and self.rect.bottom >  self.screen_rect.bottom:
            self.rect.y -= speed
            self.coming_up()
        if self.move_down:
            self.rect.y += speed/2
            self.drowning()
            # self.settings.cookie_drop_speed = 0
        if self.run:
            self.settings.purpy_velocity += 3

    def update(self):
        self.animate()
        self.update_position(self.settings.purpy_velocity)
        self.update_face_drowns()

    def blitme(self):
        """Draw Purpy at it's current location."""
        self.screen.blit(self.image, self.rect)