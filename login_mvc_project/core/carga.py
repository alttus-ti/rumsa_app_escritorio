"""Aviso de espera: solo observa la operación, nunca la confirma ni la cancela."""
from contextlib import contextmanager


@contextmanager
def cargando(ventana, mensaje, pendiente=None, *, mantener_cargando=False):
    # Permite usar los modelos y validar el controlador sin interfaz gráfica.
    if ventana is None:
        yield
        return

    from PySide6.QtCore import QCoreApplication, QEvent, QObject, QTimer, Qt
    from PySide6.QtWidgets import (
        QApplication, QDialog, QLabel, QMessageBox,
        QProgressBar, QPushButton, QVBoxLayout,
    )
    from shiboken6 import isValid

    dialogo = QDialog(ventana)
    dialogo.setObjectName("avisoCarga")
    dialogo.setWindowTitle("")
    dialogo.setWindowFlags(Qt.WindowType.Dialog | Qt.WindowType.FramelessWindowHint)
    dialogo.setWindowModality(Qt.WindowModality.WindowModal)
    dialogo.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
    dialogo.setMinimumWidth(340)
    layout = QVBoxLayout(dialogo)
    layout.setContentsMargins(20, 20, 20, 20)
    layout.setSpacing(12)
    titulo = QLabel("Cargando…", dialogo)
    titulo.setObjectName("tituloCarga")
    layout.addWidget(titulo)
    detalle = QLabel(mensaje, dialogo)
    detalle.setWordWrap(True)
    layout.addWidget(detalle)
    barra = QProgressBar(dialogo)
    barra.setObjectName("progresoCarga")
    barra.setRange(0, 0)
    barra.setTextVisible(False)
    layout.addWidget(barra)
    ocultar = QPushButton("Ocultar aviso", dialogo)
    ocultar.setProperty("uiRole", "secondary")
    ocultar.setToolTip("Solo oculta este cuadro; la operación continúa pendiente.")
    ocultar.clicked.connect(dialogo.close)
    layout.addWidget(ocultar)
    ocultar.hide()

    monitor = QTimer(dialogo)
    dialogo.finished.connect(monitor.stop)

    def cerrar():
        if isValid(dialogo):
            dialogo.close()

    class PrioridadMensajes(QObject):
        def eventFilter(self, objeto, evento):
            if evento.type() == QEvent.Type.Show and isinstance(objeto, QMessageBox):
                cerrar()
            return False

    aplicacion = QApplication.instance()
    prioridad = PrioridadMensajes(dialogo)
    aplicacion.installEventFilter(prioridad)
    dialogo.finished.connect(lambda: aplicacion.removeEventFilter(prioridad))

    def comprobar():
        # Los avisos originales de éxito, error o verificación tienen prioridad.
        if (not isValid(ventana) or not ventana.isVisible()
                or isinstance(QApplication.activeModalWidget(), QMessageBox)
                or not pendiente()):
            cerrar()

    def espera_prolongada():
        if mantener_cargando:
            return
        titulo.setText("Esperando confirmación…")
        detalle.setText(
            "La operación sigue pendiente. Puedes ocultar este aviso "
            "sin cancelarla. No repitas la operación."
        )
        ocultar.show()

    espera = QTimer(dialogo)
    espera.setSingleShot(True)
    espera.timeout.connect(espera_prolongada)
    dialogo.finished.connect(espera.stop)
    dialogo.show()
    dialogo.repaint()
    # Pintar el aviso sin ejecutar de nuevo los lectores ni procesar otros clics.
    QCoreApplication.sendPostedEvents(None, QEvent.Type.UpdateRequest)
    try:
        yield dialogo
    except BaseException:
        cerrar()
        raise
    else:
        if not isValid(dialogo) or not dialogo.isVisible():
            return
        if pendiente is None or not pendiente():
            cerrar()
        else:
            monitor.timeout.connect(comprobar)
            monitor.start(100)
            espera.start(15000)
