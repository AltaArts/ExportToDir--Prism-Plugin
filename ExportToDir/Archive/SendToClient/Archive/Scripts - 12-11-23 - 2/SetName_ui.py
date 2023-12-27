# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'SetMediaNamezfNVyE.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_setMediaNameDlg(object):
    def setupUi(self, setMediaNameDlg):
        if not setMediaNameDlg.objectName():
            setMediaNameDlg.setObjectName(u"setMediaNameDlg")
        setMediaNameDlg.resize(900, 425)
        self.verticalLayout_2 = QVBoxLayout(setMediaNameDlg)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.f_upper = QVBoxLayout()
        self.f_upper.setObjectName(u"f_upper")
        self.verticalSpacer = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.f_upper.addItem(self.verticalSpacer)

        self.f_mediaName = QHBoxLayout()
        self.f_mediaName.setObjectName(u"f_mediaName")
        self.l_mediaName = QLabel(setMediaNameDlg)
        self.l_mediaName.setObjectName(u"l_mediaName")

        self.f_mediaName.addWidget(self.l_mediaName)

        self.e_mediaName = QLineEdit(setMediaNameDlg)
        self.e_mediaName.setObjectName(u"e_mediaName")

        self.f_mediaName.addWidget(self.e_mediaName)

        self.but_nameReset = QPushButton(setMediaNameDlg)
        self.but_nameReset.setObjectName(u"but_nameReset")

        self.f_mediaName.addWidget(self.but_nameReset)


        self.f_upper.addLayout(self.f_mediaName)

        self.verticalSpacer_3 = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.f_upper.addItem(self.verticalSpacer_3)

        self.line = QFrame(setMediaNameDlg)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.f_upper.addWidget(self.line)

        self.l_DeliveryFolder = QLabel(setMediaNameDlg)
        self.l_DeliveryFolder.setObjectName(u"l_DeliveryFolder")

        self.f_upper.addWidget(self.l_DeliveryFolder)


        self.verticalLayout_2.addLayout(self.f_upper)

        self.verticalSpacer_2 = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout_2.addItem(self.verticalSpacer_2)

        self.f_mid = QHBoxLayout()
        self.f_mid.setObjectName(u"f_mid")
        self.horizontalSpacer_2 = QSpacerItem(20, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.f_mid.addItem(self.horizontalSpacer_2)

        self.f_midRt = QVBoxLayout()
        self.f_midRt.setObjectName(u"f_midRt")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.rb_ProjectFolder = QRadioButton(setMediaNameDlg)
        self.butGroup_folder = QButtonGroup(setMediaNameDlg)
        self.butGroup_folder.setObjectName(u"butGroup_folder")
        self.butGroup_folder.setExclusive(True)
        self.butGroup_folder.addButton(self.rb_ProjectFolder)
        self.rb_ProjectFolder.setObjectName(u"rb_ProjectFolder")

        self.horizontalLayout.addWidget(self.rb_ProjectFolder)

        self.l_radioProjectFolder = QLabel(setMediaNameDlg)
        self.l_radioProjectFolder.setObjectName(u"l_radioProjectFolder")

        self.horizontalLayout.addWidget(self.l_radioProjectFolder)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_4)


        self.f_midRt.addLayout(self.horizontalLayout)

        self.f_projectFolders = QHBoxLayout()
        self.f_projectFolders.setObjectName(u"f_projectFolders")
        self.horizontalSpacer = QSpacerItem(20, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.f_projectFolders.addItem(self.horizontalSpacer)

        self.cb_mediaFolders = QComboBox(setMediaNameDlg)
        self.cb_mediaFolders.setObjectName(u"cb_mediaFolders")

        self.f_projectFolders.addWidget(self.cb_mediaFolders)


        self.f_midRt.addLayout(self.f_projectFolders)

        self.verticalSpacer_4 = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.f_midRt.addItem(self.verticalSpacer_4)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.rb_customFolder = QRadioButton(setMediaNameDlg)
        self.butGroup_folder.addButton(self.rb_customFolder)
        self.rb_customFolder.setObjectName(u"rb_customFolder")

        self.horizontalLayout_2.addWidget(self.rb_customFolder)

        self.l_radioCustomFolder = QLabel(setMediaNameDlg)
        self.l_radioCustomFolder.setObjectName(u"l_radioCustomFolder")
        self.l_radioCustomFolder.setEnabled(False)

        self.horizontalLayout_2.addWidget(self.l_radioCustomFolder)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_5)


        self.f_midRt.addLayout(self.horizontalLayout_2)

        self.f_customFolder = QHBoxLayout()
        self.f_customFolder.setObjectName(u"f_customFolder")
        self.horizontalSpacer_3 = QSpacerItem(20, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.f_customFolder.addItem(self.horizontalSpacer_3)

        self.e_customLoc = QLineEdit(setMediaNameDlg)
        self.e_customLoc.setObjectName(u"e_customLoc")
        self.e_customLoc.setEnabled(False)

        self.f_customFolder.addWidget(self.e_customLoc)

        self.but_customPathSearch = QPushButton(setMediaNameDlg)
        self.but_customPathSearch.setObjectName(u"but_customPathSearch")
        self.but_customPathSearch.setEnabled(False)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.but_customPathSearch.sizePolicy().hasHeightForWidth())
        self.but_customPathSearch.setSizePolicy(sizePolicy)
        self.but_customPathSearch.setMinimumSize(QSize(60, 0))
        self.but_customPathSearch.setMaximumSize(QSize(60, 16777215))

        self.f_customFolder.addWidget(self.but_customPathSearch)


        self.f_midRt.addLayout(self.f_customFolder)


        self.f_mid.addLayout(self.f_midRt)


        self.verticalLayout_2.addLayout(self.f_mid)

        self.verticalSpacer_6 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer_6)

        self.f_outputPath = QVBoxLayout()
        self.f_outputPath.setObjectName(u"f_outputPath")
        self.f_outputLable = QHBoxLayout()
        self.f_outputLable.setObjectName(u"f_outputLable")
        self.l_outputName = QLabel(setMediaNameDlg)
        self.l_outputName.setObjectName(u"l_outputName")

        self.f_outputLable.addWidget(self.l_outputName)


        self.f_outputPath.addLayout(self.f_outputLable)

        self.f_outputPath_2 = QHBoxLayout()
        self.f_outputPath_2.setObjectName(u"f_outputPath_2")
        self.e_outputName = QLineEdit(setMediaNameDlg)
        self.e_outputName.setObjectName(u"e_outputName")
        self.e_outputName.setReadOnly(True)

        self.f_outputPath_2.addWidget(self.e_outputName)


        self.f_outputPath.addLayout(self.f_outputPath_2)


        self.verticalLayout_2.addLayout(self.f_outputPath)

        self.verticalSpacer_5 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer_5)

        self.progressBar = QProgressBar(setMediaNameDlg)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setValue(0)
        self.progressBar.setTextVisible(True)

        self.verticalLayout_2.addWidget(self.progressBar)

        self.f_buttonsMain = QVBoxLayout()
        self.f_buttonsMain.setObjectName(u"f_buttonsMain")
        self.f_buttonsSub = QHBoxLayout()
        self.f_buttonsSub.setObjectName(u"f_buttonsSub")
        self.but_explorer = QPushButton(setMediaNameDlg)
        self.but_explorer.setObjectName(u"but_explorer")

        self.f_buttonsSub.addWidget(self.but_explorer)

        self.buttonBox = QDialogButtonBox(setMediaNameDlg)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setLayoutDirection(Qt.LeftToRight)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Close|QDialogButtonBox.Save)
        self.buttonBox.setCenterButtons(False)

        self.f_buttonsSub.addWidget(self.buttonBox)


        self.f_buttonsMain.addLayout(self.f_buttonsSub)


        self.verticalLayout_2.addLayout(self.f_buttonsMain)


        self.retranslateUi(setMediaNameDlg)
        self.rb_ProjectFolder.toggled.connect(self.cb_mediaFolders.setEnabled)
        self.rb_ProjectFolder.toggled.connect(self.l_radioProjectFolder.setEnabled)
        self.rb_customFolder.toggled.connect(self.but_customPathSearch.setEnabled)
        self.rb_customFolder.toggled.connect(self.e_customLoc.setEnabled)
        self.rb_customFolder.toggled.connect(self.l_radioCustomFolder.setEnabled)

        QMetaObject.connectSlotsByName(setMediaNameDlg)
    # setupUi

    def retranslateUi(self, setMediaNameDlg):
        setMediaNameDlg.setWindowTitle(QCoreApplication.translate("setMediaNameDlg", u"Dialog", None))
        self.l_mediaName.setText(QCoreApplication.translate("setMediaNameDlg", u"Delivery Media Name:", None))
        self.but_nameReset.setText(QCoreApplication.translate("setMediaNameDlg", u"Default", None))
        self.l_DeliveryFolder.setText(QCoreApplication.translate("setMediaNameDlg", u"Delivery Folder:", None))
        self.rb_ProjectFolder.setText("")
        self.l_radioProjectFolder.setText(QCoreApplication.translate("setMediaNameDlg", u"Project Folders:", None))
        self.rb_customFolder.setText("")
        self.l_radioCustomFolder.setText(QCoreApplication.translate("setMediaNameDlg", u"Custom Folder:", None))
        self.but_customPathSearch.setText(QCoreApplication.translate("setMediaNameDlg", u"...", None))
        self.l_outputName.setText(QCoreApplication.translate("setMediaNameDlg", u"Output:", None))
        self.but_explorer.setText(QCoreApplication.translate("setMediaNameDlg", u"Open in Explorer", None))
    # retranslateUi

