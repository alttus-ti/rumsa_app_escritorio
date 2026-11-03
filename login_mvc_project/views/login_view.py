# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'login_qtdesigner.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QFrame, QHBoxLayout,
    QLabel, QLineEdit, QMainWindow, QPushButton,
    QScrollArea, QSizePolicy, QSpacerItem, QStatusBar,
    QVBoxLayout, QWidget)

from core.imagen_marca import ImagenMarca

class LoginWindow(object):
    def setupUi(self, LoginWindow):
        if not LoginWindow.objectName():
            LoginWindow.setObjectName(u"LoginWindow")
        LoginWindow.setMinimumSize(QSize(760, 680))
        LoginWindow.resize(860, 780)
        self.centralwidget = QWidget(LoginWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_main = QVBoxLayout(self.centralwidget)
        self.verticalLayout_main.setSpacing(12)
        self.verticalLayout_main.setObjectName(u"verticalLayout_main")
        self.verticalLayout_main.setContentsMargins(16, 16, 16, 16)
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
        self.labelWelcome = QLabel(self.estadoCabecera)
        self.labelWelcome.setObjectName(u"labelWelcome")
        self.labelWelcome.setProperty(u"uiRole", u"caption")
        self.labelWelcome.setAlignment(Qt.AlignLeft|Qt.AlignVCenter)
        self.labelWelcome.setWordWrap(False)
        sizePolicy.setHeightForWidth(self.labelWelcome.sizePolicy().hasHeightForWidth())
        self.labelWelcome.setSizePolicy(sizePolicy)

        self.layoutEstructura5.addWidget(self.labelWelcome, 0, Qt.AlignRight)


        self.layoutEstructura2.addWidget(self.estadoCabecera)


        self.verticalLayout_main.addWidget(self.frameHeader)

        self.areaContenido = QScrollArea(self.centralwidget)
        self.areaContenido.setObjectName(u"areaContenido")
        self.areaContenido.setWidgetResizable(True)
        self.areaContenido.setFrameShape(QFrame.NoFrame)
        self.panelAcceso = QFrame()
        self.panelAcceso.setObjectName(u"panelAcceso")
        self.panelAcceso.setProperty(u"uiRole", u"card")
        self.layoutEstructura6 = QVBoxLayout(self.panelAcceso)
        self.layoutEstructura6.setSpacing(12)
        self.layoutEstructura6.setObjectName(u"layoutEstructura6")
        self.layoutEstructura6.setContentsMargins(16, 16, 16, 16)
        self.espacioSuperiorAcceso = QSpacerItem(0, 8, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.layoutEstructura6.addItem(self.espacioSuperiorAcceso)

        self.layoutInicioConMarca = QHBoxLayout()
        self.layoutInicioConMarca.setSpacing(24)
        self.layoutInicioConMarca.setObjectName(u"layoutInicioConMarca")
        self.layoutInicioConMarca.setContentsMargins(8, 0, 8, 0)
        self.panelImagenInicio = QFrame(self.panelAcceso)
        self.panelImagenInicio.setObjectName(u"panelImagenInicio")
        self.panelImagenInicio.setMinimumSize(QSize(260, 320))
        self.panelImagenInicio.setMaximumSize(QSize(340, 380))
        self.layoutImagenInicio = QVBoxLayout(self.panelImagenInicio)
        self.layoutImagenInicio.setObjectName(u"layoutImagenInicio")
        self.layoutImagenInicio.setContentsMargins(12, 12, 12, 12)
        self.imagenInicio = ImagenMarca(self.panelImagenInicio)
        self.imagenInicio.setObjectName(u"imagenInicio")
        self.imagenInicio.setAlignment(Qt.AlignCenter)
        self.imagenInicio.setWordWrap(True)
        self.imagenInicio.setMinimumSize(QSize(230, 280))

        self.layoutImagenInicio.addWidget(self.imagenInicio)


        self.layoutInicioConMarca.addWidget(self.panelImagenInicio, 0, Qt.AlignVCenter)

        self.formularioAcceso = QWidget(self.panelAcceso)
        self.formularioAcceso.setObjectName(u"formularioAcceso")
        self.formularioAcceso.setMinimumSize(QSize(360, 0))
        self.formularioAcceso.setMaximumSize(QSize(460, 16777215))
        self.layoutEstructura7 = QVBoxLayout(self.formularioAcceso)
        self.layoutEstructura7.setSpacing(8)
        self.layoutEstructura7.setObjectName(u"layoutEstructura7")
        self.layoutEstructura7.setContentsMargins(16, 16, 16, 16)
        self.labelTitle = QLabel(self.formularioAcceso)
        self.labelTitle.setObjectName(u"labelTitle")
        self.labelTitle.setAlignment(Qt.AlignLeft|Qt.AlignVCenter)
        self.labelTitle.setWordWrap(False)
        sizePolicy.setHeightForWidth(self.labelTitle.sizePolicy().hasHeightForWidth())
        self.labelTitle.setSizePolicy(sizePolicy)
        self.labelTitle.setProperty(u"uiRole", u"heading")

        self.layoutEstructura7.addWidget(self.labelTitle)

        self.labelSubtitle = QLabel(self.formularioAcceso)
        self.labelSubtitle.setObjectName(u"labelSubtitle")
        self.labelSubtitle.setAlignment(Qt.AlignLeft|Qt.AlignVCenter)
        self.labelSubtitle.setWordWrap(False)
        sizePolicy.setHeightForWidth(self.labelSubtitle.sizePolicy().hasHeightForWidth())
        self.labelSubtitle.setSizePolicy(sizePolicy)
        self.labelSubtitle.setProperty(u"uiRole", u"caption")

        self.layoutEstructura7.addWidget(self.labelSubtitle)

        self.labelUser = QLabel(self.formularioAcceso)
        self.labelUser.setObjectName(u"labelUser")
        self.labelUser.setAlignment(Qt.AlignLeft|Qt.AlignVCenter)
        self.labelUser.setWordWrap(False)
        sizePolicy.setHeightForWidth(self.labelUser.sizePolicy().hasHeightForWidth())
        self.labelUser.setSizePolicy(sizePolicy)
        self.labelUser.setProperty(u"uiRole", u"fieldLabel")

        self.layoutEstructura7.addWidget(self.labelUser)

        self.lineEditUser = QLineEdit(self.formularioAcceso)
        self.lineEditUser.setObjectName(u"lineEditUser")
        self.lineEditUser.setMinimumSize(QSize(0, 36))
        self.lineEditUser.setMaximumSize(QSize(16777215, 40))

        self.layoutEstructura7.addWidget(self.lineEditUser)

        self.labelPassword = QLabel(self.formularioAcceso)
        self.labelPassword.setObjectName(u"labelPassword")
        self.labelPassword.setAlignment(Qt.AlignLeft|Qt.AlignVCenter)
        self.labelPassword.setWordWrap(False)
        sizePolicy.setHeightForWidth(self.labelPassword.sizePolicy().hasHeightForWidth())
        self.labelPassword.setSizePolicy(sizePolicy)
        self.labelPassword.setProperty(u"uiRole", u"fieldLabel")

        self.layoutEstructura7.addWidget(self.labelPassword)

        self.lineEditPassword = QLineEdit(self.formularioAcceso)
        self.lineEditPassword.setObjectName(u"lineEditPassword")
        self.lineEditPassword.setEchoMode(QLineEdit.Password)
        self.lineEditPassword.setMinimumSize(QSize(0, 36))
        self.lineEditPassword.setMaximumSize(QSize(16777215, 40))

        self.layoutEstructura7.addWidget(self.lineEditPassword)

        self.layoutEstructura8 = QHBoxLayout()
        self.layoutEstructura8.setSpacing(8)
        self.layoutEstructura8.setObjectName(u"layoutEstructura8")
        self.layoutEstructura8.setContentsMargins(0, 0, 0, 0)
        self.checkBoxRemember = QCheckBox(self.formularioAcceso)
        self.checkBoxRemember.setObjectName(u"checkBoxRemember")

        self.layoutEstructura8.addWidget(self.checkBoxRemember)

        self.espacioEstructura9 = QSpacerItem(8, 8, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.layoutEstructura8.addItem(self.espacioEstructura9)

        self.pushButtonForgot = QPushButton(self.formularioAcceso)
        self.pushButtonForgot.setObjectName(u"pushButtonForgot")
        self.pushButtonForgot.setFlat(True)
        self.pushButtonForgot.setMinimumSize(QSize(100, 36))
        self.pushButtonForgot.setMaximumSize(QSize(16777215, 40))
        sizePolicy.setHeightForWidth(self.pushButtonForgot.sizePolicy().hasHeightForWidth())
        self.pushButtonForgot.setSizePolicy(sizePolicy)
        self.pushButtonForgot.setProperty(u"uiRole", u"link")

        self.layoutEstructura8.addWidget(self.pushButtonForgot)


        self.layoutEstructura7.addLayout(self.layoutEstructura8)

        self.layoutEstructura10 = QHBoxLayout()
        self.layoutEstructura10.setSpacing(8)
        self.layoutEstructura10.setObjectName(u"layoutEstructura10")
        self.layoutEstructura10.setContentsMargins(0, 0, 0, 0)
        self.espacioEstructura11 = QSpacerItem(8, 8, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.layoutEstructura10.addItem(self.espacioEstructura11)

        self.pushButtonCancel = QPushButton(self.formularioAcceso)
        self.pushButtonCancel.setObjectName(u"pushButtonCancel")
        sizePolicy.setHeightForWidth(self.pushButtonCancel.sizePolicy().hasHeightForWidth())
        self.pushButtonCancel.setSizePolicy(sizePolicy)
        self.pushButtonCancel.setProperty(u"uiRole", u"secondary")
        self.pushButtonCancel.setMinimumSize(QSize(140, 38))
        self.pushButtonCancel.setMaximumSize(QSize(240, 40))

        self.layoutEstructura10.addWidget(self.pushButtonCancel)

        self.pushButtonLogin = QPushButton(self.formularioAcceso)
        self.pushButtonLogin.setObjectName(u"pushButtonLogin")
        sizePolicy.setHeightForWidth(self.pushButtonLogin.sizePolicy().hasHeightForWidth())
        self.pushButtonLogin.setSizePolicy(sizePolicy)
        self.pushButtonLogin.setProperty(u"uiRole", u"primary")
        self.pushButtonLogin.setMinimumSize(QSize(140, 38))
        self.pushButtonLogin.setMaximumSize(QSize(240, 40))

        self.layoutEstructura10.addWidget(self.pushButtonLogin)


        self.layoutEstructura7.addLayout(self.layoutEstructura10)


        self.layoutInicioConMarca.addWidget(self.formularioAcceso, 0, Qt.AlignVCenter)

        self.layoutInicioConMarca.setStretch(0, 1)
        self.layoutInicioConMarca.setStretch(1, 1)

        self.layoutEstructura6.addLayout(self.layoutInicioConMarca)

        self.espacioInferiorAcceso = QSpacerItem(0, 8, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.layoutEstructura6.addItem(self.espacioInferiorAcceso)

        self.layoutEstructura6.setStretch(0, 1)
        self.layoutEstructura6.setStretch(2, 1)
        self.areaContenido.setWidget(self.panelAcceso)

        self.verticalLayout_main.addWidget(self.areaContenido)

        self.pieAplicacion = QLabel(self.centralwidget)
        self.pieAplicacion.setObjectName(u"pieAplicacion")
        sizePolicy.setHeightForWidth(self.pieAplicacion.sizePolicy().hasHeightForWidth())
        self.pieAplicacion.setSizePolicy(sizePolicy)
        self.pieAplicacion.setProperty(u"uiRole", u"caption")
        self.pieAplicacion.setAlignment(Qt.AlignCenter)

        self.verticalLayout_main.addWidget(self.pieAplicacion)

        self.verticalLayout_main.setStretch(1, 1)
        LoginWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(LoginWindow)
        self.statusbar.setObjectName(u"statusbar")
        LoginWindow.setStatusBar(self.statusbar)

        self.retranslateUi(LoginWindow)

        QMetaObject.connectSlotsByName(LoginWindow)
    # setupUi

    def retranslateUi(self, LoginWindow):
        LoginWindow.setWindowTitle(QCoreApplication.translate("LoginWindow", u"Iniciar sesi\u00f3n", None))
        self.labelBrand.setText(QCoreApplication.translate("LoginWindow", u"RUMSA", None))
        self.labelCompany.setText(QCoreApplication.translate("LoginWindow", u"Rutas Urbanas de Matehuala S.A. de C.V.", None))
        self.labelWelcome.setText(QCoreApplication.translate("LoginWindow", u"Acceso al sistema", None))
        self.imagenInicio.setText(QCoreApplication.translate("LoginWindow", u"RUMSA\n"
"Rutas Urbanas de Matehuala\n"
"S.A. de C.V.", None))
        self.labelTitle.setText(QCoreApplication.translate("LoginWindow", u"Iniciar sesi\u00f3n", None))
        self.labelSubtitle.setText(QCoreApplication.translate("LoginWindow", u"Ingresa tus credenciales para continuar", None))
        self.labelUser.setText(QCoreApplication.translate("LoginWindow", u"Usuario:", None))
        self.lineEditUser.setPlaceholderText(QCoreApplication.translate("LoginWindow", u"Escribe tu usuario", None))
        self.labelPassword.setText(QCoreApplication.translate("LoginWindow", u"Contrase\u00f1a:", None))
        self.lineEditPassword.setPlaceholderText(QCoreApplication.translate("LoginWindow", u"Escribe tu contrase\u00f1a", None))
        self.checkBoxRemember.setText(QCoreApplication.translate("LoginWindow", u"Recordarme", None))
        #self.pushButtonForgot.setText(QCoreApplication.translate("LoginWindow", u"\u00bfOlvidaste tu contrase\u00f1a?", None))
        self.pushButtonForgot.setText("")
        self.pushButtonCancel.setText(QCoreApplication.translate("LoginWindow", u"Cancelar", None))
        self.pushButtonLogin.setText(QCoreApplication.translate("LoginWindow", u"Iniciar sesi\u00f3n", None))
        self.pieAplicacion.setText(QCoreApplication.translate("LoginWindow", u"RUMSA - Rutas Urbanas de Matehuala", None))
    # retranslateUi

