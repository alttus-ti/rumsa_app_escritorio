"""Validación del aviso de carga sin servidor, base de trabajo ni lector."""
import os
import unittest

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from core.carga import cargando

try:
    from PySide6.QtCore import QCoreApplication, QEvent, QTimer
    from PySide6.QtTest import QTest
    from PySide6.QtWidgets import QApplication, QMessageBox, QPushButton, QWidget
    from shiboken6 import isValid
    QT_DISPONIBLE = True
except ImportError:
    QT_DISPONIBLE = False


@unittest.skipUnless(QT_DISPONIBLE, "Requiere PySide6 para validar los diálogos")
class CargaTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])

    def setUp(self):
        self.ventana = QWidget()
        self.ventana.show()
        self.app.processEvents()

    def tearDown(self):
        self.ventana.close()
        self.ventana.deleteLater()
        QCoreApplication.sendPostedEvents(None, QEvent.Type.DeferredDelete)

    def visible(self, dialogo):
        return isValid(dialogo) and dialogo.isVisible()

    def test_guardado_sincrono_cierra_el_aviso(self):
        with cargando(self.ventana, "Guardando cancelación") as dialogo:
            self.assertTrue(self.visible(dialogo))
        self.assertFalse(self.visible(dialogo))

    def test_error_cierra_el_aviso_y_conserva_la_excepcion(self):
        with self.assertRaisesRegex(RuntimeError, "fallo simulado"):
            with cargando(self.ventana, "Guardando") as dialogo:
                raise RuntimeError("fallo simulado")
        self.assertFalse(self.visible(dialogo))

    def test_espera_confirmacion_real_sin_modificar_la_operacion(self):
        estado = {"pendiente": True}
        with cargando(self.ventana, "Esperando lector",
                      pendiente=lambda: estado["pendiente"]) as dialogo:
            pass
        self.assertTrue(self.visible(dialogo))
        self.assertEqual(estado, {"pendiente": True})
        estado["pendiente"] = False
        QTest.qWait(180)
        self.assertFalse(self.visible(dialogo))

    def test_mensaje_original_tiene_prioridad(self):
        with cargando(self.ventana, "Guardando",
                      pendiente=lambda: True) as dialogo:
            mensaje = QMessageBox(self.ventana)
            mensaje.setText("Resultado original")
            mensaje.show()
            self.app.processEvents()
            self.assertFalse(self.visible(dialogo))
            self.assertTrue(mensaje.isVisible())
            mensaje.close()

    def test_ocultar_espera_prolongada_no_cancela_la_operacion(self):
        estado = {"uid": "AABBCCDD", "pendiente": True}
        with cargando(self.ventana, "Esperando lector",
                      pendiente=lambda: estado["pendiente"]) as dialogo:
            pass
        espera = next(t for t in dialogo.findChildren(QTimer) if t.interval() == 15000)
        espera.timeout.emit()
        ocultar = dialogo.findChild(QPushButton)
        self.assertTrue(ocultar.isVisible())
        ocultar.click()
        self.assertFalse(self.visible(dialogo))
        self.assertEqual(estado, {"uid": "AABBCCDD", "pendiente": True})

    def test_cerrar_ventana_no_deja_un_aviso_abierto(self):
        with cargando(self.ventana, "Esperando lector",
                      pendiente=lambda: True) as dialogo:
            pass
        self.ventana.close()
        QTest.qWait(180)
        self.assertFalse(self.visible(dialogo))


class SinInterfazTest(unittest.TestCase):
    def test_validacion_sin_qt_ni_ventana(self):
        with cargando(None, "Guardando", pendiente=lambda: True) as dialogo:
            self.assertIsNone(dialogo)


if __name__ == "__main__":
    unittest.main(verbosity=2)
