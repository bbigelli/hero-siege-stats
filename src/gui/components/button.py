from PySide6.QtWidgets import QPushButton, QWidget, QHBoxLayout
from PySide6.QtCore import Qt
from src.consts.enums import Sizes

button_width = {
    Sizes.Small: 80,
    Sizes.Medium: 90,
    Sizes.Large: 100,
    Sizes.XL: 120,
}

class Button(QWidget):
    button: QPushButton

    def __init__(self, text: str, size: Sizes = Sizes.Medium):
        QWidget.__init__(self)

        layout = QHBoxLayout(self)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        self.button = QPushButton(text)
        self.button.setMinimumWidth(button_width[size])
        self.button.setFixedHeight(26)
        self.button.setCursor(Qt.PointingHandCursor)

        self.button.setStyleSheet("""
            QPushButton {
                background-color: rgba(47, 52, 54, 0.9);
                border: 2px solid rgb(150, 37, 56);
                border-radius: 5px;
                color: rgb(195, 175, 117);
                font-weight: bold;
                padding: 2px;
                font-size: 10px;
            }
            QPushButton:hover {
                background-color: rgba(60, 65, 67, 0.95);
                border: 2px solid rgb(200, 50, 75);
                color: rgb(220, 200, 140);
            }
            QPushButton:pressed {
                background-color: rgba(30, 35, 37, 0.95);
                border: 2px solid rgb(100, 25, 40);
            }
        """)

        layout.addWidget(self.button)

    def onclick(self, callback):
        """Connect click event to callback"""
        self.button.clicked.connect(callback)