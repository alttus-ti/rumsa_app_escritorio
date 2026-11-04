# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'administrador.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QHBoxLayout,
    QLabel, QMainWindow, QPushButton, QSizePolicy,
    QSpacerItem, QStackedWidget, QToolButton, QVBoxLayout,
    QWidget)

class AdminWindow(object):
    def setupUi(self, AdminWindow):
        if not AdminWindow.objectName():
            AdminWindow.setObjectName(u"AdminWindow")
        AdminWindow.setMinimumSize(QSize(760, 680))
        AdminWindow.resize(860, 780)
        self.centralwidget = QWidget(AdminWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QVBoxLayout(self.centralwidget)
        self.gridLayout.setSpacing(12)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(16, 16, 16, 16)
        self.frame_2 = QFrame(self.centralwidget)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.frame_2.setProperty(u"uiRole", u"header")
        self.frame_2.setMinimumSize(QSize(0, 90))
        self.frame_2.setMaximumSize(QSize(16777215, 90))
        self.layoutEstructura2 = QHBoxLayout(self.frame_2)
        self.layoutEstructura2.setSpacing(12)
        self.layoutEstructura2.setObjectName(u"layoutEstructura2")
        self.layoutEstructura2.setContentsMargins(12, 12, 12, 12)
        self.frame = QFrame(self.frame_2)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.frame.setProperty(u"uiRole", u"stripe")
        self.frame.setMinimumSize(QSize(5, 32))
        self.frame.setMaximumSize(QSize(5, 32))

        self.layoutEstructura2.addWidget(self.frame, 0, Qt.AlignVCenter)

        self.marcaCabecera = QWidget(self.frame_2)
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

        self.labelHeaderInfo_4 = QLabel(self.marcaCabecera)
        self.labelHeaderInfo_4.setObjectName(u"labelHeaderInfo_4")
        self.labelHeaderInfo_4.setAlignment(Qt.AlignLeft|Qt.AlignVCenter)
        sizePolicy.setHeightForWidth(self.labelHeaderInfo_4.sizePolicy().hasHeightForWidth())
        self.labelHeaderInfo_4.setSizePolicy(sizePolicy)
        self.labelHeaderInfo_4.setProperty(u"uiRole", u"caption")
        self.labelHeaderInfo_4.setWordWrap(False)

        self.layoutEstructura4.addWidget(self.labelHeaderInfo_4)


        self.layoutEstructura2.addWidget(self.marcaCabecera)

        self.espacioEstructura3 = QSpacerItem(8, 8, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.layoutEstructura2.addItem(self.espacioEstructura3)

        self.estadoCabecera = QWidget(self.frame_2)
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


        self.gridLayout.addWidget(self.frame_2)

        self.layoutEstructura6 = QHBoxLayout()
        self.layoutEstructura6.setSpacing(8)
        self.layoutEstructura6.setObjectName(u"layoutEstructura6")
        self.layoutEstructura6.setContentsMargins(0, 0, 0, 0)
        self.botonusuario = QPushButton(self.centralwidget)
        self.botonusuario.setObjectName(u"botonusuario")
        sizePolicy.setHeightForWidth(self.botonusuario.sizePolicy().hasHeightForWidth())
        self.botonusuario.setSizePolicy(sizePolicy)
        self.botonusuario.setProperty(u"uiRole", u"navigation")
        self.botonusuario.setMinimumSize(QSize(140, 36))
        self.botonusuario.setMaximumSize(QSize(180, 40))

        self.layoutEstructura6.addWidget(self.botonusuario)

        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setObjectName(u"pushButton")
        sizePolicy.setHeightForWidth(self.pushButton.sizePolicy().hasHeightForWidth())
        self.pushButton.setSizePolicy(sizePolicy)
        self.pushButton.setProperty(u"uiRole", u"navigation")
        self.pushButton.setMinimumSize(QSize(140, 36))
        self.pushButton.setMaximumSize(QSize(180, 40))

        self.layoutEstructura6.addWidget(self.pushButton)

        self.espacioEstructura7 = QSpacerItem(8, 8, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.layoutEstructura6.addItem(self.espacioEstructura7)


        self.gridLayout.addLayout(self.layoutEstructura6)

        self.stackedWidget = QStackedWidget(self.centralwidget)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.page_3 = QWidget()
        self.page_3.setObjectName(u"page_3")
        self.layoutEstructura8 = QVBoxLayout(self.page_3)
        self.layoutEstructura8.setSpacing(8)
        self.layoutEstructura8.setObjectName(u"layoutEstructura8")
        self.layoutEstructura8.setContentsMargins(0, 0, 0, 0)
        self.frameHeader_2 = QFrame(self.page_3)
        self.frameHeader_2.setObjectName(u"frameHeader_2")
        self.frameHeader_2.setFrameShape(QFrame.StyledPanel)
        self.frameHeader_2.setFrameShadow(QFrame.Raised)
        self.frameHeader_2.setProperty(u"uiRole", u"card")
        self.layoutEstructura9 = QVBoxLayout(self.frameHeader_2)
        self.layoutEstructura9.setSpacing(12)
        self.layoutEstructura9.setObjectName(u"layoutEstructura9")
        self.layoutEstructura9.setContentsMargins(16, 16, 16, 16)
        self.opcionesPersonalEspacioSuperior = QSpacerItem(0, 8, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.layoutEstructura9.addItem(self.opcionesPersonalEspacioSuperior)

        self.opcionesPersonal = QWidget(self.frameHeader_2)
        self.opcionesPersonal.setObjectName(u"opcionesPersonal")
        self.opcionesPersonal.setMinimumSize(QSize(640, 0))
        self.opcionesPersonal.setMaximumSize(QSize(720, 16777215))
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.opcionesPersonal.sizePolicy().hasHeightForWidth())
        self.opcionesPersonal.setSizePolicy(sizePolicy1)
        self.opcionesPersonalLayout = QVBoxLayout(self.opcionesPersonal)
        self.opcionesPersonalLayout.setSpacing(12)
        self.opcionesPersonalLayout.setObjectName(u"opcionesPersonalLayout")
        self.opcionesPersonalLayout.setContentsMargins(0, 0, 0, 0)
        self.menu_3 = QLabel(self.opcionesPersonal)
        self.menu_3.setObjectName(u"menu_3")
        self.menu_3.setAlignment(Qt.AlignLeft|Qt.AlignVCenter)
        self.menu_3.setWordWrap(False)
        sizePolicy.setHeightForWidth(self.menu_3.sizePolicy().hasHeightForWidth())
        self.menu_3.setSizePolicy(sizePolicy)
        self.menu_3.setProperty(u"uiRole", u"heading")

        self.opcionesPersonalLayout.addWidget(self.menu_3)

        self.labelHeaderInfo_3 = QLabel(self.opcionesPersonal)
        self.labelHeaderInfo_3.setObjectName(u"labelHeaderInfo_3")
        self.labelHeaderInfo_3.setProperty(u"uiRole", u"caption")
        self.labelHeaderInfo_3.setAlignment(Qt.AlignLeft|Qt.AlignVCenter)
        self.labelHeaderInfo_3.setWordWrap(False)
        sizePolicy.setHeightForWidth(self.labelHeaderInfo_3.sizePolicy().hasHeightForWidth())
        self.labelHeaderInfo_3.setSizePolicy(sizePolicy)

        self.opcionesPersonalLayout.addWidget(self.labelHeaderInfo_3)

        self.opcionesPersonalTarjetas = QGridLayout()
        self.opcionesPersonalTarjetas.setObjectName(u"opcionesPersonalTarjetas")
        self.opcionesPersonalTarjetas.setHorizontalSpacing(16)
        self.opcionesPersonalTarjetas.setVerticalSpacing(16)
        self.opcionesPersonalTarjetas.setContentsMargins(0, 0, 0, 0)
        self.botonalta_2 = QPushButton(self.opcionesPersonal)
        self.botonalta_2.setObjectName(u"botonalta_2")
        sizePolicy.setHeightForWidth(self.botonalta_2.sizePolicy().hasHeightForWidth())
        self.botonalta_2.setSizePolicy(sizePolicy)
        self.botonalta_2.setProperty(u"uiRole", u"menuAction")
        self.botonalta_2.setProperty(u"menuTone", u"blue")
        self.botonalta_2.setMinimumSize(QSize(0, 170))
        self.botonalta_2.setMaximumSize(QSize(16777215, 190))
        self.botonalta_2.setProperty(u"menuShape", u"tile")

        self.opcionesPersonalTarjetas.addWidget(self.botonalta_2, 0, 0, 1, 1)

        self.botonsustituir_2 = QPushButton(self.opcionesPersonal)
        self.botonsustituir_2.setObjectName(u"botonsustituir_2")
        sizePolicy.setHeightForWidth(self.botonsustituir_2.sizePolicy().hasHeightForWidth())
        self.botonsustituir_2.setSizePolicy(sizePolicy)
        self.botonsustituir_2.setProperty(u"uiRole", u"menuAction")
        self.botonsustituir_2.setProperty(u"menuTone", u"yellow")
        self.botonsustituir_2.setMinimumSize(QSize(0, 170))
        self.botonsustituir_2.setMaximumSize(QSize(16777215, 190))
        self.botonsustituir_2.setProperty(u"menuShape", u"tile")

        self.opcionesPersonalTarjetas.addWidget(self.botonsustituir_2, 0, 1, 1, 1)

        self.botoncancelar_2 = QPushButton(self.opcionesPersonal)
        self.botoncancelar_2.setObjectName(u"botoncancelar_2")
        sizePolicy.setHeightForWidth(self.botoncancelar_2.sizePolicy().hasHeightForWidth())
        self.botoncancelar_2.setSizePolicy(sizePolicy)
        self.botoncancelar_2.setProperty(u"uiRole", u"menuAction")
        self.botoncancelar_2.setProperty(u"menuTone", u"blue")
        self.botoncancelar_2.setMinimumSize(QSize(312, 170))
        self.botoncancelar_2.setMaximumSize(QSize(312, 190))
        self.botoncancelar_2.setProperty(u"menuShape", u"tile")

        self.opcionesPersonalTarjetas.addWidget(self.botoncancelar_2, 1, 0, 1, 2, Qt.AlignHCenter)

        self.opcionesPersonalTarjetas.setRowStretch(0, 1)
        self.opcionesPersonalTarjetas.setRowStretch(1, 1)
        self.opcionesPersonalTarjetas.setColumnStretch(0, 1)
        self.opcionesPersonalTarjetas.setColumnStretch(1, 1)

        self.opcionesPersonalLayout.addLayout(self.opcionesPersonalTarjetas)


        self.layoutEstructura9.addWidget(self.opcionesPersonal, 0, Qt.AlignHCenter)

        self.opcionesPersonalEspacioInferior = QSpacerItem(0, 8, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.layoutEstructura9.addItem(self.opcionesPersonalEspacioInferior)

        self.layoutEstructura9.setStretch(0, 1)
        self.layoutEstructura9.setStretch(2, 1)

        self.layoutEstructura8.addWidget(self.frameHeader_2)

        self.stackedWidget.addWidget(self.page_3)
        self.page_4 = QWidget()
        self.page_4.setObjectName(u"page_4")
        self.layoutEstructura11 = QVBoxLayout(self.page_4)
        self.layoutEstructura11.setSpacing(8)
        self.layoutEstructura11.setObjectName(u"layoutEstructura11")
        self.layoutEstructura11.setContentsMargins(0, 0, 0, 0)
        self.frameHeader = QFrame(self.page_4)
        self.frameHeader.setObjectName(u"frameHeader")
        self.frameHeader.setFrameShape(QFrame.StyledPanel)
        self.frameHeader.setFrameShadow(QFrame.Raised)
        self.frameHeader.setProperty(u"uiRole", u"card")
        self.layoutEstructura12 = QVBoxLayout(self.frameHeader)
        self.layoutEstructura12.setSpacing(12)
        self.layoutEstructura12.setObjectName(u"layoutEstructura12")
        self.layoutEstructura12.setContentsMargins(16, 16, 16, 16)
        self.opcionesPasajerosEspacioSuperior = QSpacerItem(0, 8, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.layoutEstructura12.addItem(self.opcionesPasajerosEspacioSuperior)

        self.opcionesPasajeros = QWidget(self.frameHeader)
        self.opcionesPasajeros.setObjectName(u"opcionesPasajeros")
        self.opcionesPasajeros.setMinimumSize(QSize(640, 0))
        self.opcionesPasajeros.setMaximumSize(QSize(720, 16777215))
        sizePolicy1.setHeightForWidth(self.opcionesPasajeros.sizePolicy().hasHeightForWidth())
        self.opcionesPasajeros.setSizePolicy(sizePolicy1)
        self.opcionesPasajerosLayout = QVBoxLayout(self.opcionesPasajeros)
        self.opcionesPasajerosLayout.setSpacing(12)
        self.opcionesPasajerosLayout.setObjectName(u"opcionesPasajerosLayout")
        self.opcionesPasajerosLayout.setContentsMargins(0, 0, 0, 0)
        self.menu_2 = QLabel(self.opcionesPasajeros)
        self.menu_2.setObjectName(u"menu_2")
        self.menu_2.setAlignment(Qt.AlignLeft|Qt.AlignVCenter)
        self.menu_2.setWordWrap(False)
        sizePolicy.setHeightForWidth(self.menu_2.sizePolicy().hasHeightForWidth())
        self.menu_2.setSizePolicy(sizePolicy)
        self.menu_2.setProperty(u"uiRole", u"heading")

        self.opcionesPasajerosLayout.addWidget(self.menu_2)

        self.labelHeaderInfo_2 = QLabel(self.opcionesPasajeros)
        self.labelHeaderInfo_2.setObjectName(u"labelHeaderInfo_2")
        self.labelHeaderInfo_2.setProperty(u"uiRole", u"caption")
        self.labelHeaderInfo_2.setAlignment(Qt.AlignLeft|Qt.AlignVCenter)
        self.labelHeaderInfo_2.setWordWrap(False)
        sizePolicy.setHeightForWidth(self.labelHeaderInfo_2.sizePolicy().hasHeightForWidth())
        self.labelHeaderInfo_2.setSizePolicy(sizePolicy)

        self.opcionesPasajerosLayout.addWidget(self.labelHeaderInfo_2)

        self.opcionesPasajerosTarjetas = QGridLayout()
        self.opcionesPasajerosTarjetas.setObjectName(u"opcionesPasajerosTarjetas")
        self.opcionesPasajerosTarjetas.setHorizontalSpacing(16)
        self.opcionesPasajerosTarjetas.setVerticalSpacing(16)
        self.opcionesPasajerosTarjetas.setContentsMargins(0, 0, 0, 0)
        self.botonalta = QPushButton(self.opcionesPasajeros)
        self.botonalta.setObjectName(u"botonalta")
        sizePolicy.setHeightForWidth(self.botonalta.sizePolicy().hasHeightForWidth())
        self.botonalta.setSizePolicy(sizePolicy)
        self.botonalta.setProperty(u"uiRole", u"menuAction")
        self.botonalta.setProperty(u"menuTone", u"blue")
        self.botonalta.setMinimumSize(QSize(0, 170))
        self.botonalta.setMaximumSize(QSize(16777215, 190))
        self.botonalta.setProperty(u"menuShape", u"tile")

        self.opcionesPasajerosTarjetas.addWidget(self.botonalta, 0, 0, 1, 1)

        self.botonsustituir = QPushButton(self.opcionesPasajeros)
        self.botonsustituir.setObjectName(u"botonsustituir")
        sizePolicy.setHeightForWidth(self.botonsustituir.sizePolicy().hasHeightForWidth())
        self.botonsustituir.setSizePolicy(sizePolicy)
        self.botonsustituir.setProperty(u"uiRole", u"menuAction")
        self.botonsustituir.setProperty(u"menuTone", u"yellow")
        self.botonsustituir.setMinimumSize(QSize(0, 170))
        self.botonsustituir.setMaximumSize(QSize(16777215, 190))
        self.botonsustituir.setProperty(u"menuShape", u"tile")

        self.opcionesPasajerosTarjetas.addWidget(self.botonsustituir, 0, 1, 1, 1)

        self.botonrecarga = QPushButton(self.opcionesPasajeros)
        self.botonrecarga.setObjectName(u"botonrecarga")
        sizePolicy.setHeightForWidth(self.botonrecarga.sizePolicy().hasHeightForWidth())
        self.botonrecarga.setSizePolicy(sizePolicy)
        self.botonrecarga.setProperty(u"uiRole", u"menuAction")
        self.botonrecarga.setProperty(u"menuTone", u"blue")
        self.botonrecarga.setMinimumSize(QSize(0, 170))
        self.botonrecarga.setMaximumSize(QSize(16777215, 190))
        self.botonrecarga.setProperty(u"menuShape", u"tile")

        self.opcionesPasajerosTarjetas.addWidget(self.botonrecarga, 1, 0, 1, 1)

        self.botoncancelar = QPushButton(self.opcionesPasajeros)
        self.botoncancelar.setObjectName(u"botoncancelar")
        sizePolicy.setHeightForWidth(self.botoncancelar.sizePolicy().hasHeightForWidth())
        self.botoncancelar.setSizePolicy(sizePolicy)
        self.botoncancelar.setProperty(u"uiRole", u"menuAction")
        self.botoncancelar.setProperty(u"menuTone", u"yellow")
        self.botoncancelar.setMinimumSize(QSize(0, 170))
        self.botoncancelar.setMaximumSize(QSize(16777215, 190))
        self.botoncancelar.setProperty(u"menuShape", u"tile")

        self.opcionesPasajerosTarjetas.addWidget(self.botoncancelar, 1, 1, 1, 1)

        self.opcionesPasajerosTarjetas.setRowStretch(0, 1)
        self.opcionesPasajerosTarjetas.setRowStretch(1, 1)
        self.opcionesPasajerosTarjetas.setColumnStretch(0, 1)
        self.opcionesPasajerosTarjetas.setColumnStretch(1, 1)

        self.opcionesPasajerosLayout.addLayout(self.opcionesPasajerosTarjetas)


        self.layoutEstructura12.addWidget(self.opcionesPasajeros, 0, Qt.AlignHCenter)

        self.opcionesPasajerosEspacioInferior = QSpacerItem(0, 8, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.layoutEstructura12.addItem(self.opcionesPasajerosEspacioInferior)

        self.layoutEstructura12.setStretch(0, 1)
        self.layoutEstructura12.setStretch(2, 1)

        self.layoutEstructura11.addWidget(self.frameHeader)

        self.stackedWidget.addWidget(self.page_4)

        self.gridLayout.addWidget(self.stackedWidget)

        self.labelHeaderInfo = QLabel(self.centralwidget)
        self.labelHeaderInfo.setObjectName(u"labelHeaderInfo")
        self.labelHeaderInfo.setWordWrap(False)
        sizePolicy.setHeightForWidth(self.labelHeaderInfo.sizePolicy().hasHeightForWidth())
        self.labelHeaderInfo.setSizePolicy(sizePolicy)
        self.labelHeaderInfo.setProperty(u"uiRole", u"caption")
        self.labelHeaderInfo.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.labelHeaderInfo)

        self.gridLayout.setStretch(2, 1)
        AdminWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(AdminWindow)

        self.stackedWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(AdminWindow)
    # setupUi

    def retranslateUi(self, AdminWindow):
        AdminWindow.setWindowTitle(QCoreApplication.translate("AdminWindow", u"Administrador", None))
#if QT_CONFIG(accessibility)
        AdminWindow.setAccessibleName("")
#endif // QT_CONFIG(accessibility)
        self.labelBrand.setText(QCoreApplication.translate("AdminWindow", u"RUMSA", None))
        self.labelHeaderInfo_4.setText(QCoreApplication.translate("AdminWindow", u"Rutas Urbanas de Matehuala S.A. de C.V.", None))
        self.usuario.setText(QCoreApplication.translate("AdminWindow", u"Usuario", None))
#if QT_CONFIG(tooltip)
        self.labelEstadoConexion.setToolTip(QCoreApplication.translate("AdminWindow", u"Este texto puede cambiar a: Conectando, Sin conexi\u00f3n, Sincronizando o Conectado.", None))
#endif // QT_CONFIG(tooltip)
        self.labelEstadoConexion.setText(QCoreApplication.translate("AdminWindow", u"\u25cf Conectando", None))
        self.botonusuario.setText(QCoreApplication.translate("AdminWindow", u"Pasajeros", None))
        self.pushButton.setText(QCoreApplication.translate("AdminWindow", u"Personal", None))
        self.menu_3.setText(QCoreApplication.translate("AdminWindow", u"Men\u00fa Personal", None))
        self.labelHeaderInfo_3.setText(QCoreApplication.translate("AdminWindow", u"Selecciona una Opci\u00f3n", None))
        self.botonalta_2.setText(QCoreApplication.translate("AdminWindow", u"Alta >", None))
        self.botonsustituir_2.setText(QCoreApplication.translate("AdminWindow", u"Sustituir >", None))
        self.botoncancelar_2.setText(QCoreApplication.translate("AdminWindow", u"Cancelar >", None))
        self.menu_2.setText(QCoreApplication.translate("AdminWindow", u"Men\u00fa Pasajero", None))
        self.labelHeaderInfo_2.setText(QCoreApplication.translate("AdminWindow", u"Selecciona una Opci\u00f3n", None))
        self.botonalta.setText(QCoreApplication.translate("AdminWindow", u"Dar de Alta >", None))
        self.botonsustituir.setText(QCoreApplication.translate("AdminWindow", u"Sustituir Tarjeta >", None))
        self.botonrecarga.setText(QCoreApplication.translate("AdminWindow", u"Recargar Tarjeta >", None))
        self.botoncancelar.setText(QCoreApplication.translate("AdminWindow", u"Cancelar Tarjeta >", None))
        self.labelHeaderInfo.setText(QCoreApplication.translate("AdminWindow", u"RUMSA - Rutas Urbanas de Matehuala", None))
    # retranslateUi

