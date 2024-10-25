from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QLineEdit, QPushButton, QLabel
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from terminal_window import TerminalWindow

class MainWindow(QMainWindow):
    def __init__(self, game_logic):
        super().__init__()
        self.game_logic = game_logic
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Bash Terminal Simulator")
        self.setGeometry(100, 100, 800, 600)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout()
        central_widget.setLayout(main_layout)

        # Terminal window
        self.terminal = TerminalWindow(self.game_logic)
        main_layout.addWidget(self.terminal, 2)

        # Right panel layout
        right_panel_layout = QVBoxLayout()

        # Command reference panel
        command_panel = QTextEdit()
        command_panel.setReadOnly(True)
        command_panel.setFont(QFont("Courier New", 12))  # Increased font size
        command_panel.setText(self.get_command_reference())
        command_panel.setStyleSheet("background-color: #1a1a1a; color: #00ff00; border: 1px solid #00ffff;")
        right_panel_layout.addWidget(command_panel)

        # jdmgLinux label
        jdmg_label = QLabel("jdmgLinux")
        jdmg_label.setAlignment(Qt.AlignRight | Qt.AlignBottom)
        jdmg_label.setFont(QFont("Arial", 14, QFont.Bold, True))  # Bold and italic
        jdmg_label.setStyleSheet("color: white;")
        right_panel_layout.addWidget(jdmg_label)

        main_layout.addLayout(right_panel_layout, 1)

    def get_command_reference(self):
        return """THIS IS A GAME TO LEARN BASIC LINUX TERMINAL USAGE. BE WELCOME!\n
        Available Commands:

ls $SOME_DIRECTORY$
List directory contents

cd $SOME_DIRECTORY$
Change directory

cd /
Return to root directory

cd ..
Go back to previous directory

cat $SOME_FILE$
Display file contents

rm $SOME_FILE$
Remove a file

close game
Exit the game"""
