from PySide6.QtWidgets import QLabel
from PySide6.QtCore import Qt
from PySide6.QtGui import QImage, QPixmap

class ImageWidget(QLabel):
    def __init__(self, image_path: str, parent=None):
        super().__init__(parent)

        self.setAlignment(Qt.AlignCenter)
        self.setScaledContents(False)

        self._pixmap = None
        self._original_pixmap = None

        if image_path:
            self.setIcon(image_path)

    def setIcon(self, image_path: str):
        """Set the icon from image path"""
        if image_path:
            image = QImage(image_path)
            if not image.isNull():
                self._original_pixmap = QPixmap.fromImage(image)
                self.updatePixmap()

    def updatePixmap(self):
        """Update the pixmap with current size"""
        if self._original_pixmap and not self._original_pixmap.isNull():
            scaled = self._original_pixmap.scaled(
                self.size(),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            self.setPixmap(scaled)

    def resizeEvent(self, event):
        """Handle resize to scale icon properly"""
        self.updatePixmap()
        super().resizeEvent(event)