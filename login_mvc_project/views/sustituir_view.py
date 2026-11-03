# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'sustituir.ui'
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
from PySide6.QtWidgets import (QApplication, QCalendarWidget, QComboBox, QFrame,
    QHBoxLayout, QLabel, QLineEdit, QMainWindow,
    QPushButton, QScrollArea, QSizePolicy, QSpacerItem,
    QTextBrowser, QToolButton, QVBoxLayout, QWidget)

class SustituirWindow(object):
    def setupUi(self, SustituirWindow):
        if not SustituirWindow.objectName():
            SustituirWindow.setObjectName(u"SustituirWindow")
        SustituirWindow.resize(860, 850)
        SustituirWindow.setMinimumSize(QSize(760, 680))
        self.centralwidget = QWidget(SustituirWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout_4 = QVBoxLayout(self.centralwidget)
        self.gridLayout_4.setSpacing(12)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setContentsMargins(16, 16, 16, 16)
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
        self.frame_3 = QFrame(self.frame_2)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setFrameShape(QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.frame_3.setProperty(u"uiRole", u"stripe")
        self.frame_3.setMinimumSize(QSize(5, 32))
        self.frame_3.setMaximumSize(QSize(5, 32))

        self.layoutEstructura2.addWidget(self.frame_3, 0, Qt.AlignVCenter)

        self.layoutWidget = QWidget(self.frame_2)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutEstructura4 = QVBoxLayout(self.layoutWidget)
        self.layoutEstructura4.setSpacing(2)
        self.layoutEstructura4.setObjectName(u"layoutEstructura4")
        self.layoutEstructura4.setContentsMargins(0, 0, 0, 0)
        self.labelBrand_2 = QLabel(self.layoutWidget)
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

        self.labelHeaderInfo_4 = QLabel(self.layoutWidget)
        self.labelHeaderInfo_4.setObjectName(u"labelHeaderInfo_4")
        self.labelHeaderInfo_4.setAlignment(Qt.AlignLeft|Qt.AlignVCenter)
        sizePolicy.setHeightForWidth(self.labelHeaderInfo_4.sizePolicy().hasHeightForWidth())
        self.labelHeaderInfo_4.setSizePolicy(sizePolicy)
        self.labelHeaderInfo_4.setProperty(u"uiRole", u"caption")
        self.labelHeaderInfo_4.setWordWrap(False)

        self.layoutEstructura4.addWidget(self.labelHeaderInfo_4)


        self.layoutEstructura2.addWidget(self.layoutWidget)

        self.espacioEstructura3 = QSpacerItem(8, 8, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.layoutEstructura2.addItem(self.espacioEstructura3)

        self.layoutWidget_2 = QWidget(self.frame_2)
        self.layoutWidget_2.setObjectName(u"layoutWidget_2")
        self.layoutEstructura5 = QVBoxLayout(self.layoutWidget_2)
        self.layoutEstructura5.setSpacing(4)
        self.layoutEstructura5.setObjectName(u"layoutEstructura5")
        self.layoutEstructura5.setContentsMargins(0, 0, 0, 0)
        self.usuario_2 = QToolButton(self.layoutWidget_2)
        self.usuario_2.setObjectName(u"usuario_2")
        self.usuario_2.setMinimumSize(QSize(0, 36))
        self.usuario_2.setMaximumSize(QSize(16777215, 40))
        sizePolicy.setHeightForWidth(self.usuario_2.sizePolicy().hasHeightForWidth())
        self.usuario_2.setSizePolicy(sizePolicy)

        self.layoutEstructura5.addWidget(self.usuario_2, 0, Qt.AlignRight)

        self.labelEstadoConexion_2 = QLabel(self.layoutWidget_2)
        self.labelEstadoConexion_2.setObjectName(u"labelEstadoConexion_2")
        self.labelEstadoConexion_2.setProperty(u"uiRole", u"status")
        self.labelEstadoConexion_2.setAlignment(Qt.AlignLeft|Qt.AlignVCenter)
        self.labelEstadoConexion_2.setWordWrap(False)
        sizePolicy.setHeightForWidth(self.labelEstadoConexion_2.sizePolicy().hasHeightForWidth())
        self.labelEstadoConexion_2.setSizePolicy(sizePolicy)

        self.layoutEstructura5.addWidget(self.labelEstadoConexion_2, 0, Qt.AlignRight)


        self.layoutEstructura2.addWidget(self.layoutWidget_2)


        self.gridLayout_4.addWidget(self.frame_2)

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


        self.gridLayout_4.addLayout(self.layoutEstructura6)

        self.areaContenido = QScrollArea(self.centralwidget)
        self.areaContenido.setObjectName(u"areaContenido")
        self.areaContenido.setWidgetResizable(True)
        self.areaContenido.setFrameShape(QFrame.NoFrame)
        self.frame = QFrame()
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.frame.setProperty(u"uiRole", u"card")
        self.layoutEstructura8 = QVBoxLayout(self.frame)
        self.layoutEstructura8.setSpacing(12)
        self.layoutEstructura8.setObjectName(u"layoutEstructura8")
        self.layoutEstructura8.setContentsMargins(16, 16, 16, 16)
        self.sustituirtarjeta = QLabel(self.frame)
        self.sustituirtarjeta.setObjectName(u"sustituirtarjeta")
        self.sustituirtarjeta.setAlignment(Qt.AlignLeft|Qt.AlignVCenter)
        self.sustituirtarjeta.setWordWrap(False)
        sizePolicy.setHeightForWidth(self.sustituirtarjeta.sizePolicy().hasHeightForWidth())
        self.sustituirtarjeta.setSizePolicy(sizePolicy)
        self.sustituirtarjeta.setProperty(u"uiRole", u"heading")

        self.layoutEstructura8.addWidget(self.sustituirtarjeta)

        self.labelHeaderInfo_3 = QLabel(self.frame)
        self.labelHeaderInfo_3.setObjectName(u"labelHeaderInfo_3")
        self.labelHeaderInfo_3.setAlignment(Qt.AlignLeft|Qt.AlignVCenter)
        self.labelHeaderInfo_3.setWordWrap(False)
        sizePolicy.setHeightForWidth(self.labelHeaderInfo_3.sizePolicy().hasHeightForWidth())
        self.labelHeaderInfo_3.setSizePolicy(sizePolicy)
        self.labelHeaderInfo_3.setProperty(u"uiRole", u"caption")

        self.layoutEstructura8.addWidget(self.labelHeaderInfo_3)

        self.layoutEstructura9 = QHBoxLayout()
        self.layoutEstructura9.setSpacing(8)
        self.layoutEstructura9.setObjectName(u"layoutEstructura9")
        self.layoutEstructura9.setContentsMargins(0, 0, 0, 0)
        self.buscador = QLineEdit(self.frame)
        self.buscador.setObjectName(u"buscador")
        self.buscador.setMinimumSize(QSize(0, 36))
        self.buscador.setMaximumSize(QSize(16777215, 40))

        self.layoutEstructura9.addWidget(self.buscador)

        self.pushButton = QPushButton(self.frame)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setMinimumSize(QSize(100, 36))
        self.pushButton.setMaximumSize(QSize(16777215, 40))
        sizePolicy.setHeightForWidth(self.pushButton.sizePolicy().hasHeightForWidth())
        self.pushButton.setSizePolicy(sizePolicy)
        self.pushButton.setProperty(u"uiRole", u"primary")

        self.layoutEstructura9.addWidget(self.pushButton)


        self.layoutEstructura8.addLayout(self.layoutEstructura9)

        self.layoutEstructura10 = QHBoxLayout()
        self.layoutEstructura10.setSpacing(16)
        self.layoutEstructura10.setObjectName(u"layoutEstructura10")
        self.layoutEstructura10.setContentsMargins(0, 0, 0, 0)
        self.frame_5 = QFrame(self.frame)
        self.frame_5.setObjectName(u"frame_5")
        self.frame_5.setFrameShape(QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QFrame.Raised)
        self.frame_5.setProperty(u"uiRole", u"card")
        self.layoutEstructura11 = QVBoxLayout(self.frame_5)
        self.layoutEstructura11.setSpacing(8)
        self.layoutEstructura11.setObjectName(u"layoutEstructura11")
        self.layoutEstructura11.setContentsMargins(12, 12, 12, 12)
        self.menu_6 = QLabel(self.frame_5)
        self.menu_6.setObjectName(u"menu_6")
        self.menu_6.setAlignment(Qt.AlignLeft|Qt.AlignVCenter)
        self.menu_6.setWordWrap(False)
        sizePolicy.setHeightForWidth(self.menu_6.sizePolicy().hasHeightForWidth())
        self.menu_6.setSizePolicy(sizePolicy)
        self.menu_6.setProperty(u"uiRole", u"section")

        self.layoutEstructura11.addWidget(self.menu_6)

        self.nombre_2 = QLabel(self.frame_5)
        self.nombre_2.setObjectName(u"nombre_2")
        self.nombre_2.setAlignment(Qt.AlignLeft|Qt.AlignVCenter)
        self.nombre_2.setWordWrap(False)
        sizePolicy.setHeightForWidth(self.nombre_2.sizePolicy().hasHeightForWidth())
        self.nombre_2.setSizePolicy(sizePolicy)
        self.nombre_2.setProperty(u"uiRole", u"fieldLabel")

        self.layoutEstructura11.addWidget(self.nombre_2)

        self.textonombre = QTextBrowser(self.frame_5)
        self.textonombre.setObjectName(u"textonombre")
        self.textonombre.setMinimumSize(QSize(0, 36))
        self.textonombre.setMaximumSize(QSize(16777215, 40))

        self.layoutEstructura11.addWidget(self.textonombre)

        self.curp = QLabel(self.frame_5)
        self.curp.setObjectName(u"curp")
        self.curp.setAlignment(Qt.AlignLeft|Qt.AlignVCenter)
        self.curp.setWordWrap(False)
        sizePolicy.setHeightForWidth(self.curp.sizePolicy().hasHeightForWidth())
        self.curp.setSizePolicy(sizePolicy)
        self.curp.setProperty(u"uiRole", u"fieldLabel")

        self.layoutEstructura11.addWidget(self.curp)

        self.textocurp = QLabel(self.frame_5)
        self.textocurp.setObjectName(u"textocurp")
        self.textocurp.setProperty(u"uiRole", u"value")
        self.textocurp.setAlignment(Qt.AlignLeft|Qt.AlignVCenter)
        self.textocurp.setWordWrap(False)
        sizePolicy.setHeightForWidth(self.textocurp.sizePolicy().hasHeightForWidth())
        self.textocurp.setSizePolicy(sizePolicy)

        self.layoutEstructura11.addWidget(self.textocurp)

        self.fechanacimiento = QLabel(self.frame_5)
        self.fechanacimiento.setObjectName(u"fechanacimiento")
        self.fechanacimiento.setAlignment(Qt.AlignLeft|Qt.AlignVCenter)
        self.fechanacimiento.setWordWrap(False)
        sizePolicy.setHeightForWidth(self.fechanacimiento.sizePolicy().hasHeightForWidth())
        self.fechanacimiento.setSizePolicy(sizePolicy)
        self.fechanacimiento.setProperty(u"uiRole", u"fieldLabel")

        self.layoutEstructura11.addWidget(self.fechanacimiento)

        self.textofecha = QLabel(self.frame_5)
        self.textofecha.setObjectName(u"textofecha")
        self.textofecha.setProperty(u"uiRole", u"value")
        self.textofecha.setAlignment(Qt.AlignLeft|Qt.AlignVCenter)
        self.textofecha.setWordWrap(False)
        sizePolicy.setHeightForWidth(self.textofecha.sizePolicy().hasHeightForWidth())
        self.textofecha.setSizePolicy(sizePolicy)

        self.layoutEstructura11.addWidget(self.textofecha)

        self.uid = QLabel(self.frame_5)
        self.uid.setObjectName(u"uid")
        self.uid.setAlignment(Qt.AlignLeft|Qt.AlignVCenter)
        self.uid.setWordWrap(False)
        sizePolicy.setHeightForWidth(self.uid.sizePolicy().hasHeightForWidth())
        self.uid.setSizePolicy(sizePolicy)
        self.uid.setProperty(u"uiRole", u"fieldLabel")

        self.layoutEstructura11.addWidget(self.uid)

        self.textouid = QLabel(self.frame_5)
        self.textouid.setObjectName(u"textouid")
        self.textouid.setProperty(u"uiRole", u"value")
        self.textouid.setAlignment(Qt.AlignLeft|Qt.AlignVCenter)
        self.textouid.setWordWrap(False)
        sizePolicy.setHeightForWidth(self.textouid.sizePolicy().hasHeightForWidth())
        self.textouid.setSizePolicy(sizePolicy)

        self.layoutEstructura11.addWidget(self.textouid)

        self.tipotarjeta = QLabel(self.frame_5)
        self.tipotarjeta.setObjectName(u"tipotarjeta")
        self.tipotarjeta.setAlignment(Qt.AlignLeft|Qt.AlignVCenter)
        self.tipotarjeta.setWordWrap(False)
        sizePolicy.setHeightForWidth(self.tipotarjeta.sizePolicy().hasHeightForWidth())
        self.tipotarjeta.setSizePolicy(sizePolicy)
        self.tipotarjeta.setProperty(u"uiRole", u"fieldLabel")

        self.layoutEstructura11.addWidget(self.tipotarjeta)

        self.textotipo = QLabel(self.frame_5)
        self.textotipo.setObjectName(u"textotipo")
        self.textotipo.setProperty(u"uiRole", u"value")
        self.textotipo.setAlignment(Qt.AlignLeft|Qt.AlignVCenter)
        self.textotipo.setWordWrap(False)
        sizePolicy.setHeightForWidth(self.textotipo.sizePolicy().hasHeightForWidth())
        self.textotipo.setSizePolicy(sizePolicy)

        self.layoutEstructura11.addWidget(self.textotipo)

        self.espacioEstructura12 = QSpacerItem(8, 8, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.layoutEstructura11.addItem(self.espacioEstructura12)


        self.layoutEstructura10.addWidget(self.frame_5)

        self.frame_4 = QFrame(self.frame)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setFrameShape(QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QFrame.Raised)
        self.frame_4.setProperty(u"uiRole", u"card")
        self.layoutEstructura13 = QVBoxLayout(self.frame_4)
        self.layoutEstructura13.setSpacing(8)
        self.layoutEstructura13.setObjectName(u"layoutEstructura13")
        self.layoutEstructura13.setContentsMargins(12, 12, 12, 12)
        self.menu_5 = QLabel(self.frame_4)
        self.menu_5.setObjectName(u"menu_5")
        self.menu_5.setAlignment(Qt.AlignLeft|Qt.AlignVCenter)
        self.menu_5.setWordWrap(False)
        sizePolicy.setHeightForWidth(self.menu_5.sizePolicy().hasHeightForWidth())
        self.menu_5.setSizePolicy(sizePolicy)
        self.menu_5.setProperty(u"uiRole", u"section")

        self.layoutEstructura13.addWidget(self.menu_5)

        self.labelUidNuevo = QLabel(self.frame_4)
        self.labelUidNuevo.setObjectName(u"labelUidNuevo")
        self.labelUidNuevo.setAlignment(Qt.AlignLeft|Qt.AlignVCenter)
        self.labelUidNuevo.setWordWrap(False)
        sizePolicy.setHeightForWidth(self.labelUidNuevo.sizePolicy().hasHeightForWidth())
        self.labelUidNuevo.setSizePolicy(sizePolicy)
        self.labelUidNuevo.setProperty(u"uiRole", u"fieldLabel")

        self.layoutEstructura13.addWidget(self.labelUidNuevo)

        self.textouidnuevo = QLineEdit(self.frame_4)
        self.textouidnuevo.setObjectName(u"textouidnuevo")
        self.textouidnuevo.setReadOnly(True)
        self.textouidnuevo.setMinimumSize(QSize(0, 36))
        self.textouidnuevo.setMaximumSize(QSize(16777215, 40))

        self.layoutEstructura13.addWidget(self.textouidnuevo)

        self.vigencia = QLabel(self.frame_4)
        self.vigencia.setObjectName(u"vigencia")
        self.vigencia.setAlignment(Qt.AlignLeft|Qt.AlignVCenter)
        self.vigencia.setWordWrap(False)
        sizePolicy.setHeightForWidth(self.vigencia.sizePolicy().hasHeightForWidth())
        self.vigencia.setSizePolicy(sizePolicy)
        self.vigencia.setProperty(u"uiRole", u"fieldLabel")

        self.layoutEstructura13.addWidget(self.vigencia)

        self.textovigencia = QTextBrowser(self.frame_4)
        self.textovigencia.setObjectName(u"textovigencia")
        self.textovigencia.setMinimumSize(QSize(0, 36))
        self.textovigencia.setMaximumSize(QSize(16777215, 40))

        self.layoutEstructura13.addWidget(self.textovigencia)

        self.calendario = QCalendarWidget(self.frame_4)
        self.calendario.setObjectName(u"calendario")
        self.calendario.setHorizontalHeaderFormat(QCalendarWidget.ShortDayNames)
        self.calendario.setVerticalHeaderFormat(QCalendarWidget.NoVerticalHeader)
        self.calendario.setMinimumSize(QSize(0, 210))

        self.layoutEstructura13.addWidget(self.calendario)

        self.espacioEstructura14 = QSpacerItem(8, 8, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.layoutEstructura13.addItem(self.espacioEstructura14)


        self.layoutEstructura10.addWidget(self.frame_4)

        self.layoutEstructura10.setStretch(0, 1)
        self.layoutEstructura10.setStretch(1, 1)

        self.layoutEstructura8.addLayout(self.layoutEstructura10)

        self.layoutEstructura15 = QHBoxLayout()
        self.layoutEstructura15.setSpacing(8)
        self.layoutEstructura15.setObjectName(u"layoutEstructura15")
        self.layoutEstructura15.setContentsMargins(0, 0, 0, 0)
        self.espacioEstructura16 = QSpacerItem(8, 8, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.layoutEstructura15.addItem(self.espacioEstructura16)

        self.botonguardar_2 = QPushButton(self.frame)
        self.botonguardar_2.setObjectName(u"botonguardar_2")
        sizePolicy.setHeightForWidth(self.botonguardar_2.sizePolicy().hasHeightForWidth())
        self.botonguardar_2.setSizePolicy(sizePolicy)
        self.botonguardar_2.setProperty(u"uiRole", u"secondary")
        self.botonguardar_2.setMinimumSize(QSize(140, 38))
        self.botonguardar_2.setMaximumSize(QSize(240, 40))

        self.layoutEstructura15.addWidget(self.botonguardar_2)

        self.botonsustituir = QPushButton(self.frame)
        self.botonsustituir.setObjectName(u"botonsustituir")
        sizePolicy.setHeightForWidth(self.botonsustituir.sizePolicy().hasHeightForWidth())
        self.botonsustituir.setSizePolicy(sizePolicy)
        self.botonsustituir.setProperty(u"uiRole", u"primary")
        self.botonsustituir.setMinimumSize(QSize(140, 38))
        self.botonsustituir.setMaximumSize(QSize(240, 40))

        self.layoutEstructura15.addWidget(self.botonsustituir)


        self.layoutEstructura8.addLayout(self.layoutEstructura15)

        self.areaContenido.setWidget(self.frame)

        self.gridLayout_4.addWidget(self.areaContenido)

        self.pieAplicacion = QLabel(self.centralwidget)
        self.pieAplicacion.setObjectName(u"pieAplicacion")
        sizePolicy.setHeightForWidth(self.pieAplicacion.sizePolicy().hasHeightForWidth())
        self.pieAplicacion.setSizePolicy(sizePolicy)
        self.pieAplicacion.setProperty(u"uiRole", u"caption")
        self.pieAplicacion.setAlignment(Qt.AlignCenter)

        self.gridLayout_4.addWidget(self.pieAplicacion)

        self.gridLayout_4.setStretch(2, 1)
        SustituirWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(SustituirWindow)

        QMetaObject.connectSlotsByName(SustituirWindow)
    # setupUi

    def retranslateUi(self, SustituirWindow):
        SustituirWindow.setWindowTitle(QCoreApplication.translate("SustituirWindow", u"Sustituir Tarjeta", None))
        self.labelBrand_2.setText(QCoreApplication.translate("SustituirWindow", u"RUMSA", None))
        self.labelHeaderInfo_4.setText(QCoreApplication.translate("SustituirWindow", u"Rutas Urbanas de Matehuala S.A. de C.V.", None))
        self.usuario_2.setText(QCoreApplication.translate("SustituirWindow", u"Usuario", None))
#if QT_CONFIG(tooltip)
        self.labelEstadoConexion_2.setToolTip(QCoreApplication.translate("SustituirWindow", u"Este texto puede cambiar a: Conectando, Sin conexi\u00f3n, Sincronizando o Conectado.", None))
#endif // QT_CONFIG(tooltip)
        self.labelEstadoConexion_2.setText(QCoreApplication.translate("SustituirWindow", u"\u25cf Conectando", None))
        self.botonregresar.setText(QCoreApplication.translate("SustituirWindow", u"<  Volver", None))
        self.etiquetaPuerto.setText(QCoreApplication.translate("SustituirWindow", u"Puerto del lector", None))
        self.sustituirtarjeta.setText(QCoreApplication.translate("SustituirWindow", u"Sustituir Tarjeta", None))
        self.labelHeaderInfo_3.setText(QCoreApplication.translate("SustituirWindow", u"Busca al pasajero u operador y sustituye la tarjeta", None))
        self.buscador.setText(QCoreApplication.translate("SustituirWindow", u"Buscar...", None))
        self.pushButton.setText(QCoreApplication.translate("SustituirWindow", u"Buscar", None))
        self.menu_6.setText(QCoreApplication.translate("SustituirWindow", u"Datos Personales", None))
        self.nombre_2.setText(QCoreApplication.translate("SustituirWindow", u"Nombre", None))
        self.curp.setText(QCoreApplication.translate("SustituirWindow", u"Curp", None))
        self.textocurp.setText(QCoreApplication.translate("SustituirWindow", u"Curp", None))
        self.fechanacimiento.setText(QCoreApplication.translate("SustituirWindow", u"Fecha de Nacimiento", None))
        self.textofecha.setText(QCoreApplication.translate("SustituirWindow", u"fecha de nacimiento", None))
        self.uid.setText(QCoreApplication.translate("SustituirWindow", u"UID", None))
        self.textouid.setText(QCoreApplication.translate("SustituirWindow", u"uid", None))
        self.tipotarjeta.setText(QCoreApplication.translate("SustituirWindow", u"Tipo de Tarjeta", None))
        self.textotipo.setText(QCoreApplication.translate("SustituirWindow", u"Tipo de tarjeta", None))
        self.menu_5.setText(QCoreApplication.translate("SustituirWindow", u"Datos de la tarjeta nueva", None))
        self.labelUidNuevo.setText(QCoreApplication.translate("SustituirWindow", u"UID nuevo", None))
        self.textouidnuevo.setPlaceholderText(QCoreApplication.translate("SustituirWindow", u"Acerca la tarjeta al lector", None))
        self.vigencia.setText(QCoreApplication.translate("SustituirWindow", u"Vigencia", None))
        self.botonguardar_2.setText(QCoreApplication.translate("SustituirWindow", u"Cancelar", None))
        self.botonsustituir.setText(QCoreApplication.translate("SustituirWindow", u"Sustituir", None))
        self.pieAplicacion.setText(QCoreApplication.translate("SustituirWindow", u"RUMSA - Rutas Urbanas de Matehuala", None))
    # retranslateUi

