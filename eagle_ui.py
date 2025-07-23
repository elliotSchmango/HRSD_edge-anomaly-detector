import sys
import os
import subprocess
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QToolButton, QPushButton,
    QVBoxLayout, QHBoxLayout
)
from PyQt5.QtGui import QFont, QIcon, QFontDatabase
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QSize


class Worker(QThread):
    finished = pyqtSignal(str)

    def __init__(self, command):
        super().__init__()
        self.command = command

    def run(self):
        subprocess.run(self.command)
        self.finished.emit("complete")


class JetsonUI(QWidget):
    def __init__(self, font_name):
        super().__init__()
        self.setWindowTitle("HRSD EAGLE Interface")
        self.setGeometry(100, 100, 1280, 800)
        self.setStyleSheet("background-color: white;")

        # Fonts
        self.title_font = QFont(font_name, 32, QFont.Bold)
        self.label_font = QFont(font_name, 14)
        self.status_font = QFont(font_name, 20, QFont.Medium)

        # Exit button + label
        self.exit_button = QPushButton("✕")
        self.exit_button.setFixedSize(40, 40)
        self.exit_button.setStyleSheet("""
            QPushButton {
                background-color: #ff4d4d;
                color: white;
                border-radius: 20px;
                font-weight: bold;
                font-size: 18px;
            }
            QPushButton:hover {
                background-color: #e60000;
            }
            QPushButton:pressed {
                background-color: #990000;
            }
        """)
        self.exit_button.clicked.connect(self.close)

        self.exit_label = QLabel("Exit System")
        self.exit_label.setFont(QFont(font_name, 10))
        self.exit_label.setStyleSheet("color: #000;")
        self.exit_label.setAlignment(Qt.AlignHCenter)

        exit_layout = QVBoxLayout()
        exit_layout.addWidget(self.exit_button, alignment=Qt.AlignCenter)
        exit_layout.addWidget(self.exit_label, alignment=Qt.AlignCenter)

        # Title bar layout
        title_layout = QHBoxLayout()
        self.title = QLabel("HRSD EAGLE Interface")
        self.title.setFont(self.title_font)
        self.title.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        title_layout.addWidget(self.title)
        title_layout.addStretch()
        title_layout.addLayout(exit_layout)

        # Horizontal icon buttons layout (lowered down)
        self.button_row = QHBoxLayout()
        self.button_row.setSpacing(60)
        self.button_row.setContentsMargins(100, 60, 100, 20)

        self.calib_button = self.create_icon_button("Calibration", "calibration.png", self.start_calibration)
        self.train_button = self.create_icon_button("Train", "update.png", self.start_training)
        self.sentry_button = self.create_icon_button("Sentry", "sentry.png", self.start_sentry)

        self.button_row.addWidget(self.calib_button)
        self.button_row.addWidget(self.train_button)
        self.button_row.addWidget(self.sentry_button)

        # Status bar
        self.status = QLabel("Idle")
        self.status.setFont(self.status_font)
        self.status.setStyleSheet("color: green; background-color: white;")
        self.status.setAlignment(Qt.AlignCenter)

        # layout
        layout = QVBoxLayout()
        layout.addLayout(title_layout)
        layout.addSpacing(60)

        # Secondary static caption
        self.static_caption = QLabel("Available Modes")
        self.static_caption.setFont(QFont(font_name, 30, QFont.Bold))
        self.static_caption.setStyleSheet("color: black;")
        self.static_caption.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.static_caption)

        layout.addLayout(self.button_row)
        layout.addStretch()
        layout.addWidget(self.status)
        layout.addSpacing(30)
        self.setLayout(layout)

    def create_icon_button(self, label, icon_file, handler):
        btn = QToolButton()
        icon_path = os.path.join("icons", icon_file)
        if os.path.exists(icon_path):
            btn.setIcon(QIcon(icon_path))
            btn.setIconSize(QSize(192, 192))

        btn.setText(label)
        btn.setFont(self.label_font)
        btn.setStyleSheet("""
            QToolButton {
                background-color: transparent;
                color: black;
                border: none;
                padding: 10px;
            }
            QToolButton:hover {
                background-color: rgba(0, 0, 0, 0.05);
                border-radius: 12px;
            }
            QToolButton:pressed {
                background-color: rgba(0, 0, 0, 0.1);
                border-radius: 12px;
            }
        """)
        btn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        btn.clicked.connect(handler)
        btn.setFixedSize(200, 220)
        return btn

    def start_calibration(self):
        self.status.setText("Calibrating...")
        self.status.setStyleSheet("color: orange;")
        self.worker = Worker(["python3", "calibration/calibrate_mac.py"])
        self.worker.finished.connect(lambda _: self.status.setText("Calibration Complete"))
        self.worker.start()

    def start_training(self):
        self.status.setText("Training model...")
        self.status.setStyleSheet("color: orange;")
        self.worker = Worker(["python3", "models/autoencoder/train_autoencoder.py"])
        self.worker.finished.connect(lambda _: self.status.setText("Training Complete"))
        self.worker.start()

    def start_sentry(self):
        self.status.setText("Sentry Mode Active — Monitoring...")
        self.status.setStyleSheet("color: blue;")
        self.worker = Worker(["python3", "sentry/sentry_loop.py"])
        self.worker.finished.connect(lambda _: self.status.setText("Sentry Complete"))
        self.worker.start()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Safe font loading
    font_path = os.path.join(os.path.dirname(__file__), "fonts", "Manrope-Regular.ttf")
    if os.path.exists(font_path):
        font_id = QFontDatabase.addApplicationFont(font_path)
        if font_id != -1:
            font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        else:
            print("[Warning] Could not register Manrope font.")
            font_family = "DejaVu Sans"
    else:
        print("[Warning] Font file not found.")
        font_family = "DejaVu Sans"

    ui = JetsonUI(font_family)
    ui.show()
    sys.exit(app.exec_())