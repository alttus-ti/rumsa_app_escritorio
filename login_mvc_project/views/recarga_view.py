# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'recarga.ui'
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
    QLabel, QLineEdit, QMainWindow, QPlainTextEdit,
    QPushButton, QScrollArea, QSizePolicy, QSpacerItem,
    QToolButton, QVBoxLayout, QWidget)

class RecargaWindow(object):
    def setupUi(self, RecargaWindow):
        if not RecargaWindow.objectName():
            RecargaWindow.setObjectName(u"RecargaWindow")
        RecargaWindow.setMinimumSize(QSize(760, 680))
        RecargaWindow.resize(860, 780)
        self.centralwidget = QWidget(RecargaWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.layoutPrincipalRecarga = QVBoxLayout(self.centralwidget)
        self.layoutPrincipalRecarga.setSpacing(12)
        self.layoutPrincipalRecarga.setObjectName(u"layoutPrincipalRecarga")
        self.layoutPrincipalRecarga.setContentsMargins(16, 16, 16, 16)
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
        self.frame_2 = QFrame(self.frame)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.frame_2.setProperty(u"uiRole", u"stripe")
        self.frame_2.setMinimumSize(QSize(5, 32))
        self.frame_2.setMaximumSize(QSize(5, 32))

        self.layoutEstructura2.addWidget(self.frame_2, 0, Qt.AlignVCenter)

        self.marcaCabecera = QWidget(self.frame)
        self.marcaCabecera.setObjectName(u"marcaCabecera")
        self.layoutEstructura4 = QVBoxLayout(self.marcaCabecera)
        self.layoutEstructura4.setSpacing(2)
        self.layoutEstructura4.setObjectName(u"layoutEstructura4")
        self.layoutEstructura4.setContentsMargins(0, 0, 0, 0)
        self.labelBrand_2 = QLabel(self.marcaCabecera)
        self.labelBrand_2.setObjectName(u"labelBrand_2")
        self.labelBrand_2.setAlignment(Qt.AlignLeft|Qt.AlignVCenter)
        self.labelBrand_2.setWordWrap(False)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelBrand_2.sizePolicy().hasHeightForWidth())
        self.labelBrand_2.setSizePolicy(sizePolicy)
        self.labelBrand_2.setProperty(u"uiRole", u"brand")

        self.layoutEstructura4.addWidget(self.labelBrand_2)

        self.labelHeaderInfo_3 = QLabel(self.marcaCabecera)
        self.labelHeaderInfo_3.setObjectName(u"labelHeaderInfo_3")
        self.labelHeaderInfo_3.setAlignment(Qt.AlignLeft|Qt.AlignVCenter)
        sizePolicy.setHeightForWidth(self.labelHeaderInfo_3.sizePolicy().hasHeightForWidth())
        self.labelHeaderInfo_3.setSizePolicy(sizePolicy)
        self.labelHeaderInfo_3.setProperty(u"uiRole", u"caption")
        self.labelHeaderInfo_3.setWordWrap(False)

        self.layoutEstructura4.addWidget(self.labelHeaderInfo_3)


        self.layoutEstructura2.addWidget(self.marcaCabecera)

        self.espacioEstructura3 = QSpacerItem(8, 8, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.layoutEstructura2.addItem(self.espacioEstructura3)

        self.estadoCabecera = QWidget(self.frame)
        self.estadoCabecera.setObjectName(u"estadoCabecera")
        self.layoutEstructura5 = QVBoxLayout(self.estadoCabecera)
        self.layoutEstructura5.setSpacing(4)
        self.layoutEstructura5.setObjectName(u"layoutEstructura5")
        self.layoutEstructura5.setContentsMargins(0, 0, 0, 0)
        self.usuario_2 = QToolButton(self.estadoCabecera)
        self.usuario_2.setObjectName(u"usuario_2")
        self.usuario_2.setMinimumSize(QSize(0, 36))
        self.usuario_2.setMaximumSize(QSize(16777215, 40))
        sizePolicy.setHeightForWidth(self.usuario_2.sizePolicy().hasHeightForWidth())
        self.usuario_2.setSizePolicy(sizePolicy)

        self.layoutEstructura5.addWidget(self.usuario_2, 0, Qt.AlignRight)

        self.labelEstadoConexion_2 = QLabel(self.estadoCabecera)
        self.labelEstadoConexion_2.setObjectName(u"labelEstadoConexion_2")
        self.labelEstadoConexion_2.setProperty(u"uiRole", u"status")
        self.labelEstadoConexion_2.setAlignment(Qt.AlignLeft|Qt.AlignVCenter)
        self.labelEstadoConexion_2.setWordWrap(False)
        sizePolicy.setHeightForWidth(self.labelEstadoConexion_2.sizePolicy().hasHeightForWidth())
        self.labelEstadoConexion_2.setSizePolicy(sizePolicy)

        self.layoutEstructura5.addWidget(self.labelEstadoConexion_2, 0, Qt.AlignRight)

        self.mensajeInternet = QLabel(self.estadoCabecera)
        self.mensajeInternet.setObjectName(u"mensajeInternet")
        self.mensajeInternet.setProperty(u"uiRole", u"caption")
        self.mensajeInternet.setAlignment(Qt.AlignLeft|Qt.AlignVCenter)
        self.mensajeInternet.setWordWrap(False)
        sizePolicy.setHeightForWidth(self.mensajeInternet.sizePolicy().hasHeightForWidth())
        self.mensajeInternet.setSizePolicy(sizePolicy)

        self.layoutEstructura5.addWidget(self.mensajeInternet, 0, Qt.AlignRight)


        self.layoutEstructura2.addWidget(self.estadoCabecera)


        self.layoutPrincipalRecarga.addWidget(self.frame)

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

        self.comboBox = QComboBox(self.centralwidget)
        self.comboBox.setObjectName(u"comboBox")
        self.comboBox.setMinimumSize(QSize(220, 36))
        self.comboBox.setMaximumSize(QSize(260, 40))

        self.layoutEstructura6.addWidget(self.comboBox)


        self.layoutPrincipalRecarga.addLayout(self.layoutEstructura6)

        self.areaContenido = QScrollArea(self.centralwidget)
        self.areaContenido.setObjectName(u"areaContenido")
        self.areaContenido.setWidgetResizable(True)
        self.areaContenido.setFrameShape(QFrame.NoFrame)
        self.frameHeader_4 = QFrame()
        self.frameHeader_4.setObjectName(u"frameHeader_4")
        self.frameHeader_4.setFrameShape(QFrame.StyledPanel)
        self.frameHeader_4.setFrameShadow(QFrame.Raised)
        self.frameHeader_4.setProperty(u"uiRole", u"card")
        self.layoutEstructura8 = QVBoxLayout(self.frameHeader_4)
        self.layoutEstructura8.setSpacing(12)
        self.layoutEstructura8.setObjectName(u"layoutEstructura8")
        self.layoutEstructura8.setContentsMargins(16, 16, 16, 16)
        self.menu_6 = QLabel(self.frameHeader_4)
        self.menu_6.setObjectName(u"menu_6")
        self.menu_6.setAlignment(Qt.AlignLeft|Qt.AlignVCenter)
        self.menu_6.setWordWrap(False)
        sizePolicy.setHeightForWidth(self.menu_6.sizePolicy().hasHeightForWidth())
        self.menu_6.setSizePolicy(sizePolicy)
        self.menu_6.setProperty(u"uiRole", u"heading")

        self.layoutEstructura8.addWidget(self.menu_6)

        self.layoutEstructura9 = QHBoxLayout()
        self.layoutEstructura9.setSpacing(8)
        self.layoutEstructura9.setObjectName(u"layoutEstructura9")
        self.layoutEstructura9.setContentsMargins(0, 0, 0, 0)
        self.label_2 = QLabel(self.frameHeader_4)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setProperty(u"uiRole", u"fieldLabel")
        self.label_2.setAlignment(Qt.AlignLeft|Qt.AlignVCenter)
        self.label_2.setWordWrap(False)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)

        self.layoutEstructura9.addWidget(self.label_2)

        self.listaoficina = QComboBox(self.frameHeader_4)
        self.listaoficina.setObjectName(u"listaoficina")
        self.listaoficina.setMinimumSize(QSize(0, 36))
        self.listaoficina.setMaximumSize(QSize(280, 40))

        self.layoutEstructura9.addWidget(self.listaoficina)

        self.espacioEstructura10 = QSpacerItem(8, 8, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.layoutEstructura9.addItem(self.espacioEstructura10)


        self.layoutEstructura8.addLayout(self.layoutEstructura9)

        self.layoutEstructura11 = QHBoxLayout()
        self.layoutEstructura11.setSpacing(16)
        self.layoutEstructura11.setObjectName(u"layoutEstructura11")
        self.layoutEstructura11.setContentsMargins(0, 0, 0, 0)
        self.frameHeader_2 = QFrame(self.frameHeader_4)
        self.frameHeader_2.setObjectName(u"frameHeader_2")
        self.frameHeader_2.setFrameShape(QFrame.StyledPanel)
        self.frameHeader_2.setFrameShadow(QFrame.Raised)
        self.frameHeader_2.setProperty(u"uiRole", u"card")
        self.layoutEstructura12 = QVBoxLayout(self.frameHeader_2)
        self.layoutEstructura12.setSpacing(8)
        self.layoutEstructura12.setObjectName(u"layoutEstructura12")
        self.layoutEstructura12.setContentsMargins(12, 12, 12, 12)
        self.menu_3 = QLabel(self.frameHeader_2)
        self.menu_3.setObjectName(u"menu_3")
        self.menu_3.setAlignment(Qt.AlignLeft|Qt.AlignVCenter)
        self.menu_3.setWordWrap(False)
        sizePolicy.setHeightForWidth(self.menu_3.sizePolicy().hasHeightForWidth())
        self.menu_3.setSizePolicy(sizePolicy)
        self.menu_3.setProperty(u"uiRole", u"section")

        self.layoutEstructura12.addWidget(self.menu_3)

        self.otrosdatos = QLabel(self.frameHeader_2)
        self.otrosdatos.setObjectName(u"otrosdatos")
        self.otrosdatos.setProperty(u"uiRole", u"fieldLabel")
        self.otrosdatos.setAlignment(Qt.AlignLeft|Qt.AlignVCenter)
        self.otrosdatos.setWordWrap(False)
        sizePolicy.setHeightForWidth(self.otrosdatos.sizePolicy().hasHeightForWidth())
        self.otrosdatos.setSizePolicy(sizePolicy)

        self.layoutEstructura12.addWidget(self.otrosdatos)

        self.uid = QLabel(self.frameHeader_2)
        self.uid.setObjectName(u"uid")
        self.uid.setAlignment(Qt.AlignLeft|Qt.AlignVCenter)
        self.uid.setWordWrap(False)
        sizePolicy.setHeightForWidth(self.uid.sizePolicy().hasHeightForWidth())
        self.uid.setSizePolicy(sizePolicy)
        self.uid.setProperty(u"uiRole", u"fieldLabel")

        self.layoutEstructura12.addWidget(self.uid)

        self.texto4 = QLabel(self.frameHeader_2)
        self.texto4.setObjectName(u"texto4")
        self.texto4.setProperty(u"uiRole", u"value")
        self.texto4.setAlignment(Qt.AlignLeft|Qt.AlignVCenter)
        self.texto4.setWordWrap(False)
        sizePolicy.setHeightForWidth(self.texto4.sizePolicy().hasHeightForWidth())
        self.texto4.setSizePolicy(sizePolicy)

        self.layoutEstructura12.addWidget(self.texto4)

        self.nombre = QLabel(self.frameHeader_2)
        self.nombre.setObjectName(u"nombre")
        self.nombre.setAlignment(Qt.AlignLeft|Qt.AlignVCenter)
        self.nombre.setWordWrap(False)
        sizePolicy.setHeightForWidth(self.nombre.sizePolicy().hasHeightForWidth())
        self.nombre.setSizePolicy(sizePolicy)
        self.nombre.setProperty(u"uiRole", u"fieldLabel")

        self.layoutEstructura12.addWidget(self.nombre)

        self.texto5 = QLabel(self.frameHeader_2)
        self.texto5.setObjectName(u"texto5")
        self.texto5.setProperty(u"uiRole", u"value")
        self.texto5.setAlignment(Qt.AlignLeft|Qt.AlignVCenter)
        self.texto5.setWordWrap(False)
        sizePolicy.setHeightForWidth(self.texto5.sizePolicy().hasHeightForWidth())
        self.texto5.setSizePolicy(sizePolicy)

        self.layoutEstructura12.addWidget(self.texto5)

        self.tarjeta = QLabel(self.frameHeader_2)
        self.tarjeta.setObjectName(u"tarjeta")
        self.tarjeta.setAlignment(Qt.AlignLeft|Qt.AlignVCenter)
        self.tarjeta.setWordWrap(False)
        sizePolicy.setHeightForWidth(self.tarjeta.sizePolicy().hasHeightForWidth())
        self.tarjeta.setSizePolicy(sizePolicy)
        self.tarjeta.setProperty(u"uiRole", u"fieldLabel")

        self.layoutEstructura12.addWidget(self.tarjeta)

        self.texto6 = QLabel(self.frameHeader_2)
        self.texto6.setObjectName(u"texto6")
        self.texto6.setProperty(u"uiRole", u"value")
        self.texto6.setAlignment(Qt.AlignLeft|Qt.AlignVCenter)
        self.texto6.setWordWrap(False)
        sizePolicy.setHeightForWidth(self.texto6.sizePolicy().hasHeightForWidth())
        self.texto6.setSizePolicy(sizePolicy)

        self.layoutEstructura12.addWidget(self.texto6)

        self.espacioEstructura13 = QSpacerItem(8, 8, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.layoutEstructura12.addItem(self.espacioEstructura13)


        self.layoutEstructura11.addWidget(self.frameHeader_2)

        self.frameHeader_3 = QFrame(self.frameHeader_4)
        self.frameHeader_3.setObjectName(u"frameHeader_3")
        self.frameHeader_3.setFrameShape(QFrame.StyledPanel)
        self.frameHeader_3.setFrameShadow(QFrame.Raised)
        self.frameHeader_3.setProperty(u"uiRole", u"card")
        self.layoutEstructura14 = QVBoxLayout(self.frameHeader_3)
        self.layoutEstructura14.setSpacing(8)
        self.layoutEstructura14.setObjectName(u"layoutEstructura14")
        self.layoutEstructura14.setContentsMargins(12, 12, 12, 12)
        self.menu_5 = QLabel(self.frameHeader_3)
        self.menu_5.setObjectName(u"menu_5")
        self.menu_5.setAlignment(Qt.AlignLeft|Qt.AlignVCenter)
        self.menu_5.setWordWrap(False)
        sizePolicy.setHeightForWidth(self.menu_5.sizePolicy().hasHeightForWidth())
        self.menu_5.setSizePolicy(sizePolicy)
        self.menu_5.setProperty(u"uiRole", u"section")

        self.layoutEstructura14.addWidget(self.menu_5)

        self.frame_3 = QFrame(self.frameHeader_3)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setFrameShape(QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.frame_3.setProperty(u"uiRole", u"softPanel")
        self.layoutEstructura15 = QVBoxLayout(self.frame_3)
        self.layoutEstructura15.setSpacing(8)
        self.layoutEstructura15.setObjectName(u"layoutEstructura15")
        self.layoutEstructura15.setContentsMargins(12, 12, 12, 12)
        self.saldo = QLabel(self.frame_3)
        self.saldo.setObjectName(u"saldo")
        self.saldo.setProperty(u"uiRole", u"fieldLabel")
        self.saldo.setAlignment(Qt.AlignLeft|Qt.AlignVCenter)
        self.saldo.setWordWrap(False)
        sizePolicy.setHeightForWidth(self.saldo.sizePolicy().hasHeightForWidth())
        self.saldo.setSizePolicy(sizePolicy)

        self.layoutEstructura15.addWidget(self.saldo)

        self.texto1 = QLabel(self.frame_3)
        self.texto1.setObjectName(u"texto1")
        self.texto1.setProperty(u"uiRole", u"balance")
        self.texto1.setAlignment(Qt.AlignLeft|Qt.AlignVCenter)
        self.texto1.setWordWrap(False)
        sizePolicy.setHeightForWidth(self.texto1.sizePolicy().hasHeightForWidth())
        self.texto1.setSizePolicy(sizePolicy)

        self.layoutEstructura15.addWidget(self.texto1)


        self.layoutEstructura14.addWidget(self.frame_3)

        self.plainTextEdit = QPlainTextEdit(self.frameHeader_3)
        self.plainTextEdit.setObjectName(u"plainTextEdit")
        self.plainTextEdit.setReadOnly(True)
        self.plainTextEdit.setProperty(u"uiRole", u"caption")
        self.plainTextEdit.setMaximumSize(QSize(16777215, 24))

        self.layoutEstructura14.addWidget(self.plainTextEdit)

        self.layoutMontoConMoneda = QHBoxLayout()
        self.layoutMontoConMoneda.setSpacing(8)
        self.layoutMontoConMoneda.setObjectName(u"layoutMontoConMoneda")
        self.layoutMontoConMoneda.setContentsMargins(0, 0, 0, 0)
        self.signoMonedaMonto = QLabel(self.frameHeader_3)
        self.signoMonedaMonto.setObjectName(u"signoMonedaMonto")
        self.signoMonedaMonto.setProperty(u"uiRole", u"currency")

        self.layoutMontoConMoneda.addWidget(self.signoMonedaMonto)

        self.lineEdit = QLineEdit(self.frameHeader_3)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setInputMethodHints(Qt.ImhNone)
        self.lineEdit.setDragEnabled(False)
        self.lineEdit.setMinimumSize(QSize(0, 36))
        self.lineEdit.setMaximumSize(QSize(16777215, 40))

        self.layoutMontoConMoneda.addWidget(self.lineEdit)


        self.layoutEstructura14.addLayout(self.layoutMontoConMoneda)

        self.frame_4 = QFrame(self.frameHeader_3)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setFrameShape(QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QFrame.Raised)
        self.frame_4.setProperty(u"uiRole", u"softPanel")
        self.layoutEstructura16 = QVBoxLayout(self.frame_4)
        self.layoutEstructura16.setSpacing(8)
        self.layoutEstructura16.setObjectName(u"layoutEstructura16")
        self.layoutEstructura16.setContentsMargins(12, 12, 12, 12)
        self.saldonuevo = QLabel(self.frame_4)
        self.saldonuevo.setObjectName(u"saldonuevo")
        self.saldonuevo.setProperty(u"uiRole", u"fieldLabel")
        self.saldonuevo.setAlignment(Qt.AlignLeft|Qt.AlignVCenter)
        self.saldonuevo.setWordWrap(False)
        sizePolicy.setHeightForWidth(self.saldonuevo.sizePolicy().hasHeightForWidth())
        self.saldonuevo.setSizePolicy(sizePolicy)

        self.layoutEstructura16.addWidget(self.saldonuevo)

        self.texto2 = QLabel(self.frame_4)
        self.texto2.setObjectName(u"texto2")
        self.texto2.setProperty(u"uiRole", u"balance")
        self.texto2.setAlignment(Qt.AlignLeft|Qt.AlignVCenter)
        self.texto2.setWordWrap(False)
        sizePolicy.setHeightForWidth(self.texto2.sizePolicy().hasHeightForWidth())
        self.texto2.setSizePolicy(sizePolicy)

        self.layoutEstructura16.addWidget(self.texto2)


        self.layoutEstructura14.addWidget(self.frame_4)

        self.espacioEstructura17 = QSpacerItem(8, 8, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.layoutEstructura14.addItem(self.espacioEstructura17)


        self.layoutEstructura11.addWidget(self.frameHeader_3)

        self.layoutEstructura11.setStretch(0, 1)
        self.layoutEstructura11.setStretch(1, 1)

        self.layoutEstructura8.addLayout(self.layoutEstructura11)

        self.frame_5 = QFrame(self.frameHeader_4)
        self.frame_5.setObjectName(u"frame_5")
        self.frame_5.setFrameShape(QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QFrame.Raised)
        self.layoutEstructura18 = QVBoxLayout(self.frame_5)
        self.layoutEstructura18.setSpacing(8)
        self.layoutEstructura18.setObjectName(u"layoutEstructura18")
        self.layoutEstructura18.setContentsMargins(0, 0, 0, 0)
        self.texto7 = QLabel(self.frame_5)
        self.texto7.setObjectName(u"texto7")
        self.texto7.setProperty(u"uiRole", u"value")
        self.texto7.setAlignment(Qt.AlignLeft|Qt.AlignVCenter)
        sizePolicy.setHeightForWidth(self.texto7.sizePolicy().hasHeightForWidth())
        self.texto7.setSizePolicy(sizePolicy)
        self.texto7.setWordWrap(True)

        self.layoutEstructura18.addWidget(self.texto7)


        self.layoutEstructura8.addWidget(self.frame_5)

        self.layoutEstructura19 = QHBoxLayout()
        self.layoutEstructura19.setSpacing(8)
        self.layoutEstructura19.setObjectName(u"layoutEstructura19")
        self.layoutEstructura19.setContentsMargins(0, 0, 0, 0)
        self.espacioEstructura20 = QSpacerItem(8, 8, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.layoutEstructura19.addItem(self.espacioEstructura20)

        self.botonrecargar = QPushButton(self.frameHeader_4)
        self.botonrecargar.setObjectName(u"botonrecargar")
        sizePolicy.setHeightForWidth(self.botonrecargar.sizePolicy().hasHeightForWidth())
        self.botonrecargar.setSizePolicy(sizePolicy)
        self.botonrecargar.setProperty(u"uiRole", u"primary")
        self.botonrecargar.setMinimumSize(QSize(140, 38))
        self.botonrecargar.setMaximumSize(QSize(240, 40))

        self.layoutEstructura19.addWidget(self.botonrecargar)


        self.layoutEstructura8.addLayout(self.layoutEstructura19)

        self.areaContenido.setWidget(self.frameHeader_4)

        self.layoutPrincipalRecarga.addWidget(self.areaContenido)

        self.pieAplicacion = QLabel(self.centralwidget)
        self.pieAplicacion.setObjectName(u"pieAplicacion")
        sizePolicy.setHeightForWidth(self.pieAplicacion.sizePolicy().hasHeightForWidth())
        self.pieAplicacion.setSizePolicy(sizePolicy)
        self.pieAplicacion.setProperty(u"uiRole", u"caption")
        self.pieAplicacion.setAlignment(Qt.AlignCenter)

        self.layoutPrincipalRecarga.addWidget(self.pieAplicacion)

        self.layoutPrincipalRecarga.setStretch(2, 1)
        RecargaWindow.setCentralWidget(self.centralwidget)
        QWidget.setTabOrder(self.botonregresar, self.comboBox)
        QWidget.setTabOrder(self.comboBox, self.usuario_2)
        QWidget.setTabOrder(self.usuario_2, self.listaoficina)
        QWidget.setTabOrder(self.listaoficina, self.lineEdit)
        QWidget.setTabOrder(self.lineEdit, self.botonrecargar)

        self.retranslateUi(RecargaWindow)

        QMetaObject.connectSlotsByName(RecargaWindow)
    # setupUi

    def retranslateUi(self, RecargaWindow):
        RecargaWindow.setWindowTitle(QCoreApplication.translate("RecargaWindow", u"Recarga", None))
        self.labelBrand_2.setText(QCoreApplication.translate("RecargaWindow", u"RUMSA", None))
        self.labelHeaderInfo_3.setText(QCoreApplication.translate("RecargaWindow", u"Rutas Urbanas de Matehuala S.A. de C.V.", None))
        self.usuario_2.setText(QCoreApplication.translate("RecargaWindow", u"Usuario", None))
#if QT_CONFIG(tooltip)
        self.labelEstadoConexion_2.setToolTip(QCoreApplication.translate("RecargaWindow", u"Este texto puede cambiar a: Conectando, Sin conexi\u00f3n, Sincronizando o Conectado.", None))
#endif // QT_CONFIG(tooltip)
        self.labelEstadoConexion_2.setText(QCoreApplication.translate("RecargaWindow", u"\u25cf Conectando", None))
        self.mensajeInternet.setText("")
        self.mensajeInternet.setProperty(u"estadoVisual", QCoreApplication.translate("RecargaWindow", u"error", None))
        self.botonregresar.setText(QCoreApplication.translate("RecargaWindow", u"<  Volver", None))
        self.etiquetaPuerto.setText(QCoreApplication.translate("RecargaWindow", u"Puerto del lector", None))
        self.menu_6.setText(QCoreApplication.translate("RecargaWindow", u"Recargas", None))
        self.label_2.setText(QCoreApplication.translate("RecargaWindow", u"Oficina", None))
        self.menu_3.setText(QCoreApplication.translate("RecargaWindow", u"Datos de la Tarjeta", None))
        self.otrosdatos.setText(QCoreApplication.translate("RecargaWindow", u"Otros Datos", None))
        self.uid.setText(QCoreApplication.translate("RecargaWindow", u"UID", None))
        self.texto4.setText(QCoreApplication.translate("RecargaWindow", u"Texto", None))
        self.nombre.setText(QCoreApplication.translate("RecargaWindow", u"Nombre", None))
        self.texto5.setText(QCoreApplication.translate("RecargaWindow", u"Texto", None))
        self.tarjeta.setText(QCoreApplication.translate("RecargaWindow", u"Tipo de Tarjeta", None))
        self.texto6.setText(QCoreApplication.translate("RecargaWindow", u"Texto", None))
        self.menu_5.setText(QCoreApplication.translate("RecargaWindow", u"Recarga", None))
        self.saldo.setText(QCoreApplication.translate("RecargaWindow", u"Saldo", None))
        self.texto1.setText(QCoreApplication.translate("RecargaWindow", u"$0.00", None))
        self.plainTextEdit.setPlainText(QCoreApplication.translate("RecargaWindow", u"Monto de recarga", None))
        self.signoMonedaMonto.setText(QCoreApplication.translate("RecargaWindow", u"$", None))
        self.lineEdit.setInputMask("")
        self.lineEdit.setText(QCoreApplication.translate("RecargaWindow", u"0.00", None))
        self.saldonuevo.setText(QCoreApplication.translate("RecargaWindow", u"Saldo Nuevo", None))
        self.texto2.setText(QCoreApplication.translate("RecargaWindow", u"$0.00", None))
        self.texto7.setText("")
        self.botonrecargar.setText(QCoreApplication.translate("RecargaWindow", u"Recargar", None))
        self.pieAplicacion.setText(QCoreApplication.translate("RecargaWindow", u"RUMSA - Rutas Urbanas de Matehuala", None))
    # retranslateUi

