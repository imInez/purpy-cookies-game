class Statistics:
    """A class to hold game statistics"""

    def __init__(self, game):
        """Initialize stats"""
        self.settings = game.settings
        self.reset_stats()
        self.game_active = False
        self.drowning_exit = False
        self.replay_after_drop = False

        self.score = self.settings.score
        self.final_score = 0
        self.level = self.settings.level
        self.lifes_left = self.settings.lifes
        self.cookie_drop_speed = self.settings.cookie_drop_speed
        self.dropped_count = 0

    def start_game(self):
        self.replay_after_drop = False
        self.drowning_exit = False
        self.game_active = True

    def reset_stats(self):
        self.score = self.settings.score
        self.lifes_left = self.settings.lifes
        self.dropped_count = 0
        self.level = self.settings.level
        self.cookie_drop_speed = self.settings.cookie_drop_speed





