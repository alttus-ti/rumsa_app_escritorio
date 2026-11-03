# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dar_de_alta_operador.ui'
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
    QLabel, QMainWindow, QPushButton, QRadioButton,
    QScrollArea, QSizePolicy, QSpacerItem, QStatusBar,
    QTextEdit, QToolButton, QVBoxLayout, QWidget)

class Ui_AltaOWindow(object):
    def setupUi(self, AltaOWindow):
        if not AltaOWindow.objectName():
            AltaOWindow.setObjectName(u"AltaOWindow")
        AltaOWindow.setMinimumSize(QSize(760, 680))
        AltaOWindow.resize(860, 780)
        self.centralwidget = QWidget(AltaOWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout_5 = QVBoxLayout(self.centralwidget)
        self.gridLayout_5.setSpacing(12)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridLayout_5.setContentsMargins(16, 16, 16, 16)
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

        self.verticalLayoutWidget_2 = QWidget(self.frame_2)
        self.verticalLayoutWidget_2.setObjectName(u"verticalLayoutWidget_2")
        self.layoutEstructura4 = QVBoxLayout(self.verticalLayoutWidget_2)
        self.layoutEstructura4.setSpacing(2)
        self.layoutEstructura4.setObjectName(u"layoutEstructura4")
        self.layoutEstructura4.setContentsMargins(0, 0, 0, 0)
        self.labelBrand_2 = QLabel(self.verticalLayoutWidget_2)
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

        self.labelHeaderInfo_3 = QLabel(self.verticalLayoutWidget_2)
        self.labelHeaderInfo_3.setObjectName(u"labelHeaderInfo_3")
        self.labelHeaderInfo_3.setAlignment(Qt.AlignLeft|Qt.AlignVCenter)
        sizePolicy.setHeightForWidth(self.labelHeaderInfo_3.sizePolicy().hasHeightForWidth())
        self.labelHeaderInfo_3.setSizePolicy(sizePolicy)
        self.labelHeaderInfo_3.setProperty(u"uiRole", u"caption")
        self.labelHeaderInfo_3.setWordWrap(False)

        self.layoutEstructura4.addWidget(self.labelHeaderInfo_3)


        self.layoutEstructura2.addWidget(self.verticalLayoutWidget_2)

        self.espacioEstructura3 = QSpacerItem(8, 8, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.layoutEstructura2.addItem(self.espacioEstructura3)

        self.layoutWidget = QWidget(self.frame_2)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutEstructura5 = QVBoxLayout(self.layoutWidget)
        self.layoutEstructura5.setSpacing(4)
        self.layoutEstructura5.setObjectName(u"layoutEstructura5")
        self.layoutEstructura5.setContentsMargins(0, 0, 0, 0)
        self.usuario = QToolButton(self.layoutWidget)
        self.usuario.setObjectName(u"usuario")
        self.usuario.setMinimumSize(QSize(0, 36))
        self.usuario.setMaximumSize(QSize(16777215, 40))
        sizePolicy.setHeightForWidth(self.usuario.sizePolicy().hasHeightForWidth())
        self.usuario.setSizePolicy(sizePolicy)

        self.layoutEstructura5.addWidget(self.usuario, 0, Qt.AlignRight)

        self.labelEstadoConexion_2 = QLabel(self.layoutWidget)
        self.labelEstadoConexion_2.setObjectName(u"labelEstadoConexion_2")
        self.labelEstadoConexion_2.setProperty(u"uiRole", u"status")
        self.labelEstadoConexion_2.setAlignment(Qt.AlignLeft|Qt.AlignVCenter)
        self.labelEstadoConexion_2.setWordWrap(False)
        sizePolicy.setHeightForWidth(self.labelEstadoConexion_2.sizePolicy().hasHeightForWidth())
        self.labelEstadoConexion_2.setSizePolicy(sizePolicy)

        self.layoutEstructura5.addWidget(self.labelEstadoConexion_2, 0, Qt.AlignRight)

        self.mensajeInternet = QLabel(self.layoutWidget)
        self.mensajeInternet.setObjectName(u"mensajeInternet")
        self.mensajeInternet.setProperty(u"uiRole", u"caption")
        self.mensajeInternet.setAlignment(Qt.AlignLeft|Qt.AlignVCenter)
        self.mensajeInternet.setWordWrap(False)
        sizePolicy.setHeightForWidth(self.mensajeInternet.sizePolicy().hasHeightForWidth())
        self.mensajeInternet.setSizePolicy(sizePolicy)

        self.layoutEstructura5.addWidget(self.mensajeInternet, 0, Qt.AlignRight)


        self.layoutEstructura2.addWidget(self.layoutWidget)


        self.gridLayout_5.addWidget(self.frame_2)

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


        self.gridLayout_5.addLayout(self.layoutEstructura6)

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

        self.labelHeaderInfo_2 = QLabel(self.frameHeader_4)
        self.labelHeaderInfo_2.setObjectName(u"labelHeaderInfo_2")
        self.labelHeaderInfo_2.setAlignment(Qt.AlignLeft|Qt.AlignVCenter)
        self.labelHeaderInfo_2.setWordWrap(False)
        sizePolicy.setHeightForWidth(self.labelHeaderInfo_2.sizePolicy().hasHeightForWidth())
        self.labelHeaderInfo_2.setSizePolicy(sizePolicy)
        self.labelHeaderInfo_2.setProperty(u"uiRole", u"caption")

        self.layoutEstructura8.addWidget(self.labelHeaderInfo_2)

        self.layoutEstructura9 = QHBoxLayout()
        self.layoutEstructura9.setSpacing(16)
        self.layoutEstructura9.setObjectName(u"layoutEstructura9")
        self.layoutEstructura9.setContentsMargins(0, 0, 0, 0)
        self.frameHeader_3 = QFrame(self.frameHeader_4)
        self.frameHeader_3.setObjectName(u"frameHeader_3")
        self.frameHeader_3.setFrameShape(QFrame.StyledPanel)
        self.frameHeader_3.setFrameShadow(QFrame.Raised)
        self.frameHeader_3.setProperty(u"uiRole", u"card")
        self.layoutEstructura10 = QVBoxLayout(self.frameHeader_3)
        self.layoutEstructura10.setSpacing(8)
        self.layoutEstructura10.setObjectName(u"layoutEstructura10")
        self.layoutEstructura10.setContentsMargins(12, 12, 12, 12)
        self.menu_5 = QLabel(self.frameHeader_3)
        self.menu_5.setObjectName(u"menu_5")
        self.menu_5.setAlignment(Qt.AlignLeft|Qt.AlignVCenter)
        self.menu_5.setWordWrap(False)
        sizePolicy.setHeightForWidth(self.menu_5.sizePolicy().hasHeightForWidth())
        self.menu_5.setSizePolicy(sizePolicy)
        self.menu_5.setProperty(u"uiRole", u"section")

        self.layoutEstructura10.addWidget(self.menu_5)

        self.nombre = QLabel(self.frameHeader_3)
        self.nombre.setObjectName(u"nombre")
        self.nombre.setAlignment(Qt.AlignLeft|Qt.AlignVCenter)
        self.nombre.setWordWrap(False)
        sizePolicy.setHeightForWidth(self.nombre.sizePolicy().hasHeightForWidth())
        self.nombre.setSizePolicy(sizePolicy)
        self.nombre.setProperty(u"uiRole", u"fieldLabel")

        self.layoutEstructura10.addWidget(self.nombre)

        self.textonombre = QTextEdit(self.frameHeader_3)
        self.textonombre.setObjectName(u"textonombre")
        self.textonombre.setMinimumSize(QSize(0, 36))
        self.textonombre.setMaximumSize(QSize(16777215, 40))

        self.layoutEstructura10.addWidget(self.textonombre)

        self.label_2 = QLabel(self.frameHeader_3)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setAlignment(Qt.AlignLeft|Qt.AlignVCenter)
        self.label_2.setWordWrap(False)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setProperty(u"uiRole", u"fieldLabel")

        self.layoutEstructura10.addWidget(self.label_2)

        self.textocurp = QTextEdit(self.frameHeader_3)
        self.textocurp.setObjectName(u"textocurp")
        self.textocurp.setMinimumSize(QSize(0, 36))
        self.textocurp.setMaximumSize(QSize(16777215, 40))

        self.layoutEstructura10.addWidget(self.textocurp)

        self.label_3 = QLabel(self.frameHeader_3)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setAlignment(Qt.AlignLeft|Qt.AlignVCenter)
        self.label_3.setWordWrap(False)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setProperty(u"uiRole", u"fieldLabel")

        self.layoutEstructura10.addWidget(self.label_3)

        self.textofechanacimiento = QTextEdit(self.frameHeader_3)
        self.textofechanacimiento.setObjectName(u"textofechanacimiento")
        self.textofechanacimiento.setMinimumSize(QSize(0, 36))
        self.textofechanacimiento.setMaximumSize(QSize(16777215, 40))

        self.layoutEstructura10.addWidget(self.textofechanacimiento)

        self.espacioEstructura11 = QSpacerItem(8, 8, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.layoutEstructura10.addItem(self.espacioEstructura11)


        self.layoutEstructura9.addWidget(self.frameHeader_3)

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
        self.otrosdatos.setAlignment(Qt.AlignLeft|Qt.AlignVCenter)
        self.otrosdatos.setWordWrap(False)
        sizePolicy.setHeightForWidth(self.otrosdatos.sizePolicy().hasHeightForWidth())
        self.otrosdatos.setSizePolicy(sizePolicy)
        self.otrosdatos.setProperty(u"uiRole", u"fieldLabel")

        self.layoutEstructura12.addWidget(self.otrosdatos)

        self.frame_3 = QFrame(self.frameHeader_2)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setFrameShape(QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.frame_3.setProperty(u"uiRole", u"notice")
        self.layoutEstructura13 = QVBoxLayout(self.frame_3)
        self.layoutEstructura13.setSpacing(4)
        self.layoutEstructura13.setObjectName(u"layoutEstructura13")
        self.layoutEstructura13.setContentsMargins(8, 8, 8, 8)
        self.normal_2 = QRadioButton(self.frame_3)
        self.normal_2.setObjectName(u"normal_2")

        self.layoutEstructura13.addWidget(self.normal_2)

        self.normal = QRadioButton(self.frame_3)
        self.normal.setObjectName(u"normal")

        self.layoutEstructura13.addWidget(self.normal)


        self.layoutEstructura12.addWidget(self.frame_3)

        self.vigencia = QLabel(self.frameHeader_2)
        self.vigencia.setObjectName(u"vigencia")
        self.vigencia.setAlignment(Qt.AlignLeft|Qt.AlignVCenter)
        self.vigencia.setWordWrap(False)
        sizePolicy.setHeightForWidth(self.vigencia.sizePolicy().hasHeightForWidth())
        self.vigencia.setSizePolicy(sizePolicy)
        self.vigencia.setProperty(u"uiRole", u"fieldLabel")

        self.layoutEstructura12.addWidget(self.vigencia)

        self.textovigencia = QTextEdit(self.frameHeader_2)
        self.textovigencia.setObjectName(u"textovigencia")
        self.textovigencia.setMinimumSize(QSize(0, 36))
        self.textovigencia.setMaximumSize(QSize(16777215, 40))

        self.layoutEstructura12.addWidget(self.textovigencia)

        self.label_4 = QLabel(self.frameHeader_2)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setAlignment(Qt.AlignLeft|Qt.AlignVCenter)
        self.label_4.setWordWrap(False)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        self.label_4.setProperty(u"uiRole", u"fieldLabel")

        self.layoutEstructura12.addWidget(self.label_4)

        self.layoutEstructura14 = QHBoxLayout()
        self.layoutEstructura14.setSpacing(12)
        self.layoutEstructura14.setObjectName(u"layoutEstructura14")
        self.layoutEstructura14.setContentsMargins(0, 0, 0, 0)
        self.fotoimagen = QLabel(self.frameHeader_2)
        self.fotoimagen.setObjectName(u"fotoimagen")
        self.fotoimagen.setProperty(u"uiRole", u"photo")
        self.fotoimagen.setAlignment(Qt.AlignLeft|Qt.AlignVCenter)
        self.fotoimagen.setWordWrap(False)
        sizePolicy.setHeightForWidth(self.fotoimagen.sizePolicy().hasHeightForWidth())
        self.fotoimagen.setSizePolicy(sizePolicy)
        self.fotoimagen.setMinimumSize(QSize(120, 96))
        self.fotoimagen.setMaximumSize(QSize(120, 96))

        self.layoutEstructura14.addWidget(self.fotoimagen)

        self.layoutEstructura15 = QVBoxLayout()
        self.layoutEstructura15.setSpacing(8)
        self.layoutEstructura15.setObjectName(u"layoutEstructura15")
        self.layoutEstructura15.setContentsMargins(0, 0, 0, 0)
        self.botonsubir = QPushButton(self.frameHeader_2)
        self.botonsubir.setObjectName(u"botonsubir")
        self.botonsubir.setProperty(u"uiRole", u"secondary")
        self.botonsubir.setMinimumSize(QSize(100, 36))
        self.botonsubir.setMaximumSize(QSize(16777215, 40))
        sizePolicy.setHeightForWidth(self.botonsubir.sizePolicy().hasHeightForWidth())
        self.botonsubir.setSizePolicy(sizePolicy)

        self.layoutEstructura15.addWidget(self.botonsubir)

        self.label_5 = QLabel(self.frameHeader_2)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setProperty(u"uiRole", u"caption")
        self.label_5.setAlignment(Qt.AlignLeft|Qt.AlignVCenter)
        sizePolicy.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy)
        self.label_5.setWordWrap(True)

        self.layoutEstructura15.addWidget(self.label_5)

        self.label_6 = QLabel(self.frameHeader_2)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setProperty(u"uiRole", u"link")
        self.label_6.setAlignment(Qt.AlignLeft|Qt.AlignVCenter)
        self.label_6.setWordWrap(False)
        sizePolicy.setHeightForWidth(self.label_6.sizePolicy().hasHeightForWidth())
        self.label_6.setSizePolicy(sizePolicy)

        self.layoutEstructura15.addWidget(self.label_6)


        self.layoutEstructura14.addLayout(self.layoutEstructura15)


        self.layoutEstructura12.addLayout(self.layoutEstructura14)

        self.espacioEstructura16 = QSpacerItem(8, 8, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.layoutEstructura12.addItem(self.espacioEstructura16)


        self.layoutEstructura9.addWidget(self.frameHeader_2)

        self.layoutEstructura9.setStretch(0, 1)
        self.layoutEstructura9.setStretch(1, 1)

        self.layoutEstructura8.addLayout(self.layoutEstructura9)

        self.layoutEstructura17 = QHBoxLayout()
        self.layoutEstructura17.setSpacing(8)
        self.layoutEstructura17.setObjectName(u"layoutEstructura17")
        self.layoutEstructura17.setContentsMargins(0, 0, 0, 0)
        self.espacioEstructura18 = QSpacerItem(8, 8, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.layoutEstructura17.addItem(self.espacioEstructura18)

        self.botonguardar_2 = QPushButton(self.frameHeader_4)
        self.botonguardar_2.setObjectName(u"botonguardar_2")
        sizePolicy.setHeightForWidth(self.botonguardar_2.sizePolicy().hasHeightForWidth())
        self.botonguardar_2.setSizePolicy(sizePolicy)
        self.botonguardar_2.setProperty(u"uiRole", u"secondary")
        self.botonguardar_2.setMinimumSize(QSize(140, 38))
        self.botonguardar_2.setMaximumSize(QSize(240, 40))

        self.layoutEstructura17.addWidget(self.botonguardar_2)

        self.botonguardar = QPushButton(self.frameHeader_4)
        self.botonguardar.setObjectName(u"botonguardar")
        sizePolicy.setHeightForWidth(self.botonguardar.sizePolicy().hasHeightForWidth())
        self.botonguardar.setSizePolicy(sizePolicy)
        self.botonguardar.setProperty(u"uiRole", u"primary")
        self.botonguardar.setMinimumSize(QSize(140, 38))
        self.botonguardar.setMaximumSize(QSize(240, 40))

        self.layoutEstructura17.addWidget(self.botonguardar)


        self.layoutEstructura8.addLayout(self.layoutEstructura17)

        self.areaContenido.setWidget(self.frameHeader_4)

        self.gridLayout_5.addWidget(self.areaContenido)

        self.labelHeaderInfo = QLabel(self.centralwidget)
        self.labelHeaderInfo.setObjectName(u"labelHeaderInfo")
        self.labelHeaderInfo.setWordWrap(False)
        sizePolicy.setHeightForWidth(self.labelHeaderInfo.sizePolicy().hasHeightForWidth())
        self.labelHeaderInfo.setSizePolicy(sizePolicy)
        self.labelHeaderInfo.setProperty(u"uiRole", u"caption")
        self.labelHeaderInfo.setAlignment(Qt.AlignCenter)

        self.gridLayout_5.addWidget(self.labelHeaderInfo)

        self.gridLayout_5.setStretch(2, 1)
        AltaOWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(AltaOWindow)
        self.statusbar.setObjectName(u"statusbar")
        AltaOWindow.setStatusBar(self.statusbar)

        self.retranslateUi(AltaOWindow)

        QMetaObject.connectSlotsByName(AltaOWindow)
    # setupUi

    def retranslateUi(self, AltaOWindow):
        AltaOWindow.setWindowTitle(QCoreApplication.translate("AltaOWindow", u"Alta Operador", None))
        self.labelBrand_2.setText(QCoreApplication.translate("AltaOWindow", u"RUMSA", None))
        self.labelHeaderInfo_3.setText(QCoreApplication.translate("AltaOWindow", u"Rutas Urbanas de Matehuala S.A. de C.V.", None))
        self.usuario.setText(QCoreApplication.translate("AltaOWindow", u"Usuario", None))
#if QT_CONFIG(tooltip)
        self.labelEstadoConexion_2.setToolTip(QCoreApplication.translate("AltaOWindow", u"Este texto puede cambiar a: Conectando, Sin conexi\u00f3n, Sincronizando o Conectado.", None))
#endif // QT_CONFIG(tooltip)
        self.labelEstadoConexion_2.setText(QCoreApplication.translate("AltaOWindow", u"\u25cf Conectando", None))
        self.mensajeInternet.setText("")
        self.mensajeInternet.setProperty(u"estadoVisual", QCoreApplication.translate("AltaOWindow", u"error", None))
        self.botonregresar.setText(QCoreApplication.translate("AltaOWindow", u"<  Volver", None))
        self.etiquetaPuerto.setText(QCoreApplication.translate("AltaOWindow", u"Puerto del lector", None))
        self.menu_6.setText(QCoreApplication.translate("AltaOWindow", u"Dar de Alta Personal", None))
        self.labelHeaderInfo_2.setText(QCoreApplication.translate("AltaOWindow", u"Completa datos del Personal", None))
        self.menu_5.setText(QCoreApplication.translate("AltaOWindow", u"Datos Personales", None))
        self.nombre.setText(QCoreApplication.translate("AltaOWindow", u"Nombre", None))
        self.label_2.setText(QCoreApplication.translate("AltaOWindow", u"Curp", None))
        self.label_3.setText(QCoreApplication.translate("AltaOWindow", u"Fecha Nacimineto", None))
        self.textofechanacimiento.setHtml(QCoreApplication.translate("AltaOWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body>\n"
"<p>Selecciona una fecha</p></body></html>", None))
        self.menu_3.setText(QCoreApplication.translate("AltaOWindow", u"Datos de la Tarjeta", None))
        self.otrosdatos.setText(QCoreApplication.translate("AltaOWindow", u"Tipo de Tarjeta", None))
        self.normal_2.setText(QCoreApplication.translate("AltaOWindow", u"Operador", None))
        self.normal.setText(QCoreApplication.translate("AltaOWindow", u"Despachador", None))
        self.vigencia.setText(QCoreApplication.translate("AltaOWindow", u"Vigencia", None))
        self.textovigencia.setHtml(QCoreApplication.translate("AltaOWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body>\n"
"<p>Selecciona fecha</p></body></html>", None))
        self.label_4.setText(QCoreApplication.translate("AltaOWindow", u"Fotograf\u00eda", None))
        self.fotoimagen.setText("")
        self.botonsubir.setText(QCoreApplication.translate("AltaOWindow", u"Seleccionar", None))
        self.label_5.setText(QCoreApplication.translate("AltaOWindow", u"Sin archivo seleccionado", None))
        self.label_6.setText(QCoreApplication.translate("AltaOWindow", u"Quitar foto", None))
        self.botonguardar_2.setText(QCoreApplication.translate("AltaOWindow", u"Cancelar", None))
        self.botonguardar.setText(QCoreApplication.translate("AltaOWindow", u"Guardar", None))
        self.labelHeaderInfo.setText(QCoreApplication.translate("AltaOWindow", u"RUMSA - Rutas Urbanas de Matehuala", None))
    # retranslateUi

