"""Imagen de RUMSA para el acceso, con proporciones conservadas al redimensionar."""
from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QLabel


class ImagenMarca(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._original = QPixmap()

    def showEvent(self, event):
        carpeta = Path(__file__).resolve().parent.parent / "assets"
        for nombre in ("logo.png", "logo.jpg", "logo.jpeg",
                       "logo_rumsa.png", "logo_rumsa.jpg", "logo_rumsa.jpeg"):
            ruta = carpeta / nombre
            if ruta.is_file():
                imagen = QPixmap(str(ruta))
                if not imagen.isNull():
                    self._original = imagen
                    break
        self._ajustar_imagen()
        super().showEvent(event)

    def resizeEvent(self, event):
        self._ajustar_imagen()
        super().resizeEvent(event)

    def _ajustar_imagen(self):
        if not self._original.isNull():
            self.setPixmap(self._original.scaled(
                self.contentsRect().size(),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            ))
