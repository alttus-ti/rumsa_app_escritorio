from ast import alias
from pathlib import Path

from concurrent.futures import ThreadPoolExecutor

from PySide6.QtCore import QCoreApplication, QDate, QDateTime, QSize, QTimer, Qt, QSettings, QRectF
from PySide6.QtWidgets import (
    QAbstractItemView,
    QButtonGroup,
    QCalendarWidget,
    QDialog,
    QFileDialog,
    QHeaderView,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMessageBox,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QMenu,
    QToolButton,
    QLineEdit,

)
from datetime import datetime
from typing import Optional
import re
import time
import traceback
from PySide6.QtGui import QIcon, QPixmap, QPainter, QColor, QPen, QBrush, QPainterPath, QDoubleValidator

from core.sync_config import SYNC_INTERVAL_MS
from core.date_picker import DatePicker
from models.cancelar_model import CancelarModel
from models.sustituir_model import SustituirModel


from controllers.alta_controller import AltaController
from controllers.arduino_controller import ArduinoController
from controllers.login_controller import LoginController
from models.alta_model import AltaModel
from models.recarga_model import RecargaModel
from services.sync_service import SyncService
from views.administrador_view import AdminWindow
from views.dar_de_alta_view import AltaWindow
from views.dar_de_alta_operador_view import Ui_AltaOWindow
from views.login_view import LoginWindow
from views.recarga_view import RecargaWindow
from views.empleado_view import EmpleadoWindow
from views.cancelar_view import CancelarWindow
from views.sustituir_view import SustituirWindow


class AppController:
    """Controlador principal de ventanas."""

    UID_RE = re.compile(r"^[0-9A-F]{8,20}$")

    def __init__(self):
        
        #Login
        self.current_window = None
        self.current_ui = None
        self.current_username = ""
        self.current_role = ""
        
        self.settings = QSettings("RUMSA", "LoginMVC")

        # recarga
        self.arduino = ArduinoController()
        self.recarga_model = RecargaModel()
        self.recarga_timer = None
        self.uid_actual = ""
        self.nombre_actual = ""
        self.tipo_actual = ""
        self.saldo_actual_centavos = 0
        self.monto_pendiente_centavos = 0
        self._recarga_en_curso = None
        self.tarjeta_vencida = False

        # alta
        self.alta_model = AltaModel()
        self.alta_timer = None
        self.uid_alta_actual = ""
        self.alta_pendiente = None
        
        self.foto_alta_path = ""

        # sincronizacion
        self.sync_service = SyncService()
        self._sync_executor = ThreadPoolExecutor(
            max_workers=1,
            thread_name_prefix="desktop-sync",
        )
        self._sync_future = None
        self._sync_poll = QTimer()
        self._sync_poll.timeout.connect(
            self._recibir_sincronizacion
        )
        self.sync_timer = QTimer()
        self.sync_timer.timeout.connect(self._sincronizar_pendientes)
        self.sync_timer.start(SYNC_INTERVAL_MS)
        
        # cancelar
        self.cancelar_model = CancelarModel()
        self.cancelar_timer = None
        self.uid_cancelar_actual = ""
        self.tipo_cancelar_actual = ""
        self.saldo_cancelar_actual = 0.0
        self.nombre_cancelar_actual = ""
        self.tarjeta_bloqueada = False
        
        #Sustituir
        self.sustituir_model = SustituirModel()
        self.sustituir_timer = None
        self.uid_sustituir_original = ""
        self.uid_sustituir_nueva = ""
        self.tarjeta_sustituir_seleccionada = None
        self.resultados_sustituir = []
        self.seccion_sustituir = "pasajeros"
        self.popup_resultados_sustituir = None
        self.sustituir_pendiente = None
        
        
        
        
        

    def _normalizar_uid(self, uid: str) -> str:
        uid_limpia = uid.strip().upper()
        if len(uid_limpia) % 2 != 0:
            return ""
        if not self.UID_RE.fullmatch(uid_limpia):
            return ""
        return uid_limpia

    def _limpiar_alias_para_arduino(self, nombre: str, max_len: int = 24) -> str:
        import unicodedata
        import re as _re

        s = unicodedata.normalize("NFKD", nombre)
        s = s.encode("ascii", "ignore").decode("ascii")
        s = s.replace(",", " ")
        s = s.replace("\r", " ").replace("\n", " ")
        s = _re.sub(r"\s+", " ", s).strip()
        return s[:max_len]

    def _ajustar_alias_para_comando_alta(
        self,
        uid: str,
        alias: str,
        no_tarjeta: str,
        id_tipo_tarjeta: str,
        id_tarifa: str,
        vigtarifa: str,
        vigencia12: str,
    ) -> str:
        # El nombre ocupa 24 bytes ASCII en las posiciones 40..63.
        return self._limpiar_alias_para_arduino(alias, max_len=24)

    def _parsear_trama_saldo(self, linea: str):
        partes = linea.split(",")
        if len(partes) < 4 or partes[0].strip().lower() != "sldo":
            return None

        uid = partes[1].strip()
        saldo_centavos = partes[2].strip()
        campos_nombre = partes[3:]
        tipo_fisico = ""

        if len(campos_nombre) > 1 and campos_nombre[-1].strip().upper() in ("NO", "EU", "KI", "DE"):
            tipo_fisico = campos_nombre[-1].strip().upper()
            campos_nombre = campos_nombre[:-1]

        return {
            "uid": uid,
            "saldo_centavos": saldo_centavos,
            "nombre": ",".join(campos_nombre).strip(),
            "tipo_fisico": tipo_fisico,
        }

    def show_login_window(self) -> None:
        previous_window = self._release_current_window()
        self.current_window = QMainWindow()
        self.current_ui = LoginWindow()
        self.current_ui.setupUi(self.current_window)
        self._configurar_login_window()
        self.current_window.show()
        self._close_replaced_window(previous_window)
        QTimer.singleShot(500, self._sincronizar_pendientes)

    def showLoginWindow(self) -> None:
        self.show_login_window()
        
    def _cargar_recordarme_login(self)-> None:
        if not isinstance(self.current_ui, LoginWindow):
            return
        
        recordarme = self.settings.value("login/recordarme", False, type=bool)
        usuario = self.settings.value("login/usuario","", type=str)
        
        self.current_ui.checkBoxRemember.setChecked(recordarme)
        
        if recordarme and usuario:
            self.current_ui.lineEditUser.setText(usuario)
            self.current_ui.lineEditPassword.setFocus()
        else:
            self.current_ui.lineEditUser.clear()
            self.current_ui.lineEditPassword.clear()
            self.current_ui.lineEditUser.setFocus()
            
    def _guardar_recordarme_login(self, username:str)->None:
        if not isinstance(self.current_ui, LoginWindow):
            return
        
        if self.current_ui.checkBoxRemember.isChecked():
            self.settings.setValue("login/recordarme", True)
            self.settings.setValue("login/usuario", username)
        else:
            self.settings.setValue("login/recordarme", False)
            self.settings.remove("login/usuario")
        
        self.settings.sync()
        
    def _borrar_recordarme_si_desmarca(self, checked: bool) -> None:
        if checked:
            return
        
        self.settings.setValue("login/recordarme", False)
        self.settings.remove("login/usuario")
        self.settings.sync()
        

    def _configurar_login_window(self) -> None:
        ui = self.current_ui
        ui.layoutEstructura10.addStretch(1)
        ui.layoutEstructura10.setStretch(0, 1)
        self.login_controller = LoginController()
        
        ui.lineEditPassword.setEchoMode(QLineEdit.EchoMode.Password)
        
        self.accion_ver_password = ui.lineEditPassword.addAction(
            self._crear_icono_ojo(tachado=False),
            QLineEdit.ActionPosition.TrailingPosition
        )
        self.accion_ver_password.setToolTip("Mostrar Contraseña")
        self.accion_ver_password.triggered.connect(self._alternar_visibilidad_password)

        self._cargar_recordarme_login()

        ui.pushButtonLogin.clicked.connect(self._ejecutar_login)
        ui.pushButtonCancel.clicked.connect(self.current_window.close)
        ui.checkBoxRemember.toggled.connect(self._borrar_recordarme_si_desmarca)

        ui.pushButtonForgot.clicked.connect(
            lambda: QMessageBox.information(
                self.current_window,
                "Recuperar contraseña",
                "Contacta al administrador para recuperar tu contraseña.",
            )
        )
        ui.lineEditPassword.returnPressed.connect(self._ejecutar_login)
        ui.lineEditUser.returnPressed.connect(ui.lineEditPassword.setFocus)

    def _ejecutar_login(self) -> None:
        if not isinstance(self.current_ui, LoginWindow):
            return

        username = self.current_ui.lineEditUser.text().strip()
        password = self.current_ui.lineEditPassword.text()

        ok, message = self.login_controller.authenticate(username, password)
        if not ok:
            QMessageBox.warning(self.current_window, "Login", message)
            return

        role = self.login_controller.get_role(username)
        if not role:
            QMessageBox.warning(
                self.current_window,
                "Login",
                "El usuario no tiene un rol asignado.",
            )
            return

        self._guardar_recordarme_login(username)

        self.show_window_by_role(username, role)


    def show_window_by_role(self, username: str, role: str) -> None:
        self.current_username = username
        self.current_role = role.strip().lower()

        if self.current_role == "administrador":
            self.show_admin_window(username)
            return

        if self.current_role == "empleado":
            self.show_empleado_window(username)
            return

        self.show_login_window()

    def show_admin_window(self, username: str) -> None:
        previous_window = self._release_current_window()
        self.current_window = QMainWindow()
        self.current_ui = AdminWindow()
        self.current_ui.setupUi(self.current_window)
        self._configurar_menu_usuario()

        ui = self.current_ui
        iconos_dir = Path(__file__).resolve().parent.parent / "assets" / "icons"
        botones_iconos = (
            (ui.botonusuario, "pasajeros"),
            (ui.pushButton, "operadores"),
            (ui.usuario, "pasajeros"),
            (ui.botonalta, "alta"),
            (ui.botonalta_2, "alta"),
            (ui.botonsustituir, "sustituir"),
            (ui.botonsustituir_2, "sustituir"),
            (ui.botonrecarga, "recarga"),
            (getattr(ui, "botonrecarga_2", None), "recarga"),
            (ui.botoncancelar, "cancelar"),
            (ui.botoncancelar_2, "cancelar"),
        )
        for boton, nombre_icono in botones_iconos:
            if boton is None:
                continue
            icono = QIcon()
            for modo in (QIcon.Mode.Normal, QIcon.Mode.Active):
                icono.addFile(str(iconos_dir / f"{nombre_icono}.png"), QSize(), modo, QIcon.State.Off)
                icono.addFile(str(iconos_dir / f"{nombre_icono}_selected.png"), QSize(), modo, QIcon.State.On)
            boton.setIcon(icono)
            boton.setIconSize(QSize(24, 24))
            if nombre_icono in ("alta", "sustituir", "recarga", "cancelar"):
                boton.setIconSize(QSize(36, 36))
                boton.setText(" ".join(boton.text().split()).removesuffix(">").rstrip())
                distribucion_flecha = QHBoxLayout(boton)
                distribucion_flecha.setContentsMargins(0, 0, 20, 0)
                distribucion_flecha.addStretch()
                flecha = QLabel(">", boton)
                flecha.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
                flecha.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
                flecha.setProperty("uiRole", "arrow")
                distribucion_flecha.addWidget(flecha)
        ui.usuario.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)

        for boton in (ui.botonusuario, ui.pushButton):
            boton.setCheckable(True)
        ui.grupo_menu = QButtonGroup(self.current_window)
        ui.grupo_menu.setExclusive(True)
        ui.grupo_menu.addButton(ui.botonusuario)
        ui.grupo_menu.addButton(ui.pushButton)

        def actualizar_seleccion_menu():
            ui.botonusuario.setChecked(ui.stackedWidget.currentWidget() == ui.page_4)
            ui.pushButton.setChecked(ui.stackedWidget.currentWidget() == ui.page_3)
            seccion = "personal" if ui.stackedWidget.currentWidget() == ui.page_3 else "pasajeros"
            self.settings.setValue(f"navegacion/{username}/seccion_menu", seccion)

        seccion = self.settings.value(f"navegacion/{username}/seccion_menu", "pasajeros")
        ui.stackedWidget.setCurrentWidget(ui.page_3 if seccion == "personal" else ui.page_4)
        ui.stackedWidget.currentChanged.connect(actualizar_seleccion_menu)
        actualizar_seleccion_menu()
        ui.botonusuario.clicked.connect(
            lambda: ui.stackedWidget.setCurrentWidget(ui.page_4)
        )
        ui.pushButton.clicked.connect(
            lambda: ui.stackedWidget.setCurrentWidget(ui.page_3)
        )

        self.current_ui.botonalta.clicked.connect(self.show_alta_window)
        self.current_ui.botonalta_2.clicked.connect(self.show_alta_operador_window)
        self.current_ui.botonrecarga.clicked.connect(self.show_recarga_window)
        self.current_ui.botoncancelar.clicked.connect(self.show_cancelar_window)
        self.current_ui.botoncancelar_2.clicked.connect(self.show_cancelar_window)
        self.current_ui.botonsustituir.clicked.connect(
            lambda checked=False: self.show_sustituir_window(seccion="pasajeros")
        )
        self.current_ui.botonsustituir_2.clicked.connect(
            lambda checked=False: self.show_sustituir_window(seccion="personal")
        )

        self.current_window.show()
        self._close_replaced_window(previous_window)
        self._actualizar_estado_sync_ui("connecting")
        QTimer.singleShot(300, self._sincronizar_pendientes)

    def show_empleado_window(self, username: str) -> None:
        previous_window = self._release_current_window()
        self.current_window = QMainWindow()
        self.current_ui = EmpleadoWindow()
        self.current_ui.setupUi(self.current_window)
        self._configurar_menu_usuario()

        boton = self.current_ui.botonrecarga
        iconos_dir = Path(__file__).resolve().parent.parent / "assets" / "icons"
        boton.setIcon(QIcon(str(iconos_dir / "recarga.png")))
        boton.setIconSize(QSize(36, 36))
        distribucion_flecha = QHBoxLayout(boton)
        distribucion_flecha.setContentsMargins(0, 0, 20, 0)
        distribucion_flecha.addStretch()
        flecha = QLabel(">", boton)
        flecha.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        flecha.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        flecha.setProperty("uiRole", "arrow")
        distribucion_flecha.addWidget(flecha)

        self.current_ui.botonrecarga.clicked.connect(self.show_recarga_window)

        self.current_window.show()
        self._close_replaced_window(previous_window)
        self._actualizar_estado_sync_ui("connecting")
        QTimer.singleShot(300, self._sincronizar_pendientes)

    def show_contador_window(self, username: str) -> None:
        self.show_admin_window(username)

    def showContadorWindow(self, username: str) -> None:
        self.show_contador_window(username)

    def show_alta_window(self) -> None:
        self._show_port_window(AltaWindow())
        self._configurar_alta_window()

    def show_alta_operador_window(self) -> None:
        self._show_port_window(Ui_AltaOWindow())
        ui = self.current_ui
        ui.labelEstadoConexion = ui.labelEstadoConexion_2
        ui.curpstatus = QLabel(self.current_window)
        ui.statusbar.addWidget(ui.curpstatus, 1)
        ui.calendario = QCalendarWidget(self.current_window)
        ui.calendario.hide()
        ui.calendario_nacimiento = DatePicker(
            ui.textofechanacimiento, self.current_window, "Seleccionar fecha de nacimiento"
        )
        ui.calendario_vigencia = DatePicker(
            ui.textovigencia, self.current_window, "Seleccionar vigencia"
        )
        def sincronizar_vigencia():
            fecha = QDate.fromString(ui.textovigencia.toPlainText(), "dd-MM-yyyy")
            if fecha.isValid() and fecha != ui.calendario.selectedDate():
                ui.calendario.setSelectedDate(fecha)

        ui.textovigencia.textChanged.connect(sincronizar_vigencia)
        ui.textofechanacimiento.clear()
        ui.label_6.setText('<a href="quitar">Quitar foto</a>')
        ui.label_6.setTextInteractionFlags(Qt.TextInteractionFlag.LinksAccessibleByMouse)
        ui.label_6.linkActivated.connect(self._limpiar_foto_alta)
        ui.botonguardar_2.clicked.connect(self._cancelar_formulario_alta)
        self._configurar_alta_window()

    def show_recarga_window(self) -> None:
        self._show_port_window(RecargaWindow())
        self._configurar_recarga_window()

    def show_cancelar_window(self) -> None:
        self._show_port_window(CancelarWindow())
        self._configurar_cancelar_window()

    def show_sustituir_window(self, seccion: str = "pasajeros") -> None:
        seccion = seccion.strip().lower()
        if seccion not in ("pasajeros", "personal"):
            raise ValueError("Sección de búsqueda no válida.")
        self.seccion_sustituir = seccion
        self._show_port_window(SustituirWindow())
        self._configurar_sustituir_window()

    def _show_port_window(self, ui) -> None:
        previous_window = self._release_current_window()
        self.current_window = QMainWindow()
        self.current_ui = ui
        self.current_ui.setupUi(self.current_window)
        self._adaptar_controles_ui()
        
        self._configurar_menu_usuario()

        self._llenar_lista_puertos()

        if hasattr(self.current_ui, "botonregresar"):
            self.current_ui.botonregresar.clicked.connect(
                self._regresar_pantalla_anterior
            )

        ventana = self.current_window
        ventana.closeEvent = lambda event: self._cerrar_pantalla_operacion(event, ventana)

        self.current_window.show()
        self._close_replaced_window(previous_window)
        self._actualizar_estado_sync_ui("connecting")
        QTimer.singleShot(300, self._sincronizar_pendientes)

    def _regresar_pantalla_anterior(self) -> None:
        if self.alta_pendiente or self._recarga_en_curso or self.sustituir_pendiente:
            QMessageBox.warning(
                self.current_window, "Operación en proceso",
                "Espera a que la operación de la tarjeta se compruebe y se guarde antes de salir."
            )
            return
        self.show_window_by_role(self.current_username, self.current_role)

    def _cerrar_pantalla_operacion(self, event, ventana) -> None:
        # Al reemplazar una ventana, su cierre no debe iniciar otro regreso.
        if ventana is not self.current_window:
            event.accept()
            return
        event.ignore()
        self._regresar_pantalla_anterior()

    def _adaptar_controles_ui(self) -> None:
        """Conserva los enlaces del controlador al cambiar nombres en Designer."""
        ui = self.current_ui
        aliases = {
            "labelEstadoConexion": "labelEstadoConexion_2",
            "usuario": "usuario_2",
        }
        if isinstance(ui, AltaWindow):
            aliases.update({
                "textonombre": "textonombre_7", "textocurp": "textocurp_7",
                "textofechanacimiento": "textofechanacimiento_7",
                "textovigencia": "textovigencia_7", "fotoimagen": "fotoimagen_7",
                "botonsubir": "botonsubir_7", "botonguardar": "botonguardar_14",
                "mensajeInternet": "mensajeInternet_2",
            })
        for nombre, origen in aliases.items():
            if not hasattr(ui, nombre) and hasattr(ui, origen):
                setattr(ui, nombre, getattr(ui, origen))
        if isinstance(ui, AltaWindow) and not hasattr(ui, "calendario"):
            ui.calendario = QCalendarWidget(self.current_window)
            ui.calendario.hide()
            ui.calendario_nacimiento = DatePicker(
                ui.textofechanacimiento, self.current_window, "Seleccionar fecha de nacimiento"
            )
            ui.calendario_vigencia = DatePicker(
                ui.textovigencia, self.current_window, "Seleccionar vigencia"
            )

            def sincronizar_vigencia():
                fecha = QDate.fromString(ui.textovigencia.toPlainText(), "dd-MM-yyyy")
                if fecha.isValid() and fecha != ui.calendario.selectedDate():
                    ui.calendario.setSelectedDate(fecha)

            ui.textovigencia.textChanged.connect(sincronizar_vigencia)
            ui.textofechanacimiento.clear()
            ui.curpstatus = QLabel(self.current_window)
            self.current_window.statusBar().addWidget(ui.curpstatus, 1)
            ui.botonguardar_13.clicked.connect(self._cancelar_formulario_alta)
            ui.label_34.setText('<a href="quitar">Quitar foto</a>')
            ui.label_34.setTextInteractionFlags(Qt.TextInteractionFlag.LinksAccessibleByMouse)
            ui.label_34.linkActivated.connect(self._limpiar_foto_alta)

    def _sincronizar_pendientes(self) -> None:
        if self._sync_future is not None:
            return

        pendientes = self.sync_service.count_pending()

        if pendientes:
            self._actualizar_estado_sync_ui(
                "syncing",
                pendientes,
            )

        self._sync_future = self._sync_executor.submit(
            self.sync_service.sync_pending_once
        )
        self._sync_poll.start(100)

    def _recibir_sincronizacion(self) -> None:
        if (
            self._sync_future is None
            or not self._sync_future.done()
        ):
            return

        self._sync_poll.stop()

        try:
            resultado = self._sync_future.result()

        except Exception as error:
            resultado = {
                "state": "offline",
                "pending_after": self.sync_service.count_pending(),
                "message": str(error),
            }

        self._sync_future = None

        if (
            self.current_ui is not None
            and hasattr(
                self.current_ui,
                "labelEstadoConexion",
            )
        ):
            self.current_ui.labelEstadoConexion.setToolTip(
                resultado.get("message", "")
            )

        estado = resultado.get("state", "offline")

        if estado not in {
            "connected",
            "connected_with_errors",
        }:
            estado = "offline"

        self._actualizar_estado_sync_ui(
            estado,
            int(resultado.get("pending_after", 0) or 0),
        )
        if (resultado.get("synced_count", 0) > 0
                and resultado.get("pending_after", 0) > 0
                and resultado.get("error_count", 0) == 0):
            QTimer.singleShot(0, self._sincronizar_pendientes)
        
        
    def _actualizar_estado_sync_ui(
        self, estado: str, pendientes: int = 0
    ) -> None:
        ui = self.current_ui

        if ui is None or not hasattr(ui, "labelEstadoConexion"):
            return

        pendientes = max(0, int(pendientes or 0))

        if estado == "syncing":
            texto = "Sincronizando" if pendientes else "Comprobando conexión"
            color = "warning"

        elif estado == "connected_with_errors":
            texto = "Conectado · Error de sincronización"
            color = "warning"

        elif estado == "connected":
            texto = "Conectado"
            color = "success"

        else:
            texto = "Sin conexión"
            color = "warning"

        if pendientes:
            texto += f" · Pendientes: {pendientes}"

        ui.labelEstadoConexion.setText(texto)
        ui.labelEstadoConexion.setProperty("estadoVisual", color)

        if isinstance(ui, (AltaWindow, Ui_AltaOWindow)):
            self._ocultar_error_alta_sin_internet()
            self._set_alta_inputs_enabled(
                not bool(self.alta_pendiente)
            )
    
    def _llenar_lista_puertos(self) -> None:
        alta_controller = AltaController()
        puertos = alta_controller.obtener_puertos_combo()
        lista_puertos = self._combo_puertos_actual()
        if lista_puertos is None:
            print(
                "[PUERTOS] La ventana actual no tiene combo de puertos "
                "llamado 'lista' ni 'comboBox'."
            )
            return

        lista_puertos.clear()

        if not puertos:
            lista_puertos.addItem("No hay puertos disponibles")
            return

        indice_detectado = 0

        for index, puerto in enumerate(puertos):
            lista_puertos.addItem(puerto["texto"], puerto["device"])
            if puerto["seleccionado"]:
                indice_detectado = index

        lista_puertos.setCurrentIndex(indice_detectado)

    def _combo_puertos_actual(self):
        if self.current_ui is None:
            return None

        return (
        getattr(self.current_ui, "lista", None)
        or getattr(self.current_ui, "comboBox", None)
        or getattr(self.current_ui, "puerto", None)
    )

    def _release_current_window(self):
        if isinstance(self.current_ui, RecargaWindow):
            if self.recarga_timer is not None:
                self.recarga_timer.stop()
            self.arduino.cerrar()

        if isinstance(self.current_ui, (AltaWindow, Ui_AltaOWindow)):
            if self.alta_timer is not None:
                self.alta_timer.stop()
            self.arduino.cerrar()
        
        if isinstance(self.current_ui, CancelarWindow):
            if self.cancelar_timer is not None:
                self.cancelar_timer.stop()
            self.arduino.cerrar()
            
        if isinstance(self.current_ui, SustituirWindow):
            if self.sustituir_timer is not None:
                self.sustituir_timer.stop()
            self.arduino.cerrar()
            self.popup_resultados_sustituir = None

        previous_window = self.current_window
        self.current_window = None
        self.current_ui = None
        return previous_window

    def _close_replaced_window(self, previous_window) -> None:
        if previous_window is not None:
            previous_window.close()

    def _close_current_window(self) -> None:
        previous_window = self._release_current_window()
        self._close_replaced_window(previous_window)

    # =========================
    # RECARGA
    # =========================

    def _configurar_recarga_window(self) -> None:
        ui = self.current_ui
        
        self._aplicar_estilos_sustituir()

        self.uid_actual = ""
        self.nombre_actual = ""
        self.tipo_actual = ""
        self.saldo_actual_centavos = 0
        self.monto_pendiente_centavos = 0
        self.tarjeta_vencida = False

        ui.texto4.setText("-")
        ui.texto5.setText("-")
        ui.texto6.setText("-")
        ui.texto1.setText("$0.00")
        ui.texto2.setText("$0.00")
        ui.texto7.setText("")
        ui.botonrecargar.setEnabled(True)
        
        self.oficina_recarga_actual = ""
        self._llenar_oficinas_recarga()
        

        monto = self._campo_monto_recarga()
        if monto is not None:
            monto.setReadOnly(False)
            monto.clear()
            validador_moto = QDoubleValidator(-42949672.95, 400.00, 2)
            validador_moto.setNotation(QDoubleValidator.StandardNotation)
            monto.setValidator(validador_moto)
            monto.setPlaceholderText("0.00")
            monto.setMaxLength(14)
            
            monto.textChanged.connect(self._preview_saldo_nuevo)
            monto.editingFinished.connect(self._formatear_monto_recarga)

        ui.botonrecargar.clicked.connect(self._ejecutar_recarga)

        lista_puertos = self._combo_puertos_actual()
        if lista_puertos is not None:
            lista_puertos.currentIndexChanged.connect(self._conectar_puerto_recarga)

        if self.recarga_timer is None:
            self.recarga_timer = QTimer()
            self.recarga_timer.timeout.connect(self._leer_serial_recarga)

        self._conectar_puerto_recarga()
        self.recarga_timer.start(300)   
   
    def _llenar_oficinas_recarga(self) -> None:
        ui = self.current_ui
        
        if ui is None or not hasattr(ui, "listaoficina"):
            return
        
        ui.listaoficina.clear()
        ui.listaoficina.addItem("Selecciona oficina", "")
        
        oficinas = [
            "Oficina Centro",
            "Oficina Terminal",
            "Oficina Norte",
        ]
        
        for oficina in oficinas:
            ui.listaoficina.addItem(oficina, oficina)         
    
    def _oficina_seleccionada_recarga(self) -> str:
        ui = self.current_ui
        
        if ui is None or not hasattr(ui, "listaoficina"):
            return ""
        
        oficina = ui.listaoficina.currentData()
        
        if oficina is None:
            oficina = ui.listaoficina.currentText()
        
        return str(oficina).strip()        
         
    def _parsear_vigencia_tarjeta(self, vigencia_raw) -> Optional[datetime]:
        if vigencia_raw is None:
            return None

        texto_vigencia = str(vigencia_raw).strip()
        if not texto_vigencia:
            return None

        formatos = (
            "%d%m%y%H%M%S",
            "%d-%m-%Y %H:%M:%S",
            "%Y-%m-%d %H:%M:%S",
        )

        for formato in formatos:
            try:
                return datetime.strptime(texto_vigencia, formato)
            except ValueError:
                continue

        return None

    def _actualizar_estado_vencimiento_tarjeta(self, tarjeta_db) -> None:
        if not isinstance(self.current_ui, RecargaWindow):
            return

        ui = self.current_ui
        monto = self._campo_monto_recarga()

        vigencia_raw = tarjeta_db["vigencia"] if tarjeta_db else None
        fecha_vigencia = self._parsear_vigencia_tarjeta(vigencia_raw)

        self.tarjeta_vencida = bool(
            fecha_vigencia and fecha_vigencia <= datetime.now()
        )

        if self.tarjeta_vencida:
            if monto is not None:
                monto.clear()
                monto.setEnabled(False)

            ui.texto2.setText(f"${self.saldo_actual_centavos / 100:.2f}")
            ui.botonrecargar.setEnabled(False)
            ui.texto7.setText(
                "Tarjeta vencida "
                f"({fecha_vigencia.strftime('%d-%m-%Y %H:%M:%S')})."
            )
            ui.texto7.setProperty("estadoVisual", "error")
            return

        if monto is not None and not getattr(self, "tarjeta_bloqueada", False):
            monto.setEnabled(True)

        if not getattr(self, "tarjeta_bloqueada", False):
            ui.botonrecargar.setEnabled(True)

        if "Tarjeta vencida" in ui.texto7.text():
            ui.texto7.setText("")
            ui.texto7.setProperty("estadoVisual", "")
                      
    def _fallo_recarga(self, motivo: str, error: Optional[Exception] = None) -> None:
        if isinstance(self.current_ui, RecargaWindow):
            self.current_ui.texto7.setText("Fallo recarga")
            self.current_ui.texto7.setMaximumHeight(50)
            self.current_ui.texto7.setProperty("estadoVisual", "error")
            

        if error is None:
            print(f"[RECARGA] Fallo recarga: {motivo}")
            return

        print(f"[RECARGA] Fallo recarga: {motivo}. Error: {error}")
        traceback.print_exception(type(error), error, error.__traceback__)

    def _conectar_puerto_recarga(self, *args) -> None:
        lista_puertos = self._combo_puertos_actual()
        puerto = lista_puertos.currentData() if lista_puertos is not None else None
        if not puerto:
            self._fallo_recarga("No hay puerto seleccionado")
            return

        try:
            self.arduino.conectar(puerto, 115200)
        except Exception as e:
            self._fallo_recarga(f"No se pudo conectar al puerto {puerto}", e)

    def _leer_serial_recarga(self) -> None:
        if not isinstance(self.current_ui, RecargaWindow):
            return

        while True:
            linea = self.arduino.leer_linea()
            if not linea:
                break

            if linea.lower().startswith("sldo,"):
                self._procesar_saldo_recarga(linea)
            elif linea.startswith("ok,"):
                self._procesar_respuesta_recarga(linea)
            elif linea == "st":
                self._limpiar_interfaz_por_retiro_tarjeta()
            elif linea.lower().startswith("error"):
                self._fallo_recarga(f"Arduino reporto error: {linea}")
                    
    def _procesar_saldo_recarga(self, linea: str) -> None:
        ui = self.current_ui

        try:
            saldo = self._parsear_trama_saldo(linea)
            if not saldo:
                self._fallo_recarga(f"Trama sldo incompleta: {linea}")
                return

            pendiente = self._recarga_en_curso
            if (pendiente and saldo['uid'] == pendiente['uid']
                    and int(saldo['saldo_centavos']) == pendiente['objetivo']):
                self._procesar_respuesta_recarga(
                    f"ok,{pendiente['uid']},{pendiente['objetivo']},saldo_verificado"
                )
                return

            tipo_fisico = str(
                saldo["tipo_fisico"] or ""
            ).strip().upper()

            self.tipo_actual = tipo_fisico
            self.uid_actual = saldo["uid"]
            self.nombre_actual = saldo["nombre"]
            self.saldo_actual_centavos = int(saldo["saldo_centavos"])

            ui.texto4.setText(self.uid_actual or "-")
            ui.texto5.setText(self.nombre_actual or "-")
            ui.texto1.setText(f"${self.saldo_actual_centavos / 100:.2f}")
            
            if self.tipo_actual in ("KI", "DE"):
                self._bloquear_recarga_operador()
                return

            tipo_desde_tarjeta = ""

            if tipo_fisico == "NO":
                tipo_desde_tarjeta = "Normal"
            elif tipo_fisico == "EU":
                tipo_desde_tarjeta = "Preferencial"
            

            tarjeta_db = self.recarga_model.obtener_tarjeta_por_uid(self.uid_actual)
            
            if tarjeta_db:
                tipo_bd = str(
                    tarjeta_db["tipo_tarjeta"] or ""
                ).strip().lower()

                if (
                    tipo_bd in {"ki", "ope", "operador", "de", "despachador"}
                    or "operador" in tipo_bd
                    or "despachador" in tipo_bd
                ):
                    self.tipo_actual = (
                        "DE"
                        if tipo_bd == "de" or "despachador" in tipo_bd
                        else "KI"
                    )
                    self._bloquear_recarga_operador()
                    return

            if tarjeta_db:
                ui.texto6.setText(tipo_desde_tarjeta or tarjeta_db["tipo_tarjeta"])

                if int(tarjeta_db["en_lista_negra"]) == 1:
                    self._aplicar_bloqueo_lista_negra_recarga(True)
                    return
                else:
                    self._aplicar_bloqueo_lista_negra_recarga(False)

               
                self._actualizar_estado_vencimiento_tarjeta(tarjeta_db)

            else:
                ui.texto6.setText(tipo_desde_tarjeta or "No registrada")
                self.tarjeta_vencida = False
                self._aplicar_bloqueo_lista_negra_recarga(False)

            self._preview_saldo_nuevo()

        except Exception as e:
            self._fallo_recarga(f"No se pudo procesar la linea de saldo: {linea}", e)

    def _procesar_respuesta_recarga(self, linea: str) -> None:
        ui = self.current_ui

        try:
            partes = linea.split(",")
            if len(partes) < 4:
                self._fallo_recarga(f"Respuesta de recarga incompleta: {linea}")
                return

            _, uid, nuevo_saldo_centavos, folio = partes[:4]
            pendiente = self._recarga_en_curso
            if (not pendiente or self._normalizar_uid(uid) != pendiente['uid']
                    or int(nuevo_saldo_centavos) != pendiente['objetivo']):
                return
            self.monto_pendiente_centavos = pendiente['monto']
            self.nombre_actual = pendiente['nombre']
            self.oficina_recarga_actual = pendiente['oficina']
            nuevo_saldo = int(nuevo_saldo_centavos) / 100
            monto = self.monto_pendiente_centavos / 100

            try:
                self.recarga_model.guardar_recarga_flexible(
                    uid=uid,
                    username=self.current_username,
                    monto=monto,
                    nuevo_saldo=nuevo_saldo,
                    nombre_pasajero=self.nombre_actual,
                    oficina=self.oficina_recarga_actual,
                    referencia=f"Folio: {folio}"
                )

            except Exception as error:
                print(f"[RECARGA] ERROR AL GUARDAR EN SQLITE: {error}")
                raise

            print(f"[RECARGA] Guardada localmente: UID={uid}")
            self._recarga_en_curso = None
            from core.database import DATABASE_PATH, get_connection

            print(f"[RECARGA] BASE REAL: {DATABASE_PATH.resolve()}")

            with get_connection() as conn:
                recargas = conn.execute(
                    "SELECT COUNT(*) FROM recargas"
                ).fetchone()[0]

                pendientes = conn.execute(
                    """
                    SELECT COUNT(*) FROM sync_queue
                    WHERE event_type = 'recarga_tarjeta'
                    AND status IN ('pending', 'error')
                    """
                ).fetchone()[0]

            print(f"[RECARGA] Total guardadas: {recargas}")
            print(f"[RECARGA] Pendientes de subir: {pendientes}")
            print(f"[RECARGA] Monto: {monto}")
            print(f"[RECARGA] Saldo nuevo: {nuevo_saldo}")

            QTimer.singleShot(0, self._sincronizar_pendientes)

            self.saldo_actual_centavos = int(nuevo_saldo_centavos)
            ui.texto1.setText(f"${nuevo_saldo:.2f}")
            ui.texto2.setText(f"${nuevo_saldo:.2f}")
            
            ui.texto7.clear()
            ui.texto7.setMaximumHeight(80)
            
            mensaje = (
                "Descuento exitoso"
                if self.monto_pendiente_centavos < 0
                else "Recarga Exitosa"
            )
            
            if hasattr(ui.texto7, "setPlainText"):
                ui.texto7.setPlainText(mensaje)
            else:
                                ui.texto7.setText(mensaje)
                
            ui.texto7.setProperty("estadoVisual", "success")
            
            ui.texto7.repaint()
            QTimer.singleShot(2500, self._limpiar_mensaje_recarga_exitosa)
            

            monto = self._campo_monto_recarga()
            if monto is not None:
                monto.clear()

            self.monto_pendiente_centavos = 0

            tarjeta_db = self.recarga_model.obtener_tarjeta_por_uid(self.uid_actual)
            if tarjeta_db:
                tipo_bd = str(
                    tarjeta_db["tipo_tarjeta"] or ""
                ).strip().lower()

                if (
                    tipo_bd in {"ki", "ope", "operador", "de", "despachador"}
                    or "operador" in tipo_bd
                    or "despachador" in tipo_bd
                ):
                    self.tipo_actual = (
                        "DE" if tipo_bd == "de" or "despachador" in tipo_bd else "KI"
                    )
                    self._bloquear_recarga_operador()
                    return
            if tarjeta_db:
                ui.texto6.setText(tarjeta_db["tipo_tarjeta"])
            self._actualizar_estado_vencimiento_tarjeta(tarjeta_db)

        except Exception as e:
            self._fallo_recarga(f"No se pudo procesar la respuesta de recarga: {linea}", e)

    def _campo_monto_recarga(self):
        if self.current_ui is None:
            return None

        return getattr(
            self.current_ui,
            "texto3",
            getattr(self.current_ui, "lineEdit", None)
        )

    def _texto_monto_recarga(self) -> str:
        monto = self._campo_monto_recarga()
        if monto is None:
            return ""

        if hasattr(monto, "toPlainText"):
            return monto.toPlainText().strip().replace(",", ".")

        return monto.text().strip().replace(",", ".")

    def _preview_saldo_nuevo(self, *args) -> None:
        ui = self.current_ui

        if not isinstance(ui, RecargaWindow):
            return

        if self.tipo_actual in ("KI", "DE"):
            self._bloquear_recarga_operador()
            return

        ui.botonrecargar.setEnabled(False)

        if not self.uid_actual:
            return

        if self.tarjeta_bloqueada or self.tarjeta_vencida:
            return

        texto = self._texto_monto_recarga()

        # Limpiar solamente los avisos de esta validación.
        if ui.texto7.text().startswith(
            ("No se puede exceder", "No puedes descontar")
        ):
            ui.texto7.clear()
            ui.texto7.setProperty("estadoVisual", "")

        if not texto:
            ui.texto2.setText(
                f"${self.saldo_actual_centavos / 100:.2f}"
            )
            return

        try:
            monto = float(texto)

            if not (-42949672.95 <= monto <= 42949672.95):
                raise ValueError

            centavos = round(monto * 100)
        except ValueError:
            ui.texto2.setText("Monto inválido")
            return

        nuevo = self.saldo_actual_centavos + centavos
        ui.texto2.setText(f"${nuevo / 100:.2f}")

        mensaje = ""

        if centavos > 0 and nuevo > 40000:
            disponible = max(
                0, 40000 - self.saldo_actual_centavos
            )
            mensaje = (
                "No se puede exceder el saldo de $400.00. "
                f"Puedes recargar hasta ${disponible / 100:.2f}."
            )
        elif nuevo < 0:
            mensaje = (
                "No puedes descontar más del saldo disponible."
            )

        if mensaje:
            ui.texto7.setText(mensaje)
            ui.texto7.setWordWrap(True)
            ui.texto7.setMaximumHeight(80)
            ui.texto7.setProperty("estadoVisual", "error")
            return

        ui.botonrecargar.setEnabled(centavos != 0)
    
    def _ejecutar_recarga(self) -> None:
        from core.carga import cargando
        with cargando(self.current_window, "Guardando recarga y esperando al lector…",
                      pendiente=lambda: self._recarga_en_curso is not None and self.current_ui.texto7.property("estadoVisual") != "error"):
            if self._recarga_en_curso:
                QMessageBox.warning(
                    self.current_window, 'Recarga pendiente',
                    'La recarga anterior aún no está comprobada y guardada. '
                    'Retira y acerca esa tarjeta para consultar su saldo antes de continuar. '
                    'No repitas la recarga ni cierres la aplicación.'
                )
                return
            ui = self.current_ui

            if not self.uid_actual:
                QMessageBox.warning(self.current_window, "Error", "Primero acerca una tarjeta.")
                return

            tarjeta_db = self.recarga_model.obtener_tarjeta_por_uid(
                self.uid_actual
            )
            es_operador = self.tipo_actual in ("KI", "DE")

            if tarjeta_db:
                tipo_bd = str(
                    tarjeta_db["tipo_tarjeta"] or ""
                ).strip().lower()

                es_operador = (
                    es_operador
                    or tipo_bd in {
                        "ki", "ope", "operador",
                        "de", "despachador"
                    }
                    or "operador" in tipo_bd
                    or "despachador" in tipo_bd
                )

                if tipo_bd == "de" or "despachador" in tipo_bd:
                    self.tipo_actual = "DE"

            if es_operador:
                if self.tipo_actual != "DE":
                    self.tipo_actual = "KI"

                self._bloquear_recarga_operador()

                QMessageBox.warning(
                    self.current_window,
                    "Tarjeta de personal",
                    "La tarjeta de Despachador no admite recargas."
                    if self.tipo_actual == "DE"
                    else "La tarjeta de operador no admite recargas.",
                )
                return

            if tarjeta_db and int(tarjeta_db["en_lista_negra"]) == 1:
                self._aplicar_bloqueo_lista_negra_recarga(True)
                QMessageBox.warning(
                    self.current_window,
                    "Tarjeta en lista negra",
                    "La tarjeta está en lista negra y no se puede recargar."
                )
                return
            else:
                self._aplicar_bloqueo_lista_negra_recarga(False)

    
            self._actualizar_estado_vencimiento_tarjeta(tarjeta_db)
            if self.tarjeta_vencida:
                QMessageBox.warning(
                    self.current_window,
                    "Tarjeta vencida",
                    "La tarjeta está vencida y no se puede recargar."
                )
                return
        
            oficina = self._oficina_seleccionada_recarga()
        
            if not oficina:
                QMessageBox.warning(
                    self.current_window,
                    "Oficina requerida",
                    "Selecciona una oficina."
                )
                return
            self.oficina_recarga_actual = oficina

            texto_monto = self._texto_monto_recarga()
            if not texto_monto:
                QMessageBox.warning(self.current_window, "Error", "Captura el monto.")
                return

            try:
                monto = float(texto_monto)
            except ValueError:
                QMessageBox.warning(self.current_window, "Error", "Monto invalido.")
                return

                    # También rechaza valores no válidos como infinito o NaN.
            if not (-42949672.95 <= monto <= 400.00):
                QMessageBox.warning(
                    self.current_window,
                    "Monto inválido",
                    "Para recargar, captura hasta $400.\n"
                    "Para descontar, escribe una cantidad negativa."
                )
                return

            centavos = round(monto * 100)

            if centavos == 0:
                QMessageBox.warning(
                    self.current_window, "Error",
                    "El monto debe ser diferente de cero."
                )
                return

            nuevo_saldo = self.saldo_actual_centavos + centavos

            if nuevo_saldo < 0:
                QMessageBox.warning(
                    self.current_window,
                    "Saldo insuficiente",
                    "No puedes descontar más del saldo disponible."
                )
                return

            # El máximo de $400 aplica solamente al agregar saldo.
            if centavos > 0 and nuevo_saldo > 40000:
                disponible = max(0, 40000 - self.saldo_actual_centavos)

                QMessageBox.warning(
                    self.current_window,
                    "Saldo máximo permitido",
                    "No se puede exceder el saldo máximo de $400.00.\n\n"
                    f"Saldo actual: ${self.saldo_actual_centavos / 100:.2f}\n"
                    f"Intentas recargar: ${centavos / 100:.2f}\n"
                    f"Puedes recargar hasta: ${disponible / 100:.2f}"
                )
                return

            if centavos < 0:
                respuesta = QMessageBox.question(
                    self.current_window,
                    "Confirmar descuento",
                    f"¿Descontar ${abs(centavos) / 100:,.2f}?\n"
                    f"Tarjeta: {self.uid_actual}\n"
                    f"Saldo resultante: ${nuevo_saldo / 100:,.2f}",
                    QMessageBox.Yes | QMessageBox.No,
                    QMessageBox.No
                )
                if respuesta != QMessageBox.Yes:
                    return

            self.monto_pendiente_centavos = centavos

            try:
                accion = "di" if centavos < 0 else "rc"
                comando = f"{accion},{self.uid_actual},{abs(centavos)}"
                self._recarga_en_curso = {
                    'uid': self.uid_actual, 'objetivo': nuevo_saldo,
                    'monto': centavos, 'nombre': self.nombre_actual,
                    'oficina': self.oficina_recarga_actual,
                }
                self.arduino.enviar_linea(comando)
                ui.texto7.setText("Enviando recarga...")
                ui.texto7.setMaximumHeight(40)
                ui.texto7.setProperty("estadoVisual", "info")
            
            
            except Exception as e:
                self._fallo_recarga("No se pudo enviar la recarga al Arduino", e)
                QMessageBox.critical(self.current_window, "Error", f"No se pudo enviar la recarga: {e}")
            
    # =========================
    #         BLOQUEO DE RECARGA OPERADOR
    # =========================
    def _bloquear_recarga_operador(self) -> None:
        if not isinstance(self.current_ui, RecargaWindow):
            return

        ui = self.current_ui

        monto = self._campo_monto_recarga()

        if monto is not None:
            estado_anterior = monto.blockSignals(True)
            monto.clear()
            monto.blockSignals(estado_anterior)
            monto.setEnabled(False)

        self.monto_pendiente_centavos = 0

        ui.texto6.setText("Despachador" if self.tipo_actual == "DE" else "Operador")
        ui.texto2.setText(
            f"${self.saldo_actual_centavos / 100:.2f}"
        )

        ui.botonrecargar.setEnabled(False)

        ui.texto7.setText(
            "La tarjeta de Despachador no admite recargas."
            if self.tipo_actual == "DE"
            else "La tarjeta de operador no admite recargas."
        )

        ui.texto7.setProperty("estadoVisual", "warning")
    
    
    # =========================
    #           ALTA
    # =========================
    def _hay_internet_para_alta(self) -> bool:
        try:
            return self.sync_service.ping()
        except Exception:
            return False


    def _mostrar_error_alta_sin_internet(self) -> None:
        ui = self.current_ui
        ui.labelEstadoConexion.setProperty("estadoVisual", "error")
        ui.labelEstadoConexion.setText(
            "Sin conexion"
        )
        if hasattr(ui, "mensajeInternet"):
            ui.mensajeInternet.setText("Sin conexion a internet, intente mas tarde.")
            ui.mensajeInternet.setVisible(True)
        self._set_alta_inputs_enabled(False)


    def _ocultar_error_alta_sin_internet(self) -> None:
        if not isinstance(self.current_ui, (AltaWindow, Ui_AltaOWindow)):
            return

        if hasattr(self.current_ui, "mensajeInternet"):
            self.current_ui.mensajeInternet.setText("")
            self.current_ui.mensajeInternet.setVisible(False)


    def _set_alta_inputs_enabled(self, enabled: bool) -> None:
        if not isinstance(self.current_ui, (AltaWindow, Ui_AltaOWindow)):
            return

        ui = self.current_ui
        for nombre_widget in (
            "textonombre",
            "textocurp",
            "textofechanacimiento",
            "textovigencia",
            "pushButton",
            "normal",
            "preferencial",
            "calendario",
            "botonsubir",
            "botontomar",
            "botonguardar",
        ):
            if hasattr(ui, nombre_widget):
                getattr(ui, nombre_widget).setEnabled(enabled)
                
    
    def _limpiar_forulario_alta(self) -> None:
        if not isinstance(self.current_ui, (AltaWindow, Ui_AltaOWindow)):
            return
        
        ui = self.current_ui
        
        self.uid_alta_actual = ""
        self.alta_pendiente = None
        self.foto_alta_path = ""
        
        widgets_con_senales = [getattr(ui, nombre) for nombre in (
            "textonombre", "textocurp", "textofechanacimiento", "textovigencia",
            "calendario", "normal", "preferencial"
        ) if hasattr(ui, nombre)]
        
        for widget in widgets_con_senales:
            widget.blockSignals(True)
            
        try:
            ui.textonombre.clear()
            ui.textocurp.clear()
            ui.textofechanacimiento.clear()
            
            if hasattr(ui, "curpstatus"):
                ui.curpstatus.clear()
                
            ui.normal.setChecked(True)
            if hasattr(ui, "preferencial"):
                ui.preferencial.setChecked(False)
            
            ui.calendario.setSelectedDate(QDate.currentDate())
            ui.textovigencia.setPlainText(
                ui.calendario.selectedDate().toString("dd-MM-yyyy")
            )
            
            ui.fotoimagen.clear()
            ui.fotoimagen.setText("Sin foto")
            if isinstance(ui, AltaWindow) and hasattr(ui, "label_33"):
                ui.label_33.setText("Sin archivo seleccionado")
            if isinstance(ui, Ui_AltaOWindow):
                ui.label_5.setText("Sin archivo seleccionado")
            
            ui.textonombre.setFocus()
            
        finally:
            for widget in widgets_con_senales:
                widget.blockSignals(False)

    def _cancelar_formulario_alta(self) -> None:
        if self.alta_pendiente:
            QMessageBox.warning(
                self.current_window, "Alta en proceso",
                "Espera la confirmación de la tarjeta antes de cancelar."
            )
            return
        self._regresar_pantalla_anterior()
    
     

    def _seleccionar_foto_alta(self) -> None:
        if not isinstance(self.current_ui, (AltaWindow, Ui_AltaOWindow)):
            return

        ui = self.current_ui

        archivo, _ = QFileDialog.getOpenFileName(
            self.current_window,
            "Seleccionar foto",
            "",
            "Imagenes (*.png *.jpg *.jpeg *.bmp)"
        )

        if not archivo:
            return

        origen = Path(archivo)
        if not origen.is_file():
            QMessageBox.warning(
                self.current_window,
                "Foto",
                "El archivo seleccionado no está disponible.",
            )
            return

        self.foto_alta_path = str(origen)

        pixmap = QPixmap(str(origen))
        ui.fotoimagen.setPixmap(
            pixmap.scaled(200, 200)
        )
        if isinstance(ui, Ui_AltaOWindow):
            ui.label_5.setText(origen.name)
        elif hasattr(ui, "label_33"):
            ui.label_33.setText(origen.name)


    def _limpiar_foto_alta(self) -> None:
        if not isinstance(self.current_ui, (AltaWindow, Ui_AltaOWindow)):
            return

        self.foto_alta_path = ""
        self.current_ui.fotoimagen.clear()
        self.current_ui.fotoimagen.setText("Sin foto")
        if isinstance(self.current_ui, Ui_AltaOWindow):
            self.current_ui.label_5.setText("Sin archivo seleccionado")
        elif hasattr(self.current_ui, "label_33"):
            self.current_ui.label_33.setText("Sin archivo seleccionado")


    def _mostrar_calendario_nacimiento(self) -> None:
        if not isinstance(self.current_ui, (AltaWindow, Ui_AltaOWindow)):
            return

        dialog = QDialog(self.current_window)
        dialog.setWindowTitle("Seleccionar fecha")

        layout = QVBoxLayout(dialog)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(8)
        calendario = QCalendarWidget(dialog)
        layout.addWidget(calendario)

        def seleccionar_fecha():
            fecha = calendario.selectedDate()
            self.current_ui.textofechanacimiento.setPlainText(
                fecha.toString("dd-MM-yyyy")
            )
            dialog.accept()

        calendario.clicked.connect(seleccionar_fecha)

        dialog.exec()
        
    

    def _configurar_alta_window(self) -> None:
        ui = self.current_ui

        self.uid_alta_actual = ""
        self.alta_pendiente = None

        ui.textonombre.clear()
        ui.textovigencia.clear()
        
        ui.textocurp.textChanged.connect(self._limitar_curp_alta)
        ui.textonombre.textChanged.connect(self._solo_letras_espacios_nombre_alta)
        ui.textofechanacimiento.textChanged.connect(self._formatear_fecha_nacimiento_alta)
        
        if hasattr(ui, "curpstatus"):
            ui.curpstatus.setProperty("estadoVisual", "error")
            if hasattr(ui.curpstatus, "setPlainText"):
                ui.curpstatus.setPlainText("")
            else:
                ui.curpstatus.setText("")

        self._ocultar_error_alta_sin_internet()
        self._set_alta_inputs_enabled(False)

        ui.textovigencia.setReadOnly(True)
        ui.normal.setChecked(True)
        
        self.foto_alta_path = ""
        
        ui.fotoimagen.setText("Sin foto")
        ui.fotoimagen.setScaledContents(True)
  
        ui.botonsubir.clicked.connect(self._seleccionar_foto_alta)
        if hasattr(ui, "botontomar"):
            ui.botontomar.clicked.connect(self._limpiar_foto_alta)

        # ESTE ES EL QUE TE FALTA
        if hasattr(ui, "pushButton"):
            ui.pushButton.clicked.connect(self._mostrar_calendario_nacimiento)

        icono_calendario = Path(__file__).resolve().parent.parent / "assets" / "calendario.png"

        if hasattr(ui, "pushButton") and icono_calendario.exists():
            ui.pushButton.setIcon(QIcon(str(icono_calendario)))
            ui.pushButton.setIconSize(QSize(24, 24))
            ui.pushButton.setText("")
        elif hasattr(ui, "pushButton"):
            print(f"No se encontró el icono: {icono_calendario}")

        ui.labelEstadoConexion.setProperty("estadoVisual", "info")
        ui.labelEstadoConexion.setText("● Listo")
        

        self._actualizar_vigencia_desde_calendario()

        ui.calendario.selectionChanged.connect(self._actualizar_vigencia_desde_calendario)
        ui.botonguardar.clicked.connect(self._ejecutar_alta)

        lista_puertos = self._combo_puertos_actual()
        if lista_puertos is not None:
            lista_puertos.currentIndexChanged.connect(self._conectar_puerto_alta)

        if self.alta_timer is None:
            self.alta_timer = QTimer()
            self.alta_timer.timeout.connect(self._leer_serial_alta)

        self._conectar_puerto_alta()
        self.alta_timer.start(300)
        

    def _actualizar_vigencia_desde_calendario(self) -> None:
        if not isinstance(self.current_ui, (AltaWindow, Ui_AltaOWindow)):
            return

        ui = self.current_ui
        fecha = ui.calendario.selectedDate()
        ui.textovigencia.setPlainText(f"{fecha.toString('dd-MM-yyyy')}")

    def _conectar_puerto_alta(self, *args) -> None:
        lista_puertos = self._combo_puertos_actual()
        puerto = lista_puertos.currentData() if lista_puertos is not None else None

        if not puerto:
            return

        try:
            self.arduino.conectar(puerto, 115200)
        except Exception as e:
            print(f"[ALTA] Error al conectar al puerto {puerto}: {e}")
            traceback.print_exception(type(e), e, e.__traceback__)
            QMessageBox.critical(
                self.current_window,
                "Error",
                f"No se pudo conectar al puerto {puerto}: {e}"
            )

    def _leer_serial_alta(self, mostrar_errores: bool = True) -> None:
        if not isinstance(self.current_ui, (AltaWindow, Ui_AltaOWindow)):
            return

        ui = self.current_ui

        while True:
            linea = self.arduino.leer_linea()
            if not linea:
                break

            print("[ALTA]", linea)
            linea_minusculas = linea.lower()

            if linea_minusculas.startswith("sldo,"):
                try:
                    saldo = self._parsear_trama_saldo(linea)
                    if not saldo:
                        print(f"[ALTA] Trama sldo incompleta: {linea}")
                        continue

                    uid = saldo["uid"]
                    saldo_centavos = saldo["saldo_centavos"]
                    nombre = saldo["nombre"]
                    uid_detectada = self._normalizar_uid(uid)
                    if not uid_detectada:
                        print(f"[ALTA] UID invalida en trama sldo: {uid}")
                        continue

                    self.uid_alta_actual = uid_detectada

                    print(
                        "[ALTA] Tarjeta detectada "
                        f"UID={self.uid_alta_actual} "
                        f"saldo_centavos={saldo_centavos} "
                        f"nombre={nombre}"
                    )

                    if not ui.textonombre.toPlainText().strip() and nombre.strip() and nombre.strip() != "-":
                        ui.textonombre.setPlainText(nombre.strip())
                        
                        
                except Exception as e:
                    print(f"[ALTA] Error completo al procesar linea: {linea}")
                    traceback.print_exception(type(e), e, e.__traceback__)

            elif linea_minusculas.startswith("uid,"):
                try:
                    _, uid = linea.split(",", 1)
                    uid_detectada = self._normalizar_uid(uid)
                    if not uid_detectada:
                        print(f"[ALTA] UID invalida: {uid.strip()}")
                        continue

                    self.uid_alta_actual = uid_detectada
                    print(f"[ALTA] Tarjeta detectada UID={self.uid_alta_actual}")

                except Exception as e:
                    print(f"[ALTA] Error completo al procesar UID: {linea}")
                    traceback.print_exception(type(e), e, e.__traceback__)

            elif linea_minusculas == "ok,alta":
                if not self.alta_pendiente:
                    print("[ALTA] Llego ok,alta pero no hay alta pendiente.")
                    continue

                try:
                    uid = self.alta_pendiente["uid"]
                    nombre = self.alta_pendiente.get(
                        "alias_tarjeta",
                        self.alta_pendiente["nombre_pasajero"],
                    )

                    comando_nombre = f"nm,{uid},{nombre}"
                    print("[ALTA] Enviando nombre:", comando_nombre)
                    self.arduino.enviar_linea(comando_nombre)

                    self.alta_pendiente["fase"] = "esperando_nombre"

                except Exception as e:
                    print(f"[ALTA] Error al enviar nombre: {e}")
                    traceback.print_exception(type(e), e, e.__traceback__)
                    self.alta_pendiente = None

                    if mostrar_errores:
                        QMessageBox.critical(
                            self.current_window,
                            "Error",
                            f"La tarjeta se dio de alta, pero no se pudo enviar el nombre: {e}"
                        )

            elif linea_minusculas == "ok,nombre":
                if not self.alta_pendiente:
                    print("[ALTA] Llego ok,nombre pero no hay alta pendiente.")
                    continue

                if not self._guardar_alta_local_confirmada():
                    return

                QMessageBox.information(
                    self.current_window,
                    "Alta",
                    "Tarjeta dada de alta correctamente."
                )

            elif linea_minusculas.startswith("ok,"):
                # compatibilidad para lecturas tipo:
                # ok,300426235959,0413243AC75A80,juan
                try:
                    partes = linea.split(",")
                    if len(partes) >= 3:
                        uid_detectada = self._normalizar_uid(partes[2])
                        if not uid_detectada:
                            print(f"[ALTA] UID invalida en trama ok: {partes[2].strip()}")
                            continue

                        self.uid_alta_actual = uid_detectada
                        nombre = partes[3].strip() if len(partes) >= 4 else ""

                        print(
                            "[ALTA] Tarjeta detectada "
                            f"UID={self.uid_alta_actual} "
                            f"desde_trama={linea}"
                        )

                        if not ui.textonombre.toPlainText().strip() and nombre:
                            ui.textonombre.setPlainText(nombre)
                    else:
                        print(f"[ALTA] Trama ok incompleta: {linea}")

                except Exception as e:
                    print(f"[ALTA] Error completo al procesar ok: {linea}")
                    traceback.print_exception(type(e), e, e.__traceback__)

            elif linea == "st":
                self._limpiar_interfaz_por_retiro_tarjeta()
                continue

            elif linea == "ok":
                # compatibilidad con firmware viejo
                if not self.alta_pendiente:
                    continue

                if not self._guardar_alta_local_confirmada():
                    return

                QMessageBox.information(
                    self.current_window,
                    "Alta",
                    "Tarjeta dada de alta correctamente."
                )

            elif linea_minusculas.startswith("error"):
                errores_de_lectura_automatica = {
                    "error,estado_tisc4",
                    "error,estado_tisc3",
                    "error,estado_tisc2",
                    "error,vigencia0",
                    "error,leer_saldo",
                    "error,leer_saldo2",
                }

                if linea_minusculas in errores_de_lectura_automatica:
                    print(f"[ALTA] Error automatico de verSaldo ignorado durante alta: {linea}")
                    continue

                if "error en las 3 aplicaciones" in linea_minusculas:
                    if self.alta_pendiente:
                        reintentos = self.alta_pendiente.get("reintentos_alta", 0)
                        comando = self.alta_pendiente.get("comando_alta")

                        if comando and reintentos < 2:
                            self.alta_pendiente["reintentos_alta"] = reintentos + 1

                            print(
                                "[ALTA] Reintentando alta por error en aplicaciones "
                                f"intento {reintentos + 1}: {comando}"
                            )

                            QTimer.singleShot(
                                1000,
                                lambda c=comando: self.arduino.enviar_linea(c)
                            )
                            continue
                    
                if not self.alta_pendiente:
                    print(f"[ALTA] Error de lectura ignorado sin alta pendiente: {linea}")
                    continue

                fase = self.alta_pendiente.get("fase", "desconocida")
                self.alta_pendiente = None

                if mostrar_errores:
                    QMessageBox.warning(
                        self.current_window,
                        "Error",
                        f"El Arduino rechazo la alta en fase '{fase}': {linea}\n\n"
                        "No se guardo la tarjeta en la base local porque el alta "
                        "solo se persiste cuando Arduino confirma completamente."
                    )
                    

    def _esperar_uid_alta_disponible(self) -> bool:
        print("[ALTA] No hay UID guardado. Solicitando UID real al Arduino con: uid")
        try:
            self.arduino.enviar_linea("uid")
        except Exception as e:
            print(f"[ALTA] No se pudo solicitar UID al Arduino: {e}")

        limite = time.monotonic() + 5.0
        while time.monotonic() < limite:
            self._leer_serial_alta(False)
            if self.uid_alta_actual:
                print(f"[ALTA] UID real detectada desde serial: {self.uid_alta_actual}")
                return True

            QCoreApplication.processEvents()
            time.sleep(0.05)

        print("[ALTA] No se recibio UID real desde serial.")
        return False

    def _guardar_alta_local_confirmada(self) -> bool:
        if not self.alta_pendiente:
            return True

        try:
            payload = {
                "uid": self.alta_pendiente["uid"],
                "nombre_pasajero": self.alta_pendiente["nombre_pasajero"],
                "tipo": self.alta_pendiente["tipo"],
                "vigencia": self.alta_pendiente["vigencia"],
                "curp": self.alta_pendiente.get("curp", ""),
                "fecha_nacimiento": self.alta_pendiente.get("fecha_nacimiento", ""),
                "foto": self.alta_pendiente.get("foto", ""),
            }

            self.alta_model.guardar_alta_local(**payload)

            print(
                "[ALTA] Alta guardada en DB local "
                f"UID={payload['uid']}"
            )

            self.alta_pendiente = None
            self._sincronizar_pendientes()
            self._limpiar_forulario_alta()
            return True

        except Exception as e:
            print(f"[ALTA] Error al guardar alta en DB local: {e}")
            traceback.print_exception(type(e), e, e.__traceback__)
            QMessageBox.critical(
                self.current_window,
                "Error",
                f"El Arduino confirmo el alta, pero no se pudo guardar en la base local: {e}"
            )
            return False
        
     
    def _mostrar_error_uid_alta_no_disponible(self) -> None:
        QMessageBox.warning(
            self.current_window,
            "UID no disponible",
            "No hay una UID real disponible para dar de alta la tarjeta.\n\n"
            "La app no puede inventar una UID. Con el firmware actual no se "
            "puede obtener la UID de una tarjeta nueva si el Arduino no "
            "responde al comando 'uid' con una trama 'uid,<UID>'.\n\n"
            "Acerca o lee una tarjeta hasta que la app reciba una UID real "
            "por serial y vuelve a intentar."
        )

    def _set_curp_status_alta(self, mensaje: str, *, error: bool = False) -> None:
        if not isinstance(self.current_ui, (AltaWindow, Ui_AltaOWindow)):
            return

        if not hasattr(self.current_ui, "curpstatus"):
            return

        color = "error" if error else "success"
        self.current_ui.curpstatus.setProperty("estadoVisual", color)
        self.current_ui.curpstatus.setText(mensaje)

    def _ejecutar_alta(self) -> None:
        if not isinstance(self.current_ui, (AltaWindow, Ui_AltaOWindow)):
            return

        from core.carga import cargando
        with cargando(self.current_window, "Guardando alta de tarjeta…",
                      pendiente=lambda: self.alta_pendiente is not None):
            ui = self.current_ui

            self.alta_pendiente = None

            self._leer_serial_alta(False)

            if not self.uid_alta_actual and not self._esperar_uid_alta_disponible():
                self._mostrar_error_uid_alta_no_disponible()
                return

            nombre_pasajero_completo = re.sub(
                r"\s+",
                " ",
                ui.textonombre.toPlainText().strip(),
            )
            alias_tarjeta = self._limpiar_alias_para_arduino(nombre_pasajero_completo)

            if not nombre_pasajero_completo or not alias_tarjeta:
                QMessageBox.warning(
                    self.current_window,
                    "Error",
                    "Captura el nombre."
                )
                return

            curp_alta = ui.textocurp.toPlainText().strip().upper()

            if not curp_alta or curp_alta == "-":
                QMessageBox.warning(
                    self.current_window,
                    "CURP requerida",
                    "Captura la CURP."
                )
                return

            # 1. Validar primero en la base local
            try:
                curp_local = self.alta_model.buscar_curp_local(curp_alta)
            except Exception as e:
                QMessageBox.critical(
                    self.current_window,
                    "Error",
                    f"No se pudo validar la CURP en la base local:\n\n{e}"
                )
                return

            if curp_local:
                self._set_curp_status_alta(
                    f"La CURP {curp_alta} ya esta registrado.",
                    error=True
                )
                return

            # 2. Validar también en el servidor
                    # Si no responde el servidor, se permite guardar localmente.
            try:
                curp_servidor = (
                    self.alta_model.buscar_curp_servidor(curp_alta)
                )
            except Exception:
                curp_servidor = None

            uid_alta = self._normalizar_uid(self.uid_alta_actual)

            if not uid_alta:
                self._mostrar_error_uid_alta_no_disponible()
                return
        
            from core.database import get_connection
            from core.lista_negra_local import bloqueo_local

            with get_connection() as connection:
                existe_uid = connection.execute(
                    "SELECT 1 FROM tarjetas WHERE uid = ?",
                    (uid_alta,),
                ).fetchone()

            if existe_uid or bloqueo_local(uid_alta):
                QMessageBox.warning(
                    self.current_window,
                    "Tarjeta registrada",
                    "La tarjeta ya existe o está bloqueada. "
                    "Usa la operación correspondiente.",
                )
                return
        
            if isinstance(ui, Ui_AltaOWindow):
                no_tarjeta = "KI"

            if curp_servidor:
                self._set_curp_status_alta(
                    f"La CURP {curp_alta} ya esta registrado.",
                    error=True
                )
                return


            fecha = ui.calendario.selectedDate()
            self._set_curp_status_alta(
                f"CURP {curp_alta} disponible.",
                error=False
            )
            vigtarifa = fecha.toString("ddMMyy")
            hora_actual = QDateTime.currentDateTime().toString("HHmmss")
            vigencia12 = vigtarifa + hora_actual

            if len(vigtarifa) != 6 or not vigtarifa.isdigit():
                QMessageBox.warning(
                    self.current_window,
                    "Error",
                    "VIGTARIFA invalida."
                )
                return

            if len(vigencia12) != 12 or not vigencia12.isdigit():
                QMessageBox.warning(
                    self.current_window,
                    "Error",
                    "VIGENCIA12 invalida."
                )
                return

            uid_alta = self._normalizar_uid(self.uid_alta_actual)

            if not uid_alta:
                self._mostrar_error_uid_alta_no_disponible()
                return

            if isinstance(ui, Ui_AltaOWindow):
                tipo_local = "DE" if ui.normal.isChecked() else "KI"
                no_tarjeta = tipo_local
            elif hasattr(ui, "preferencial") and ui.preferencial.isChecked():
                no_tarjeta = "EU"
                tipo_local = "EU"
            else:
                no_tarjeta = "NO"
                tipo_local = "NO"

            id_tipo_tarjeta = "02"
            id_tarifa = "01"
            alias_tarjeta = self._ajustar_alias_para_comando_alta(
                uid_alta,
                alias_tarjeta,
                no_tarjeta,
                id_tipo_tarjeta,
                id_tarifa,
                vigtarifa,
                vigencia12,
            )

            if not alias_tarjeta:
                QMessageBox.warning(
                    self.current_window,
                    "Error",
                    "El nombre queda vacio al preparar el comando para Arduino."
                )
                return

            comando = (
                f"al,{uid_alta},{alias_tarjeta},{no_tarjeta},"
                f"{id_tipo_tarjeta},{id_tarifa},{vigtarifa},{vigencia12}"
            )

            self.alta_pendiente = {
                "uid": uid_alta,
                "nombre_pasajero": nombre_pasajero_completo,
                "alias_tarjeta": alias_tarjeta,
                "tipo": tipo_local,
                "vigencia": vigencia12,
                "curp": curp_alta,
                "fecha_nacimiento": ui.textofechanacimiento.toPlainText().strip(),
                "foto": self.foto_alta_path,
                "fase": "esperando_alta",
                "comando_alta": comando,
                "reintentos_alta": 0,
            }

        

            print("[ALTA] Enviando alta:", comando)
            self.arduino.enviar_linea(comando)
        
        
    # =========================
    # CANCELAR
    # =========================
            
    def _configurar_cancelar_window(self) -> None:
        if not isinstance(self.current_ui, CancelarWindow):
            return

        ui = self.current_ui

        self.uid_cancelar_actual = ""
        self.tipo_cancelar_actual = ""
        self.saldo_cancelar_actual = 0.0
        self.nombre_cancelar_actual = ""

        ui.textonombre.setPlainText("")
        
        ui.textonombre.textChanged.connect(self._solo_letras_espacios_nombre_cancelar)
        
        ui.textouid.setText("-")
        ui.listanegra.setChecked(False)
        ui.textomotivo.setPlainText("")

        ui.botoncancelar.clicked.connect(self._ejecutar_cancelar)
        ui.pushButton.clicked.connect(self._quitar_lista_negra)

        lista_puertos = self._combo_puertos_actual()
        if lista_puertos is not None:
            lista_puertos.currentIndexChanged.connect(self._conectar_puerto_cancelar)

        if self.cancelar_timer is None:
            self.cancelar_timer = QTimer()
            self.cancelar_timer.timeout.connect(self._leer_serial_cancelar)

        self._conectar_puerto_cancelar()
        self.cancelar_timer.start(300)
    
    def _conectar_puerto_cancelar(self, *args) -> None:
        lista_puertos = self._combo_puertos_actual()
        puerto = lista_puertos.currentData() if lista_puertos is not None else None

        if not puerto:
            return

        try:
            self.arduino.conectar(puerto, 115200)
        except Exception as e:
            print(f"[CANCELAR] Error al conectar al puerto {puerto}: {e}")
            
    def _leer_serial_cancelar(self) -> None:
        if not isinstance(self.current_ui, CancelarWindow):
            return

        ui = self.current_ui

        while True:
            linea = self.arduino.leer_linea()
            if not linea:
                break

            print("[CANCELAR]", linea)
            linea_minusculas = linea.lower()

            if linea_minusculas.startswith("sldo,"):
                try:
                    lectura = self._parsear_trama_saldo(linea)

                    if not lectura:
                        continue

                    uid = self._normalizar_uid(
                        lectura["uid"]
                    )
                    saldo = lectura["saldo_centavos"]
                    nombre = lectura["nombre"]

                    self.tipo_cancelar_actual = (
                        lectura["tipo_fisico"]
                    )
                    self.saldo_cancelar_actual = (
                        int(saldo) / 100
                    )
                    if not uid:
                        continue
                    self.uid_cancelar_actual = uid
                    self.nombre_cancelar_actual = nombre.strip()

                    ui.textouid.setText(uid)
                    ui.textonombre.setPlainText(self.nombre_cancelar_actual)

                    try:
                        saldo_valor = int(str(saldo).strip()) / 100
                    except Exception:
                        saldo_valor = 0.0

                    tarjeta = self.cancelar_model.obtener_tarjeta_por_uid(uid)

                    if tarjeta:
                        self._mostrar_datos_tarjeta_cancelar(
                            tarjeta,
                            nombre_fallback=self.nombre_cancelar_actual,
                        )
                        #ui.listanegra.setChecked(bool(tarjeta["en_lista_negra"]))
                        #if bool(tarjeta["en_lista_negra"]):
                         #   ui.textomotivo.setPlainText(tarjeta["motivo_baja"] or "")
                        #else:
                        #    ui.textomotivo.setPlainText("")
                        #nombre_db = (tarjeta["nombre_pasajero"] or "").strip()
                        #if nombre_db:
                        #    self.nombre_cancelar_actual = nombre_db
                        #    ui.textonombre.setPlainText(nombre_db)
                    else:
                        ui.listanegra.setChecked(False)
                        ui.textomotivo.setPlainText("")

                except Exception as e:
                    print(f"[CANCELAR] Error al procesar saldo: {e}")

            elif linea_minusculas.startswith("uid,"):
                try:
                    _, uid = linea.split(",", 1)
                    uid = self._normalizar_uid(uid)
                    if not uid:
                        continue

                    self.uid_cancelar_actual = uid
                    ui.textouid.setText(uid)

                    tarjeta = self.cancelar_model.obtener_tarjeta_por_uid(uid)

                    if tarjeta:
                        self._mostrar_datos_tarjeta_cancelar(tarjeta)
                    else:
                        # No viene nombre desde serial, pero ya dejas la UID lista
                        self.nombre_cancelar_actual = ""
                        ui.textonombre.setPlainText("")
                        ui.listanegra.setChecked(False)
                        ui.textomotivo.setPlainText("")

                except Exception as e:
                    print(f"[CANCELAR] Error al procesar uid: {e}")
                    
            elif linea == "st":
                self._limpiar_interfaz_por_retiro_tarjeta()
                continue

    def _mostrar_datos_tarjeta_cancelar(self, tarjeta, nombre_fallback: str = "") -> None:
        if not isinstance(self.current_ui, CancelarWindow) or not tarjeta:
            return

        ui = self.current_ui
        nombre_db = (tarjeta["nombre_pasajero"] or "").strip()
        motivo_db = (tarjeta["motivo_baja"] or "").strip()
        tipo_db = str(dict(tarjeta).get("tipo_tarjeta") or "").strip().lower()
        if tipo_db == "de" or "despachador" in tipo_db:
            self.tipo_cancelar_actual = "DE"
        elif tipo_db in ("ki", "ope") or "operador" in tipo_db:
            self.tipo_cancelar_actual = "KI"
        elif tipo_db == "eu" or "prefer" in tipo_db:
            self.tipo_cancelar_actual = "EU"
        elif tipo_db in ("no", "normal"):
            self.tipo_cancelar_actual = "NO"

        self.nombre_cancelar_actual = nombre_db or nombre_fallback.strip()
        ui.textonombre.setPlainText(self.nombre_cancelar_actual)
        ui.listanegra.setChecked(bool(tarjeta["en_lista_negra"]))
        ui.textomotivo.setPlainText(motivo_db)
                    
    def _ejecutar_cancelar(self) -> None:
        if not isinstance(self.current_ui, CancelarWindow):
            return

        from core.carga import cargando
        with cargando(self.current_window, "Guardando cancelación…"):
            ui = self.current_ui

            if not self.uid_cancelar_actual:
                QMessageBox.warning(self.current_window, "Error", "Primero acerca una tarjeta.")
                return

            motivo = ui.textomotivo.toPlainText().strip()
            nombre_capturado = ui.textonombre.toPlainText().strip()

            if not motivo:
                QMessageBox.warning(self.current_window, "Error", "Captura el motivo de la baja.")
                return

            try:
                tarjeta_id = self.cancelar_model.cancelar_tarjeta_flexible(
                    uid=self.uid_cancelar_actual,
                    nombre_pasajero=nombre_capturado,
                    saldo_actual=0.0,
                    en_lista_negra=True,
                    motivo_baja=motivo,
                    tipo_codigo_local=self.tipo_cancelar_actual,
                )

                ui.listanegra.setChecked(True)

                QMessageBox.information(
                    self.current_window,
                    "Cancelar",
                    f"Tarjeta Cancelada correctamente."
                )

            except Exception as e:
                QMessageBox.critical(
                    self.current_window,
                    "Error",
                    f"No se pudo cancelar la tarjeta: {e}"
                )
            
    # =========================
    # REACTIVAR TARJETA (LISTA NEGRA)
    # =========================
    
    def _quitar_lista_negra(self) -> None:
        if not isinstance(self.current_ui, CancelarWindow):
            return

        ui = self.current_ui

        if not self.uid_cancelar_actual:
            QMessageBox.warning(self.current_window, "Error", "Primero acerca una tarjeta.")
            return
        
        nombre_capturado = ui.textonombre.toPlainText().strip()
        
        try:
            self.cancelar_model.cancelar_tarjeta_flexible(
                uid = self.uid_cancelar_actual,
                nombre_pasajero = nombre_capturado,
                saldo_actual = 0.0,
                en_lista_negra=False,
                motivo_baja = "",
                tipo_codigo_local=self.tipo_cancelar_actual,
            )
            
            ui.listanegra.setChecked(False)
            ui.textomotivo.setPlainText("")
            
            QMessageBox.information(
                self.current_window,
                "Lista negra",
                "La tarjeta fue reactivada correctamente."
            )
        
        except Exception as e:
            QMessageBox.critical(
                self.current_window,
                "Error",
                f"No se pudo reactivar la tarjeta: {e}"
            )


          
    def _aplicar_bloqueo_lista_negra_recarga(
        self,
        bloqueada: bool,
    ) -> None:
        if not isinstance(self.current_ui, RecargaWindow):
            return

        if self.tipo_actual in ("KI", "DE"):
            self._bloquear_recarga_operador()
            return

        ui = self.current_ui
        self.tarjeta_bloqueada = bloqueada

        monto = self._campo_monto_recarga()
        
        if bloqueada:
            if monto is not None:
                monto.clear()
                monto.setEnabled(False)
                
            ui.texto2.setText(f"${self.saldo_actual_centavos / 100:.2f}")
            ui.botonrecargar.setEnabled(False)
            ui.texto7.setText("Tarjeta en lista negra.")
            ui.texto7.setProperty("estadoVisual", "error")
            return
        
        if monto is not None:
            monto.setEnabled(not self.tarjeta_vencida)
        
        ui.texto2.setText(f"${self.saldo_actual_centavos / 100:.2f}")
        ui.botonrecargar.setEnabled(not self.tarjeta_vencida)
        
        texto_actual = ""
        if hasattr(ui.texto7, "toPlainText"):
            texto_actual = ui.texto7.toPlainText().strip()
        elif hasattr(ui.texto7, "text"):
            texto_actual = ui.texto7.text().strip()
            
        if texto_actual == "Tarjeta en lista negra.":
            ui.texto7.clear()
            
        ui.texto7.setProperty("estadoVisual", "")
        
        
    def _limpiar_interfaz_por_retiro_tarjeta(self) -> None:
        if isinstance(self.current_ui, RecargaWindow):
            self._limpiar_recarga_por_retiro()
            return

        if isinstance(self.current_ui, (AltaWindow, Ui_AltaOWindow)):
            self._limpiar_alta_por_retiro()
            return

        if isinstance(self.current_ui, CancelarWindow):
            self._limpiar_cancelar_por_retiro()
            return

        if isinstance(self.current_ui, SustituirWindow):
            self._limpiar_sustituir_por_retiro()
            return


    def _limpiar_recarga_por_retiro(self) -> None:
        if not isinstance(self.current_ui, RecargaWindow):
            return

        ui = self.current_ui

        self.uid_actual = ""
        self.nombre_actual = ""
        self.tipo_actual = ""
        self.saldo_actual_centavos = 0
        self.monto_pendiente_centavos = 0
        self.tarjeta_vencida = False
        self.tarjeta_bloqueada = False

        ui.texto4.setText("-")
        ui.texto5.setText("-")
        ui.texto6.setText("-")
        ui.texto1.setText("$0.00")
        ui.texto2.setText("$0.00")
        ui.texto7.clear()
        ui.texto7.setProperty("estadoVisual", "")
        ui.botonrecargar.setEnabled(True)

        monto = self._campo_monto_recarga()
        if monto is not None:
            monto.clear()
            monto.setEnabled(True)


    def _limpiar_alta_por_retiro(self) -> None:
        if not isinstance(self.current_ui, (AltaWindow, Ui_AltaOWindow)):
            return

        if self.alta_pendiente:
            return

        self._limpiar_forulario_alta()


    def _limpiar_cancelar_por_retiro(self) -> None:
        if not isinstance(self.current_ui, CancelarWindow):
            return

        ui = self.current_ui

        self.uid_cancelar_actual = ""
        self.nombre_cancelar_actual = ""
        self.tarjeta_bloqueada = False

        ui.textouid.setText("-")
        ui.textonombre.setPlainText("")
        ui.listanegra.setChecked(False)
        ui.textomotivo.setPlainText("")


    def _limpiar_sustituir_por_retiro(self) -> None:
        if not isinstance(self.current_ui, SustituirWindow):
            return

        if self.sustituir_pendiente:
            return

        ui = self.current_ui

        self.uid_sustituir_nueva = ""

        if hasattr(ui, "textouid"):
            ui.textouid.setText(self.uid_sustituir_original or "-")        
        if hasattr(ui, "textouidnuevo"):
            ui.textouidnuevo.clear()
        
        
        
        
        
        
        
            
            
    #========================
    #   SUSTITUIR
    #========================
    
    
    
    def _configurar_sustituir_window(self) -> None:
        if not isinstance(self.current_ui, SustituirWindow):
            return
        
        ui = self.current_ui
        
        self.uid_sustituir_original = ""
        self.uid_sustituir_nueva = ""
        self.tarjeta_sustituir_seleccionada = None
        self.resultados_sustituir = []
        
        ui.buscador.clear()
        ui.buscador.setMaximumWidth(900)
        ui.textonombre.setPlainText("")
        ui.textocurp.setText("-")
        ui.textofecha.setText("-")
        ui.textouid.setText("-")
        ui.textotipo.setText("-")
        ui.textovigencia.clear()
        if hasattr(ui, "textouidnuevo"):
            ui.textouidnuevo.setReadOnly(True)
            ui.textouidnuevo.clear()
        ui.textovigencia.setReadOnly(True)
        ui.botonsustituir.clicked.connect(self._ejecutar_sustitucion)
        ui.botonguardar_2.clicked.connect(self._limpiar_formulario_sustituir)
        
        self._crear_popup_resultados_sustituir()
        self._activar_busqueda_sustituir_al_presionar()
        ui.buscador.textChanged.connect(self._buscar_pasajeros_sustituir)
        ui.buscador.editingFinished.connect(self._ocultar_popup_sustituir)
        ui.calendario.selectionChanged.connect(self._actualizar_vigencia_sustituir_desde_calendario)
        
        lista_puertos = self._combo_puertos_actual()
        if lista_puertos is not None:
            lista_puertos.currentIndexChanged.connect(self._conectar_puerto_sustituir)
            
        if self.sustituir_timer is None:
            self.sustituir_timer = QTimer()
            self.sustituir_timer.timeout.connect(self._leer_serial_sustituir)

        self._conectar_puerto_sustituir()
        self.sustituir_timer.start(300)
        self._actualizar_vigencia_sustituir_desde_calendario()
        
    def _activar_busqueda_sustituir_al_presionar(self) -> None:
        if not isinstance(self.current_ui, SustituirWindow):
            return

        buscador = self.current_ui.buscador
        mouse_press_original = buscador.mousePressEvent
        focus_in_original = buscador.focusInEvent

        def mouse_press_event(event):
            mouse_press_original(event)
            self._buscar_pasajeros_sustituir(buscador.text())

        def focus_in_event(event):
            focus_in_original(event)
            self._buscar_pasajeros_sustituir(buscador.text())

        buscador.mousePressEvent = mouse_press_event
        buscador.focusInEvent = focus_in_event
        
    
    def _aplicar_estilos_sustituir(self)-> None:
        if not isinstance(self.current_ui, SustituirWindow):
            return
        
        ui = self.current_ui
        ui.buscador.setPlaceholderText("Buscar por nombre, UID, o Curp...")
        
        
        
        
            
    
    def _crear_popup_resultados_sustituir(self) -> None:
        if not isinstance(self.current_ui, SustituirWindow):
            return

        ui = self.current_ui

        if self.popup_resultados_sustituir is None:
            self.popup_resultados_sustituir = QTableWidget(ui.centralwidget)
            self.popup_resultados_sustituir.setObjectName("tablaResultadosSustituir")

            self.popup_resultados_sustituir.setColumnCount(6)
            self.popup_resultados_sustituir.setHorizontalHeaderLabels([
                "Nombre", "UID", "Vigencia", "Tipo", "CURP", "Nacimiento"
            ])

            self.popup_resultados_sustituir.setEditTriggers(QAbstractItemView.NoEditTriggers)
            self.popup_resultados_sustituir.setSelectionBehavior(QAbstractItemView.SelectRows)
            self.popup_resultados_sustituir.setSelectionMode(QAbstractItemView.SingleSelection)
            self.popup_resultados_sustituir.setAlternatingRowColors(True)
            self.popup_resultados_sustituir.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
            self.popup_resultados_sustituir.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
            self.popup_resultados_sustituir.setWordWrap(False)

            self.popup_resultados_sustituir.verticalHeader().setVisible(False)
            self.popup_resultados_sustituir.horizontalHeader().setStretchLastSection(False)

            self.popup_resultados_sustituir.itemClicked.connect(
                self._seleccionar_resultado_popup_sustituir
            )

            header = self.popup_resultados_sustituir.horizontalHeader()
            header.setSectionResizeMode(0, QHeaderView.Interactive)
            header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
            header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
            header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
            header.setSectionResizeMode(4, QHeaderView.ResizeToContents)
            header.setSectionResizeMode(5, QHeaderView.ResizeToContents)


            self.popup_resultados_sustituir.hide()

        posicion = ui.buscador.mapTo(
            ui.centralwidget, ui.buscador.rect().bottomLeft()
        )
        margen = 16
        ancho_disponible = ui.centralwidget.width() - posicion.x() - margen
        alto_disponible = ui.centralwidget.height() - posicion.y() - margen - 8

        self.popup_resultados_sustituir.setGeometry(
            posicion.x(),
            posicion.y() + 8,
            ancho_disponible,
            min(260, alto_disponible),
        )    
   
    def _formatear_vigencia_sustituir(self, vigencia_raw) -> str:
        fecha = self._parsear_vigencia_tarjeta(vigencia_raw)
        if fecha:
            return fecha.strftime('%d-%m-%Y %H:%M:%S')
        return str(vigencia_raw or '-')

    def _formatear_fecha_simple_sustituir(self, fecha_raw) -> str:
        texto_fecha = str(fecha_raw or '').strip()
        if not texto_fecha:
            return '-'

        formatos = (
            '%Y-%m-%d',
            '%Y-%m-%d %H:%M:%S',
            '%d-%m-%Y',
            '%d/%m/%Y',
        )

        for formato in formatos:
            try:
                return datetime.strptime(texto_fecha, formato).strftime('%d-%m-%Y')
            except ValueError:
                continue

        return texto_fecha
    
    def _actualizar_vigencia_sustituir_desde_calendario(self) -> None:
        if not isinstance(self.current_ui, SustituirWindow):
            return
        fecha = self.current_ui.calendario.selectedDate()
        self.current_ui.textovigencia.setPlainText(fecha.toString('dd-MM-yyyy'))
        
    def _buscar_pasajeros_sustituir(self, texto: str) -> None:
        if not isinstance(self.current_ui, SustituirWindow):
            return

        self._crear_popup_resultados_sustituir()
        termino = (texto or '').strip()

        try:
            self.resultados_sustituir = list(
                self.sustituir_model.buscar_tarjetas_por_nombre(
                    termino, seccion=self.seccion_sustituir
                )
            )
        except Exception as e:
            self.resultados_sustituir = []
            self.popup_resultados_sustituir.hide()
            print(f"[SUSTITUIR] Error al buscar en servidor: {e}")
            return

        tabla = self.popup_resultados_sustituir
        tabla.setRowCount(0)

        for fila, row in enumerate(self.resultados_sustituir):
            curp = str(row.get('curp') or '-')
            fecha_nacimiento = self._formatear_fecha_simple_sustituir(
                row.get('fecha_nacimiento')
            )

            valores = [
                row.get('nombre_pasajero') or '-',
                row.get('uid') or '-',
                self._formatear_vigencia_sustituir(row.get('vigencia')),
                row.get('tipo_tarjeta') or '-',
                curp,
                fecha_nacimiento,
            ]

            tabla.insertRow(fila)

            for columna, valor in enumerate(valores):
                item = QTableWidgetItem(str(valor))
                item.setData(Qt.UserRole, row.get('uid'))
                item.setTextAlignment(Qt.AlignVCenter | Qt.AlignLeft)
                tabla.setItem(fila, columna, item)

        tabla.resizeColumnsToContents()
        tabla.setColumnWidth(0, max(tabla.columnWidth(0), 220))
        tabla.setColumnWidth(4, max(tabla.columnWidth(4), 160))

        if tabla.rowCount() > 0:
            tabla.show()
            tabla.raise_()
        else:
            tabla.hide()
            
            
    def _seleccionar_resultado_popup_sustituir(self, item) -> None:
        if item is None:
            return

        uid = item.data(Qt.UserRole)

        for row in self.resultados_sustituir:
            if row.get('uid') == uid:
                self._cargar_tarjeta_sustituir(row)
                break
        

    def _cargar_tarjeta_sustituir(self, row) -> None:
        if not isinstance(self.current_ui, SustituirWindow):
            return

        ui = self.current_ui
        self.tarjeta_sustituir_seleccionada = dict(row)
        self.uid_sustituir_original = self._normalizar_uid(str(row.get('uid') or ''))
        self.uid_sustituir_nueva = ''
        if hasattr(ui, "textouidnuevo"):
            ui.textouidnuevo.clear()

        ui.buscador.blockSignals(True)
        ui.buscador.clear()
        ui.buscador.blockSignals(False)
        ui.textonombre.setPlainText(row['nombre_pasajero'] or '')
        ui.textocurp.setText(str(row.get('curp') or '-'))
        ui.textofecha.setText(
            self._formatear_fecha_simple_sustituir(row.get('fecha_nacimiento'))
        )
        ui.textouid.setText(self.uid_sustituir_original or '-')
        ui.textotipo.setText(row['tipo_tarjeta'] or '-')

        fecha_vigencia = self._parsear_vigencia_tarjeta(row['vigencia'])
        if fecha_vigencia:
            ui.calendario.setSelectedDate(QDate(fecha_vigencia.year, fecha_vigencia.month, fecha_vigencia.day))
        self._actualizar_vigencia_sustituir_desde_calendario()
        self._ocultar_popup_sustituir()

    def _ocultar_popup_sustituir(self) -> None:
        if self.popup_resultados_sustituir is not None:
            self.popup_resultados_sustituir.hide()

    def _conectar_puerto_sustituir(self, *args) -> None:
        lista_puertos = self._combo_puertos_actual()
        puerto = lista_puertos.currentData() if lista_puertos is not None else None
        if not puerto:
            return
        try:
            self.arduino.conectar(puerto, 115200)
        except Exception as e:
            print(f'[SUSTITUIR] Error al conectar al puerto {puerto}: {e}')

    def _leer_serial_sustituir(self, mostrar_errores: bool = True) -> None:
        if not isinstance(self.current_ui, SustituirWindow):
            return

        ui = self.current_ui

        while True:
            linea = self.arduino.leer_linea()
            if not linea:
                break

            print('[SUSTITUIR]', linea)
            linea_minusculas = linea.lower()

            try:
                if linea_minusculas.startswith('uid,'):
                    _, uid = linea.split(',', 1)
                    uid = self._normalizar_uid(uid)
                    if not uid:
                        continue
                    self._registrar_uid_sustituir_leida(uid)

                elif linea_minusculas.startswith("sldo,"):
                    partes = linea.split(",", 3)

                    if len(partes) < 4:
                        continue

                    uid = self._normalizar_uid(partes[1])

                    if not uid:
                        continue

                    self._registrar_uid_sustituir_leida(uid)

                    pendiente = self.sustituir_pendiente

                    if (
                        pendiente
                        and uid == pendiente["uid_nueva"]
                        and pendiente.get("fase") in (
                            "esperando_saldo",
                            "verificando_saldo",
                        )
                    ):
                        self._procesar_saldo_para_sustitucion(
                            int(partes[2])
                        )
                
                elif linea == "st":
                    self._limpiar_interfaz_por_retiro_tarjeta()
                    continue

                elif linea_minusculas == 'ok,alta':
                    if not self.sustituir_pendiente:
                        print('[SUSTITUIR] Llego ok,alta pero no hay sustitucion pendiente.')
                        continue

                    if self.sustituir_pendiente.get('fase') != 'esperando_alta':
                        continue

                    uid = self.sustituir_pendiente['uid_nueva']
                    nombre = self.sustituir_pendiente['nombre_pasajero']
                    comando_nombre = f'nm,{uid},{nombre}'
                    print('[SUSTITUIR] Enviando nombre:', comando_nombre)
                    self.arduino.enviar_linea(comando_nombre)
                    self.sustituir_pendiente['fase'] = 'esperando_nombre'

                elif linea_minusculas == 'ok,nombre':
                    if not self.sustituir_pendiente:
                        print('[SUSTITUIR] Llego ok,nombre pero no hay sustitucion pendiente.')
                        continue

                    if self.sustituir_pendiente.get('fase') == 'esperando_nombre':
                        self._continuar_sustitucion_con_saldo()

                elif linea_minusculas == "ok":
                    pendiente = self.sustituir_pendiente

                    if not pendiente:
                        continue

                    if pendiente.get("fase") in (
                        "esperando_alta",
                        "esperando_nombre",
                    ):
                        self._continuar_sustitucion_con_saldo()

                elif linea_minusculas.startswith('ok,'):
                    pendiente = self.sustituir_pendiente
                    partes = linea.split(',')
                    if (pendiente and pendiente.get('fase') == 'verificando_saldo'
                            and len(partes) >= 4
                            and self._normalizar_uid(partes[1]) == pendiente['uid_nueva']):
                        # La respuesta de escritura no sustituye la lectura física.
                        self._verificar_saldo_sustitucion(pendiente)

                elif linea_minusculas.startswith('error'):

                    errores_de_lectura_automatica = {
                        'error,estado_tisc4',
                        'error,estado_tisc3',
                        'error,estado_tisc2',
                        'error,vigencia0',
                        'error,leer_saldo',
                        'error,leer_saldo2',
                    }

                    if linea_minusculas in errores_de_lectura_automatica:
                        print(f'[SUSTITUIR] Error automatico de lectura ignorado: {linea}')
                        continue

                    if 'error en las 3 aplicaciones' in linea_minusculas:
                        if (self.sustituir_pendiente
                                and self.sustituir_pendiente.get('fase') == 'esperando_alta'):
                            reintentos = self.sustituir_pendiente.get('reintentos_alta', 0)
                            comando = self.sustituir_pendiente.get('comando_sustitucion')

                            if comando and reintentos < 2:
                                self.sustituir_pendiente['reintentos_alta'] = reintentos + 1

                                print(
                                    '[SUSTITUIR] Reintentando sustitucion por error en aplicaciones '
                                    f'intento {reintentos + 1}: {comando}'
                                )

                                QTimer.singleShot(
                                    1000,
                                    lambda c=comando, p=self.sustituir_pendiente: (
                                        self.arduino.enviar_linea(c)
                                        if self.sustituir_pendiente is p
                                        and p.get('fase') == 'esperando_alta'
                                        else None
                                    )
                                )
                                continue

                    if not self.sustituir_pendiente:
                        print(f'[SUSTITUIR] Error de lectura ignorado sin sustitucion pendiente: {linea}')
                        continue

                    if self.sustituir_pendiente.get('fase') in (
                            'esperando_saldo', 'verificando_saldo', 'guardando_local'):
                        self._verificar_saldo_sustitucion(self.sustituir_pendiente)
                        continue

                    self.sustituir_pendiente = None

                    if mostrar_errores:
                        QMessageBox.warning(
                            self.current_window,
                            'Sustituir',
                            'No se pudo preparar la tarjeta nueva. Intenta acercarla de nuevo y vuelve a presionar Sustituir.'
                        )
                    return
            except Exception as e:
                print(f'[SUSTITUIR] Error al procesar serial: {e}')
                traceback.print_exception(type(e), e, e.__traceback__)

    def _registrar_uid_sustituir_leida(self, uid: str) -> None:
        uid = self._normalizar_uid(uid)
        if not uid:
            return

        uid_original = self._normalizar_uid(self.uid_sustituir_original)
        if uid_original and uid == uid_original and not self.sustituir_pendiente:
            print(f'[SUSTITUIR] UID anterior ignorada como nueva: {uid}')
            return

        self.uid_sustituir_nueva = uid
        if isinstance(self.current_ui, SustituirWindow):
            if hasattr(self.current_ui, "textouidnuevo"):
                self.current_ui.textouidnuevo.setText(uid)
            else:
                self.current_ui.textouid.setText(uid)

    def _esperar_uid_sustituir_disponible(self) -> bool:
        try:
            self.arduino.enviar_linea('uid')
        except Exception:
            pass

        limite = time.monotonic() + 5.0
        while time.monotonic() < limite:
            self._leer_serial_sustituir()
            if self.uid_sustituir_nueva:
                return True
            QCoreApplication.processEvents()
            time.sleep(0.05)
        return False

    def _ejecutar_sustitucion(self) -> None:
        if not isinstance(self.current_ui, SustituirWindow):
            return

        from core.carga import cargando
        with cargando(self.current_window, "Guardando sustitución de tarjeta…",
                      pendiente=lambda: self.sustituir_pendiente is not None):
            if self.sustituir_pendiente:
                self._verificar_saldo_sustitucion(self.sustituir_pendiente)
                return

            if not self.tarjeta_sustituir_seleccionada or not self.uid_sustituir_original:
                QMessageBox.warning(
                    self.current_window,
                    'Error',
                    'Primero selecciona un pasajero del buscador.'
                )
                return

            self.uid_sustituir_original = self._normalizar_uid(self.uid_sustituir_original)
            self.uid_sustituir_nueva = ''
            self._leer_serial_sustituir(False)
            if not self.uid_sustituir_nueva and not self._esperar_uid_sustituir_disponible():
                QMessageBox.warning(
                    self.current_window,
                    'Error',
                    'Acerca la tarjeta nueva al lector.'
                )
                return

            if self._normalizar_uid(self.uid_sustituir_nueva) == self.uid_sustituir_original:
                QMessageBox.warning(
                    self.current_window,
                    'Error',
                    'La tarjeta nueva no puede ser la misma que la anterior.'
                )
                return

            fecha = self.current_ui.calendario.selectedDate()
            vigtarifa = fecha.toString('ddMMyy')
            hora_actual = QDateTime.currentDateTime().toString('HHmmss')
            nueva_vigencia = vigtarifa + hora_actual

            if len(vigtarifa) != 6 or not vigtarifa.isdigit():
                QMessageBox.warning(
                    self.current_window,
                    'Error',
                    'VIGTARIFA invalida.'
                )
                return

            if len(nueva_vigencia) != 12 or not nueva_vigencia.isdigit():
                QMessageBox.warning(
                    self.current_window,
                    'Error',
                    'VIGENCIA12 invalida.'
                )
                return

            row = dict(self.tarjeta_sustituir_seleccionada)
            nombre_tarjeta = self._limpiar_alias_para_arduino(row.get('nombre_pasajero') or '')

            if not nombre_tarjeta:
                QMessageBox.warning(
                    self.current_window,
                    'Error',
                    'La tarjeta seleccionada no tiene nombre valido para copiar.'
                )
                return

            tipo_tarjeta_raw = str(
                row.get("tipo_tarjeta") or ""
            ).strip().lower()

            if tipo_tarjeta_raw == "de" or "despachador" in tipo_tarjeta_raw:
                no_tarjeta = "DE"
                tipo_local = "DE"
            elif (
                "operador" in tipo_tarjeta_raw
                or tipo_tarjeta_raw in ("ki", "ope")
            ):
                no_tarjeta = "KI"
                tipo_local = "KI"
            elif (
                "prefer" in tipo_tarjeta_raw
                or tipo_tarjeta_raw == "eu"
            ):
                no_tarjeta = "EU"
                tipo_local = "EU"
            else:
                no_tarjeta = "NO"
                tipo_local = "NO"

            try:
                from decimal import Decimal

                objetivo = (
                    0
                    if tipo_local in ("KI", "DE")
                    else int(
                        (
                            Decimal(str(row.get("saldo") or 0)) * 100
                        ).quantize(Decimal("1"))
                    )
                )

                if not 0 <= objetivo <= 40000:
                    raise ValueError(
                        "El saldo a transferir debe estar entre $0 y $400."
                    )

                self.sustituir_model.validar_sustitucion_local(
                    self.uid_sustituir_original,
                    self.uid_sustituir_nueva,
                )

                nombre_tarjeta = self._ajustar_alias_para_comando_alta(
                    self.uid_sustituir_nueva,
                    nombre_tarjeta,
                    no_tarjeta,
                    '02',
                    '01',
                    vigtarifa,
                    nueva_vigencia,
                )

                if not nombre_tarjeta:
                    QMessageBox.warning(
                        self.current_window,
                        'Error',
                        'El nombre queda vacio al preparar el comando para Arduino.'
                    )
                    return

                comando = (
                    f'al,{self.uid_sustituir_nueva},{nombre_tarjeta},{no_tarjeta},'
                    f'02,01,{vigtarifa},{nueva_vigencia}'
                )

                self.sustituir_pendiente = {
                    'uid_anterior': self.uid_sustituir_original,
                    'uid_nueva': self.uid_sustituir_nueva,
                    'nombre_pasajero': nombre_tarjeta,
                    'tipo_codigo_local': tipo_local,
                    'nueva_vigencia': nueva_vigencia,
                    'fase': 'esperando_alta',
                    'comando_sustitucion': comando,
                    'reintentos_alta': 0,
                    'saldo_objetivo_centavos': objetivo,
                    'datos_original': row,
                }

                print('[SUSTITUIR] Enviando sustitucion:', comando)
                self.arduino.enviar_linea(comando)

            except Exception as e:
                self.sustituir_pendiente = None
                print(f'[SUSTITUIR] Error completo al enviar sustitucion: {e}')
                traceback.print_exception(type(e), e, e.__traceback__)
                QMessageBox.critical(
                    self.current_window,
                    'Error',
                    f'No se pudo enviar la sustitucion: {e}'
                )

    def _continuar_sustitucion_con_saldo(self) -> None:
        pendiente = self.sustituir_pendiente
        if not pendiente:
            return
        if pendiente['tipo_codigo_local'] in ('KI', 'DE'):
            self._finalizar_sustitucion_local()
            return
        pendiente['fase'] = 'esperando_saldo'
        self._verificar_saldo_sustitucion(pendiente)

    def _procesar_saldo_para_sustitucion(self, saldo_centavos: int) -> None:
        pendiente = self.sustituir_pendiente
        if not pendiente:
            return
        objetivo = pendiente['saldo_objetivo_centavos']
        if saldo_centavos == objetivo:
            pendiente['saldo_verificado'] = True
            self._finalizar_sustitucion_local()
            return
        if pendiente.get('escritura_saldo_enviada'):
            # Una lectura diferente no prueba que un comando anterior no siga
            # en ejecución. Nunca repetir una recarga de resultado incierto.
            return
        if not 0 <= saldo_centavos < objetivo:
            return
        pendiente['escritura_saldo_enviada'] = True
        pendiente['fase'] = 'verificando_saldo'
        self.arduino.enviar_linea(
            f"rc,{pendiente['uid_nueva']},{objetivo - saldo_centavos}"
        )
        QTimer.singleShot(1500, lambda p=pendiente: self._verificar_saldo_sustitucion(p))

    def _verificar_saldo_sustitucion(self, pendiente=None) -> None:
        pendiente = pendiente or self.sustituir_pendiente
        if not pendiente or self.sustituir_pendiente is not pendiente:
            return
        if pendiente.get('fase') == 'guardando_local':
            self._finalizar_sustitucion_local()
            return
        if pendiente.get('fase') not in ('esperando_saldo', 'verificando_saldo'):
            return
        # Se utiliza la lectura automática sldo del lector. No se inventa un
        # comando de consulta que el firmware actual pueda no soportar.
        if not pendiente.get('aviso_verificacion_programado'):
            pendiente['aviso_verificacion_programado'] = True
            def avisar():
                if self.sustituir_pendiente is pendiente:
                    QMessageBox.warning(
                        self.current_window, 'Sustituir',
                        'Sustitución pendiente de comprobar el saldo o guardar en SQLite. '
                        'Retira y acerca la tarjeta nueva para leer su saldo. '
                        'No repitas el alta ni la recarga. No cierres la aplicación: '
                        'la escritura física y SQLite no forman una transacción única.'
                    )
            QTimer.singleShot(8000, avisar)

    def _finalizar_sustitucion_local(self) -> None:
        pendiente = self.sustituir_pendiente
        if not pendiente:
            return
        if pendiente['tipo_codigo_local'] not in ('KI', 'DE') and not pendiente.get('saldo_verificado'):
            return
        pendiente['fase'] = 'guardando_local'
        if self._guardar_sustitucion_confirmada():
            QMessageBox.information(
                self.current_window, 'Sustituir',
                f"Tarjeta sustituida localmente.\nNueva: {pendiente['uid_nueva']}\n"
                'Sincronización pendiente de confirmación del servidor.'
            )
            self._limpiar_formulario_sustituir()

    def _guardar_sustitucion_confirmada(self) -> bool:
        if not self.sustituir_pendiente:
            return True

        try:
            payload = {
                'uid_anterior': self.sustituir_pendiente['uid_anterior'],
                'uid_nueva': self.sustituir_pendiente['uid_nueva'],
                'nueva_vigencia': self.sustituir_pendiente['nueva_vigencia'],
                'nombre_pasajero': self.sustituir_pendiente['nombre_pasajero'],
                'tipo_codigo_local': self.sustituir_pendiente['tipo_codigo_local'],
                'datos_original': self.sustituir_pendiente['datos_original'],
            }

            self.sustituir_model.guardar_sustitucion_local(**payload)

            print(
                '[SUSTITUIR] Sustitucion guardada en SQLite '
                f"UID_ANTERIOR={payload['uid_anterior']} UID_NUEVA={payload['uid_nueva']}"
            )

            self.sustituir_pendiente = None
            self._sincronizar_pendientes()
            return True

        except Exception as e:
            print(f'[SUSTITUIR] Error al guardar sustitucion en servidor: {e}')
            traceback.print_exception(type(e), e, e.__traceback__)
            QMessageBox.critical(
                self.current_window,
                'Error',
                f'La tarjeta fue escrita, pero no se pudo guardar en SQLite: {e}. '
                'No cierres la aplicación ni repitas la recarga. Vuelve a presionar Sustituir para guardar.'
            )
            return False

    def _limpiar_formulario_sustituir(self) -> None:
        if not isinstance(self.current_ui, SustituirWindow):
            return

        self.uid_sustituir_original = ''
        self.uid_sustituir_nueva = ''
        self.tarjeta_sustituir_seleccionada = None
        self.resultados_sustituir = []
        self.sustituir_pendiente = None

        self.current_ui.buscador.clear()
        self.current_ui.textonombre.setPlainText('')
        self.current_ui.textocurp.setText('-')
        self.current_ui.textofecha.setText('-')
        self.current_ui.textouid.setText('-')
        self.current_ui.textotipo.setText('-')
        if hasattr(self.current_ui, "textouidnuevo"):
            self.current_ui.textouidnuevo.clear()
        self._actualizar_vigencia_sustituir_desde_calendario()
        self._ocultar_popup_sustituir()
        
    
    def _configurar_menu_usuario(self) -> None:
        ui = self.current_ui

        if ui is None or not hasattr(ui, "usuario"):
            return

        ui.usuario.setText(self.current_username or "Usuario")
        ui.usuario.setToolTip("Opciones de usuario")
        ui.usuario.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextOnly)
        ui.usuario.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)
        ui.usuario.setArrowType(Qt.ArrowType.NoArrow)

        menu = QMenu(self.current_window)

        accion_cerrar = menu.addAction("Cerrar sesión")
        accion_cerrar.triggered.connect(self._cerrar_sesion)

        ui.usuario.setMenu(menu)

    def _cerrar_sesion(self) -> None:
        self.current_username = ""
        self.current_role = ""
        self.show_login_window()
        
    def _crear_icono_ojo(self, tachado: bool = False) -> QIcon:
        pixmap = QPixmap(24, 24)
        pixmap.fill(Qt.GlobalColor.transparent)
        
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        color = QColor("#245E91")
        painter.setPen(QPen(color, 2))
        painter.setBrush(Qt.BrushStyle.NoBrush)
        
        path = QPainterPath()
        path.moveTo(3, 12)
        path.cubicTo(7, 5, 17, 5, 21, 12)
        path.cubicTo(17, 19, 7, 19, 3, 12)
        
        painter.drawPath(path)
        
        painter.setBrush(QBrush(color))
        painter.drawEllipse(QRectF(10, 10, 4, 4))
        
        if tachado:
            painter.setPen(QPen(color, 2))
            painter.drawLine(5, 20, 20, 5)
            
        painter.end()
        
        return QIcon(pixmap)
    
    
    def _alternar_visibilidad_password(self) -> None:
        if not isinstance(self.current_ui, LoginWindow):
            return
        
        campo = self.current_ui.lineEditPassword
        
        if campo.echoMode() == QLineEdit.EchoMode.Password:
            campo.setEchoMode(QLineEdit.EchoMode.Normal)
            self.accion_ver_password.setIcon(self._crear_icono_ojo(tachado=True))
            self.accion_ver_password.setToolTip("Ocultar Contraseña")
        else:
            campo.setEchoMode(QLineEdit.EchoMode.Password)
            self.accion_ver_password.setIcon(self._crear_icono_ojo(tachado= False))
            self.accion_ver_password.setToolTip("Mostrar Contraseña")
            
            
    #----------------------------------------------
    #                     CURP
    #----------------------------------------------
    
    def _limitar_curp_alta(self) -> None:
        if not isinstance(self.current_ui, (AltaWindow, Ui_AltaOWindow)):
            return

        campo = self.current_ui.textocurp
        texto_actual = campo.toPlainText()
        texto_limitado = texto_actual.strip().upper()[:18]

        if texto_actual != texto_limitado:
            campo.blockSignals(True)
            campo.setPlainText(texto_limitado)
            cursor = campo.textCursor()
            cursor.movePosition(cursor.MoveOperation.End)
            campo.setTextCursor(cursor)
            campo.blockSignals(False)
            
#---------------------------------------------------
#              NOMBRE Y ESPACIOS
#---------------------------------------------------

    def _solo_letras_espacios_nombre_alta(self) -> None:
        if not isinstance(self.current_ui, (AltaWindow, Ui_AltaOWindow)):
            return
        
        campo = self.current_ui.textonombre
        texto = campo.toPlainText()
        
        texto_limpio = re.sub(
            r"[^A-Za-zÁÉÍÓÚÜÑáéíóúüñ\s]",
            "",
            texto
        )
        
        if campo.toPlainText() != texto_limpio:
            campo.blockSignals(True)
            campo.setPlainText(texto_limpio)
            
            cursor = campo.textCursor()
            cursor.movePosition(cursor.MoveOperation.End)
            campo.setTextCursor(cursor)
            
            campo.blockSignals(False)
            


#--------------------------------------------------
#               FECHA NACIMINETO(DD-MM-AAAA)
#--------------------------------------------------
    def _formatear_fecha_nacimiento_alta(self) -> None:
        if not isinstance(self.current_ui, (AltaWindow, Ui_AltaOWindow)):
            return
        
        campo = self.current_ui.textofechanacimiento
        texto_actual = campo.toPlainText()
        numeros = re.sub(r"\D", "", texto_actual)[:8]

        if len(numeros) <= 2:
            texto_formateado = numeros
            if len(numeros) == 2:
                texto_formateado += "-"
        elif len(numeros) <= 4:
            texto_formateado = numeros[:2] + "-" + numeros[2:]
            if len(numeros) == 4:
                texto_formateado += "-"
        else:
            texto_formateado = numeros[:2] + "-" + numeros[2:4] + "-" + numeros[4:]

        if texto_actual != texto_formateado:
            campo.blockSignals(True)
            campo.setPlainText(texto_formateado)

            cursor = campo.textCursor()
            cursor.movePosition(cursor.MoveOperation.End)
            campo.setTextCursor(cursor)

            campo.blockSignals(False)

#---------------------------------------------
#                MONTO DE RECARGA
#---------------------------------------------
    def _formatear_monto_recarga(self) -> None:
        monto = self._campo_monto_recarga()
        if monto is None:
            return
        texto = self._texto_monto_recarga()
        
        if not texto:
            return
        
        try:
            cantidad = float(texto)
        except ValueError:
            return
        monto.setText(f"{cantidad:.2f}")

    def _solo_letras_espacios_nombre_cancelar(self) -> None:
        if not isinstance(self.current_ui, CancelarWindow):
            return

        campo = self.current_ui.textonombre
        texto = campo.toPlainText()

        limpio = re.sub(
            "[^A-Za-z\\u00c1\\u00c9\\u00cd\\u00d3\\u00da\\u00dc\\u00d1"
            "\\u00e1\\u00e9\\u00ed\\u00f3\\u00fa\\u00fc\\u00f1\\s]",
            "",
            texto,
        )
        limpio = re.sub(r"\s+", " ", limpio)

        if texto == limpio:
            return

        campo.blockSignals(True)
        campo.setPlainText(limpio)

        cursor = campo.textCursor()
        cursor.movePosition(cursor.MoveOperation.End)
        campo.setTextCursor(cursor)

        campo.blockSignals(False)
        
#----------------------------------------------------------
#                   TEXTO EN CANCELAR
#----------------------------------------------------------

    def _solo_letras_espacios_nombre_cancelar(self) -> None:
        if not isinstance(self.current_ui, CancelarWindow):
            return
        
        campo = self.current_ui.textonombre
        texto = campo.toPlainText()
        
        limpio = re.sub(r"[^A-Za-zÁÉÍÓÚáéíóúÑñÜü\s]", "", texto)
        limpio = re.sub(r"\s+", " ", limpio)
        
        if texto == limpio:
            return
        
        campo.blockSignals(True)
        campo.setPlainText(limpio)

        cursor = campo.textCursor()
        cursor.movePosition(cursor.MoveOperation.End)
        campo.setTextCursor(cursor)

        campo.blockSignals(False)
        
        
#-------------------------------------------------------
#       Borra "Recarga Exitosa" despues de recarga
#-------------------------------------------------------
    def _limpiar_mensaje_recarga_exitosa(self) -> None:
        if not isinstance(self.current_ui, RecargaWindow):
            return
        
        ui = self.current_ui
        texto_actual = ""
        
        if hasattr(ui.texto7, "toPlainText"):
            texto_actual = ui.texto7.toPlainText().strip()
        elif hasattr(ui.texto7, "text"):
            texto_actual = ui.texto7.text().strip()
            
        if texto_actual == "Recarga Exitosa":
            ui.texto7.clear()
            ui.texto7.setProperty("estadoVisual", "")
