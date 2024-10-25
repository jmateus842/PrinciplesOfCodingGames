from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QListWidget, QGraphicsView, QGraphicsScene, QGraphicsObject, QGraphicsRectItem, QGraphicsTextItem, QProgressBar, QGraphicsProxyWidget, QMessageBox, QInputDialog
from PyQt5.QtCore import QTimer, Qt, QPropertyAnimation, QEasingCurve, QRectF, QPointF
from PyQt5.QtGui import QColor, QLinearGradient, QPainter, QFont, QBrush, QPen
from packet import Packet
from leaderboard import Leaderboard
import random

class CyberpunkButton(QPushButton):
    def __init__(self, text):
        super().__init__(text)
        self.setStyleSheet("""
            QPushButton {
                background-color: #0f1923;
                color: #00ff00;
                border: 2px solid #00ff00;
                border-radius: 5px;
                padding: 5px;
                font-family: 'Courier New', monospace;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #00ff00;
                color: #0f1923;
            }
        """)

class PacketGraphicsItem(QGraphicsObject):
    def __init__(self, packet, width, height):
        super().__init__()
        self.packet = packet
        self.width = width
        self.height = height
        self.rect_item = QGraphicsRectItem(0, 0, width, height, self)
        
        # Use grey for blacklisted IPs and some non-blacklisted IPs
        if packet.is_blacklisted or random.random() < 0.3:  # 30% chance for non-blacklisted to be grey
            color = QColor(150, 150, 150)
        else:
            color = QColor(100, 150, 100)  # Green for safe packets
        
        self.rect_item.setBrush(QBrush(color.lighter(150)))
        self.rect_item.setPen(QPen(color.darker(150), 2))

        text = f"IP: {packet.ip_address}\n{packet.description}"
        text_item = QGraphicsTextItem(text, self)
        text_item.setDefaultTextColor(QColor(0, 0, 0))
        text_item.setPos(5, 5)

        self.timer_bar = QProgressBar()
        self.timer_bar.setRange(0, 30)
        self.timer_bar.setValue(30)
        self.timer_bar.setStyleSheet("""
            QProgressBar {
                background-color: #1a1a1a;
                border: 1px solid #00ff00;
                border-radius: 5px;
            }
            QProgressBar::chunk {
                background-color: #00ff00;
            }
        """)
        timer_proxy = QGraphicsProxyWidget(self)
        timer_proxy.setWidget(self.timer_bar)
        timer_proxy.setPos(5, height - 25)
        timer_proxy.setMinimumWidth(width - 10)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)
        self.timer.start(1000)  # Update every second

    def boundingRect(self):
        return QRectF(0, 0, self.width, self.height)

    def paint(self, painter, option, widget=None):
        pass

    def update_timer(self):
        current_value = self.timer_bar.value()
        if current_value > 0:
            self.timer_bar.setValue(current_value - 1)
        else:
            self.timer.stop()
            if self.scene():
                self.scene().packet_expired.emit(self)

class GameWindow(QMainWindow):
    def __init__(self, game_logic, leaderboard):
        super().__init__()
        self.game_logic = game_logic
        self.leaderboard = leaderboard
        self.setWindowTitle("Cyberpunk Protocol Game")
        self.setGeometry(100, 100, 1000, 700)
        self.setStyleSheet("background-color: #0f1923; color: #00ff00;")

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)

        self.setup_start_screen()
        self.setup_game_area()
        self.setup_blacklist_area()
        self.setup_end_game_buttons()

        self.game_area.hide()
        self.blacklist_area.hide()

        self.packet_items = []

    def setup_start_screen(self):
        self.start_screen = QWidget()
        start_layout = QVBoxLayout(self.start_screen)

        title_label = QLabel("Cyberpunk Protocol Game")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #00ff00; margin-bottom: 20px;")
        title_label.setAlignment(Qt.AlignCenter)
        start_layout.addWidget(title_label)

        self.leaderboard_widget = QListWidget()
        self.leaderboard_widget.setStyleSheet("""
            QListWidget {
                background-color: #0f1923;
                color: #00ff00;
                border: 2px solid #00ff00;
                font-family: 'Courier New', monospace;
            }
            QListWidget::item:selected {
                background-color: #00ff00;
                color: #0f1923;
            }
        """)
        self.update_leaderboard_display()
        start_layout.addWidget(self.leaderboard_widget)

        self.start_button = CyberpunkButton("Start Game")
        self.start_button.clicked.connect(self.start_game)
        start_layout.addWidget(self.start_button, alignment=Qt.AlignCenter)

        self.main_layout.addWidget(self.start_screen)

    def update_leaderboard_display(self):
        self.leaderboard_widget.clear()
        for i, entry in enumerate(self.leaderboard.get_top_scores(), 1):
            self.leaderboard_widget.addItem(f"{i}. {entry['player_name']} - {entry['score']} ({entry['timestamp']})")

    def start_game(self):
        self.start_screen.hide()
        self.game_area.show()
        self.blacklist_area.show()
        self.generate_new_packets(4)
        self.game_logic.__init__()  # Reset game logic
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_game)
        self.timer.start(1000)  # Update every second

    def setup_game_area(self):
        self.game_area = QWidget()
        game_layout = QVBoxLayout(self.game_area)

        self.scene = QGraphicsScene(self)
        self.view = QGraphicsView(self.scene)
        self.view.setStyleSheet("border: 2px solid #00ff00;")
        self.view.setMinimumSize(600, 400)
        game_layout.addWidget(self.view)

        button_layout = QHBoxLayout()
        self.tcp_button = CyberpunkButton("TCP")
        self.udp_button = CyberpunkButton("UDP")
        self.block_button = CyberpunkButton("Block")
        
        self.tcp_button.clicked.connect(lambda: self.handle_action("tcp"))
        self.udp_button.clicked.connect(lambda: self.handle_action("udp"))
        self.block_button.clicked.connect(lambda: self.handle_action("block"))

        button_layout.addWidget(self.tcp_button)
        button_layout.addWidget(self.udp_button)
        button_layout.addWidget(self.block_button)
        game_layout.addLayout(button_layout)

        self.result_label = QLabel("")
        self.result_label.setStyleSheet("font-family: 'Courier New', monospace; font-size: 14px;")
        game_layout.addWidget(self.result_label)

        self.score_label = QLabel("Score: 0")
        self.score_label.setStyleSheet("font-family: 'Courier New', monospace; font-size: 18px; font-weight: bold;")
        game_layout.addWidget(self.score_label)

        self.time_label = QLabel("Time: 1:30")
        self.time_label.setStyleSheet("font-family: 'Courier New', monospace; font-size: 18px; font-weight: bold;")
        game_layout.addWidget(self.time_label)

        self.game_over_label = QLabel("")
        self.game_over_label.setStyleSheet("font-family: 'Courier New', monospace; font-size: 24px; font-weight: bold; color: #ff0000;")
        self.game_over_label.setAlignment(Qt.AlignCenter)
        self.game_over_label.hide()
        game_layout.addWidget(self.game_over_label)

        self.main_layout.addWidget(self.game_area)

    def setup_blacklist_area(self):
        self.blacklist_area = QWidget()
        blacklist_layout = QVBoxLayout(self.blacklist_area)
        blacklist_label = QLabel("Blacklisted IPs:")
        blacklist_label.setStyleSheet("font-family: 'Courier New', monospace; font-size: 16px; font-weight: bold;")
        blacklist_layout.addWidget(blacklist_label)
        
        self.blacklist_widget = QListWidget()
        self.blacklist_widget.setStyleSheet("""
            QListWidget {
                background-color: #0f1923;
                color: #ff0000;
                border: 2px solid #ff0000;
                font-family: 'Courier New', monospace;
            }
            QListWidget::item:selected {
                background-color: #ff0000;
                color: #0f1923;
            }
        """)
        for ip in self.game_logic.get_blacklist():
            self.blacklist_widget.addItem(ip)
        
        blacklist_layout.addWidget(self.blacklist_widget)
        self.main_layout.addWidget(self.blacklist_area)

    def setup_end_game_buttons(self):
        button_layout = QHBoxLayout()
        
        self.reset_button = CyberpunkButton("Reset Game")
        self.reset_button.clicked.connect(self.reset_game)
        self.reset_button.hide()
        
        self.exit_button = CyberpunkButton("Exit Game")
        self.exit_button.clicked.connect(self.close)
        self.exit_button.hide()
        
        button_layout.addWidget(self.reset_button)
        button_layout.addWidget(self.exit_button)
        
        self.main_layout.addLayout(button_layout)

    def generate_new_packets(self, count):
        packet_width = 200
        packet_height = 100
        spacing = 10
        start_y = 50

        for i in range(count):
            packet = Packet.generate_random_packet(self.game_logic.get_blacklist())
            packet_item = PacketGraphicsItem(packet, packet_width, packet_height)
            packet_item.setPos(10 + i * (packet_width + spacing), start_y)
            self.scene.addItem(packet_item)
            self.packet_items.append(packet_item)

    def handle_action(self, action):
        if self.packet_items:
            current_packet = self.packet_items[0].packet
            correct, message = self.game_logic.check_packet(current_packet, action)
            self.result_label.setText(message)
            self.score_label.setText(f"Score: {self.game_logic.get_score()}")
            self.remove_packet(self.packet_items[0])

            # Check if all packets are gone, then generate 4 new ones
            if not self.packet_items:
                self.generate_new_packets(4)

    def remove_packet(self, packet_item):
        if packet_item in self.packet_items:
            self.scene.removeItem(packet_item)
            self.packet_items.remove(packet_item)
            self.shift_packets()

    def shift_packets(self):
        packet_width = 200
        spacing = 10
        animations = []
        for i, packet_item in enumerate(self.packet_items):
            target_x = 10 + i * (packet_width + spacing)
            animation = QPropertyAnimation(packet_item, b"pos")
            animation.setDuration(300)
            animation.setStartValue(packet_item.pos())
            animation.setEndValue(QPointF(target_x, packet_item.y()))
            animation.setEasingCurve(QEasingCurve.InOutQuad)
            animations.append(animation)
        
        for animation in animations:
            animation.start()

    def handle_expired_packet(self):
        expired_packet = self.sender()
        if expired_packet.packet.is_blacklisted:
            self.game_logic.deduct_points_for_missed_blacklist()
            self.result_label.setText("You missed a blacklisted IP! -10 points.")
        self.remove_packet(expired_packet)

    def check_packets(self):
        # This method is no longer needed as packets will remove themselves when they expire
        pass

    def paintEvent(self, event):
        painter = QPainter(self)
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0, QColor(15, 25, 35))
        gradient.setColorAt(1, QColor(25, 35, 45))
        painter.fillRect(self.rect(), gradient)

    def update_game(self):
        remaining_time = self.game_logic.get_remaining_time()
        minutes = remaining_time // 60
        seconds = remaining_time % 60
        self.time_label.setText(f"Time: {minutes}:{seconds:02d}")

        if self.game_logic.is_game_over():
            self.timer.stop()
            self.show_game_over_message()

    def show_game_over_message(self):
        score = self.game_logic.get_score()
        self.game_over_label.setText(f"Game Over! Final Score: {score}")
        self.game_over_label.show()
        self.reset_button.show()
        self.exit_button.show()
        self.tcp_button.setEnabled(False)
        self.udp_button.setEnabled(False)
        self.block_button.setEnabled(False)

        player_name, ok = QInputDialog.getText(self, "Enter Your Name", "Enter your name for the leaderboard:")
        if ok and player_name:
            self.leaderboard.add_score(player_name, score)
            self.update_leaderboard_display()

    def reset_game(self):
        self.game_area.hide()
        self.blacklist_area.hide()
        self.start_screen.show()
        self.game_over_label.hide()
        self.reset_button.hide()
        self.exit_button.hide()
        self.tcp_button.setEnabled(True)
        self.udp_button.setEnabled(True)
        self.block_button.setEnabled(True)
        
        for packet_item in self.packet_items:
            self.scene.removeItem(packet_item)
        self.packet_items.clear()
        
        if self.timer.isActive():
            self.timer.stop()

        self.update_leaderboard_display()