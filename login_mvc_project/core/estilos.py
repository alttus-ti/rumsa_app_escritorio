"""Carga del tema compartido; no interviene en el funcionamiento de las pantallas."""
from pathlib import Path

from PySide6.QtCore import QEvent, QObject
from PySide6.QtWidgets import QWidget


class _ActualizarEstadoVisual(QObject):
    def eventFilter(self, objeto, evento):
        if (evento.type() == QEvent.Type.DynamicPropertyChange
                and evento.propertyName() == b"estadoVisual"
                and isinstance(objeto, QWidget)):
            objeto.style().unpolish(objeto)
            objeto.style().polish(objeto)
            objeto.update()
        return False


def cargar_estilos(aplicacion):
    """Resuelve el QSS desde el proyecto, independientemente del directorio actual."""
    ruta = Path(__file__).resolve().parent.parent / "estilos.qss"
    estilos = ruta.read_text(encoding="utf-8")
    estilos = estilos.replace('url("assets/', f'url("{ruta.parent.as_posix()}/assets/')
    aplicacion.setStyleSheet(estilos)
    filtro = _ActualizarEstadoVisual(aplicacion)
    aplicacion.installEventFilter(filtro)
    # QObject conserva la propiedad del filtro durante toda la aplicación.
    return filtro
