# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dar_de_alta.ui'
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
    QScrollArea, QSizePolicy, QSpacerItem, QTextEdit,
    QToolButton, QVBoxLayout, QWidget)

class AltaWindow(object):
    def setupUi(self, AltaWindow):
        if not AltaWindow.objectName():
            AltaWindow.setObjectName(u"AltaWindow")
        AltaWindow.setMinimumSize(QSize(760, 680))
        AltaWindow.resize(860, 780)
        self.centralwidget = QWidget(AltaWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout_14 = QVBoxLayout(self.centralwidget)
        self.gridLayout_14.setSpacing(12)
        self.gridLayout_14.setObjectName(u"gridLayout_14")
        self.gridLayout_14.setContentsMargins(16, 16, 16, 16)
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

        self.verticalLayoutWidget_2 = QWidget(self.frame)
        self.verticalLayoutWidget_2.setObjectName(u"verticalLayoutWidget_2")
        self.layoutEstructura4 = QVBoxLayout(self.verticalLayoutWidget_2)
        self.layoutEstructura4.setSpacing(2)
        self.layoutEstructura4.setObjectName(u"layoutEstructura4")
        self.layoutEstructura4.setContentsMargins(0, 0, 0, 0)
        self.labelBrand = QLabel(self.verticalLayoutWidget_2)
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

        self.layoutWidget = QWidget(self.frame)
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

        self.mensajeInternet_2 = QLabel(self.layoutWidget)
        self.mensajeInternet_2.setObjectName(u"mensajeInternet_2")
        self.mensajeInternet_2.setProperty(u"uiRole", u"caption")
        self.mensajeInternet_2.setAlignment(Qt.AlignLeft|Qt.AlignVCenter)
        self.mensajeInternet_2.setWordWrap(False)
        sizePolicy.setHeightForWidth(self.mensajeInternet_2.sizePolicy().hasHeightForWidth())
        self.mensajeInternet_2.setSizePolicy(sizePolicy)

        self.layoutEstructura5.addWidget(self.mensajeInternet_2, 0, Qt.AlignRight)


        self.layoutEstructura2.addWidget(self.layoutWidget)


        self.gridLayout_14.addWidget(self.frame)

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


        self.gridLayout_14.addLayout(self.layoutEstructura6)

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
        self.menu_23 = QLabel(self.frameHeader_4)
        self.menu_23.setObjectName(u"menu_23")
        self.menu_23.setAlignment(Qt.AlignLeft|Qt.AlignVCenter)
        self.menu_23.setWordWrap(False)
        sizePolicy.setHeightForWidth(self.menu_23.sizePolicy().hasHeightForWidth())
        self.menu_23.setSizePolicy(sizePolicy)
        self.menu_23.setProperty(u"uiRole", u"heading")

        self.layoutEstructura8.addWidget(self.menu_23)

        self.labelHeaderInfo_9 = QLabel(self.frameHeader_4)
        self.labelHeaderInfo_9.setObjectName(u"labelHeaderInfo_9")
        self.labelHeaderInfo_9.setAlignment(Qt.AlignLeft|Qt.AlignVCenter)
        self.labelHeaderInfo_9.setWordWrap(False)
        sizePolicy.setHeightForWidth(self.labelHeaderInfo_9.sizePolicy().hasHeightForWidth())
        self.labelHeaderInfo_9.setSizePolicy(sizePolicy)
        self.labelHeaderInfo_9.setProperty(u"uiRole", u"caption")

        self.layoutEstructura8.addWidget(self.labelHeaderInfo_9)

        self.layoutEstructura9 = QHBoxLayout()
        self.layoutEstructura9.setSpacing(16)
        self.layoutEstructura9.setObjectName(u"layoutEstructura9")
        self.layoutEstructura9.setContentsMargins(0, 0, 0, 0)
        self.frameHeader_16 = QFrame(self.frameHeader_4)
        self.frameHeader_16.setObjectName(u"frameHeader_16")
        self.frameHeader_16.setFrameShape(QFrame.StyledPanel)
        self.frameHeader_16.setFrameShadow(QFrame.Raised)
        self.frameHeader_16.setProperty(u"uiRole", u"card")
        self.layoutEstructura10 = QVBoxLayout(self.frameHeader_16)
        self.layoutEstructura10.setSpacing(8)
        self.layoutEstructura10.setObjectName(u"layoutEstructura10")
        self.layoutEstructura10.setContentsMargins(12, 12, 12, 12)
        self.menu_22 = QLabel(self.frameHeader_16)
        self.menu_22.setObjectName(u"menu_22")
        self.menu_22.setAlignment(Qt.AlignLeft|Qt.AlignVCenter)
        self.menu_22.setWordWrap(False)
        sizePolicy.setHeightForWidth(self.menu_22.sizePolicy().hasHeightForWidth())
        self.menu_22.setSizePolicy(sizePolicy)
        self.menu_22.setProperty(u"uiRole", u"section")

        self.layoutEstructura10.addWidget(self.menu_22)

        self.nombre_7 = QLabel(self.frameHeader_16)
        self.nombre_7.setObjectName(u"nombre_7")
        self.nombre_7.setAlignment(Qt.AlignLeft|Qt.AlignVCenter)
        self.nombre_7.setWordWrap(False)
        sizePolicy.setHeightForWidth(self.nombre_7.sizePolicy().hasHeightForWidth())
        self.nombre_7.setSizePolicy(sizePolicy)
        self.nombre_7.setProperty(u"uiRole", u"fieldLabel")

        self.layoutEstructura10.addWidget(self.nombre_7)

        self.textonombre_7 = QTextEdit(self.frameHeader_16)
        self.textonombre_7.setObjectName(u"textonombre_7")
        self.textonombre_7.setMinimumSize(QSize(0, 36))
        self.textonombre_7.setMaximumSize(QSize(16777215, 40))

        self.layoutEstructura10.addWidget(self.textonombre_7)

        self.label_35 = QLabel(self.frameHeader_16)
        self.label_35.setObjectName(u"label_35")
        self.label_35.setAlignment(Qt.AlignLeft|Qt.AlignVCenter)
        self.label_35.setWordWrap(False)
        sizePolicy.setHeightForWidth(self.label_35.sizePolicy().hasHeightForWidth())
        self.label_35.setSizePolicy(sizePolicy)
        self.label_35.setProperty(u"uiRole", u"fieldLabel")

        self.layoutEstructura10.addWidget(self.label_35)

        self.textocurp_7 = QTextEdit(self.frameHeader_16)
        self.textocurp_7.setObjectName(u"textocurp_7")
        self.textocurp_7.setMinimumSize(QSize(0, 36))
        self.textocurp_7.setMaximumSize(QSize(16777215, 40))

        self.layoutEstructura10.addWidget(self.textocurp_7)

        self.label_36 = QLabel(self.frameHeader_16)
        self.label_36.setObjectName(u"label_36")
        self.label_36.setAlignment(Qt.AlignLeft|Qt.AlignVCenter)
        self.label_36.setWordWrap(False)
        sizePolicy.setHeightForWidth(self.label_36.sizePolicy().hasHeightForWidth())
        self.label_36.setSizePolicy(sizePolicy)
        self.label_36.setProperty(u"uiRole", u"fieldLabel")

        self.layoutEstructura10.addWidget(self.label_36)

        self.textofechanacimiento_7 = QTextEdit(self.frameHeader_16)
        self.textofechanacimiento_7.setObjectName(u"textofechanacimiento_7")
        self.textofechanacimiento_7.setMinimumSize(QSize(0, 36))
        self.textofechanacimiento_7.setMaximumSize(QSize(16777215, 40))

        self.layoutEstructura10.addWidget(self.textofechanacimiento_7)

        self.espacioEstructura11 = QSpacerItem(8, 8, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.layoutEstructura10.addItem(self.espacioEstructura11)


        self.layoutEstructura9.addWidget(self.frameHeader_16)

        self.frameHeader_15 = QFrame(self.frameHeader_4)
        self.frameHeader_15.setObjectName(u"frameHeader_15")
        self.frameHeader_15.setFrameShape(QFrame.StyledPanel)
        self.frameHeader_15.setFrameShadow(QFrame.Raised)
        self.frameHeader_15.setProperty(u"uiRole", u"card")
        self.layoutEstructura12 = QVBoxLayout(self.frameHeader_15)
        self.layoutEstructura12.setSpacing(8)
        self.layoutEstructura12.setObjectName(u"layoutEstructura12")
        self.layoutEstructura12.setContentsMargins(12, 12, 12, 12)
        self.menu_21 = QLabel(self.frameHeader_15)
        self.menu_21.setObjectName(u"menu_21")
        self.menu_21.setAlignment(Qt.AlignLeft|Qt.AlignVCenter)
        self.menu_21.setWordWrap(False)
        sizePolicy.setHeightForWidth(self.menu_21.sizePolicy().hasHeightForWidth())
        self.menu_21.setSizePolicy(sizePolicy)
        self.menu_21.setProperty(u"uiRole", u"section")

        self.layoutEstructura12.addWidget(self.menu_21)

        self.otrosdatos_7 = QLabel(self.frameHeader_15)
        self.otrosdatos_7.setObjectName(u"otrosdatos_7")
        self.otrosdatos_7.setAlignment(Qt.AlignLeft|Qt.AlignVCenter)
        self.otrosdatos_7.setWordWrap(False)
        sizePolicy.setHeightForWidth(self.otrosdatos_7.sizePolicy().hasHeightForWidth())
        self.otrosdatos_7.setSizePolicy(sizePolicy)
        self.otrosdatos_7.setProperty(u"uiRole", u"fieldLabel")

        self.layoutEstructura12.addWidget(self.otrosdatos_7)

        self.verticalLayoutWidget_3 = QWidget(self.frameHeader_15)
        self.verticalLayoutWidget_3.setObjectName(u"verticalLayoutWidget_3")
        self.layoutEstructura13 = QVBoxLayout(self.verticalLayoutWidget_3)
        self.layoutEstructura13.setSpacing(8)
        self.layoutEstructura13.setObjectName(u"layoutEstructura13")
        self.layoutEstructura13.setContentsMargins(0, 0, 0, 0)
        self.frame_3 = QFrame(self.verticalLayoutWidget_3)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setFrameShape(QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.frame_3.setProperty(u"uiRole", u"notice")
        self.layoutEstructura14 = QVBoxLayout(self.frame_3)
        self.layoutEstructura14.setSpacing(4)
        self.layoutEstructura14.setObjectName(u"layoutEstructura14")
        self.layoutEstructura14.setContentsMargins(8, 8, 8, 8)
        self.normal = QRadioButton(self.frame_3)
        self.normal.setObjectName(u"normal")

        self.layoutEstructura14.addWidget(self.normal)

        self.preferencial = QRadioButton(self.frame_3)
        self.preferencial.setObjectName(u"preferencial")

        self.layoutEstructura14.addWidget(self.preferencial)


        self.layoutEstructura13.addWidget(self.frame_3)


        self.layoutEstructura12.addWidget(self.verticalLayoutWidget_3)

        self.vigencia_7 = QLabel(self.frameHeader_15)
        self.vigencia_7.setObjectName(u"vigencia_7")
        self.vigencia_7.setAlignment(Qt.AlignLeft|Qt.AlignVCenter)
        self.vigencia_7.setWordWrap(False)
        sizePolicy.setHeightForWidth(self.vigencia_7.sizePolicy().hasHeightForWidth())
        self.vigencia_7.setSizePolicy(sizePolicy)
        self.vigencia_7.setProperty(u"uiRole", u"fieldLabel")

        self.layoutEstructura12.addWidget(self.vigencia_7)

        self.textovigencia_7 = QTextEdit(self.frameHeader_15)
        self.textovigencia_7.setObjectName(u"textovigencia_7")
        self.textovigencia_7.setMinimumSize(QSize(0, 36))
        self.textovigencia_7.setMaximumSize(QSize(16777215, 40))

        self.layoutEstructura12.addWidget(self.textovigencia_7)

        self.label_32 = QLabel(self.frameHeader_15)
        self.label_32.setObjectName(u"label_32")
        self.label_32.setAlignment(Qt.AlignLeft|Qt.AlignVCenter)
        self.label_32.setWordWrap(False)
        sizePolicy.setHeightForWidth(self.label_32.sizePolicy().hasHeightForWidth())
        self.label_32.setSizePolicy(sizePolicy)
        self.label_32.setProperty(u"uiRole", u"fieldLabel")

        self.layoutEstructura12.addWidget(self.label_32)

        self.layoutEstructura15 = QHBoxLayout()
        self.layoutEstructura15.setSpacing(12)
        self.layoutEstructura15.setObjectName(u"layoutEstructura15")
        self.layoutEstructura15.setContentsMargins(0, 0, 0, 0)
        self.fotoimagen_7 = QLabel(self.frameHeader_15)
        self.fotoimagen_7.setObjectName(u"fotoimagen_7")
        self.fotoimagen_7.setProperty(u"uiRole", u"photo")
        self.fotoimagen_7.setAlignment(Qt.AlignLeft|Qt.AlignVCenter)
        self.fotoimagen_7.setWordWrap(False)
        sizePolicy.setHeightForWidth(self.fotoimagen_7.sizePolicy().hasHeightForWidth())
        self.fotoimagen_7.setSizePolicy(sizePolicy)
        self.fotoimagen_7.setMinimumSize(QSize(120, 96))
        self.fotoimagen_7.setMaximumSize(QSize(120, 96))

        self.layoutEstructura15.addWidget(self.fotoimagen_7)

        self.layoutEstructura16 = QVBoxLayout()
        self.layoutEstructura16.setSpacing(8)
        self.layoutEstructura16.setObjectName(u"layoutEstructura16")
        self.layoutEstructura16.setContentsMargins(0, 0, 0, 0)
        self.botonsubir_7 = QPushButton(self.frameHeader_15)
        self.botonsubir_7.setObjectName(u"botonsubir_7")
        self.botonsubir_7.setProperty(u"uiRole", u"secondary")
        self.botonsubir_7.setMinimumSize(QSize(100, 36))
        self.botonsubir_7.setMaximumSize(QSize(16777215, 40))
        sizePolicy.setHeightForWidth(self.botonsubir_7.sizePolicy().hasHeightForWidth())
        self.botonsubir_7.setSizePolicy(sizePolicy)

        self.layoutEstructura16.addWidget(self.botonsubir_7)

        self.label_33 = QLabel(self.frameHeader_15)
        self.label_33.setObjectName(u"label_33")
        self.label_33.setProperty(u"uiRole", u"caption")
        self.label_33.setAlignment(Qt.AlignLeft|Qt.AlignVCenter)
        sizePolicy.setHeightForWidth(self.label_33.sizePolicy().hasHeightForWidth())
        self.label_33.setSizePolicy(sizePolicy)
        self.label_33.setWordWrap(True)

        self.layoutEstructura16.addWidget(self.label_33)

        self.label_34 = QLabel(self.frameHeader_15)
        self.label_34.setObjectName(u"label_34")
        self.label_34.setProperty(u"uiRole", u"link")
        self.label_34.setAlignment(Qt.AlignLeft|Qt.AlignVCenter)
        self.label_34.setWordWrap(False)
        sizePolicy.setHeightForWidth(self.label_34.sizePolicy().hasHeightForWidth())
        self.label_34.setSizePolicy(sizePolicy)

        self.layoutEstructura16.addWidget(self.label_34)


        self.layoutEstructura15.addLayout(self.layoutEstructura16)


        self.layoutEstructura12.addLayout(self.layoutEstructura15)

        self.espacioEstructura17 = QSpacerItem(8, 8, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.layoutEstructura12.addItem(self.espacioEstructura17)


        self.layoutEstructura9.addWidget(self.frameHeader_15)

        self.layoutEstructura9.setStretch(0, 1)
        self.layoutEstructura9.setStretch(1, 1)

        self.layoutEstructura8.addLayout(self.layoutEstructura9)

        self.layoutEstructura18 = QHBoxLayout()
        self.layoutEstructura18.setSpacing(8)
        self.layoutEstructura18.setObjectName(u"layoutEstructura18")
        self.layoutEstructura18.setContentsMargins(0, 0, 0, 0)
        self.espacioEstructura19 = QSpacerItem(8, 8, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.layoutEstructura18.addItem(self.espacioEstructura19)

        self.botonguardar_13 = QPushButton(self.frameHeader_4)
        self.botonguardar_13.setObjectName(u"botonguardar_13")
        sizePolicy.setHeightForWidth(self.botonguardar_13.sizePolicy().hasHeightForWidth())
        self.botonguardar_13.setSizePolicy(sizePolicy)
        self.botonguardar_13.setProperty(u"uiRole", u"secondary")
        self.botonguardar_13.setMinimumSize(QSize(140, 38))
        self.botonguardar_13.setMaximumSize(QSize(240, 40))

        self.layoutEstructura18.addWidget(self.botonguardar_13)

        self.botonguardar_14 = QPushButton(self.frameHeader_4)
        self.botonguardar_14.setObjectName(u"botonguardar_14")
        sizePolicy.setHeightForWidth(self.botonguardar_14.sizePolicy().hasHeightForWidth())
        self.botonguardar_14.setSizePolicy(sizePolicy)
        self.botonguardar_14.setProperty(u"uiRole", u"primary")
        self.botonguardar_14.setMinimumSize(QSize(140, 38))
        self.botonguardar_14.setMaximumSize(QSize(240, 40))

        self.layoutEstructura18.addWidget(self.botonguardar_14)


        self.layoutEstructura8.addLayout(self.layoutEstructura18)

        self.areaContenido.setWidget(self.frameHeader_4)

        self.gridLayout_14.addWidget(self.areaContenido)

        self.labelHeaderInfo = QLabel(self.centralwidget)
        self.labelHeaderInfo.setObjectName(u"labelHeaderInfo")
        self.labelHeaderInfo.setWordWrap(False)
        sizePolicy.setHeightForWidth(self.labelHeaderInfo.sizePolicy().hasHeightForWidth())
        self.labelHeaderInfo.setSizePolicy(sizePolicy)
        self.labelHeaderInfo.setProperty(u"uiRole", u"caption")
        self.labelHeaderInfo.setAlignment(Qt.AlignCenter)

        self.gridLayout_14.addWidget(self.labelHeaderInfo)

        self.gridLayout_14.setStretch(2, 1)
        AltaWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(AltaWindow)

        QMetaObject.connectSlotsByName(AltaWindow)
    # setupUi

    def retranslateUi(self, AltaWindow):
        AltaWindow.setWindowTitle(QCoreApplication.translate("AltaWindow", u"Dar de alta", None))
        self.labelBrand.setText(QCoreApplication.translate("AltaWindow", u"RUMSA", None))
        self.labelHeaderInfo_3.setText(QCoreApplication.translate("AltaWindow", u"Rutas Urbanas de Matehuala S.A. de C.V.", None))
        self.usuario.setText(QCoreApplication.translate("AltaWindow", u"Usuario", None))
#if QT_CONFIG(tooltip)
        self.labelEstadoConexion_2.setToolTip(QCoreApplication.translate("AltaWindow", u"Este texto puede cambiar a: Conectando, Sin conexi\u00f3n, Sincronizando o Conectado.", None))
#endif // QT_CONFIG(tooltip)
        self.labelEstadoConexion_2.setText(QCoreApplication.translate("AltaWindow", u"\u25cf Conectando", None))
        self.mensajeInternet_2.setText("")
        self.mensajeInternet_2.setProperty(u"estadoVisual", QCoreApplication.translate("AltaWindow", u"error", None))
        self.botonregresar.setText(QCoreApplication.translate("AltaWindow", u"<  Volver", None))
        self.etiquetaPuerto.setText(QCoreApplication.translate("AltaWindow", u"Puerto del lector", None))
        self.menu_23.setText(QCoreApplication.translate("AltaWindow", u"Dar de Alta", None))
        self.labelHeaderInfo_9.setText(QCoreApplication.translate("AltaWindow", u"Completa los datos", None))
        self.menu_22.setText(QCoreApplication.translate("AltaWindow", u"Datos Personales", None))
        self.nombre_7.setText(QCoreApplication.translate("AltaWindow", u"Nombre", None))
        self.label_35.setText(QCoreApplication.translate("AltaWindow", u"Curp", None))
        self.label_36.setText(QCoreApplication.translate("AltaWindow", u"Fecha Nacimineto", None))
        self.textofechanacimiento_7.setHtml(QCoreApplication.translate("AltaWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body>\n"
"<p>Selecciona una fecha</p></body></html>", None))
        self.menu_21.setText(QCoreApplication.translate("AltaWindow", u"Datos de la Tarjeta", None))
        self.otrosdatos_7.setText(QCoreApplication.translate("AltaWindow", u"Tipo de Tarjeta", None))
        self.normal.setText(QCoreApplication.translate("AltaWindow", u"Normal", None))
        self.preferencial.setText(QCoreApplication.translate("AltaWindow", u"Preferencial", None))
        self.vigencia_7.setText(QCoreApplication.translate("AltaWindow", u"Vigencia", None))
        self.textovigencia_7.setHtml(QCoreApplication.translate("AltaWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body>\n"
"<p>Selecciona fecha</p></body></html>", None))
        self.label_32.setText(QCoreApplication.translate("AltaWindow", u"Fotograf\u00eda", None))
        self.fotoimagen_7.setText("")
        self.botonsubir_7.setText(QCoreApplication.translate("AltaWindow", u"Seleccionar", None))
        self.label_33.setText(QCoreApplication.translate("AltaWindow", u"Sin archivo seleccionado", None))
        self.label_34.setText(QCoreApplication.translate("AltaWindow", u"Quitar foto", None))
        self.botonguardar_13.setText(QCoreApplication.translate("AltaWindow", u"Cancelar", None))
        self.botonguardar_14.setText(QCoreApplication.translate("AltaWindow", u"Guardar", None))
        self.labelHeaderInfo.setText(QCoreApplication.translate("AltaWindow", u"RUMSA - Rutas Urbanas de Matehuala", None))
    # retranslateUi

