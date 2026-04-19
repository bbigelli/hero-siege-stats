from PySide6.QtCore import Qt
from PySide6.QtWidgets import QHBoxLayout, QWidget, QFrame, QLabel
from src.gui.components.image import ImageWidget
from src.consts import assets as assets_const
from src.consts.enums import Sizes
from src.utils import assets

display_width = {
    Sizes.Small: 80,
    Sizes.Medium: 90,
    Sizes.Large: 100,
    Sizes.XL: 120,
}

class GroupBox(QFrame):
    icon: ImageWidget
    label: QLabel

    def __init__(self, icon: str | None = None, value: str | None = None, size: Sizes = Sizes.Large):
        super().__init__()

        self.setObjectName("GroupBox")
        
        self.setStyleSheet("""
            QFrame#GroupBox {
                background-color: rgba(0, 0, 0, 0.7);
                border: 2px solid rgb(150, 37, 56);
                border-radius: 5px;
            }
            QLabel {
                color: rgb(195, 175, 117);
                font-weight: bold;
                font-size: 10px;
            }
        """)

        self.setMinimumWidth(display_width[size])
        self.setFixedHeight(30)
        
        layout = QHBoxLayout(self)
        layout.setSpacing(5)
        layout.setContentsMargins(4, 0, 5, 0)
        layout.setAlignment(Qt.AlignVCenter)

        if icon is not None:
            self.icon = ImageWidget(assets.icon(icon))
            self.icon.setFixedSize(20, 20)
            layout.addWidget(self.icon, alignment=Qt.AlignVCenter)

        self.label = QLabel(value or "")
        self.label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.label.setWordWrap(False)

        layout.addWidget(self.label, stretch=1)

    def setIcon(self, icon: str):
        if hasattr(self, 'icon'):
            self.icon.setIcon(assets.icon(icon))
    
    def setValue(self, value: str):
        self.label.setText(value)


class ValueDisplay(QWidget):
    groupBox: GroupBox

    def __init__(self, icon: str | None = None, value: str | None = None, size: Sizes = Sizes.Large):
        super().__init__()

        layout = QHBoxLayout(self)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        self.groupBox = GroupBox(icon=icon, value=value, size=size)
        layout.addWidget(self.groupBox)

    def setIcon(self, icon: str):
        self.groupBox.setIcon(icon)

    def setValue(self, value: str):
        self.groupBox.setValue(value)