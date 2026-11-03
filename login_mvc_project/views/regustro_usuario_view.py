# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'regitro_usuario.ui'
##
## Created by: Qt User Interface Compiler version 6.12.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QFrame, QHBoxLayout,
    QLabel, QMainWindow, QPushButton, QScrollArea,
    QSizePolicy, QSpacerItem, QTextEdit, QToolButton,
    QVBoxLayout, QWidget)

class RegistroUsuarioWindow(object):
    def setupUi(self, RegistroUsuarioWindow):
        if not RegistroUsuarioWindow.objectName():
            RegistroUsuarioWindow.setObjectName(u"RegistroUsuarioWindow")
        RegistroUsuarioWindow.setMinimumSize(QSize(760, 680))
        RegistroUsuarioWindow.resize(860, 780)
        self.centralwidget = QWidget(RegistroUsuarioWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout_2 = QVBoxLayout(self.centralwidget)
        self.gridLayout_2.setSpacing(12)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(16, 16, 16, 16)
        self.frame = QFrame(self.centralwidget)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.frame.setProperty(u"uiRole", u"header")
        self.frame.setMinimumSize(QSize(0, 90))
        self.frame.setMaximumSize(QSize(16777215, 90))
        self.layoutEstructura2 = QHBoxLayout(self.frame)
        self.layoutEstructura2.setSpacing(12)
        self.layoutEstructura2.setObjectName(u"layoutEstructura2")
        self.layoutEstructura2.setContentsMargins(12, 12, 12, 12)
        self.franjaCabecera = QFrame(self.frame)
        self.franjaCabecera.setObjectName(u"franjaCabecera")
        self.franjaCabecera.setProperty(u"uiRole", u"stripe")
        self.franjaCabecera.setMinimumSize(QSize(5, 32))
        self.franjaCabecera.setMaximumSize(QSize(5, 32))

        self.layoutEstructura2.addWidget(self.franjaCabecera, 0, Qt.AlignVCenter)

        self.marcaCabecera = QWidget(self.frame)
        self.marcaCabecera.setObjectName(u"marcaCabecera")
        self.layoutEstructura4 = QVBoxLayout(self.marcaCabecera)
        self.layoutEstructura4.setSpacing(2)
        self.layoutEstructura4.setObjectName(u"layoutEstructura4")
        self.layoutEstructura4.setContentsMargins(0, 0, 0, 0)
        self.Rumsa = QLabel(self.marcaCabecera)
        self.Rumsa.setObjectName(u"Rumsa")
        self.Rumsa.setAlignment(Qt.AlignLeft|Qt.AlignVCenter)
        self.Rumsa.setWordWrap(False)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Rumsa.sizePolicy().hasHeightForWidth())
        self.Rumsa.setSizePolicy(sizePolicy)
        self.Rumsa.setProperty(u"uiRole", u"brand")

        self.layoutEstructura4.addWidget(self.Rumsa)

        self.labelCompany = QLabel(self.marcaCabecera)
        self.labelCompany.setObjectName(u"labelCompany")
        self.labelCompany.setAlignment(Qt.AlignLeft|Qt.AlignVCenter)
        sizePolicy.setHeightForWidth(self.labelCompany.sizePolicy().hasHeightForWidth())
        self.labelCompany.setSizePolicy(sizePolicy)
        self.labelCompany.setProperty(u"uiRole", u"caption")
        self.labelCompany.setWordWrap(False)

        self.layoutEstructura4.addWidget(self.labelCompany)


        self.layoutEstructura2.addWidget(self.marcaCabecera)

        self.espacioEstructura3 = QSpacerItem(8, 8, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.layoutEstructura2.addItem(self.espacioEstructura3)

        self.estadoCabecera = QWidget(self.frame)
        self.estadoCabecera.setObjectName(u"estadoCabecera")
        self.layoutEstructura5 = QVBoxLayout(self.estadoCabecera)
        self.layoutEstructura5.setSpacing(4)
        self.layoutEstructura5.setObjectName(u"layoutEstructura5")
        self.layoutEstructura5.setContentsMargins(0, 0, 0, 0)
        self.usuario = QToolButton(self.estadoCabecera)
        self.usuario.setObjectName(u"usuario")
        self.usuario.setMinimumSize(QSize(0, 36))
        self.usuario.setMaximumSize(QSize(16777215, 40))
        sizePolicy.setHeightForWidth(self.usuario.sizePolicy().hasHeightForWidth())
        self.usuario.setSizePolicy(sizePolicy)

        self.layoutEstructura5.addWidget(self.usuario, 0, Qt.AlignRight)

        self.labelEstadoConexion = QLabel(self.estadoCabecera)
        self.labelEstadoConexion.setObjectName(u"labelEstadoConexion")
        self.labelEstadoConexion.setProperty(u"uiRole", u"status")
        self.labelEstadoConexion.setAlignment(Qt.AlignLeft|Qt.AlignVCenter)
        self.labelEstadoConexion.setWordWrap(False)
        sizePolicy.setHeightForWidth(self.labelEstadoConexion.sizePolicy().hasHeightForWidth())
        self.labelEstadoConexion.setSizePolicy(sizePolicy)

        self.layoutEstructura5.addWidget(self.labelEstadoConexion, 0, Qt.AlignRight)


        self.layoutEstructura2.addWidget(self.estadoCabecera)


        self.gridLayout_2.addWidget(self.frame)

        self.layoutEstructura6 = QHBoxLayout()
        self.layoutEstructura6.setSpacing(8)
        self.layoutEstructura6.setObjectName(u"layoutEstructura6")
        self.layoutEstructura6.setContentsMargins(0, 0, 0, 0)
        self.botonregresar = QPushButton(self.centralwidget)
        self.botonregresar.setObjectName(u"botonregresar")
        self.botonregresar.setMinimumSize(QSize(100, 36))
        sizePolicy.setHeightForWidth(self.botonregresar.sizePolicy().hasHeightForWidth())
        self.botonregresar.setSizePolicy(sizePolicy)
        self.botonregresar.setProperty(u"uiRole", u"back")
        self.botonregresar.setMaximumSize(QSize(110, 40))

        self.layoutEstructura6.addWidget(self.botonregresar)

        self.espacioEstructura7 = QSpacerItem(8, 8, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.layoutEstructura6.addItem(self.espacioEstructura7)

        self.etiquetaPuerto = QLabel(self.centralwidget)
        self.etiquetaPuerto.setObjectName(u"etiquetaPuerto")
        self.etiquetaPuerto.setProperty(u"uiRole", u"caption")
        sizePolicy.setHeightForWidth(self.etiquetaPuerto.sizePolicy().hasHeightForWidth())
        self.etiquetaPuerto.setSizePolicy(sizePolicy)

        self.layoutEstructura6.addWidget(self.etiquetaPuerto)

        self.lista = QComboBox(self.centralwidget)
        self.lista.setObjectName(u"lista")
        self.lista.setMinimumSize(QSize(220, 36))
        self.lista.setMaximumSize(QSize(260, 40))

        self.layoutEstructura6.addWidget(self.lista)


        self.gridLayout_2.addLayout(self.layoutEstructura6)

        self.areaContenido = QScrollArea(self.centralwidget)
        self.areaContenido.setObjectName(u"areaContenido")
        self.areaContenido.setWidgetResizable(True)
        self.areaContenido.setFrameShape(QFrame.NoFrame)
        self.panelRegistroUsuario = QFrame()
        self.panelRegistroUsuario.setObjectName(u"panelRegistroUsuario")
        self.panelRegistroUsuario.setProperty(u"uiRole", u"card")
        self.layoutEstructura8 = QVBoxLayout(self.panelRegistroUsuario)
        self.layoutEstructura8.setSpacing(12)
        self.layoutEstructura8.setObjectName(u"layoutEstructura8")
        self.layoutEstructura8.setContentsMargins(16, 16, 16, 16)
        self.sustituirtarjeta = QLabel(self.panelRegistroUsuario)
        self.sustituirtarjeta.setObjectName(u"sustituirtarjeta")
        self.sustituirtarjeta.setAlignment(Qt.AlignLeft|Qt.AlignVCenter)
        self.sustituirtarjeta.setWordWrap(False)
        sizePolicy.setHeightForWidth(self.sustituirtarjeta.sizePolicy().hasHeightForWidth())
        self.sustituirtarjeta.setSizePolicy(sizePolicy)
        self.sustituirtarjeta.setProperty(u"uiRole", u"heading")

        self.layoutEstructura8.addWidget(self.sustituirtarjeta)

        self.labelHeaderInfo = QLabel(self.panelRegistroUsuario)
        self.labelHeaderInfo.setObjectName(u"labelHeaderInfo")
        self.labelHeaderInfo.setAlignment(Qt.AlignLeft|Qt.AlignVCenter)
        self.labelHeaderInfo.setWordWrap(False)
        sizePolicy.setHeightForWidth(self.labelHeaderInfo.sizePolicy().hasHeightForWidth())
        self.labelHeaderInfo.setSizePolicy(sizePolicy)
        self.labelHeaderInfo.setProperty(u"uiRole", u"caption")

        self.layoutEstructura8.addWidget(self.labelHeaderInfo)

        self.layoutEstructura9 = QHBoxLayout()
        self.layoutEstructura9.setSpacing(16)
        self.layoutEstructura9.setObjectName(u"layoutEstructura9")
        self.layoutEstructura9.setContentsMargins(0, 0, 0, 0)
        self.datosRegistro = QFrame(self.panelRegistroUsuario)
        self.datosRegistro.setObjectName(u"datosRegistro")
        self.datosRegistro.setProperty(u"uiRole", u"card")
        self.layoutEstructura10 = QVBoxLayout(self.datosRegistro)
        self.layoutEstructura10.setSpacing(8)
        self.layoutEstructura10.setObjectName(u"layoutEstructura10")
        self.layoutEstructura10.setContentsMargins(12, 12, 12, 12)
        self.datosRegistroTitulo = QLabel(self.datosRegistro)
        self.datosRegistroTitulo.setObjectName(u"datosRegistroTitulo")
        self.datosRegistroTitulo.setProperty(u"uiRole", u"section")
        sizePolicy.setHeightForWidth(self.datosRegistroTitulo.sizePolicy().hasHeightForWidth())
        self.datosRegistroTitulo.setSizePolicy(sizePolicy)

        self.layoutEstructura10.addWidget(self.datosRegistroTitulo)

        self.nombre = QLabel(self.datosRegistro)
        self.nombre.setObjectName(u"nombre")
        self.nombre.setAlignment(Qt.AlignLeft|Qt.AlignVCenter)
        self.nombre.setWordWrap(False)
        sizePolicy.setHeightForWidth(self.nombre.sizePolicy().hasHeightForWidth())
        self.nombre.setSizePolicy(sizePolicy)
        self.nombre.setProperty(u"uiRole", u"fieldLabel")

        self.layoutEstructura10.addWidget(self.nombre)

        self.textonombre = QTextEdit(self.datosRegistro)
        self.textonombre.setObjectName(u"textonombre")
        self.textonombre.setMinimumSize(QSize(0, 36))
        self.textonombre.setMaximumSize(QSize(16777215, 40))

        self.layoutEstructura10.addWidget(self.textonombre)

        self.correo = QLabel(self.datosRegistro)
        self.correo.setObjectName(u"correo")
        self.correo.setAlignment(Qt.AlignLeft|Qt.AlignVCenter)
        self.correo.setWordWrap(False)
        sizePolicy.setHeightForWidth(self.correo.sizePolicy().hasHeightForWidth())
        self.correo.setSizePolicy(sizePolicy)
        self.correo.setProperty(u"uiRole", u"fieldLabel")

        self.layoutEstructura10.addWidget(self.correo)

        self.textocorreo = QTextEdit(self.datosRegistro)
        self.textocorreo.setObjectName(u"textocorreo")
        self.textocorreo.setMinimumSize(QSize(0, 36))
        self.textocorreo.setMaximumSize(QSize(16777215, 40))

        self.layoutEstructura10.addWidget(self.textocorreo)

        self.espacioEstructura11 = QSpacerItem(8, 8, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.layoutEstructura10.addItem(self.espacioEstructura11)


        self.layoutEstructura9.addWidget(self.datosRegistro)

        self.accesoRegistro = QFrame(self.panelRegistroUsuario)
        self.accesoRegistro.setObjectName(u"accesoRegistro")
        self.accesoRegistro.setProperty(u"uiRole", u"card")
        self.layoutEstructura12 = QVBoxLayout(self.accesoRegistro)
        self.layoutEstructura12.setSpacing(8)
        self.layoutEstructura12.setObjectName(u"layoutEstructura12")
        self.layoutEstructura12.setContentsMargins(12, 12, 12, 12)
        self.accesoRegistroTitulo = QLabel(self.accesoRegistro)
        self.accesoRegistroTitulo.setObjectName(u"accesoRegistroTitulo")
        self.accesoRegistroTitulo.setProperty(u"uiRole", u"section")
        sizePolicy.setHeightForWidth(self.accesoRegistroTitulo.sizePolicy().hasHeightForWidth())
        self.accesoRegistroTitulo.setSizePolicy(sizePolicy)

        self.layoutEstructura12.addWidget(self.accesoRegistroTitulo)

        self.password = QLabel(self.accesoRegistro)
        self.password.setObjectName(u"password")
        self.password.setAlignment(Qt.AlignLeft|Qt.AlignVCenter)
        self.password.setWordWrap(False)
        sizePolicy.setHeightForWidth(self.password.sizePolicy().hasHeightForWidth())
        self.password.setSizePolicy(sizePolicy)
        self.password.setProperty(u"uiRole", u"fieldLabel")

        self.layoutEstructura12.addWidget(self.password)

        self.textopassword = QTextEdit(self.accesoRegistro)
        self.textopassword.setObjectName(u"textopassword")
        self.textopassword.setMinimumSize(QSize(0, 36))
        self.textopassword.setMaximumSize(QSize(16777215, 40))

        self.layoutEstructura12.addWidget(self.textopassword)

        self.rol = QLabel(self.accesoRegistro)
        self.rol.setObjectName(u"rol")
        self.rol.setAlignment(Qt.AlignLeft|Qt.AlignVCenter)
        self.rol.setWordWrap(False)
        sizePolicy.setHeightForWidth(self.rol.sizePolicy().hasHeightForWidth())
        self.rol.setSizePolicy(sizePolicy)
        self.rol.setProperty(u"uiRole", u"fieldLabel")

        self.layoutEstructura12.addWidget(self.rol)

        self.listaroles = QComboBox(self.accesoRegistro)
        self.listaroles.setObjectName(u"listaroles")
        self.listaroles.setMinimumSize(QSize(0, 36))
        self.listaroles.setMaximumSize(QSize(16777215, 40))

        self.layoutEstructura12.addWidget(self.listaroles)

        self.espacioEstructura13 = QSpacerItem(8, 8, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.layoutEstructura12.addItem(self.espacioEstructura13)


        self.layoutEstructura9.addWidget(self.accesoRegistro)

        self.layoutEstructura9.setStretch(0, 1)
        self.layoutEstructura9.setStretch(1, 1)

        self.layoutEstructura8.addLayout(self.layoutEstructura9)

        self.layoutEstructura14 = QHBoxLayout()
        self.layoutEstructura14.setSpacing(8)
        self.layoutEstructura14.setObjectName(u"layoutEstructura14")
        self.layoutEstructura14.setContentsMargins(0, 0, 0, 0)
        self.espacioEstructura15 = QSpacerItem(8, 8, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.layoutEstructura14.addItem(self.espacioEstructura15)

        self.botonguardar = QPushButton(self.panelRegistroUsuario)
        self.botonguardar.setObjectName(u"botonguardar")
        sizePolicy.setHeightForWidth(self.botonguardar.sizePolicy().hasHeightForWidth())
        self.botonguardar.setSizePolicy(sizePolicy)
        self.botonguardar.setProperty(u"uiRole", u"primary")
        self.botonguardar.setMinimumSize(QSize(140, 38))
        self.botonguardar.setMaximumSize(QSize(240, 40))

        self.layoutEstructura14.addWidget(self.botonguardar)


        self.layoutEstructura8.addLayout(self.layoutEstructura14)

        self.areaContenido.setWidget(self.panelRegistroUsuario)

        self.gridLayout_2.addWidget(self.areaContenido)

        self.pieAplicacion = QLabel(self.centralwidget)
        self.pieAplicacion.setObjectName(u"pieAplicacion")
        sizePolicy.setHeightForWidth(self.pieAplicacion.sizePolicy().hasHeightForWidth())
        self.pieAplicacion.setSizePolicy(sizePolicy)
        self.pieAplicacion.setProperty(u"uiRole", u"caption")
        self.pieAplicacion.setAlignment(Qt.AlignCenter)

        self.gridLayout_2.addWidget(self.pieAplicacion)

        self.gridLayout_2.setStretch(2, 1)
        RegistroUsuarioWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(RegistroUsuarioWindow)

        QMetaObject.connectSlotsByName(RegistroUsuarioWindow)
    # setupUi

    def retranslateUi(self, RegistroUsuarioWindow):
        RegistroUsuarioWindow.setWindowTitle(QCoreApplication.translate("RegistroUsuarioWindow", u"MainWindow", None))
        self.Rumsa.setText(QCoreApplication.translate("RegistroUsuarioWindow", u"RUMSA", None))
        self.labelCompany.setText(QCoreApplication.translate("RegistroUsuarioWindow", u"Rutas Urbanas de Matehuala S.A. de C.V.", None))
        self.usuario.setText(QCoreApplication.translate("RegistroUsuarioWindow", u"Usuario", None))
        self.labelEstadoConexion.setText(QCoreApplication.translate("RegistroUsuarioWindow", u"\u25cf Conectando", None))
        self.botonregresar.setText(QCoreApplication.translate("RegistroUsuarioWindow", u"<  Volver", None))
        self.etiquetaPuerto.setText(QCoreApplication.translate("RegistroUsuarioWindow", u"Puerto del lector", None))
        self.sustituirtarjeta.setText(QCoreApplication.translate("RegistroUsuarioWindow", u"Registro Empleados", None))
        self.labelHeaderInfo.setText(QCoreApplication.translate("RegistroUsuarioWindow", u"M\u00f3dulo de Registro Empleados", None))
        self.datosRegistroTitulo.setText(QCoreApplication.translate("RegistroUsuarioWindow", u"Datos personales", None))
        self.nombre.setText(QCoreApplication.translate("RegistroUsuarioWindow", u"Nombre", None))
        self.correo.setText(QCoreApplication.translate("RegistroUsuarioWindow", u"Correo", None))
        self.accesoRegistroTitulo.setText(QCoreApplication.translate("RegistroUsuarioWindow", u"Acceso al sistema", None))
        self.password.setText(QCoreApplication.translate("RegistroUsuarioWindow", u"Contrase\u00f1a", None))
        self.rol.setText(QCoreApplication.translate("RegistroUsuarioWindow", u"Rol", None))
        self.botonguardar.setText(QCoreApplication.translate("RegistroUsuarioWindow", u"Guardar", None))
        self.pieAplicacion.setText(QCoreApplication.translate("RegistroUsuarioWindow", u"RUMSA - Rutas Urbanas de Matehuala", None))
    # retranslateUi

