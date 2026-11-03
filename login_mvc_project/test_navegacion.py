"""Navegación con Qt y ajustes temporales, sin base, red ni lector."""
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PySide6.QtCore import QSettings
from PySide6.QtWidgets import QApplication
from controllers.app_controller import AppController
from views.administrador_view import AdminWindow
from views.empleado_view import EmpleadoWindow


class NavegacionTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        settings = QSettings(str(Path(self.temp.name) / "ajustes.ini"), QSettings.IniFormat)
        self.patches = [
            patch("controllers.app_controller.QSettings", return_value=settings),
            patch("sqlite3.connect", side_effect=AssertionError("No acceder a SQLite")),
            patch("requests.get", side_effect=AssertionError("No acceder a la red")),
            patch("requests.post", side_effect=AssertionError("No acceder a la red")),
            patch.object(AppController, "_sincronizar_pendientes"),
            patch.object(AppController, "_llenar_lista_puertos"),
        ]
        for method in ("_configurar_alta_window", "_configurar_recarga_window",
                       "_configurar_sustituir_window", "_configurar_cancelar_window"):
            self.patches.append(patch.object(AppController, method))
        for item in self.patches:
            item.start()
        self.controller = AppController()
        self.controller.show_window_by_role("prueba", "administrador")

    def tearDown(self):
        c = self.controller
        c.sync_timer.stop()
        c._sync_poll.stop()
        c._close_current_window()
        c._sync_executor.shutdown(wait=True)
        self.app.processEvents()
        for item in reversed(self.patches):
            item.stop()
        self.temp.cleanup()

    def assert_menu(self, seccion):
        ui = self.controller.current_ui
        self.assertIsInstance(ui, AdminWindow)
        page = ui.page_3 if seccion == "personal" else ui.page_4
        self.assertIs(ui.stackedWidget.currentWidget(), page)
        self.assertEqual(ui.pushButton.isChecked(), seccion == "personal")
        self.assertEqual(ui.botonusuario.isChecked(), seccion == "pasajeros")

    def test_volver_recuerda_ambas_secciones(self):
        c = self.controller
        c.current_ui.pushButton.click()
        c.show_sustituir_window("personal")
        c.current_ui.botonregresar.click()
        self.assert_menu("personal")
        c.current_ui.botonusuario.click()
        c.show_recarga_window()
        c.current_ui.botonregresar.click()
        self.assert_menu("pasajeros")

    def test_cancelar_altas_regresa_al_menu(self):
        c = self.controller
        c.current_ui.pushButton.click()
        c.show_alta_operador_window()
        c.current_ui.botonguardar_2.click()
        self.assert_menu("personal")
        c.current_ui.botonusuario.click()
        c.show_alta_window()
        c.current_ui.botonguardar_13.click()
        self.assert_menu("pasajeros")

    def test_cerrar_con_x_y_cambio_de_usuario(self):
        c = self.controller
        c.current_ui.pushButton.click()
        c.show_cancelar_window()
        c.current_window.close()
        self.assert_menu("personal")
        c.show_window_by_role("otra_persona", "administrador")
        self.assert_menu("pasajeros")
        c.show_window_by_role("prueba", "administrador")
        self.assert_menu("personal")

    def test_empleado_regresa_a_su_menu(self):
        c = self.controller
        c.show_window_by_role("empleado", "empleado")
        c.show_recarga_window()
        c.current_ui.botonregresar.click()
        self.assertIsInstance(c.current_ui, EmpleadoWindow)

    def test_no_salir_durante_escritura_pendiente(self):
        c = self.controller
        c.show_recarga_window()
        window = c.current_window
        c._recarga_en_curso = {"uid": "AABBCCDD"}
        with patch("controllers.app_controller.QMessageBox.warning") as warning:
            c.current_ui.botonregresar.click()
            window.close()
            self.assertIs(c.current_window, window)
            self.assertEqual(warning.call_count, 2)
        c._recarga_en_curso = None


if __name__ == "__main__":
    unittest.main(verbosity=2)
