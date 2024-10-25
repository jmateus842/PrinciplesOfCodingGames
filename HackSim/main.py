# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QFile, QTextStream
from gui_layout import MainWindow
from game_logic import GameLogic
from filesystem_simulation import FileSystemSimulation

def load_stylesheet(app):
    file = QFile("style.qss")
    file.open(QFile.ReadOnly | QFile.Text)
    stream = QTextStream(file)
    app.setStyleSheet(stream.readAll())

def main():
    app = QApplication(sys.argv)
    
    # Apply stylesheet
    load_stylesheet(app)
    
    # Initialize the file system simulation
    file_system = FileSystemSimulation()
    
    # Initialize the game logic
    game_logic = GameLogic(file_system)
    
    # Create and show the main window
    main_window = MainWindow(game_logic)
    main_window.show()
    
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
