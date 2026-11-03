# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'empleado.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QLabel,
    QMainWindow, QPushButton, QScrollArea, QSizePolicy,
    QSpacerItem, QToolButton, QVBoxLayout, QWidget)

class EmpleadoWindow(object):
    def setupUi(self, EmpleadoWindow):
        if not EmpleadoWindow.objectName():
            EmpleadoWindow.setObjectName(u"EmpleadoWindow")
        EmpleadoWindow.setMinimumSize(QSize(760, 680))
        EmpleadoWindow.resize(860, 780)
        self.centralwidget = QWidget(EmpleadoWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QVBoxLayout(self.centralwidget)
        self.gridLayout.setSpacing(12)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(16, 16, 16, 16)
        self.frameHeader = QFrame(self.centralwidget)
        self.frameHeader.setObjectName(u"frameHeader")
        self.frameHeader.setFrameShape(QFrame.StyledPanel)
        self.frameHeader.setFrameShadow(QFrame.Raised)
        self.frameHeader.setProperty(u"uiRole", u"header")
        self.frameHeader.setMinimumSize(QSize(0, 90))
        self.frameHeader.setMaximumSize(QSize(16777215, 90))
        self.layoutEstructura2 = QHBoxLayout(self.frameHeader)
        self.layoutEstructura2.setSpacing(12)
        self.layoutEstructura2.setObjectName(u"layoutEstructura2")
        self.layoutEstructura2.setContentsMargins(12, 12, 12, 12)
        self.franjaCabecera = QFrame(self.frameHeader)
        self.franjaCabecera.setObjectName(u"franjaCabecera")
        self.franjaCabecera.setProperty(u"uiRole", u"stripe")
        self.franjaCabecera.setMinimumSize(QSize(5, 32))
        self.franjaCabecera.setMaximumSize(QSize(5, 32))

        self.layoutEstructura2.addWidget(self.franjaCabecera, 0, Qt.AlignVCenter)

        self.marcaCabecera = QWidget(self.frameHeader)
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

        self.estadoCabecera = QWidget(self.frameHeader)
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


        self.gridLayout.addWidget(self.frameHeader)

        self.areaContenido = QScrollArea(self.centralwidget)
        self.areaContenido.setObjectName(u"areaContenido")
        self.areaContenido.setWidgetResizable(True)
        self.areaContenido.setFrameShape(QFrame.NoFrame)
        self.panelEmpleado = QFrame()
        self.panelEmpleado.setObjectName(u"panelEmpleado")
        self.panelEmpleado.setProperty(u"uiRole", u"card")
        self.layoutEstructura6 = QVBoxLayout(self.panelEmpleado)
        self.layoutEstructura6.setSpacing(12)
        self.layoutEstructura6.setObjectName(u"layoutEstructura6")
        self.layoutEstructura6.setContentsMargins(16, 16, 16, 16)
        self.espacioSuperiorEmpleado = QSpacerItem(8, 8, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.layoutEstructura6.addItem(self.espacioSuperiorEmpleado)

        self.opcionesEmpleado = QWidget(self.panelEmpleado)
        self.opcionesEmpleado.setObjectName(u"opcionesEmpleado")
        self.opcionesEmpleado.setMinimumSize(QSize(560, 0))
        self.opcionesEmpleado.setMaximumSize(QSize(640, 16777215))
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.opcionesEmpleado.sizePolicy().hasHeightForWidth())
        self.opcionesEmpleado.setSizePolicy(sizePolicy1)
        self.opcionesEmpleadoLayout = QVBoxLayout(self.opcionesEmpleado)
        self.opcionesEmpleadoLayout.setSpacing(12)
        self.opcionesEmpleadoLayout.setObjectName(u"opcionesEmpleadoLayout")
        self.opcionesEmpleadoLayout.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(self.opcionesEmpleado)
        self.label.setObjectName(u"label")
        self.label.setAlignment(Qt.AlignLeft|Qt.AlignVCenter)
        self.label.setWordWrap(False)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setProperty(u"uiRole", u"heading")

        self.opcionesEmpleadoLayout.addWidget(self.label)

        self.labelHeaderInfo = QLabel(self.opcionesEmpleado)
        self.labelHeaderInfo.setObjectName(u"labelHeaderInfo")
        self.labelHeaderInfo.setAlignment(Qt.AlignLeft|Qt.AlignVCenter)
        self.labelHeaderInfo.setWordWrap(False)
        sizePolicy.setHeightForWidth(self.labelHeaderInfo.sizePolicy().hasHeightForWidth())
        self.labelHeaderInfo.setSizePolicy(sizePolicy)
        self.labelHeaderInfo.setProperty(u"uiRole", u"caption")

        self.opcionesEmpleadoLayout.addWidget(self.labelHeaderInfo)

        self.botonrecarga = QPushButton(self.opcionesEmpleado)
        self.botonrecarga.setObjectName(u"botonrecarga")
        sizePolicy.setHeightForWidth(self.botonrecarga.sizePolicy().hasHeightForWidth())
        self.botonrecarga.setSizePolicy(sizePolicy)
        self.botonrecarga.setProperty(u"uiRole", u"menuAction")
        self.botonrecarga.setMinimumSize(QSize(312, 170))
        self.botonrecarga.setMaximumSize(QSize(312, 190))
        self.botonrecarga.setProperty(u"menuShape", u"tile")

        self.opcionesEmpleadoLayout.addWidget(self.botonrecarga, 0, Qt.AlignHCenter)


        self.layoutEstructura6.addWidget(self.opcionesEmpleado, 0, Qt.AlignHCenter)

        self.espacioEstructura7 = QSpacerItem(8, 8, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.layoutEstructura6.addItem(self.espacioEstructura7)

        self.layoutEstructura6.setStretch(0, 1)
        self.layoutEstructura6.setStretch(2, 1)
        self.areaContenido.setWidget(self.panelEmpleado)

        self.gridLayout.addWidget(self.areaContenido)

        self.pieAplicacion = QLabel(self.centralwidget)
        self.pieAplicacion.setObjectName(u"pieAplicacion")
        sizePolicy.setHeightForWidth(self.pieAplicacion.sizePolicy().hasHeightForWidth())
        self.pieAplicacion.setSizePolicy(sizePolicy)
        self.pieAplicacion.setProperty(u"uiRole", u"caption")
        self.pieAplicacion.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.pieAplicacion)

        self.gridLayout.setStretch(1, 1)
        EmpleadoWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(EmpleadoWindow)

        QMetaObject.connectSlotsByName(EmpleadoWindow)
    # setupUi

    def retranslateUi(self, EmpleadoWindow):
        EmpleadoWindow.setWindowTitle(QCoreApplication.translate("EmpleadoWindow", u"Empleado", None))
        self.labelBrand.setText(QCoreApplication.translate("EmpleadoWindow", u"RUMSA", None))
        self.labelCompany.setText(QCoreApplication.translate("EmpleadoWindow", u"Rutas Urbanas de Matehuala S.A. de C.V.", None))
        self.usuario.setText(QCoreApplication.translate("EmpleadoWindow", u"Usuario", None))
#if QT_CONFIG(tooltip)
        self.labelEstadoConexion.setToolTip(QCoreApplication.translate("EmpleadoWindow", u"Este texto puede cambiar a: Conectando, Sin conexi\u00f3n, Sincronizando o Conectado.", None))
#endif // QT_CONFIG(tooltip)
        self.labelEstadoConexion.setText(QCoreApplication.translate("EmpleadoWindow", u"\u25cf Conectando", None))
        self.label.setText(QCoreApplication.translate("EmpleadoWindow", u"Men\u00fa principal", None))
        self.labelHeaderInfo.setText(QCoreApplication.translate("EmpleadoWindow", u"Rutas Urbanas de Matehuala", None))
        self.botonrecarga.setText(QCoreApplication.translate("EmpleadoWindow", u"Recargar", None))
        self.pieAplicacion.setText(QCoreApplication.translate("EmpleadoWindow", u"RUMSA - Rutas Urbanas de Matehuala", None))
    # retranslateUi

