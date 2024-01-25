# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ExportToDirbrrLPJ.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_exportToDirDlg(object):
    def setupUi(self, exportToDirDlg):
        if not exportToDirDlg.objectName():
            exportToDirDlg.setObjectName(u"exportToDirDlg")
        exportToDirDlg.resize(900, 479)
        self.verticalLayout_2 = QVBoxLayout(exportToDirDlg)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.f_upper = QVBoxLayout()
        self.f_upper.setObjectName(u"f_upper")
        self.verticalSpacer = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.f_upper.addItem(self.verticalSpacer)

        self.f_mediaName = QHBoxLayout()
        self.f_mediaName.setObjectName(u"f_mediaName")
        self.l_mediaName = QLabel(exportToDirDlg)
        self.l_mediaName.setObjectName(u"l_mediaName")

        self.f_mediaName.addWidget(self.l_mediaName)

        self.e_mediaName = QLineEdit(exportToDirDlg)
        self.e_mediaName.setObjectName(u"e_mediaName")

        self.f_mediaName.addWidget(self.e_mediaName)

        self.but_nameReset = QPushButton(exportToDirDlg)
        self.but_nameReset.setObjectName(u"but_nameReset")

        self.f_mediaName.addWidget(self.but_nameReset)


        self.f_upper.addLayout(self.f_mediaName)

        self.f_sequenceSelection = QHBoxLayout()
        self.f_sequenceSelection.setObjectName(u"f_sequenceSelection")
        self.horizontalSpacer_6 = QSpacerItem(120, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.f_sequenceSelection.addItem(self.horizontalSpacer_6)

        self.rb_singleImage = QRadioButton(exportToDirDlg)
        self.butGroup_imageSeq = QButtonGroup(exportToDirDlg)
        self.butGroup_imageSeq.setObjectName(u"butGroup_imageSeq")
        self.butGroup_imageSeq.addButton(self.rb_singleImage)
        self.rb_singleImage.setObjectName(u"rb_singleImage")

        self.f_sequenceSelection.addWidget(self.rb_singleImage)

        self.horizontalSpacer_8 = QSpacerItem(40, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.f_sequenceSelection.addItem(self.horizontalSpacer_8)

        self.rb_imageSeq = QRadioButton(exportToDirDlg)
        self.butGroup_imageSeq.addButton(self.rb_imageSeq)
        self.rb_imageSeq.setObjectName(u"rb_imageSeq")

        self.f_sequenceSelection.addWidget(self.rb_imageSeq)

        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.f_sequenceSelection.addItem(self.horizontalSpacer_7)


        self.f_upper.addLayout(self.f_sequenceSelection)

        self.line = QFrame(exportToDirDlg)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.f_upper.addWidget(self.line)

        self.verticalSpacer_3 = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.f_upper.addItem(self.verticalSpacer_3)

        self.l_DeliveryFolder = QLabel(exportToDirDlg)
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
        self.rb_ProjectFolder = QRadioButton(exportToDirDlg)
        self.butGroup_folder = QButtonGroup(exportToDirDlg)
        self.butGroup_folder.setObjectName(u"butGroup_folder")
        self.butGroup_folder.setExclusive(True)
        self.butGroup_folder.addButton(self.rb_ProjectFolder)
        self.rb_ProjectFolder.setObjectName(u"rb_ProjectFolder")

        self.horizontalLayout.addWidget(self.rb_ProjectFolder)

        self.l_radioProjectFolder = QLabel(exportToDirDlg)
        self.l_radioProjectFolder.setObjectName(u"l_radioProjectFolder")

        self.horizontalLayout.addWidget(self.l_radioProjectFolder)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_4)


        self.f_midRt.addLayout(self.horizontalLayout)

        self.f_projectFolders = QHBoxLayout()
        self.f_projectFolders.setObjectName(u"f_projectFolders")
        self.horizontalSpacer = QSpacerItem(20, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.f_projectFolders.addItem(self.horizontalSpacer)

        self.cb_mediaFolders = QComboBox(exportToDirDlg)
        self.cb_mediaFolders.setObjectName(u"cb_mediaFolders")

        self.f_projectFolders.addWidget(self.cb_mediaFolders)


        self.f_midRt.addLayout(self.f_projectFolders)

        self.verticalSpacer_4 = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.f_midRt.addItem(self.verticalSpacer_4)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.rb_customFolder = QRadioButton(exportToDirDlg)
        self.butGroup_folder.addButton(self.rb_customFolder)
        self.rb_customFolder.setObjectName(u"rb_customFolder")

        self.horizontalLayout_2.addWidget(self.rb_customFolder)

        self.l_radioCustomFolder = QLabel(exportToDirDlg)
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

        self.e_customLoc = QLineEdit(exportToDirDlg)
        self.e_customLoc.setObjectName(u"e_customLoc")
        self.e_customLoc.setEnabled(False)

        self.f_customFolder.addWidget(self.e_customLoc)

        self.but_customPathSearch = QPushButton(exportToDirDlg)
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

        self.verticalSpacer_5 = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout_2.addItem(self.verticalSpacer_5)

        self.f_appendFolder = QHBoxLayout()
        self.f_appendFolder.setObjectName(u"f_appendFolder")
        self.l_appendFolder = QLabel(exportToDirDlg)
        self.l_appendFolder.setObjectName(u"l_appendFolder")

        self.f_appendFolder.addWidget(self.l_appendFolder)

        self.e_appendFolder = QLineEdit(exportToDirDlg)
        self.e_appendFolder.setObjectName(u"e_appendFolder")

        self.f_appendFolder.addWidget(self.e_appendFolder)

        self.horizontalSpacer_14 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.f_appendFolder.addItem(self.horizontalSpacer_14)


        self.verticalLayout_2.addLayout(self.f_appendFolder)

        self.verticalSpacer_6 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer_6)

        self.f_outputPath = QVBoxLayout()
        self.f_outputPath.setObjectName(u"f_outputPath")
        self.f_outputLable = QHBoxLayout()
        self.f_outputLable.setObjectName(u"f_outputLable")
        self.l_outputName = QLabel(exportToDirDlg)
        self.l_outputName.setObjectName(u"l_outputName")

        self.f_outputLable.addWidget(self.l_outputName)

        self.horizontalSpacer_9 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.f_outputLable.addItem(self.horizontalSpacer_9)

        self.chb_zipFile = QCheckBox(exportToDirDlg)
        self.chb_zipFile.setObjectName(u"chb_zipFile")

        self.f_outputLable.addWidget(self.chb_zipFile)

        self.horizontalSpacer_10 = QSpacerItem(40, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.f_outputLable.addItem(self.horizontalSpacer_10)


        self.f_outputPath.addLayout(self.f_outputLable)

        self.f_outputPath_2 = QHBoxLayout()
        self.f_outputPath_2.setObjectName(u"f_outputPath_2")
        self.e_outputName = QLineEdit(exportToDirDlg)
        self.e_outputName.setObjectName(u"e_outputName")
        self.e_outputName.setReadOnly(True)

        self.f_outputPath_2.addWidget(self.e_outputName)


        self.f_outputPath.addLayout(self.f_outputPath_2)


        self.verticalLayout_2.addLayout(self.f_outputPath)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalSpacer_12 = QSpacerItem(10, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_12)

        self.l_status = QLabel(exportToDirDlg)
        self.l_status.setObjectName(u"l_status")

        self.horizontalLayout_3.addWidget(self.l_status)

        self.horizontalSpacer_11 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_11)


        self.verticalLayout_2.addLayout(self.horizontalLayout_3)

        self.progressBar = QProgressBar(exportToDirDlg)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setMaximumSize(QSize(16777215, 10))
        self.progressBar.setValue(0)
        self.progressBar.setTextVisible(False)

        self.verticalLayout_2.addWidget(self.progressBar)

        self.f_buttonsMain = QVBoxLayout()
        self.f_buttonsMain.setObjectName(u"f_buttonsMain")
        self.f_buttonsSub = QHBoxLayout()
        self.f_buttonsSub.setObjectName(u"f_buttonsSub")
        self.but_explorer = QPushButton(exportToDirDlg)
        self.but_explorer.setObjectName(u"but_explorer")

        self.f_buttonsSub.addWidget(self.but_explorer)

        self.horizontalSpacer_13 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.f_buttonsSub.addItem(self.horizontalSpacer_13)

        self.but_execute = QPushButton(exportToDirDlg)
        self.but_execute.setObjectName(u"but_execute")

        self.f_buttonsSub.addWidget(self.but_execute)

        self.but_close = QPushButton(exportToDirDlg)
        self.but_close.setObjectName(u"but_close")

        self.f_buttonsSub.addWidget(self.but_close)


        self.f_buttonsMain.addLayout(self.f_buttonsSub)


        self.verticalLayout_2.addLayout(self.f_buttonsMain)


        self.retranslateUi(exportToDirDlg)
        self.rb_ProjectFolder.toggled.connect(self.cb_mediaFolders.setEnabled)
        self.rb_ProjectFolder.toggled.connect(self.l_radioProjectFolder.setEnabled)
        self.rb_customFolder.toggled.connect(self.but_customPathSearch.setEnabled)
        self.rb_customFolder.toggled.connect(self.e_customLoc.setEnabled)
        self.rb_customFolder.toggled.connect(self.l_radioCustomFolder.setEnabled)

        QMetaObject.connectSlotsByName(exportToDirDlg)
    # setupUi

    def retranslateUi(self, exportToDirDlg):
        exportToDirDlg.setWindowTitle(QCoreApplication.translate("exportToDirDlg", u"Dialog", None))
        self.l_mediaName.setText(QCoreApplication.translate("exportToDirDlg", u"Delivery Media Name:", None))
        self.but_nameReset.setText(QCoreApplication.translate("exportToDirDlg", u"Default", None))
        self.rb_singleImage.setText(QCoreApplication.translate("exportToDirDlg", u"Single Image", None))
        self.rb_imageSeq.setText(QCoreApplication.translate("exportToDirDlg", u"Image Sequence", None))
        self.l_DeliveryFolder.setText(QCoreApplication.translate("exportToDirDlg", u"Delivery Folder:", None))
        self.rb_ProjectFolder.setText("")
        self.l_radioProjectFolder.setText(QCoreApplication.translate("exportToDirDlg", u"Project Folders", None))
        self.rb_customFolder.setText("")
        self.l_radioCustomFolder.setText(QCoreApplication.translate("exportToDirDlg", u"Custom Folder:", None))
        self.but_customPathSearch.setText(QCoreApplication.translate("exportToDirDlg", u"...", None))
        self.l_appendFolder.setText(QCoreApplication.translate("exportToDirDlg", u"Append Folder (optional):  ", None))
        self.e_appendFolder.setPlaceholderText(QCoreApplication.translate("exportToDirDlg", u"None", None))
        self.l_outputName.setText(QCoreApplication.translate("exportToDirDlg", u"Output:", None))
        self.chb_zipFile.setText(QCoreApplication.translate("exportToDirDlg", u"Create Zip File", None))
        self.l_status.setText(QCoreApplication.translate("exportToDirDlg", u"TextLabel", None))
        self.but_explorer.setText(QCoreApplication.translate("exportToDirDlg", u"Open in Explorer", None))
        self.but_execute.setText(QCoreApplication.translate("exportToDirDlg", u"Execute", None))
        self.but_close.setText(QCoreApplication.translate("exportToDirDlg", u"Close", None))
    # retranslateUi

