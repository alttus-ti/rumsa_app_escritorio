# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'cancelar.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QFrame,
    QHBoxLayout, QLabel, QMainWindow, QPlainTextEdit,
    QPushButton, QScrollArea, QSizePolicy, QSpacerItem,
    QToolButton, QVBoxLayout, QWidget)

class CancelarWindow(object):
    def setupUi(self, CancelarWindow):
        if not CancelarWindow.objectName():
            CancelarWindow.setObjectName(u"CancelarWindow")
        CancelarWindow.setMinimumSize(QSize(760, 680))
        CancelarWindow.resize(860, 780)
        self.centralwidget = QWidget(CancelarWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QVBoxLayout(self.centralwidget)
        self.gridLayout.setSpacing(12)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(16, 16, 16, 16)
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
        self.labelBrand = QLabel(self.marcaCabecera)
        self.labelBrand.setObjectName(u"labelBrand")
        self.labelBrand.setAlignment(Qt.AlignLeft|Qt.AlignVCenter)
        self.labelBrand.setWordWrap(False)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelBrand.sizePolicy().hasHeightForWidth())
        self.labelBrand.setSizePolicy(sizePolicy)
        self.labelBrand.setProperty(u"uiRole", u"brand")

        self.layoutEstructura4.addWidget(self.labelBrand)

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


        self.gridLayout.addWidget(self.frame)

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

        self.puerto = QComboBox(self.centralwidget)
        self.puerto.setObjectName(u"puerto")
        self.puerto.setMinimumSize(QSize(220, 36))
        self.puerto.setMaximumSize(QSize(260, 40))

        self.layoutEstructura6.addWidget(self.puerto)


        self.gridLayout.addLayout(self.layoutEstructura6)

        self.areaContenido = QScrollArea(self.centralwidget)
        self.areaContenido.setObjectName(u"areaContenido")
        self.areaContenido.setWidgetResizable(True)
        self.areaContenido.setFrameShape(QFrame.NoFrame)
        self.panelCancelacion = QFrame()
        self.panelCancelacion.setObjectName(u"panelCancelacion")
        self.panelCancelacion.setProperty(u"uiRole", u"card")
        self.layoutEstructura8 = QVBoxLayout(self.panelCancelacion)
        self.layoutEstructura8.setSpacing(12)
        self.layoutEstructura8.setObjectName(u"layoutEstructura8")
        self.layoutEstructura8.setContentsMargins(16, 16, 16, 16)
        self.textocancelar = QLabel(self.panelCancelacion)
        self.textocancelar.setObjectName(u"textocancelar")
        self.textocancelar.setAlignment(Qt.AlignLeft|Qt.AlignVCenter)
        self.textocancelar.setWordWrap(False)
        sizePolicy.setHeightForWidth(self.textocancelar.sizePolicy().hasHeightForWidth())
        self.textocancelar.setSizePolicy(sizePolicy)
        self.textocancelar.setProperty(u"uiRole", u"heading")

        self.layoutEstructura8.addWidget(self.textocancelar)

        self.labelHeaderInfo = QLabel(self.panelCancelacion)
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
        self.datosTarjetaCancelacion = QFrame(self.panelCancelacion)
        self.datosTarjetaCancelacion.setObjectName(u"datosTarjetaCancelacion")
        self.datosTarjetaCancelacion.setProperty(u"uiRole", u"card")
        self.layoutEstructura10 = QVBoxLayout(self.datosTarjetaCancelacion)
        self.layoutEstructura10.setSpacing(8)
        self.layoutEstructura10.setObjectName(u"layoutEstructura10")
        self.layoutEstructura10.setContentsMargins(12, 12, 12, 12)
        self.tituloDatosCancelacion = QLabel(self.datosTarjetaCancelacion)
        self.tituloDatosCancelacion.setObjectName(u"tituloDatosCancelacion")
        self.tituloDatosCancelacion.setProperty(u"uiRole", u"section")
        sizePolicy.setHeightForWidth(self.tituloDatosCancelacion.sizePolicy().hasHeightForWidth())
        self.tituloDatosCancelacion.setSizePolicy(sizePolicy)

        self.layoutEstructura10.addWidget(self.tituloDatosCancelacion)

        self.nombre = QLabel(self.datosTarjetaCancelacion)
        self.nombre.setObjectName(u"nombre")
        self.nombre.setAlignment(Qt.AlignLeft|Qt.AlignVCenter)
        self.nombre.setWordWrap(False)
        sizePolicy.setHeightForWidth(self.nombre.sizePolicy().hasHeightForWidth())
        self.nombre.setSizePolicy(sizePolicy)
        self.nombre.setProperty(u"uiRole", u"fieldLabel")

        self.layoutEstructura10.addWidget(self.nombre)

        self.textonombre = QPlainTextEdit(self.datosTarjetaCancelacion)
        self.textonombre.setObjectName(u"textonombre")
        self.textonombre.setMinimumSize(QSize(0, 36))
        self.textonombre.setMaximumSize(QSize(16777215, 40))

        self.layoutEstructura10.addWidget(self.textonombre)

        self.uid = QLabel(self.datosTarjetaCancelacion)
        self.uid.setObjectName(u"uid")
        self.uid.setAlignment(Qt.AlignLeft|Qt.AlignVCenter)
        self.uid.setWordWrap(False)
        sizePolicy.setHeightForWidth(self.uid.sizePolicy().hasHeightForWidth())
        self.uid.setSizePolicy(sizePolicy)
        self.uid.setProperty(u"uiRole", u"fieldLabel")

        self.layoutEstructura10.addWidget(self.uid)

        self.textouid = QLabel(self.datosTarjetaCancelacion)
        self.textouid.setObjectName(u"textouid")
        self.textouid.setProperty(u"uiRole", u"value")
        self.textouid.setAlignment(Qt.AlignLeft|Qt.AlignVCenter)
        self.textouid.setWordWrap(False)
        sizePolicy.setHeightForWidth(self.textouid.sizePolicy().hasHeightForWidth())
        self.textouid.setSizePolicy(sizePolicy)

        self.layoutEstructura10.addWidget(self.textouid)

        self.listanegra = QCheckBox(self.datosTarjetaCancelacion)
        self.listanegra.setObjectName(u"listanegra")

        self.layoutEstructura10.addWidget(self.listanegra)

        self.espacioEstructura11 = QSpacerItem(8, 8, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.layoutEstructura10.addItem(self.espacioEstructura11)


        self.layoutEstructura9.addWidget(self.datosTarjetaCancelacion)

        self.motivoCancelacion = QFrame(self.panelCancelacion)
        self.motivoCancelacion.setObjectName(u"motivoCancelacion")
        self.motivoCancelacion.setProperty(u"uiRole", u"card")
        self.layoutEstructura12 = QVBoxLayout(self.motivoCancelacion)
        self.layoutEstructura12.setSpacing(8)
        self.layoutEstructura12.setObjectName(u"layoutEstructura12")
        self.layoutEstructura12.setContentsMargins(12, 12, 12, 12)
        self.tituloMotivoCancelacion = QLabel(self.motivoCancelacion)
        self.tituloMotivoCancelacion.setObjectName(u"tituloMotivoCancelacion")
        self.tituloMotivoCancelacion.setProperty(u"uiRole", u"section")
        sizePolicy.setHeightForWidth(self.tituloMotivoCancelacion.sizePolicy().hasHeightForWidth())
        self.tituloMotivoCancelacion.setSizePolicy(sizePolicy)

        self.layoutEstructura12.addWidget(self.tituloMotivoCancelacion)

        self.motivo = QLabel(self.motivoCancelacion)
        self.motivo.setObjectName(u"motivo")
        self.motivo.setAlignment(Qt.AlignLeft|Qt.AlignVCenter)
        self.motivo.setWordWrap(False)
        sizePolicy.setHeightForWidth(self.motivo.sizePolicy().hasHeightForWidth())
        self.motivo.setSizePolicy(sizePolicy)
        self.motivo.setProperty(u"uiRole", u"fieldLabel")

        self.layoutEstructura12.addWidget(self.motivo)

        self.textomotivo = QPlainTextEdit(self.motivoCancelacion)
        self.textomotivo.setObjectName(u"textomotivo")
        self.textomotivo.setMinimumSize(QSize(0, 140))
        self.textomotivo.setMaximumSize(QSize(16777215, 200))

        self.layoutEstructura12.addWidget(self.textomotivo)

        self.espacioEstructura13 = QSpacerItem(8, 8, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.layoutEstructura12.addItem(self.espacioEstructura13)


        self.layoutEstructura9.addWidget(self.motivoCancelacion)

        self.layoutEstructura9.setStretch(0, 1)
        self.layoutEstructura9.setStretch(1, 1)

        self.layoutEstructura8.addLayout(self.layoutEstructura9)

        self.layoutEstructura14 = QHBoxLayout()
        self.layoutEstructura14.setSpacing(8)
        self.layoutEstructura14.setObjectName(u"layoutEstructura14")
        self.layoutEstructura14.setContentsMargins(0, 0, 0, 0)
        self.espacioEstructura15 = QSpacerItem(8, 8, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.layoutEstructura14.addItem(self.espacioEstructura15)

        self.pushButton = QPushButton(self.panelCancelacion)
        self.pushButton.setObjectName(u"pushButton")
        sizePolicy.setHeightForWidth(self.pushButton.sizePolicy().hasHeightForWidth())
        self.pushButton.setSizePolicy(sizePolicy)
        self.pushButton.setProperty(u"uiRole", u"secondary")
        self.pushButton.setMinimumSize(QSize(140, 38))
        self.pushButton.setMaximumSize(QSize(240, 40))

        self.layoutEstructura14.addWidget(self.pushButton)

        self.botoncancelar = QPushButton(self.panelCancelacion)
        self.botoncancelar.setObjectName(u"botoncancelar")
        sizePolicy.setHeightForWidth(self.botoncancelar.sizePolicy().hasHeightForWidth())
        self.botoncancelar.setSizePolicy(sizePolicy)
        self.botoncancelar.setProperty(u"uiRole", u"accent")
        self.botoncancelar.setMinimumSize(QSize(140, 38))
        self.botoncancelar.setMaximumSize(QSize(240, 40))

        self.layoutEstructura14.addWidget(self.botoncancelar)


        self.layoutEstructura8.addLayout(self.layoutEstructura14)

        self.areaContenido.setWidget(self.panelCancelacion)

        self.gridLayout.addWidget(self.areaContenido)

        self.pieAplicacion = QLabel(self.centralwidget)
        self.pieAplicacion.setObjectName(u"pieAplicacion")
        sizePolicy.setHeightForWidth(self.pieAplicacion.sizePolicy().hasHeightForWidth())
        self.pieAplicacion.setSizePolicy(sizePolicy)
        self.pieAplicacion.setProperty(u"uiRole", u"caption")
        self.pieAplicacion.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.pieAplicacion)

        self.gridLayout.setStretch(2, 1)
        CancelarWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(CancelarWindow)

        QMetaObject.connectSlotsByName(CancelarWindow)
    # setupUi

    def retranslateUi(self, CancelarWindow):
        CancelarWindow.setWindowTitle(QCoreApplication.translate("CancelarWindow", u"Cancelar", None))
        self.labelBrand.setText(QCoreApplication.translate("CancelarWindow", u"RUMSA", None))
        self.labelCompany.setText(QCoreApplication.translate("CancelarWindow", u"Rutas Urbanas de Matehuala S.A. de C.V.", None))
        self.usuario.setText(QCoreApplication.translate("CancelarWindow", u"Usuario", None))
        self.labelEstadoConexion.setText(QCoreApplication.translate("CancelarWindow", u"\u25cf Conectando", None))
        self.botonregresar.setText(QCoreApplication.translate("CancelarWindow", u"<  Volver", None))
        self.etiquetaPuerto.setText(QCoreApplication.translate("CancelarWindow", u"Puerto del lector", None))
        self.textocancelar.setText(QCoreApplication.translate("CancelarWindow", u"Cancelar Tarjeta", None))
        self.labelHeaderInfo.setText(QCoreApplication.translate("CancelarWindow", u"M\u00f3dulo de cancelaci\u00f3n", None))
        self.tituloDatosCancelacion.setText(QCoreApplication.translate("CancelarWindow", u"Datos de la tarjeta", None))
        self.nombre.setText(QCoreApplication.translate("CancelarWindow", u"Nombre", None))
        self.uid.setText(QCoreApplication.translate("CancelarWindow", u"UID", None))
        self.textouid.setText(QCoreApplication.translate("CancelarWindow", u"UID", None))
        self.listanegra.setText(QCoreApplication.translate("CancelarWindow", u"Lista Negra", None))
        self.tituloMotivoCancelacion.setText(QCoreApplication.translate("CancelarWindow", u"Cancelaci\u00f3n", None))
        self.motivo.setText(QCoreApplication.translate("CancelarWindow", u"Motivo", None))
        self.pushButton.setText(QCoreApplication.translate("CancelarWindow", u"Reactivar Tarjeta", None))
        self.botoncancelar.setText(QCoreApplication.translate("CancelarWindow", u"Cancelar Tarjeta", None))
        self.pieAplicacion.setText(QCoreApplication.translate("CancelarWindow", u"RUMSA - Rutas Urbanas de Matehuala", None))
    # retranslateUi

