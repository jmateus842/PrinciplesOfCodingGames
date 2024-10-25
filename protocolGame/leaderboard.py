import json
from datetime import datetime

class Leaderboard:
    def __init__(self, filename='leaderboard.json'):
        self.filename = filename
        self.scores = self.load_scores()

    def load_scores(self):
        try:
            with open(self.filename, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return []

    def save_scores(self):
        with open(self.filename, 'w') as file:
            json.dump(self.scores, file)

    def add_score(self, player_name, score):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_entry = {
            "player_name": player_name,
            "score": score,
            "timestamp": timestamp
        }
        self.scores.append(new_entry)
        self.scores.sort(key=lambda x: x['score'], reverse=True)
        self.scores = self.scores[:10]  # Keep only top 10 scores
        self.save_scores()

    def get_top_scores(self, n=10):
        return self.scores[:n]

    def display_leaderboard(self):
        print("=== LEADERBOARD ===")
        for i, entry in enumerate(self.scores, 1):
            print(f"{i}. {entry['player_name']} - {entry['score']} ({entry['timestamp']})")

if __name__ == "__main__":
    # Test the Leaderboard class
    leaderboard = Leaderboard()
    leaderboard.add_score("Player1", 100)
    leaderboard.add_score("Player2", 150)
    leaderboard.add_score("Player3", 75)
    leaderboard.display_leaderboard()