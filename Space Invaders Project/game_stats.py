import json

class GameStats:
    """Track statistics for Alien Invasion."""

    def __init__(self, ai_game):
        """Initialize statistics."""
        self.settings = ai_game.settings
        self.reset_stats()

        # High score should never be reset.
        self.high_score = self.load_high_scores()

    def reset_stats(self):
        """Initialize statistics that can change during the game."""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1
        
    def load_high_scores(self):
        """Load high scores from a file."""
        try:
            with open('high_scores.json', 'r') as f:
                return json.load(f)  
        except (FileNotFoundError, json.JSONDecodeError):
            return 0  

    def save_high_score(self):
        """Save the high scores to a file."""
        with open('high_scores.json', 'w') as f:
            json.dump(self.high_score, f)  