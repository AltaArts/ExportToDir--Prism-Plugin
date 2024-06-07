# -*- coding: utf-8 -*-
#
####################################################
#
# PRISM - Pipeline for animation and VFX projects
#
# www.prism-pipeline.com
#
# contact: contact@prism-pipeline.com
#
####################################################
#
#
# Copyright (C) 2016-2021 Richard Frangenberg
#
# Licensed under GNU LGPL-3.0-or-later
#
# This file is part of Prism.
#
# Prism is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Prism is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Prism.  If not, see <https://www.gnu.org/licenses/>.
####################################################
#
#           ExportToDir Plugin for Prism2
#
#                 Joshua Breckeen
#                    Alta Arts
#                josh@alta-arts.com
#
####################################################


import os
import shutil
import re
import subprocess
import threading
import zipfile
import tempfile
import json
import ntpath
import logging
from datetime import datetime

from qtpy.QtCore import *
from qtpy.QtGui import *
from qtpy.QtWidgets import *

from PrismUtils.Decorators import err_catcher_plugin as err_catcher

#   Prism Core logger
logger = logging.getLogger(__name__)

from ExportToDir import ExportToDir

#   Colors for Progress Bar
PROG_GREEN = "QProgressBar::chunk { background-color: rgb(0, 150, 0); }"
PROG_BLUE = "QProgressBar::chunk { background-color: rgb(0, 131, 195); }"
PROG_RED = "QProgressBar::chunk { background-color: rgb(225, 0, 0); }"


class Prism_ExportToDir_Functions(object):
    def __init__(self, core, plugin):
        self.core = core
        self.plugin = plugin

        self.loadedPlugins = []
        self.singleFileMode = True

        #   Global Settings File Data
        pluginLocation = os.path.dirname(os.path.dirname(__file__))
        self.settingsFile = os.path.join(pluginLocation, "ExportToDir_Config.json")

        self.loadSettings()

        #   Callbacks      
        self.core.registerCallback("projectWidgetGetContextMenu", self.projectWidgetGetContextMenu, plugin=self)      
        self.core.registerCallback("openPBAssetContextMenu", self.openPBAssetContextMenu, plugin=self)   
        self.core.registerCallback("openPBShotContextMenu", self.openPBShotContextMenu, plugin=self)   
        self.core.registerCallback("openPBFileContextMenu", self.openPBFileContextMenu, plugin=self)   
        self.core.registerCallback("productSelectorContextMenuRequested", self.productSelectorContextMenuRequested, plugin=self)        
        self.core.registerCallback("mediaPlayerContextMenuRequested", self.mediaPlayerContextMenuRequested, plugin=self)        
        self.core.registerCallback("textureLibraryTextureContextMenuRequested", self.textureLibraryTextureContextMenuRequested, plugin=self)
        self.core.registerCallback("userSettings_loadUI", self.userSettings_loadUI, plugin=self)
        self.core.registerCallback("onUserSettingsSave", self.onUserSettingsSave, plugin=self)


    # if returns true, the plugin will be loaded by Prism
    @err_catcher(name=__name__)
    def isActive(self):
        return True
    
    #   Called with Callback - User Settings
    @err_catcher(name=__name__)
    def onUserSettingsSave(self, origin):

        self.saveSettings(mode="Settings")
        

    # #   Called with Callback - Project Widget
    @err_catcher(name=__name__)
    def projectWidgetGetContextMenu(self, origin, menu):

        self.menuContext = "Project Files:"
        self.singleFileMode = False
        fileData = {}

        try:
            logger.debug("Loading Project Data")

            pdata = origin.data
            fileData["project_name"] = pdata["name"]
            fileData["filename"] = pdata["name"]
            fileData["sourcePath"] = os.path.dirname(os.path.dirname(pdata["configPath"]))
            fileData["user"] = self.core.user

        except Exception as e:
            msg = f"Error accessing Project Data {str(e)}"
            self.core.popup(msg)
            logger.warning(f"ERROR: Cannot access Project Data: {msg}")

        #   Sends File Info to get sorted
        self.sortData(fileData)

        #   Adds Right Click Item
        if os.path.exists(fileData["sourcePath"]):
            exportToAct = QAction("Export to Dir...", menu)
            exportToAct.triggered.connect(lambda: self.exportToDialogue())
            menu.addAction(exportToAct)


    #   Called with Callback - Asset Browser
    @err_catcher(name=__name__)
    def openPBShotContextMenu(self, origin, rcmenu, pos):

        if origin.entityType == "shot":
            try:
                cItem = origin.tw_tree.itemFromIndex(pos)
                if cItem is None:
                    return
            except:
                return
            
        self.menuContext = "Shot Files:"
        self.singleFileMode = False
        fileData = {}

        #   Retrieves Asset Info
        try:
            logger.debug("Loading Shot Data")

            shotData = cItem.data(0, Qt.UserRole)
            sequence = shotData["sequence"]
            shot = shotData["shot"]
            shotPath = shotData["paths"][0]["path"]

            fileData["filename"] = f"{sequence}--{shot}"
            fileData["sourcePath"] = shotPath
            fileData["sequence"] = sequence
            fileData["shot"] = shot
            fileData["sourceFilename"] = shot
            fileData["user"] = self.core.user

        except Exception as e:
            msg = f"Error accessing Shot Data {str(e)}"
            self.core.popup(msg)
            logger.warning(f"ERROR: Cannot access Shot Data: {msg}")

        #   Retrieves File Info from Project Config
        try:
            logger.debug("Loading Project Data")
            pData = self.core.getConfig(config="project", dft=3)        
            fileData["project_name"] = pData["globals"]["project_name"]

        except Exception as e:
            msg = f"Error opening Config File {str(e)}"
            self.core.popup(msg)
            logger.warning(f"ERROR: Cannot load Project Data: {msg}")

        #   Sends File Info to get sorted
        self.sortData(fileData)

        #   Adds Right Click Item
        if os.path.exists(fileData["sourcePath"]):
            exportToAct = QAction("Export to Dir...", rcmenu)
            exportToAct.triggered.connect(lambda: self.exportToDialogue())
            rcmenu.addAction(exportToAct)


    #   Called with Callback - Asset Browser
    @err_catcher(name=__name__)
    def openPBAssetContextMenu(self, origin, rcmenu, pos):

        if origin.entityType == "asset":
            try:
                cItem = origin.tw_tree.itemFromIndex(pos)
                if cItem is None:
                    return
            except:
                return

        self.menuContext = "Asset Files:"
        self.singleFileMode = False
        fileData = {}

        #   Retrieves Asset Info
        try:
            logger.debug("Loading Asset Data")
            assetData = cItem.data(0, Qt.UserRole)
            fileData["filename"] = assetData["asset"]
            fileData["sourcePath"] = assetData["paths"][0]
            fileData["asset"] = assetData["asset"]
            fileData["sourceFilename"] = assetData["asset"]
            fileData["user"] = self.core.user

        except Exception as e:
            msg = f"Error accessing Asset Data {str(e)}"
            self.core.popup(msg)
            logger.warning(f"ERROR: Cannot access Asset Data: {msg}")

        #   Retrieves File Info from Project Config
        try:
            logger.debug("Loading Project Data")
            pData = self.core.getConfig(config="project", dft=3)        
            fileData["project_name"] = pData["globals"]["project_name"]

        except Exception as e:
            msg = f"Error opening Config File {str(e)}"
            self.core.popup(msg)
            logger.warning(f"ERROR: Cannot load Project Data: {msg}")

        #   Sends File Info to get sorted
        self.sortData(fileData)

        #   Adds Right Click Item
        if os.path.exists(fileData["sourcePath"]):
            exportToAct = QAction("Export to Dir...", rcmenu)
            exportToAct.triggered.connect(lambda: self.exportToDialogue())
            rcmenu.addAction(exportToAct)


    #   Called with Callback - SceneFiles Browser
    @err_catcher(name=__name__)
    def openPBFileContextMenu(self, origin, rcmenu, filePath):
        self.menuContext = "Scene Files:"
        self.singleFileMode = True
        fileData = None

        #   Retrieves File Info from Core
        try:
            logger.debug("Loading Scene Data")
            fileData = self.core.getScenefileData(filePath)
            fileData["sourceDir"], fileData["sourceFilename"] = ntpath.split(fileData["filename"])
            fileData["sourcePath"] = fileData["filename"]

        except Exception as e:
            msg = f"Error opening Config File {str(e)}"
            self.core.popup(msg)
            logger.warning(f"ERROR: Cannot load Scene Data: {msg}")

        #   Retrieves File Info from Project Config
        try:
            logger.debug("Loading Project Data")
            pData = self.core.getConfig(config="project", dft=3)        
            fileData["project_name"] = pData["globals"]["project_name"]

        except Exception as e:
            msg = f"Error opening Config File {str(e)}"
            self.core.popup(msg)
            logger.warning(f"ERROR: Cannot load Project Data: {msg}")

        #   Sends File Info to get sorted
        self.sortData(fileData)

        #   Adds Right Click Item
        if os.path.isfile(fileData["filename"]):
            exportToAct = QAction("Export to Dir...", rcmenu)
            exportToAct.triggered.connect(lambda: self.exportToDialogue())
            rcmenu.addAction(exportToAct)


    #   Called with Callback - Product Browser
    @err_catcher(name=__name__)
    def productSelectorContextMenuRequested(self, origin, viewUi, pos, rcmenu):
        #   Checks to ensure that the selected item is a version
        version = origin.getCurrentVersion()
        if not version:
            return
        if viewUi != origin.tw_versions:
            return
        
        self.menuContext = "Product Files:"
        self.singleFileMode = True
        fileData = None

        try:
            logger.debug("Loading Product Data")
            #   Gets Source Path from Last Column
            row = viewUi.rowAt(pos.y())
            numCols = viewUi.columnCount()
            if row >= 0:
                sourcePath = viewUi.item(row, numCols - 1).text()

            #   Retrieves File Info        
            infoFolder = self.core.products.getVersionInfoPathFromProductFilepath(sourcePath)
            infoPath = self.core.getVersioninfoPath(infoFolder)
            fileData = self.core.getConfig(configPath=infoPath)

            fileData["project_name"] = self.core.projectName
            fileData["sourcePath"] = sourcePath
            fileData["sourceDir"], fileData["sourceFilename"] = ntpath.split(sourcePath)
            fileData["extension"] = os.path.splitext(fileData["sourceFilename"])[1]

        except Exception as e:
            msg = f"Error opening Config File {str(e)}"
            self.core.popup(msg)
            logger.warning(f"ERROR: Failed to Load Product Data: {msg}")
            return
        
        #   Sends File Info to get sorted
        self.sortData(fileData)

        #   Adds Right Click Item
        if os.path.exists(sourcePath):
            exportToAct = QAction("Export to Dir...", viewUi)
            exportToAct.triggered.connect(lambda: self.exportToDialogue())
            rcmenu.addAction(exportToAct)
        

    #   Called with Callback - Media Browser
    @err_catcher(name=__name__)
    def mediaPlayerContextMenuRequested(self, origin, menu):
        #   Checks to make sure right-click was on Media Browser
        if not type(origin.origin).__name__ == "MediaBrowser":
            return

        version = origin.origin.getCurrentVersion()
        if not version:
            return 

        self.menuContext = "Media Files:"
        fileData = None

        if not origin.seq:
            return

        try:
            logger.debug("Loading Media Data")
            #   Retrieves some File Data
            rawData = origin.getSelectedContexts()
            if rawData and isinstance(rawData[0], dict):
                fileData = rawData[0]
            else:
                fileData = {}

            fileData["sourceDir"] = fileData["path"]
            fileData["extension"] = os.path.splitext(fileData["source"])[1]

        except Exception as e:
            msg = f"Error Getting File Context Info {str(e)}"
            self.core.popup(msg)
            logger.warning(f"ERROR: Cannot Load Media Data: {e}")

        #   If the item is a single file
        if len(origin.seq) < 2:
            self.singleFileMode = True
            fileData["sourcePath"] = origin.seq[0]
            fileData["sourceFilename"] = os.path.basename(origin.seq[0])

        #   If the item is an Image Sequence
        elif len(origin.seq) > 1:
            self.singleFileMode = False
            fileData["currentFrame"] = os.path.basename(origin.seq[origin.getCurrentFrame()])
            filenameNoExt = os.path.splitext(fileData["currentFrame"])[0]
            fileData["frameNumber"] = os.path.splitext(filenameNoExt)[1]
            fileData["sourceFilename"] = fileData["source"]

            fileList = []
            for file in origin.seq:
                fileList.append(file)
            fileData["sourcePath"] = fileList

        self.sortData(fileData)

        exportToAct = QAction("Export to Dir...", self.core.pb.mediaBrowser)
        exportToAct.triggered.connect(lambda: self.exportToDialogue())
        menu.addAction(exportToAct)


    #   Called with Callback - Library Browser
    @err_catcher(name=__name__)                                             #   TODO Handle Tex Groups
    def textureLibraryTextureContextMenuRequested(self, origin, menu):

        if not type(origin).__name__ == "TextureWidget":
            return
        
        self.menuContext = "Library Files:"
        self.singleFileMode = True

        logger.debug("Loading Library Data")

        try:                                                            #   TODO    Still want to get more Details
            sourcePath = origin.path
            sourceDir = os.path.dirname(sourcePath)
            sourceBasename = os.path.basename(sourcePath)
            sourceFilename, sourceExt = os.path.splitext(sourceBasename)

            fileData = {}

            pData = self.core.getConfig(config="project", dft=3)        
            fileData["project_name"] = pData["globals"]["project_name"]

            fileData["sourcePath"] = sourcePath
            fileData["sourceDir"] = sourceDir
            fileData["sourceFilename"] = sourceFilename
            fileData["extension"] = sourceExt
            fileData["user"] = self.core.user

        except Exception as e:
            msg = f"Error opening Config File {str(e)}"
            self.core.popup(msg)
            logger.warning(f"ERROR: {msg}")

        self.sortData(fileData)        
            
        if os.path.isfile(fileData["sourcePath"]):
            exportToAct = QAction("Export to Dir...", self.core.pb.mediaBrowser)
            exportToAct.triggered.connect(lambda: self.exportToDialogue())
            menu.addAction(exportToAct)


    #   Called with Callback
    @err_catcher(name=__name__)                                                         #   TODO MAKE TEMPLATE ERROR CEHCKING
    def userSettings_loadUI(self, origin):  # ADDING "Export to Dir" TO SETTINGS

        logger.debug("Loading ExportToDir Menu")

        self.getLoadedPlugins()

        # Create a Widget
        origin.w_exportTo = QWidget()
        origin.lo_exportTo = QVBoxLayout(origin.w_exportTo)

        # Add a new box for "File Naming Template" before "Export to Dir"
        gb_fileNamingTemplate = QGroupBox("File Naming Template                         (templates used to build Export name)")
        lo_fileNamingTemplate = QVBoxLayout()

        #   Template for Tooltips
        templates = {
            "@PROJECT@": ["Project", "Asset", "Shot", "Scene", "Product", "Media", "Library"],
            "@USER@": ["Project", "Asset", "Shot", "Scene", "Product", "Media", "Library"],
            "@DATE@": ["Project", "Asset", "Shot", "Scene", "Product", "Media", "Library"],
            "@TYPE@": ["Scene", "Product", "Media"],
            "@SEQUENCE@": ["Shot", "Scene", "Product", "Media"],
            "@SHOT@": ["Shot", "Scene", "Product", "Media"],
            "@ASSET@": ["Asset", "Scene", "Product", "Media"],
            "@DEPARTMENT@": ["Scene", "Product", "Media"],
            "@TASK@": ["Scene", "Product", "Media"],
            "@FILENAME@": ["Asset", "Shot", "Scene", "Product", "Media", "Library"],
            "@VERSION@": ["Scene", "Product", "Media"],
            "@FILETYPE@": ["Scene", "Product", "Media"],
            "@EXTENSION@": ["Scene", "Product", "Media", "Library"],
            "@PRODUCT@": ["Product"],
            "@AOV@": ["Media"],
            "@CHANNEL@": ["Media"],
            "@IDENTIFIER@": ["Media"]
            }

        # Add Text Boxes
        self.l_naming_ProjectFiles = QLabel("Project Files:")
        self.e_naming_ProjectFiles = QLineEdit()
        projectFileTip = self.getToolTipItems(templates, "Project")
        self.e_naming_ProjectFiles.setToolTip(projectFileTip)

        self.l_naming_AssetFiles = QLabel("Asset Files:")
        self.e_naming_AssetFiles = QLineEdit()
        assetFileTip = self.getToolTipItems(templates, "Asset")
        self.e_naming_AssetFiles.setToolTip(assetFileTip)

        self.l_naming_ShotFiles = QLabel("Shot Files:")
        self.e_naming_ShotFiles = QLineEdit()
        shotFileTip = self.getToolTipItems(templates, "Shot")
        self.e_naming_ShotFiles.setToolTip(shotFileTip)

        self.l_naming_SceneFiles = QLabel("Scene Files:")
        self.e_naming_SceneFiles = QLineEdit()
        sceneFileTip = self.getToolTipItems(templates, "Scene")
        self.e_naming_SceneFiles.setToolTip(sceneFileTip)

        self.l_naming_ProductFiles = QLabel("Product Files:")
        self.e_naming_ProductFiles = QLineEdit()
        productFileTip = self.getToolTipItems(templates, "Product")
        self.e_naming_ProductFiles.setToolTip(productFileTip)

        self.l_naming_MediaFiles = QLabel("Media Files:")
        self.e_naming_MediaFiles = QLineEdit()
        mediaFileTip = self.getToolTipItems(templates, "Media")
        self.e_naming_MediaFiles.setToolTip(mediaFileTip)        

        self.l_naming_LibraryFiles = QLabel("Library Files:")
        self.e_naming_LibraryFiles = QLineEdit()
        libraryFileTip = self.getToolTipItems(templates, "Library")
        self.e_naming_LibraryFiles.setToolTip(libraryFileTip)        

        # Add a grid layout
        lo_fileNamingTemplate = QGridLayout()

        # Add each QLabel and QLineEdit to the layout with the same starting position
        lo_fileNamingTemplate.addWidget(self.l_naming_ProjectFiles, 0, 0)
        lo_fileNamingTemplate.addWidget(self.e_naming_ProjectFiles, 0, 1)        

        lo_fileNamingTemplate.addWidget(self.l_naming_AssetFiles, 1, 0)
        lo_fileNamingTemplate.addWidget(self.e_naming_AssetFiles, 1, 1)

        lo_fileNamingTemplate.addWidget(self.l_naming_ShotFiles, 2, 0)
        lo_fileNamingTemplate.addWidget(self.e_naming_ShotFiles, 2, 1)

        lo_fileNamingTemplate.addWidget(self.l_naming_SceneFiles, 3, 0)
        lo_fileNamingTemplate.addWidget(self.e_naming_SceneFiles, 3, 1)

        lo_fileNamingTemplate.addWidget(self.l_naming_ProductFiles, 4, 0)
        lo_fileNamingTemplate.addWidget(self.e_naming_ProductFiles, 4, 1)

        lo_fileNamingTemplate.addWidget(self.l_naming_MediaFiles, 5, 0)
        lo_fileNamingTemplate.addWidget(self.e_naming_MediaFiles, 5, 1)

        if "Libraries" in self.loadedPlugins:
            lo_fileNamingTemplate.addWidget(self.l_naming_LibraryFiles, 6, 0)
            lo_fileNamingTemplate.addWidget(self.e_naming_LibraryFiles, 6, 1)

        # Set column stretch to make sure line edits are aligned
        lo_fileNamingTemplate.setColumnStretch(1, 1)

        gb_fileNamingTemplate.setLayout(lo_fileNamingTemplate)

        # Add the "File Naming Template" box before the "Export to Dir" group box
        origin.lo_exportTo.addWidget(gb_fileNamingTemplate)
        spacer = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)
        origin.lo_exportTo.addItem(spacer)

        # Add the "Export to Dir" group box
        gb_exportTo = QGroupBox("User Export to Dir Locations")
        lo_exportTo = QVBoxLayout()
        gb_exportTo.setLayout(lo_exportTo)

        headerLabels = ["Name", "Path"]
        self.tw_exportTo = QTableWidget()
        self.tw_exportTo.setColumnCount(len(headerLabels))
        self.tw_exportTo.setHorizontalHeaderLabels(headerLabels)
        self.tw_exportTo.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.tw_exportTo.horizontalHeader().setDefaultAlignment(Qt.AlignLeft)

        # Configure table options
        self.tw_exportTo.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.tw_exportTo.setSelectionBehavior(QTableWidget.SelectRows)
        self.tw_exportTo.setSelectionMode(QTableWidget.SingleSelection)

        # Adds Buttons
        w_exportTo = QWidget()
        lo_exportToButtons = QHBoxLayout()

        b_moveItemUp = QPushButton("Move Up")
        b_moveItemDn = QPushButton("Move Down")
        b_addoexportTo = QPushButton("Add...")
        b_removeoexportTo = QPushButton("Remove")

        w_exportTo.setLayout(lo_exportToButtons)
        lo_exportToButtons.addWidget(b_moveItemUp)
        lo_exportToButtons.addWidget(b_moveItemDn)
        # Add stretch to separate the buttons
        lo_exportToButtons.addStretch()
        lo_exportToButtons.addWidget(b_addoexportTo)
        lo_exportToButtons.addWidget(b_removeoexportTo)

        lo_exportTo.addWidget(self.tw_exportTo)
        lo_exportTo.addWidget(w_exportTo)
        origin.lo_exportTo.addWidget(gb_exportTo)

        # Sets Columns
        self.tw_exportTo.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))
        # Makes ReadOnly
        self.tw_exportTo.setEditTriggers(QAbstractItemView.NoEditTriggers)

        # Executes button actions
        b_moveItemUp.clicked.connect(lambda: self.moveItemUp())
        b_moveItemDn.clicked.connect(lambda: self.moveItemDn())
        b_addoexportTo.clicked.connect(lambda: self.addExportToDir(origin, self.tw_exportTo))
        b_removeoexportTo.clicked.connect(lambda: self.removeExportToDir(origin, self.tw_exportTo))

        # Populates lists from Settings File Data
        namingTemplateData = self.nameTemplateData

        self.e_naming_ProjectFiles.setText(namingTemplateData.get("Project Files:", ""))

        self.e_naming_AssetFiles.setText(namingTemplateData.get("Asset Files:", ""))
        self.e_naming_ShotFiles.setText(namingTemplateData.get("Shot Files:", ""))
        self.e_naming_SceneFiles.setText(namingTemplateData.get("Scene Files:", ""))
        self.e_naming_ProductFiles.setText(namingTemplateData.get("Product Files:", ""))
        self.e_naming_MediaFiles.setText(namingTemplateData.get("Media Files:", ""))
        self.e_naming_LibraryFiles.setText(namingTemplateData.get("Library Files:", ""))

        for item in self.exportPaths:
            row_position = self.tw_exportTo.rowCount()
            self.tw_exportTo.insertRow(row_position)
            self.tw_exportTo.setItem(row_position, 0, QTableWidgetItem(item.get("Name", "")))
            self.tw_exportTo.setItem(row_position, 1, QTableWidgetItem(item.get("Path", "")))

        #   Tooltips
        tip = ("Directories that will be available in ExportToDir in addition to Project Locations.\n\n"
               "Short Name will be displayed in the right-click menu."
                )
        self.tw_exportTo.setToolTip(tip)

        tip = "Move selected item up in list."
        b_moveItemUp.setToolTip(tip)

        tip = "Move selected item down in list."
        b_moveItemDn.setToolTip(tip)

        tip = "Opens dialogue to add directory to ExportToDir list dropdown."
        b_addoexportTo.setToolTip(tip)

        tip = ("Removes directory from ExportToDir list dropdown.\n\n"
               "Will not delete any files in the directory."
                )
        b_removeoexportTo.setToolTip(tip)

        # Initialize button states
        self.updateButtonStates(b_moveItemUp, b_moveItemDn, b_removeoexportTo)

        # Connect item selection changed signal to the method
        self.tw_exportTo.itemSelectionChanged.connect(lambda: self.updateButtonStates(b_moveItemUp, b_moveItemDn, b_removeoexportTo))

        # Add Tab to User Settings
        origin.addTab(origin.w_exportTo, "Export to Dir")


    #   Set Settings Tooltips
    @err_catcher(name=__name__)
    def getToolTipItems(self, template, textbox):
        #   Adds tooltip to each template box
        templateItems = "Available variables:\n\n"
        for key, value in template.items():
            if textbox in value:
                templateItems += key + "\n"
        
        logger.debug("Loading Template Items")

        return templateItems


    @err_catcher(name=__name__)
    def updateButtonStates(self, b_moveItemUp, b_moveItemDn, b_removeOpenWith):
        selectedItems = self.tw_exportTo.selectedItems()
        hasSelection = bool(selectedItems)
        
        b_moveItemUp.setEnabled(hasSelection)
        b_moveItemDn.setEnabled(hasSelection)
        b_removeOpenWith.setEnabled(hasSelection)


    @err_catcher(name=__name__)
    def moveItemUp(self):
        currentRow = self.tw_exportTo.currentRow()
        if currentRow > 0:
            self.tw_exportTo.insertRow(currentRow - 1)
            for column in range(self.tw_exportTo.columnCount()):
                item = self.tw_exportTo.takeItem(currentRow + 1, column)
                self.tw_exportTo.setItem(currentRow - 1, column, item)
            self.tw_exportTo.removeRow(currentRow + 1)
            self.tw_exportTo.setCurrentCell(currentRow - 1, 0)


    @err_catcher(name=__name__)
    def moveItemDn(self):
        currentRow = self.tw_exportTo.currentRow()
        if currentRow < self.tw_exportTo.rowCount() - 1:
            self.tw_exportTo.insertRow(currentRow + 2)
            for column in range(self.tw_exportTo.columnCount()):
                item = self.tw_exportTo.takeItem(currentRow, column)
                self.tw_exportTo.setItem(currentRow + 2, column, item)
            self.tw_exportTo.removeRow(currentRow)
            self.tw_exportTo.setCurrentCell(currentRow + 1, 0)


    #   Check Loaded Plugins
    @err_catcher(name=__name__)
    def getLoadedPlugins(self):

        pluginNames = ["Standalone",
                       "Libraries",
                       "USD"
                       ]
        
        for plugin in pluginNames:
            pluginName = self.core.plugins.getPlugin(plugin)
            if pluginName is not None:
                self.loadedPlugins.append(plugin)

        logger.debug("Getting Loaded Plugins")


    #   Receives File Data and Populates Variables
    @err_catcher(name=__name__)
    def sortData(self, fileData):
        try:
            if fileData == None:
                logger.debug("No File Data Found")

            self.projectName = ""
            self.userName = ""
            self.entityType = ""
            self.sequenceName = ""
            self.shotName = ""
            self.assetName = ""
            self.deptName = ""
            self.taskName = ""
            self.productName = ""
            self.identifier = ""
            self.version = ""
            self.aov = ""
            self.channel = ""
            self.sourcePath = ""            
            self.sourceFilename = ""
            self.currentFrame = None
            self.frameNumber = ""
            self.sourceExt = ""

            if "project_name" in fileData:
                self.projectName = fileData["project_name"]
            if "user" in fileData:
                self.userName = fileData["user"]                    
            if "type" in fileData:
                self.entityType = fileData["type"]                  
            if "sequence" in fileData:
                self.sequenceName = fileData["sequence"]
            if "shot" in fileData:
                self.shotName = fileData["shot"]
            if "asset" in fileData:
                self.assetName = fileData["asset"]
            if "department" in fileData:
                self.deptName = fileData["department"]
            if "task" in fileData:
                self.taskName = fileData["task"]
            if "product" in fileData:
                self.productName = fileData["product"]                
            if "identifier" in fileData:
                self.identifier = fileData["identifier"]
            if "version" in fileData:
                self.version = fileData["version"]                        
            if "aov" in fileData:
                self.aov = fileData["aov"]
            if "channel" in fileData:
                self.channel = fileData["channel"]                
            if "sourcePath" in fileData:
                self.sourcePath = fileData["sourcePath"]                     
            if "sourceDir" in fileData:
                self.sourceDir = fileData["sourceDir"]                
            if "sourceFilename" in fileData:
                self.sourceFilename = fileData["sourceFilename"]
            if "currentFrame" in fileData:
                self.currentFrame = fileData["currentFrame"]
            if "frameNumber" in fileData:
                self.frameNumber = fileData["frameNumber"]                
            if "extension" in fileData:
                self.sourceExt = fileData["extension"]

            curDate = datetime.now()
            self.dateStamp = curDate.strftime("%d%m%y")

        except Exception as e:
            msg = f"Error opening Config File {str(e)}"
            self.core.popup(msg)
            logger.warning(f"Error opening Config File {str(e)}")


    #   Load Settings from Global Settings File
    @err_catcher(name=__name__)
    def loadSettings(self):
        logger.debug("Loading Settings")

        try:
            with open(self.settingsFile, "r") as json_file:
                settingsData = json.load(json_file)

            self.nameTemplateData = settingsData["NamingTemplate"]
            self.exportPaths = settingsData["ExportPaths"]
            self.recents = settingsData["Recents"]

        except FileNotFoundError:
            logger.debug("Setting do not exist.  Creating new Settings Files.")
            # Create the settings file if it doesn't exist
            self.createSettings()
            self.loadSettings()
        
        except Exception as e:
            self.core.popup(f"ExportToDir Config file is corrupt.\n"
                            f"Will create new Config file.\n\n"
                            f"{e}"
                            )
            #   Removes Corrupt Settings File and creates new
            os.remove(self.settingsFile)
            self.createSettings()
            self.loadSettings()
            

    #   Saves Settings to Global Settings File
    @err_catcher(name=__name__)
    def createSettings(self):
        #   Simple Defaults
        namingTemplateData = {}
        exportPathsData = []
        recents = []
        NameTemplates = ["Project Files:",
                        "Asset Files:",
                        "Shot Files:",
                        "Scene Files:",
                        "Product Files:",
                        "Media Files:",
                        "Library Files:"
                        ]

        # Populates naming Template data from line edits
        for name in NameTemplates:
            namingTemplateData[name] = "@PROJECT@--@FILENAME@"
        
        namingTemplateData["Project Files:"] = "@PROJECT@--@USER@--@DATE@"
        namingTemplateData["Asset Files:"] = "@PROJECT@--@ASSET@--@USER@--@DATE@"
        namingTemplateData["Shot Files:"] = "@PROJECT@--@SEQUENCE@-@SHOT@--@DATE@"

        #   Makes the data list
        self.settingsData = {"NamingTemplate": namingTemplateData,
                            "ExportPaths": exportPathsData,
                            "Recents": recents}

        self.saveSettings()
        logger.debug("Created Settings File")
    

    #   Saves Settings to Global Settings File
    @err_catcher(name=__name__)
    def makeRecents(self):
        #   Gets current Recents data
        recentsList = self.recents

        #   Makes new Recent Items based on UI items
        currRecents = {}
        currRecents["ProjectName"] = self.core.projectName

        if self.dlg.rb_ProjectFolder.isChecked():
            currRecents["folderType"] = "Project"
        elif self.dlg.rb_customFolder.isChecked():
            currRecents["folderType"] = "Custom"

        currRecents["projectFolder"] = self.dlg.cb_mediaFolders.currentText()
        currRecents["customFolder"] = self.dlg.e_customLoc.text()
        currRecents["appendFolder"] = self.dlg.e_appendFolder.text()
        currRecents["useZip"] = self.dlg.chb_zipFile.isChecked()

        # Check if an item with the same "ProjectName" already exists and remove if exists
        for existingRecents in recentsList:
            if existingRecents["ProjectName"] == currRecents["ProjectName"]:
                recentsList.remove(existingRecents)
                break

        # If there are already five items, remove the oldest one
        if len(recentsList) >= 5:
            recentsList.pop(0)
        #   Add current Recent to bottom of list
        recentsList.append(currRecents)

        return recentsList
    

    @err_catcher(name=__name__)
    def getRecents(self):
        #   Gets active Project Name
        projectName = self.core.projectName

        #   Return item that matches current Project
        for recentsItem in self.recents:
            if recentsItem.get("ProjectName") == projectName:
                return recentsItem

        # Return None if no match is found
        return None


    #   Saves Settings to Global Settings File
    @err_catcher(name=__name__)
    def saveSettings(self, mode=None):
        #   Used from Prism User Settings Menu
        if mode == "Settings":
            namingTemplateData = {}
            exportPathsData = []
            NameTemplates = ["ProjectFiles",
                            "AssetFiles",
                            "ShotFiles",
                            "SceneFiles",
                            "ProductFiles",
                            "MediaFiles",
                            "LibraryFiles"]

            # Populates naming Template data from line edits
            for name in NameTemplates:
                label = getattr(self, f"l_naming_{name}")
                line_edit = getattr(self, f"e_naming_{name}")

                labelText = label.text()
                contents = line_edit.text()
                namingTemplateData[labelText] = contents

            # Populates export paths data from UI List
            for row in range(self.tw_exportTo.rowCount()):
                nameItem = self.tw_exportTo.item(row, 0)
                pathItem = self.tw_exportTo.item(row, 1)

                if nameItem and pathItem:
                    name = nameItem.text()
                    location = pathItem.text()
                    exportPathsData.append({"Name": name, "Path": location})

            #   Updates current with new
            self.nameTemplateData = namingTemplateData        
            self.exportPaths = exportPathsData

            #   Builds dict but does not update recents list
            self.settingsData = {"NamingTemplate": namingTemplateData,
                                "ExportPaths": exportPathsData,
                                "Recents": self.recents}

        #   Used from Export Dialogue when executing
        elif mode == "Recents":
            #   Sets recents
            self.recents = self.makeRecents()

            #   Builds dict and only updates recent list
            self.settingsData = {"NamingTemplate": self.nameTemplateData,
                                "ExportPaths": self.exportPaths,
                                "Recents": self.recents}

        # Save to file
        with open(self.settingsFile, "w") as json_file:
            json.dump(self.settingsData, json_file, indent=4)

        logger.debug("Settings Saved")


    #   Adds Dir to ExportToDir User Settings GUI
    @err_catcher(name=__name__)
    def addExportToDir(self, origin, tw_exportTo):
        #   Calls Custon Dialog
        dialog = AddDirDialog(origin)

        #   Adds Name and Path to UI List
        if dialog.exec_() == QDialog.Accepted:
            name, path = dialog.getValues()

            if name and path:
                row_position = tw_exportTo.rowCount()
                tw_exportTo.insertRow(row_position)
                tw_exportTo.setItem(row_position, 0, QTableWidgetItem(name))
                tw_exportTo.setItem(row_position, 1, QTableWidgetItem(path))

            logger.debug("Export Directory added.")
            #   Saves UI List to JSON file
            self.saveSettings(mode="Settings")


    #   Removes Dir to ExportToDir User Settings GUI
    @err_catcher(name=__name__)
    def removeExportToDir(self, origin, tw_exportTo):
        #   Removes row from table
        selectedRow = tw_exportTo.currentRow()
        if selectedRow != -1:
            tw_exportTo.removeRow(selectedRow)

            logger.debug("Removed Export Directory.")

            #   Saves UI List to JSON file
            self.saveSettings(mode="Settings")


    @err_catcher(name=__name__)
    def loadData(self):
        #   Loads default dir to Custom Dir
        try:
            pData = self.core.getConfig(config="project", dft=3)
            self.loadSaveDirs(pData)
            self.dlg.e_customLoc.setText(self.sourceDir)

            logger.debug("Loaded Project data.")

        except:
            logger.warning("ERROR: Failed to Load Project data.")


    @err_catcher(name=__name__)
    def loadSaveDirs(self, pData):
        logger.debug("Loading ExportTo Directories")

        projectPaths = set()
        self.saveDirs = []

        # Loads Dirs from Project Render Locations
        if pData["render_paths"]:
            renderLocs = pData["render_paths"]

            for locName, locPath in renderLocs.items():
                if locPath not in projectPaths:
                    projectPaths.add(locPath)
                    self.saveDirs.append({"Name": locName, "Path": locPath})

        # Loads Dirs from Project Export Locations
        if pData["export_paths"]:
            exportLocs = pData["export_paths"]

            for locName, locPath in exportLocs.items():
                if locPath not in projectPaths:
                    projectPaths.add(locPath)
                    self.saveDirs.append({"Name": locName, "Path": locPath})

        # Load Dirs from Export to Dir User Settings
        exportToList = self.exportPaths
        for item in exportToList:
            name = item.get("Name")
            path = item.get("Path")
            if path and path not in projectPaths:
                projectPaths.add(path)
                self.saveDirs.append({"Name": name, "Path": path})


    @err_catcher(name=__name__)
    def exportToDialogue(self):
        #   Creates Dialogue Instance
        self.dlg = ExportToDir()

        self.dlg.setWindowTitle("Export to Directory")

        #   Configures UI based on SingleImage
        self.dlg.rb_singleImage.hide()
        self.dlg.rb_imageSeq.hide()
        self.dlg.rb_singleImage.setChecked(True)

        #   Loads Settings Data
        self.loadData()

        #   Retrieves Locations list
        formattedDirList = self.getFormattedDirs()
        self.dlg.cb_mediaFolders.addItems(formattedDirList)
        #   Defaults to Project Folder
        self.dlg.rb_ProjectFolder.setChecked(True)

        #   Sets Placeholder name based on Template
        self.setPlaceholderName(load=True)
        #   Configures Single or Image Sequence
        self.setSequenceMode()

        #   Loads Project Recents if they exist
        recents = self.getRecents()
        if recents != None:
            if recents["folderType"] == "Project":
                self.dlg.rb_ProjectFolder.setChecked(True)
            elif recents["folderType"] == "Custom":
                self.dlg.rb_customFolder.setChecked(True)

            index = self.dlg.cb_mediaFolders.findText(recents["projectFolder"])
            if index != -1:
                self.dlg.cb_mediaFolders.setCurrentIndex(index)

            self.dlg.e_customLoc.setText(recents["customFolder"])
            self.dlg.e_appendFolder.setText(recents["appendFolder"])
            self.dlg.chb_zipFile.setChecked(recents["useZip"])

        #   Tooltips for Dialogue
        tip = "Filename for export.  Template used to create default can be modified in User Settings"
        self.dlg.l_mediaName.setToolTip(tip)
        self.dlg.e_mediaName.setToolTip(tip)
        tip = "Click to revert to template filename"
        self.dlg.but_nameReset.setToolTip(tip)
        tip = "Export single image from sequence"
        self.dlg.rb_singleImage.setToolTip(tip)
        tip = "Export complete image sequence"
        self.dlg.rb_imageSeq.setToolTip(tip)    
        tip = "Directories listed in Project Settings->Locations and User Settings->ExportToDir"
        self.dlg.rb_ProjectFolder.setToolTip(tip)
        self.dlg.l_radioProjectFolder.setToolTip(tip)
        self.dlg.cb_mediaFolders.setToolTip(tip)
        tip = "Custom Directory"
        self.dlg.rb_customFolder.setToolTip(tip)
        self.dlg.l_radioCustomFolder.setToolTip(tip)
        self.dlg.e_customLoc.setToolTip(tip)
        tip = "Sub directory that will be appended to the Dir selected above"
        self.dlg.l_appendFolder.setToolTip(tip)
        self.dlg.e_appendFolder.setToolTip(tip)          
        tip = "Select to .zip the export contents to a single file"
        self.dlg.chb_zipFile.setToolTip(tip)  
        tip = "Final output path of export"
        self.dlg.e_outputName.setToolTip(tip)  
        tip = "Open export directory"
        self.dlg.but_explorer.setToolTip(tip)  

        #   Connections
        self.dlg.e_mediaName.textEdited.connect(lambda: self.refreshOutputName())
        self.dlg.but_nameReset.clicked.connect(lambda: self.setPlaceholderName(load=True))
        self.dlg.butGroup_folder.buttonClicked.connect(lambda: self.refreshOutputName())
        self.dlg.butGroup_imageSeq.buttonClicked.connect(lambda: self.setSequenceMode())
        self.dlg.cb_mediaFolders.currentIndexChanged.connect(lambda: self.refreshOutputName())
        self.dlg.but_customPathSearch.clicked.connect(lambda: self.openExplorer(self.sourcePath, set=True))
        self.dlg.e_appendFolder.textEdited.connect(lambda: self.formatAppendFolder())
        self.dlg.chb_zipFile.clicked.connect(lambda: self.setSequenceMode())
        self.dlg.but_explorer.clicked.connect(lambda: self.openExplorer(self.outputPath))        
        self.dlg.but_execute.clicked.connect(lambda: self.execute())
        self.dlg.but_close.clicked.connect(self.dlg.reject)        

        self.refreshOutputName()
        self.dlg.exec_()
    

    @err_catcher(name=__name__)
    def getFormattedDirs(self):
        # Get the font of the combobox
        font = self.dlg.cb_mediaFolders.font()

        max_name_width = 0
        formattedFolders = []

        # Calculate the maximum width of the "Name" text items
        metrics = QFontMetrics(font)
        for entry in self.saveDirs:
            name_width = metrics.width(entry['Name'])
            max_name_width = max(max_name_width, name_width)

        # Format the items with individually calculated padding for "Path" text
        for entry in self.saveDirs:
            name_width = metrics.width(entry['Name'])
            padding_width = max_name_width - name_width
            half_padding = padding_width // 3  # Divide by 3 for even distribution
            padding = ' ' * half_padding
            formattedFolders.append(f"{entry['Name']}:{padding}      {os.path.normpath(entry['Path'])}")

        return formattedFolders


    @err_catcher(name=__name__)
    def setSequenceMode(self):    
        if self.menuContext == "Media Files:":
            if self.dlg.rb_singleImage.isChecked():
                self.singleFileMode = True
            else:
                self.singleFileMode = False

            if self.dlg.rb_imageSeq.isChecked() and not self.dlg.chb_zipFile.isChecked():
                self.dlg.e_mediaName.setReadOnly(True)
                self.dlg.e_mediaName.setStyleSheet("color: rgb(120, 120, 120);")
            else:
                self.dlg.e_mediaName.setReadOnly(False)
                self.dlg.e_mediaName.setStyleSheet("color: ;")

        self.setPlaceholderName()

        logger.debug(f"Sequence Mode changed to {not self.singleFileMode}")


    @err_catcher(name=__name__)
    def setPlaceholderName(self, load=False):
        if self.singleFileMode:
            #   Formats Filename
            if self.currentFrame:
                baseName = os.path.basename(self.currentFrame)
                fileNameNoExt = os.path.splitext(baseName)[0]
            else:
                fileNameNoExt = os.path.splitext(self.sourceFilename)[0]

        elif self.menuContext in ["Project Files:", "Asset Files:", "Shot Files:"]:
            fileNameNoExt = self.sourceFilename

        else:
            #   If image sequence detected will display the mode options
            self.dlg.rb_singleImage.show()
            self.dlg.rb_imageSeq.show()
            
            if self.dlg.rb_imageSeq.isChecked():
                fileNameNoExt = os.path.splitext(self.sourceFilename)[0]
            else:
                fileNameNoExt = os.path.splitext(self.currentFrame)[0]
            
        formattedNameNoExt = self.formatName(fileNameNoExt)
        formattedName = formattedNameNoExt + self.sourceExt

        #   Possible replacements
        replacements = {
            "@PROJECT@": self.projectName,
            "@USER@": self.userName,
            "@DATE@": self.dateStamp,
            "@TYPE@": self.entityType,
            "@SEQUENCE@": self.sequenceName,
            "@SHOT@": self.shotName,
            "@ASSET@": self.assetName,
            "@DEPARTMENT@": self.deptName,
            "@TASK@": self.taskName,
            "@PRODUCT@": self.productName,
            "@IDENTIFIER@": self.identifier,
            "@VERSION@": self.version,
            "@AOV@": self.aov,
            "@CHANNEL@": self.channel,
            "@FILENAME@": formattedName,
            "@FRAME@": self.frameNumber,
            "@FILETYPE@": self.sourceExt.removeprefix(".").upper(),
            "@EXTENSION@": self.sourceExt
            }

        # Perform replacements
        templateData = self.nameTemplateData
        template = templateData.get(self.menuContext)
       
        if template:    #   Check if template loaded from Settings File
            placeholderName = template  # Initialize with the original template
            for placeholder, value in replacements.items():
                placeholderName = placeholderName.replace(placeholder, value)
        else:
            placeholderName = formattedName     #   Fallback name

        self.dlg.e_mediaName.setText(placeholderName)

        if not load:
            self.refreshOutputName()


    def formatName(self, inputName):
        # Replace invalid characters with underscores
        validName = re.sub(r"[^a-zA-Z0-9_\- ()#.]", "_", inputName)

        # Check for reserved names for outputName
        reserved_names = set(['CON', 'PRN', 'AUX', 'NUL'] + [f'COM{i}' for i in range(1, 10)] + [f'LPT{i}' for i in range(1, 10)])
        if validName.upper() in reserved_names:
            self.core.popup("Name Not Allowed\n\nDo Not Use:\n\n   CON, PRN, AUX, NUL, COM, LPT")

        return validName


    @err_catcher(name=__name__)
    def formatAppendFolder(self):
        currentText = self.dlg.e_appendFolder.text()
        placeholderText = self.dlg.e_appendFolder.placeholderText()

        if currentText and currentText != placeholderText:
            # Check if the currentText needs a leading backslash
            if not currentText.startswith("\\"):
                currentText = "\\" + currentText

            # Call formatName without modifying e_appendFolder
            formatted_name = self.formatName(currentText[1:])

            # Check if formatted_name is not None before further processing
            if formatted_name is not None:
                # Update the e_appendFolder text with the formatted name
                self.dlg.e_appendFolder.setText("\\" + formatted_name)

            self.refreshOutputName()


    @err_catcher(name=__name__)                                     #   TODO RENAMING SEQ's
    def refreshOutputName(self):
        #   Get name form UI
        placeholderName = self.dlg.e_mediaName.text()
        root, extension = os.path.splitext(placeholderName)

        #   Check if name in UI has an extension
        if extension:
            fileNameNoExt = root
        else:
            fileNameNoExt = placeholderName                                             
        
        formatedName = self.formatName(fileNameNoExt)
        
        #   Change extension to .zip if checked
        if self.dlg.chb_zipFile.isChecked():
            if not self.singleFileMode:
                formatedName = formatedName.rstrip('#_.')
            formatedName = formatedName + ".zip"
        else:
            formatedName = fileNameNoExt + self.sourceExt

        #   User selected output folder type
        if self.dlg.rb_ProjectFolder.isChecked():
            pathItem = self.dlg.cb_mediaFolders.currentText()
            # Split the selected text into "Name" and "Path" based on the ":" delimiter
            name, path = map(str.strip, pathItem.split(":", 1))
            outputPath = path
        elif self.dlg.rb_customFolder.isChecked():
            outputPath = self.dlg.e_customLoc.text()

        #   Adds append folder if needed
        if self.dlg.e_appendFolder.text():
            appendFolder = self.dlg.e_appendFolder.text()

            if appendFolder.startswith("\\"):
                appendFolder = appendFolder[1:]

            AppendedOutputPath = os.path.normpath(os.path.join(outputPath, appendFolder))
            self.outputPath = os.path.normpath(os.path.join(AppendedOutputPath, formatedName))

        else:
            self.outputPath = os.path.join(outputPath, formatedName)

        self.dlg.e_outputName.setText(self.outputPath)

        self.resetProgBar()


    @err_catcher(name=__name__)
    def openExplorer(self, path, set=False):
         #   Sets location to open Dialogue to        
        if self.dlg.rb_ProjectFolder.isChecked():
            pathItem = self.dlg.cb_mediaFolders.currentText()
            # Split the selected text into "Name" and "Path" based on the ":" delimiter
            name, path = map(str.strip, pathItem.split(":", 1))
        elif self.dlg.rb_customFolder.isChecked():
            path = self.dlg.e_customLoc.text()
  
        path = path.replace("/", "\\")

        #   If set True then opens selectable Dialogue
        if set == True:
            customDir = QFileDialog.getExistingDirectory(None, "Select Save Directory", path)
            customDir = customDir.replace("/", "\\")
            self.dlg.e_customLoc.setText(customDir)

            logger.debug("Directory Selected")

        #   If set not True, then just opens File Explorer
        else:
            cmd = "explorer " + path
            subprocess.Popen(cmd)

        self.refreshOutputName()


    @err_catcher(name=__name__)
    def resetProgBar(self):
        #   Resets Prog Bar status and color
        self.dlg.l_status.setText("Idle...")
        self.dlg.progressBar.reset()
        self.dlg.progressBar.setStyleSheet(PROG_BLUE)


    @err_catcher(name=__name__)
    def execute(self):

        self.resetProgBar()

        #   Saves selected optiosn to recents list
        self.saveSettings(mode="Recents")

        #   Retrieves Name from UI
        outputName = self.dlg.e_mediaName.text()
        fileName, extension = os.path.splitext(outputName)
        if fileName == "":
            self.core.popup("The Output Filename is blank.  Please enter a Filename")
            return

        outputPath = self.dlg.e_outputName.text()

        #   Changes output to .zip if needed
        zipFiles = self.dlg.chb_zipFile.isChecked()
        if zipFiles:
            outputPath = os.path.splitext(outputPath)[0] + '.zip'

        # Copy a single file
        if self.singleFileMode:
            if self.menuContext == "Media Files:":
                if self.currentFrame:
                    sourcePath = os.path.join(self.sourceDir, self.currentFrame)
                else:
                    sourcePath = self.sourcePath
            else:
                sourcePath = self.sourcePath

            #   Checks if file already exists and then opens Dialogue
            if os.path.exists(outputPath):
                if self.executePopUp("File", outputPath) == False:
                    logger.debug(f"File already exists: {outputPath}")
                    return

            #   Makes Dir if it doesn't exist    
            outputDir = os.path.dirname(outputPath)
            if not os.path.exists(outputDir):
                os.mkdir(outputDir)

            copyThread = CopyThread(self.core, self.dlg, 1, sourcePath, outputPath, zipFiles)

        # Copy entire directory
        elif not self.singleFileMode and not zipFiles:
            if self.menuContext in ["Project Files:", "Asset Files:", "Shot Files:"]:
                sourceDir = self.sourcePath
                outputDir = outputPath

                #   Checks if Dir exists and then opens Dialogue
                if os.path.exists(outputDir):
                    if self.executePopUp("Directory", outputDir) == False:
                        return

                else:   #   Makes Dir if it doesn't exist
                    os.makedirs(outputDir)

                copyThread = CopyThread(self.core, self.dlg, 2, sourceDir, outputDir, zipFiles)

            else:    
                sourceDir = os.path.dirname(self.sourcePath[0])
                outputDir = os.path.dirname(outputPath)

                #   Checks if Dir exists and then opens Dialogue
                if os.path.exists(outputDir):
                    if self.executePopUp("Directory", outputDir) == False:
                        return
                    
                else:   #   Makes Dir if it doesn't exist
                    os.mkdir(outputDir)

                copyThread = CopyThread(self.core, self.dlg, 3, sourceDir, outputDir, zipFiles)

        # Copy and Zip directory
        else:
            if self.menuContext in ["Project Files:", "Asset Files:", "Shot Files:"]:
                sourceDir = self.sourcePath
                outputDir = os.path.dirname(outputPath)

                #   Checks if file already exists and then opens Dialogue
                if os.path.exists(outputPath):
                    if self.executePopUp("File", outputPath) == False:
                        return

                #   Makes Dir if it doesn't exist    
                if not os.path.exists(outputDir):
                    os.makedirs(outputDir)
                    
                copyThread = CopyThread(self.core, self.dlg, 4, sourceDir, outputPath, zipFiles)  

            else:
                sourceDir = os.path.dirname(self.sourcePath[0])
                outputDir = os.path.dirname(outputPath)

                #   Checks if file already exists and then opens Dialogue
                if os.path.exists(outputPath):
                    if self.executePopUp("File", outputPath) == False:
                        return
                    
                #   Makes Dir if it doesn't exist    
                if not os.path.exists(outputDir):
                    os.mkdir(outputDir)
                    
                copyThread = CopyThread(self.core, self.dlg, 5, sourceDir, outputPath, zipFiles)

        copyThread.progressUpdated.connect(self.dlg.progressBar.setValue)
        thread = threading.Thread(target=copyThread.run)
        thread.start()


    @err_catcher(name=__name__)
    def executePopUp(self, checkType, output):
        reply = QMessageBox.question(
            self.dlg,
            f"{checkType} Exists",
            f"The {checkType} already exists:\n\n"
            f"{output}\n\n"
            f"Do you want to overwrite it?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        return reply == QMessageBox.Yes
        


class CopyThread(QObject):
    progressUpdated = Signal(int)

    def __init__(self, core, dlg, case, sourcePath, outputPath, zipFiles=False):
        super().__init__()
        self.core = core
        self.dlg = dlg
        self.case = case
        self.sourcePath = sourcePath
        self.outputPath = outputPath
        self.zipFiles = zipFiles
   
    
    @err_catcher(name=__name__)
    def run(self):
        logger.info("Executing Export")
        try:
            originalPath = self.sourcePath
            self.tempDir = None

            #   Single File
            if self.case == 1:
                if self.zipFiles:
                    #   Changes extension to .zip if needed
                    filename = os.path.basename(originalPath)
                    zipFilename = os.path.splitext(filename)[0] + ".zip"

                    #   Zips file in tempDir made in the method
                    zipPath = self.executeZip(originalPath, zipFilename)
                    #   Copies to the file with progress
                    self.dlg.l_status.setText("Copying...")
                    self.copyFile(zipPath, self.outputPath)
                    #   Sets Prog Bar to finished
                    self.progressUpdated.emit(100)
                    self.dlg.l_status.setText("Complete.")
                    self.dlg.progressBar.setStyleSheet(PROG_GREEN)

                else:
                    outputPathWithExt = self.outputPath
                    #   Copies to the file with progress
                    self.dlg.l_status.setText("Copying...")
                    self.copyFile(originalPath, outputPathWithExt)
                    self.progressUpdated.emit(100)
                    self.dlg.l_status.setText("Complete.")
                    self.dlg.progressBar.setStyleSheet(PROG_GREEN)

            #   Complete Directory Tree
            elif self.case == 2:
                self.copyEntireDirectory(originalPath, self.outputPath)

            #   Single Directory without Zip
            elif self.case == 3:    
                self.copyDirectory(originalPath, self.outputPath)

            #   Complete Directory Tree with Zip
            elif self.case == 4:
                #   Changes extension to .zip
                zipFilename = f"{os.path.basename(self.outputPath)}.zip"
                #   Zips file in tempDir made in the method
                zipPath = self.executeZip(originalPath, zipFilename)
                #   Copies to the file with progress
                self.copyFile(zipPath, self.outputPath)

            #   Single Directory with Zip
            elif self.case == 5:
                #   Changes extension to .zip
                zipFilename = f"{os.path.basename(self.outputPath)}.zip"
                #   Zips file in tempDir made in the method
                zipPath = self.executeZip(originalPath, zipFilename)
                #   Copies to the file with progress
                self.copyFile(zipPath, self.outputPath)

            else:
                return
            
            #   Removes tempDir
            if self.tempDir:
                shutil.rmtree(self.tempDir)

        except Exception as e:
            self.dlg.l_status.setText("ERROR")
            self.dlg.progressBar.setStyleSheet(PROG_RED)
            self.progressUpdated.emit(100)
            self.core.popup(e)
            logger.warning(f"ERROR: Export Failed:  {e}")


    @err_catcher(name=__name__)
    def copyFile(self, src, dest, showProg=True):
        logger.debug(f"Copying: {src}")

        try:
            if showProg:
                self.progressUpdated.emit(0)
                self.dlg.l_status.setText("Copying...")

            if os.path.isdir(src):
                # If it's a directory, use copy2 to preserve metadata
                shutil.copy2(src, dest)
            elif os.path.isfile(src):
                # If it's a file, call self.copyFile
                totalSize = os.path.getsize(src)
                copiedSize = 0
                with open(src, 'rb') as srcFile, open(dest, 'wb') as destFile:
                    while True:
                        chunk = srcFile.read(4096)
                        if not chunk:
                            break
                        destFile.write(chunk)
                        copiedSize += len(chunk)
                        if showProg:
                            progressPercentage = int(copiedSize / totalSize * 100)
                            self.progressUpdated.emit(progressPercentage)
            else:
                logger.warning(f"Skipping unsupported item: {src}")

            if showProg:
                self.dlg.l_status.setText("Complete.")
                self.dlg.progressBar.setStyleSheet(PROG_GREEN)

            logger.debug(f"SUCCESS: Copied {src}")

        except Exception as e:
            self.dlg.l_status.setText("ERROR")
            self.dlg.progressBar.setStyleSheet(PROG_RED)
            self.progressUpdated.emit(100)
            self.core.popup(e)
            logger.warning(f"ERROR: Failed to copy: {e}")


    @err_catcher(name=__name__)
    def dirFileAmount(self, dirPath, mode="shallow"):
        #   Gets number of files in directory
        try:
            #   For only counting files in this dir
            if mode == "shallow":
                if os.path.isdir(dirPath):
                    entries = os.listdir(dirPath)
                    files = [entry for entry in entries if os.path.isfile(os.path.join(dirPath, entry))]
                    return len(files)
                else:
                    return 0
            #   For counting all files in dir and child dirs
            elif  mode == "deep":
                fileCount = 0
                for root, _, files in os.walk(dirPath):
                    fileCount += len(files)

                return fileCount
            
        except FileNotFoundError:
            return 0
        

    @err_catcher(name=__name__)
    def copyDirectory(self, src, dest):
        logger.debug("Copying Directory")
        try:
            self.dlg.l_status.setText("Copying...")
            #   Gets number of files in directory
            totalFiles = self.dirFileAmount(src)
            copiedFiles = 0
            #   Copies all files in dir with progress
            for root, _, files in os.walk(src):
                for file in files:
                    srcFile = os.path.join(root, file)
                    # Ensure it's a file and not in a subdirectory
                    if os.path.isfile(srcFile) and os.path.dirname(srcFile) == src:
                        destFile = os.path.join(dest, os.path.relpath(srcFile, src))

                        #   Calls copyFile for each file, but disables prog for each file
                        self.copyFile(srcFile, destFile, showProg=False)

                        copiedFiles += 1
                        progressPercentage = int(copiedFiles / totalFiles * 100)
                        self.progressUpdated.emit(progressPercentage)

            self.dlg.l_status.setText("Complete.")
            self.progressUpdated.emit(100)
            self.dlg.progressBar.setStyleSheet(PROG_GREEN)
            logger.debug(f"SUCCESS: Copied {src}")

        except Exception as e:
            self.dlg.l_status.setText("ERROR.")
            self.progressUpdated.emit(100)
            self.dlg.progressBar.setStyleSheet(PROG_RED)
            self.core.popup(e)  # TESTING
            logger.warning(f"ERROR: Copying failed for {src}")
            logger.warning(e)


    @err_catcher(name=__name__)
    def copyEntireDirectory(self, src, dest):
        logger.debug("Copying Directory")
        try:
            self.dlg.l_status.setText("Copying...")

            totalFiles = self.dirFileAmount(src, mode="deep")
            copiedFiles = 0

            # Iterate through all items in the source directory
            for root, dirs, files in os.walk(src):
                # Copy directories
                for dirName in dirs:
                    srcDir = os.path.join(root, dirName)
                    destDir = os.path.join(dest, os.path.relpath(srcDir, src))
                    os.makedirs(destDir, exist_ok=True)

                # Copy files
                for fileName in files:
                    srcFile = os.path.join(root, fileName)
                    destFile = os.path.join(dest, os.path.relpath(srcFile, src))
                    self.copyFile(srcFile, destFile, showProg=False)

                    copiedFiles += 1
                    progressPercentage = int(copiedFiles / totalFiles * 100)
                    self.progressUpdated.emit(progressPercentage)

            self.dlg.l_status.setText("Complete.")
            self.progressUpdated.emit(100)
            self.dlg.progressBar.setStyleSheet(PROG_GREEN)
            logger.debug(f"SUCCESS: Copied {src}")

        except Exception as e:
            self.dlg.l_status.setText("ERROR.")
            self.progressUpdated.emit(100)
            self.dlg.progressBar.setStyleSheet(PROG_RED)
            self.core.popup(e)
            logger.warning(f"ERROR: Copying failed for {src}")
            logger.warning(e)


    @err_catcher(name=__name__)
    def executeZip(self, originalPath, zipFilename):                        #   TODO  RENAME FILES
        zippedFiles = 0
        #   Makes tempDir
        self.tempDir = tempfile.mkdtemp(prefix="PrismTemp_")
        zipPath = os.path.join(self.tempDir, zipFilename)

        self.dlg.l_status.setText("Zipping...")
        logger.debug(f"Zipping {zipFilename}")

        try:
            with zipfile.ZipFile(zipPath, 'w', zipfile.ZIP_DEFLATED) as zipFile:
                if os.path.isdir(originalPath):
                    if self.case == 4:
                        #   Get number of files in dir and sub dirs
                        totalFiles = self.dirFileAmount(originalPath, mode="deep")

                        for root, dirs, files in os.walk(originalPath):
                            for fileName in files:
                                filePath = os.path.join(root, fileName)
                                arcname = os.path.relpath(filePath, originalPath)
                                zipFile.write(filePath, arcname=arcname)
                                zippedFiles += 1
                                progressPercentage = int(zippedFiles / totalFiles * 100)
                                self.progressUpdated.emit(progressPercentage)

                            # Explicitly add empty directories to the zip file
                            for dirName in dirs:
                                dirPath = os.path.join(root, dirName)
                                arcname = os.path.relpath(dirPath, originalPath)
                                zipFile.write(dirPath, arcname=arcname)

                    else:
                        #   Get number of files in directory
                        totalFiles = self.dirFileAmount(originalPath)

                        # Iterate over files directly in the specified directory
                        for file in os.listdir(originalPath):
                            filePath = os.path.join(originalPath, file)
                            # Ensure it's a file (not a directory)
                            if os.path.isfile(filePath):
                                arcname = os.path.relpath(filePath, originalPath)
                                zipFile.write(filePath, arcname=arcname)
                                zippedFiles += 1
                                progressPercentage = int(zippedFiles / totalFiles * 100)
                                self.progressUpdated.emit(progressPercentage)
                else:
                    self.progressUpdated.emit(20)

                    arcname = os.path.basename(originalPath)
                    zipFile.write(originalPath, arcname=arcname)

                    self.progressUpdated.emit(75)
                    logger.debug(f"SUCCESS: Zipped {zipFilename}")

            return zipPath
    
        except Exception as e:
            self.dlg.l_status.setText("ERROR.")
            self.progressUpdated.emit(100)
            self.dlg.progressBar.setStyleSheet(PROG_RED)
            self.core.popup(e)  # TESTING
            logger.warning(f"ERROR: Failed to Zip {zipFilename}")


class AddDirDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        #   Sets up Custon File Selection UI
        self.setWindowTitle("Add Export to Dir Location")

        self.l_name = QLabel("Short Name:")
        self.le_name = QLineEdit()
        tip = "Name displayed in right-click menu."
        self.l_name.setToolTip(tip)
        self.le_name.setToolTip(tip)

        self.l_location = QLabel("Location:")
        self.but_location = QPushButton("Select Location")
        tip = "Opens dialogue to select path to directory."
        self.l_location.setToolTip(tip)
        self.but_location.setToolTip(tip)
        self.but_location.clicked.connect(lambda: self.selectLocation(self))

        self.but_ok = QPushButton("OK")
        self.but_ok.clicked.connect(self.accept)

        layout = QVBoxLayout()
        layout.addWidget(self.l_name)
        layout.addWidget(self.le_name)
        layout.addWidget(self.l_location)
        layout.addWidget(self.but_location)
        layout.addWidget(self.but_ok)

        self.setLayout(layout)
        self.setFixedWidth(300)


    def selectLocation(self, origin):
        #   Calls native File Dialog
        windowTitle = "Select Export to Dir Location"
        directory = QFileDialog.getExistingDirectory(origin, windowTitle, QDir.homePath())

        if directory:
            self.l_location.setText(directory)


    def getValues(self):
        name = self.le_name.text()
        location = self.l_location.text()
        return name, location


