import random
import time

class GameLogic:
    def __init__(self):
        self.score = 0
        self.blacklist = set()
        self.generate_blacklist()
        self.start_time = time.time()
        self.game_duration = 90  # 1.5 minutes in seconds

    def generate_blacklist(self):
        for _ in range(10):  # Increase to 10 blacklisted IPs
            ip = f"{random.randint(1, 255)}.{random.randint(0, 255)}." \
                 f"{random.randint(0, 255)}.{random.randint(0, 255)}"
            self.blacklist.add(ip)

    def check_packet(self, packet, action):
        if packet.is_blacklisted:
            if action == "block":
                self.score += 20
                return True, "Correct! Malicious IP blocked."
            else:
                self.score -= 20
                return False, "Wrong! You allowed a malicious IP."
        elif action == packet.protocol.lower():
            self.score += 10
            return True, f"Correct! {packet.protocol} packet identified."
        elif action == "block":
            self.score -= 10
            return False, f"Wrong! You blocked a legitimate {packet.protocol} packet."
        else:
            self.score -= 5
            return False, f"Wrong! This was a {packet.protocol} packet."

    def deduct_points_for_missed_blacklist(self):
        self.score -= 10

    def get_score(self):
        return self.score

    def get_blacklist(self):
        return list(self.blacklist)

    def is_game_over(self):
        return time.time() - self.start_time >= self.game_duration

    def get_remaining_time(self):
        elapsed_time = time.time() - self.start_time
        remaining_time = max(0, self.game_duration - elapsed_time)
        return int(remaining_time)
