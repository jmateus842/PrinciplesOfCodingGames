import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFontDatabase, QFont
from gui import GameWindow
from game_logic import GameLogic
from leaderboard import Leaderboard

def main():
    app = QApplication(sys.argv)
    
    # Set cyberpunk font
    font_id = QFontDatabase.addApplicationFont("path/to/cyberpunk_font.ttf")
    if font_id != -1:
        font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        cyberpunk_font = QFont(font_family)
        app.setFont(cyberpunk_font)

    game_logic = GameLogic()
    leaderboard = Leaderboard()
    window = GameWindow(game_logic, leaderboard)
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()