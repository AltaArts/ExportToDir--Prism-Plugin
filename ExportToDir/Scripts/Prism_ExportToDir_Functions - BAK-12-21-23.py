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
# Plugin author: Elise Vidal
# Contact: evidal@artfx.fr
# Beta Testeur: Simon 'ca marche pas' Tarsiguel

try:
    from PySide2.QtCore import *
    from PySide2.QtGui import *
    from PySide2.QtWidgets import *
    from PySide2.QtCore import QObject, Signal

except:
    from PySide.QtCore import *
    from PySide.QtGui import *

from PrismUtils.Decorators import err_catcher_plugin as err_catcher

import os                                           #   CLEANUP     TODO
from distutils.dir_util import copy_tree
import shutil
import datetime
import re
import subprocess
import threading
import zipfile
import tempfile
from dataclasses import dataclass                   #   NEEDED?     TODO

from functools import partial

from ExportToDir import ExportToDir

class Prism_ExportToDir_Functions(object):
    def __init__(self, core, plugin):
        self.core = core
        self.plugin = plugin

        self.menuContext = ""
        self.projectName = ""
        self.sourcePath = ""
        self.sourceExt = ""
        self.savePaths = ""
        self.outputPath = ""

        #   Callbacks

        #   TODO    Doesn't seem to be a callback for the Project Chooser
        self.core.registerCallback("projectBrowserContextMenuRequested", self.projectBrowserContextMenuRequested, plugin=self)      

        self.core.registerCallback("openPBFileContextMenu", self.openPBFileContextMenu, plugin=self)   
        self.core.registerCallback("productSelectorContextMenuRequested", self.productSelectorContextMenuRequested, plugin=self)        
        self.core.registerCallback("mediaPlayerContextMenuRequested", self.mediaPlayerContextMenuRequested, plugin=self)        
        self.core.registerCallback("textureLibraryTextureContextMenuRequested", self.textureLibraryTextureContextMenuRequested, plugin=self)


    # if returns true, the plugin will be loaded by Prism
    @err_catcher(name=__name__)
    def isActive(self):
        return True
    
    
    @err_catcher(name=__name__)                                                     #   TODO
    def projectBrowserContextMenuRequested(self, origin, menu):


        pass


    #   SceneFiles Browser Area
    @err_catcher(name=__name__)
    def openPBFileContextMenu(self, origin, rcmenu, filePath):

        self.menuContext = "SceneBrowser"

        self.sourcePath = filePath

        if os.path.isfile(self.sourcePath):
            sendToAct = QAction("Export to Dir...", rcmenu)
            sendToAct.triggered.connect(lambda: self.sendToDialogue())
            rcmenu.addAction(sendToAct)


    @err_catcher(name=__name__)
    def productSelectorContextMenuRequested(self, origin, viewUi, pos, rcmenu):

        version = origin.getCurrentVersion()
        if not version:
            return
        
        self.menuContext = "ProductBrowser"
        
        #   This assumes that the file path is always the last column
        row = viewUi.rowAt(pos.y())
        numCols = viewUi.columnCount()

        if row >= 0:
            self.sourcePath = viewUi.item(row, numCols - 1).text()

            if os.path.exists(self.sourcePath):
                sendToAct = QAction("Export to Dir...", viewUi)
                sendToAct.triggered.connect(lambda: self.sendToDialogue())
                rcmenu.addAction(sendToAct)

        
    @err_catcher(name=__name__)
    def mediaPlayerContextMenuRequested(self, origin, menu):

        if not type(origin.origin).__name__ == "MediaBrowser":
            return

        version = origin.origin.getCurrentVersion()
        if not version:
            return 

        self.menuContext = "MediaBrowser"

        if not origin.seq:
            return

        if len(origin.seq) < 2:
            self.sourcePath = origin.seq[0]         #   NEED TO HANDLE SEQUENCES

        elif len(origin.seq) > 1:                   #   TODO
            self.sourcePath = []
            for file in origin.seq:
                self.sourcePath.append(file)

        sendToAct = QAction("Export to Dir...", self.core.pb.mediaBrowser)
        sendToAct.triggered.connect(lambda: self.sendToDialogue())
        menu.addAction(sendToAct)


    @err_catcher(name=__name__)                                             #   TODO Handle Tex Groups
    def textureLibraryTextureContextMenuRequested(self, origin, menu):

        if not type(origin).__name__ == "TextureWidget":
            return
        
        self.menuContext = "Libraries"

        self.sourcePath = origin.path
            
        if os.path.exists(self.sourcePath):
            sendToAct = QAction("Export to Dir...", self.core.pb.mediaBrowser)
            sendToAct.triggered.connect(lambda: self.sendToDialogue())
            menu.addAction(sendToAct)



    @err_catcher(name=__name__)
    def loadData(self, dlg):

        pData = self.core.getConfig(config="project", dft=3)
        self.projectName = pData["globals"]["project_name"]

        self.loadSavePaths(pData)

        sourceDir = os.path.dirname(self.sourcePath[0])
        dlg.e_customLoc.setText(sourceDir)


    @err_catcher(name=__name__)
    def loadSavePaths(self, pData):    

        projectPaths = set()
        self.savePaths = []

        if pData["render_paths"]:
            renderLocs = pData["render_paths"]

            for locName, locPath in renderLocs.items():
                if locPath not in projectPaths:
                    projectPaths.add(locPath)
                    self.savePaths.append(locPath)

        if pData["export_paths"]:
            exportLocs = pData["export_paths"]

            for locName, locPath in exportLocs.items():
                if locPath not in projectPaths:
                    projectPaths.add(locPath)
                    self.savePaths.append(locPath)

########################        #   NOT USED        TODO
#        if "recent_external_paths" in pData and pData["recent_external_paths"]:
#            recentPaths = pData["recent_external_paths"]
#
#            for path in recentPaths.items():
#                self.savePaths.append(path)
########################


    @err_catcher(name=__name__)
    def sendToDialogue(self):

        dlg = ExportToDir()

        # GET MEDIA NAME FROM USER INPUT
        dlg.setWindowTitle("Export to Directory")

        dlg.rb_singleImage.hide()
        dlg.rb_imageSeq.hide()

        self.loadData(dlg)

        self.setPlaceholderName(dlg, load=True)

        existingFolders = self.savePaths
        dlg.cb_mediaFolders.addItems(existingFolders)

        dlg.rb_ProjectFolder.setChecked(True)

        #   Connections
        dlg.e_mediaName.textEdited.connect(lambda: self.refreshOutputName(dlg))
        dlg.but_nameReset.clicked.connect(lambda: self.setPlaceholderName(dlg))
        dlg.butGroup_folder.buttonClicked.connect(lambda: self.refreshOutputName(dlg))
        dlg.cb_mediaFolders.currentIndexChanged.connect(lambda: self.refreshOutputName(dlg))
        dlg.but_customPathSearch.clicked.connect(lambda: self.openExplorer(dlg, self.sourcePath, set=True))
        dlg.but_explorer.clicked.connect(lambda: self.openExplorer(dlg, self.outputPath))        
        dlg.buttonBox.button(QDialogButtonBox.Save).clicked.connect(lambda: self.execute(dlg))
        dlg.buttonBox.button(QDialogButtonBox.Close).clicked.connect(dlg.reject)        

        self.refreshOutputName(dlg)

        dlg.exec_()
    

    @err_catcher(name=__name__)                                 #   TODO    CLEAN THIS UP
    def setPlaceholderName(self, dlg, load=False):

        if isinstance(self.sourcePath, str):
            baseName = os.path.basename(self.sourcePath)
            fileNameNoExt, self.sourceExt = os.path.splitext(baseName)

        else:

            dlg.rb_singleImage.show()
            dlg.rb_imageSeq.show()

            baseName = os.path.basename(self.sourcePath[0])
            fileNameNoExt, self.sourceExt = os.path.splitext(baseName)  

            match = re.search(r'\d+$', fileNameNoExt)

            if match:
                numeric_length = match.end() - match.start()
                placeholder = 'x' * numeric_length

                fileNameNoExt = fileNameNoExt[:match.start()] + placeholder
            
            self.core.popup(f"fileNameNoExt:  {fileNameNoExt}")                 #   TESTING
         

        formattedName = self.formatName(fileNameNoExt)


        #   These are split in case it is desired for diff formats for types
        if self.menuContext == "SceneBrowser":      
            placeholderName = f"{self.projectName}--{formattedName}"

        elif self.menuContext == "ProductBrowser":
            placeholderName = f"{self.projectName}--{formattedName}"

        elif self.menuContext == "MediaBrowser":
            placeholderName = f"{self.projectName}--{formattedName}"

        elif self.menuContext == "Libraries":
            placeholderName = f"{self.projectName}--{formattedName}"

        dlg.e_mediaName.setText(placeholderName)

        if not load:
            self.refreshOutputName(dlg)


    @err_catcher(name=__name__)
    def formatName(self, fileNameNoExt):

        fileNameNoExt = re.sub(r"[^a-zA-Z0-9_\- ]", "_", fileNameNoExt)
        formatedName = fileNameNoExt + self.sourceExt

        return formatedName


    @err_catcher(name=__name__)
    def refreshOutputName(self, dlg):

        placeholderName = dlg.e_mediaName.text()
        root, extension = os.path.splitext(placeholderName)

        if extension:
            fileNameNoExt = root
        else:
            fileNameNoExt = placeholderName

        formatedName = self.formatName(fileNameNoExt)

        if dlg.rb_ProjectFolder.isChecked():
            outputPath = dlg.cb_mediaFolders.currentText()

        elif dlg.rb_customFolder.isChecked():
            outputPath = dlg.e_customLoc.text()

        self.outputPath = os.path.join(outputPath, formatedName)

        dlg.e_outputName.setText(self.outputPath)


    @err_catcher(name=__name__)
    def openExplorer(self, dlg, path, set=False):
 
        if dlg.rb_ProjectFolder.isChecked():
            path = dlg.cb_mediaFolders.currentText()

        elif dlg.rb_customFolder.isChecked():
            path = dlg.e_customLoc.text()
  
        path = path.replace("/", "\\")

        if set == True:
            customDir = QFileDialog.getExistingDirectory(None, "Select Save Directory", path)
            customDir = customDir.replace("/", "\\")
            dlg.e_customLoc.setText(customDir)
        else:
            cmd = "explorer " + path
            subprocess.Popen(cmd)

        self.refreshOutputName(dlg)
    

###################          #   NOT USED        TODO
#    @err_catcher(name=__name__)                            
#    def saveRecents(self):
#
#        return
###################
    





    @err_catcher(name=__name__)
    def execute(self, dlg):
        outputName = dlg.e_mediaName.text()
        fileName, extension = os.path.splitext(outputName)

        if fileName == "":
            self.core.popup("The Output Filename is blank.  Please enter a Filename")
            return

        outputPath = dlg.e_outputName.text()
        zipFiles = dlg.chb_zipFile.isChecked()              # Check if the checkbox is checked
        if zipFiles:
            outputPath = os.path.splitext(outputPath)[0] + '.zip'        

        if isinstance(self.sourcePath, str):        

            # Case #1: Copy a single file
            if os.path.exists(outputPath):
                reply = QMessageBox.question(
                    dlg,
                    'File Exists',
                    f'The file already exists:\n\n'
                    f'{outputPath}\n\n'
                    f'Do you want to overwrite it?',
                    QMessageBox.Yes | QMessageBox.No,
                    QMessageBox.No
                )
                if reply == QMessageBox.No:
                    return

            copyThread = CopyThread(self.sourcePath, outputPath, zipFiles)

        else:                                                   #   TODO Sort out Multi Files
            # Case #2: Copy entire directory
            sourceDir = os.path.dirname(self.sourcePath[0])
            outputDir = os.path.dirname(outputPath)

            if os.path.exists(outputDir):
                reply = QMessageBox.question(
                    dlg,
                    'Directory Exists',
                    f'The directory already exists:\n\n'
                    f'{outputPath}\n\n'
                    f'Do you want to overwrite it?',
                    QMessageBox.Yes | QMessageBox.No,
                    QMessageBox.No
                )
                if reply == QMessageBox.No:
                    return

            copyThread = CopyThread(sourceDir, outputDir, zipFiles)

        # Connect both progress signals to the same slot
        copyThread.progressUpdated.connect(dlg.progressBar.setValue)
        copyThread.zipProgressUpdated.connect(dlg.progressBar.setValue)
        
        thread = threading.Thread(target=copyThread.run)
        thread.start()



from PySide2.QtCore import QObject, Signal
import threading
import zipfile
import os
import shutil
import tempfile

class CopyThread(QObject):
    progressUpdated = Signal(int)
    zipProgressUpdated = Signal(int)

    def __init__(self, path, outputPath, zipFiles=False):
        super().__init__()
        self.path = path
        self.outputPath = outputPath
        self.zipFiles = zipFiles

    def get_total_size(self, directory):
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(directory):
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                total_size += os.path.getsize(filepath)
        return total_size

    def copy_file(self, src, dest):
        totalSize = os.path.getsize(src)
        copiedSize = 0
        with open(src, 'rb') as src_file, open(dest, 'wb') as dest_file:
            while True:
                chunk = src_file.read(4096)
                if not chunk:
                    break
                dest_file.write(chunk)
                copiedSize += len(chunk)
                progressPercentage = int(copiedSize / totalSize * 100)
                self.progressUpdated.emit(progressPercentage)

    def copy_directory(self, src, dest):
        total_size = self.get_total_size(src)
        copied_size = 0
        for root, dirs, files in os.walk(src):
            for file in files:
                src_file = os.path.join(root, file)
                dest_file = os.path.join(dest, os.path.relpath(src_file, src))
                self.copy_file(src_file, dest_file)
                copied_size += os.path.getsize(src_file)
                progressPercentage = int(copied_size / total_size * 100)
                self.progressUpdated.emit(progressPercentage)

    def run(self):
        original_path = self.path
        temp_dir = None

        if self.zipFiles:
            temp_dir = tempfile.mkdtemp()
            zip_filename = f"{os.path.basename(self.outputPath)}.zip"
            zip_path = os.path.join(temp_dir, zip_filename)

            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                if os.path.isdir(original_path):
                    total_size = self.get_total_size(original_path)
                    for root, dirs, files in os.walk(original_path):
                        for file in files:
                            file_path = os.path.join(root, file)
                            arcname = os.path.relpath(file_path, original_path)
                            zip_file.write(file_path, arcname=arcname)
                            progressPercentage = int(zip_file.fp.tell() / total_size * 50)
                            self.zipProgressUpdated.emit(progressPercentage)
                else:
                    total_size = os.path.getsize(original_path)
                    arcname = os.path.basename(original_path)
                    zip_file.write(original_path, arcname=arcname)
                    progressPercentage = int(zip_file.fp.tell() / total_size * 50)
                    self.zipProgressUpdated.emit(progressPercentage)

            self.path = zip_path

        if os.path.isdir(original_path):
            total_size = self.get_total_size(original_path)
            if self.zipFiles:
                zip_output_path = os.path.splitext(self.outputPath)[0] + '.zip'
                shutil.copy(zip_path, zip_output_path)
                progressPercentage = 50
                self.progressUpdated.emit(progressPercentage)
            else:
                self.copy_directory(original_path, self.outputPath)
        else:
            output_path_with_ext = os.path.splitext(self.outputPath)[0] + '.zip' if self.zipFiles else self.outputPath
            total_size = os.path.getsize(original_path)
            if self.zipFiles:
                shutil.copy(zip_path, output_path_with_ext)
                progressPercentage = 50
                self.progressUpdated.emit(progressPercentage)
            else:
                self.copy_file(original_path, output_path_with_ext)
                progressPercentage = 100
                self.progressUpdated.emit(progressPercentage)

        if temp_dir:
            shutil.rmtree(temp_dir)





