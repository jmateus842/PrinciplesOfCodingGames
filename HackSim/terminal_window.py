from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QLineEdit, QHBoxLayout, QLabel, QMessageBox
from PyQt5.QtGui import QFont, QTextCursor
from PyQt5.QtCore import Qt

class TerminalWindow(QWidget):
    def __init__(self, game_logic):
        super().__init__()
        self.game_logic = game_logic
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Output display
        self.output_display = QTextEdit()
        self.output_display.setReadOnly(True)
        self.output_display.setFont(QFont("Courier New", 10))
        layout.addWidget(self.output_display)

        # Input layout
        input_layout = QHBoxLayout()
        
        # Prompt label
        self.prompt_label = QLabel(">")
        self.prompt_label.setStyleSheet("color: #00ffff; font-weight: bold;")
        input_layout.addWidget(self.prompt_label)

        # Input line
        self.input_line = QLineEdit()
        self.input_line.setFont(QFont("Courier New", 10))
        self.input_line.returnPressed.connect(self.process_command)
        input_layout.addWidget(self.input_line)

        layout.addLayout(input_layout)

        self.display_prompt()

    def display_prompt(self):
        prompt = f"{self.game_logic.get_current_path()}$ "
        self.output_display.append(prompt)
        self.output_display.moveCursor(QTextCursor.End)

    def process_command(self):
        command = self.input_line.text()
        self.input_line.clear()

        # Display the command
        self.output_display.insertPlainText(command + '\n')

        # Check for 'close game' command
        if command.strip().lower() == 'close game':
            reply = QMessageBox.question(self, 'Exit Game', 
                                         "Are you sure you want to exit the game?",
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.game_logic.execute_command(command)
            else:
                self.display_prompt()
            return

        # Execute the command
        result = self.game_logic.execute_command(command)

        # Display the result
        if result:
            self.output_display.append(result)

        # Check if the game is won
        if self.game_logic.is_game_won() and result != self.game_logic.get_win_reason():
            self.output_display.append(self.game_logic.get_win_reason())
        
        self.display_prompt()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Tab:
            # Implement tab completion here
            pass
        else:
            super().keyPressEvent(event)

    def get_command_reference(self):
        return """ THIS IS A GAME TO LEARN BASIC LINUX TERMINAL USAGE. BE WELCOME!\n
        Available Commands:
ls $SOME_DIRECTORY$ - List directory contents
cd $SOME_DIRECTORY$ - Change directory
cd / - Return to root directory
cd .. - Go back to previous directory
pwd $SOME_DIRECTORY$ - Print working directory
cat $SOME_FILE$ - Display file contents
rm $SOME_FILE$ - Remove a file
echo $SOME_TEXT$ - Display a line of text
close game - Exit the game"""
