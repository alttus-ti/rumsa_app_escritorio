from pathlib import Path

from PySide6.QtCore import QFile, QIODevice
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QWidget
from core.imagen_marca import ImagenMarca


BASE_DIR = Path(__file__).resolve().parent.parent


def load_ui(relative_path: str) -> QWidget:
    """Carga un archivo .ui sin convertirlo a .py."""
    ui_path = BASE_DIR / relative_path

    if not ui_path.exists():
        raise FileNotFoundError(f"No existe el archivo UI: {ui_path}")

    ui_file = QFile(str(ui_path))
    if not ui_file.open(QIODevice.ReadOnly):
        raise RuntimeError(f"No se pudo abrir el archivo UI: {ui_path}")

    loader = QUiLoader()
    loader.registerCustomWidget(ImagenMarca)
    window = loader.load(ui_file)
    ui_file.close()

    if window is None:
        raise RuntimeError(f"No se pudo cargar el archivo UI: {ui_path}")

    return window
