import json
import sys

class GameLogic:
    def __init__(self, file_system):
        self.file_system = file_system
        self.current_directory = self.file_system.root
        self.command_history = []
        self.target_file = self.file_system.config['game']['target_file']
        self.target_content = "You're about to be hacked. I AM MALWARE.\nYou won't be able to delete me."
        self.game_won = False
        self.win_reason = ""

    def execute_command(self, command):
        parts = command.split()
        cmd = parts[0]
        args = parts[1:]

        if cmd == 'close' and len(args) > 0 and args[0] == 'game':
            sys.exit()

        result = self.file_system.execute_command(cmd, args)
        self.command_history.append(command)

        # Verificar si el juego se gana cuando se usa el comando 'cat' en el archivo objetivo
        if cmd == 'cat' and args and args[0] == self.target_file:
            self.game_won = self.check_win_condition(result)
            if self.game_won:
                self.win_reason = "You've found the malware file!"

        # Verificar si el juego se gana cuando se usa el comando 'rm' en el archivo objetivo
        if cmd == 'rm' and args and args[0] == self.target_file:
            self.game_won = True
            self.win_reason = "You can now close the game using the terminal!"
            return self.win_reason

        return result

    def get_current_path(self):
        return self.file_system._pwd()

    def check_win_condition(self, file_content):
        return self.target_content in file_content

    def is_game_won(self):
        return self.game_won

    def get_win_reason(self):
        return self.win_reason
