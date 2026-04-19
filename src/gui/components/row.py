from PySide6.QtWidgets import QBoxLayout, QWidget
from PySide6.QtCore import Qt

class Row(QWidget):
    def __init__(self, widgets):
        super().__init__()

        self.setStyleSheet("""
            QWidget {
                background-color: transparent;
            }
        """)

        layout = QBoxLayout(QBoxLayout.LeftToRight, self)
        
        layout.setSpacing(6)
        layout.setContentsMargins(2, 2, 2, 2)

        for widget in widgets:
            layout.addWidget(widget)

        # Empurra tudo para a esquerda
        layout.addStretch()