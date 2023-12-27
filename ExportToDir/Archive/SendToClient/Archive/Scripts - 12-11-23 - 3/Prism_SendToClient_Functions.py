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
from dataclasses import dataclass                   #   NEEDED?     TODO

from functools import partial

from SetName import SetName

class Prism_SendToClient_Functions(object):
    def __init__(self, core, plugin):
        self.core = core
        self.plugin = plugin

        self.menuContext = ""
        self.projectName = ""
        self.imagePath = ""
        self.savePaths = ""

        #   Callbacks
        self.core.registerCallback("mediaPlayerContextMenuRequested", self.mediaPlayerContextMenuRequested, plugin=self)        
        self.core.registerCallback("textureLibraryTextureContextMenuRequested", self.textureLibraryTextureContextMenuRequested, plugin=self)


    # if returns true, the plugin will be loaded by Prism
    @err_catcher(name=__name__)
    def isActive(self):
        return True
    
        
    @err_catcher(name=__name__)
    def mediaPlayerContextMenuRequested(self, origin, menu):

        if not type(origin.origin).__name__ == "MediaBrowser":
            return
        
        self.menuContext = "MediaBrowser"

        version = origin.origin.getCurrentVersion()
        if not version:
            return

        if not origin.seq:
            return

#        self.core.popup(origin.seq)                        #   TESTING

        if len(origin.seq) < 2:
            filePath = origin.seq[0]

        elif len(origin.seq) > 1:
            filePath = origin.seq[0]



#        if os.path.splitext(filePath)[1] in self.core.media.videoFormats:                  #   NEEDED???   TODO
#            return

        if os.path.exists(filePath):
            self.imagePath = filePath

            sendToAct = QAction("Send to Client...", self.core.pb.mediaBrowser)
            sendToAct.triggered.connect(lambda: self.sendToDialogue(self.imagePath))
            menu.addAction(sendToAct)


    @err_catcher(name=__name__)
    def textureLibraryTextureContextMenuRequested(self, origin, menu):

        if not type(origin).__name__ == "TextureWidget":
            return
        
        self.menuContext = "Libraries"

        filePath = origin.path

        if os.path.splitext(filePath)[1] in self.core.media.videoFormats:
            return

        if os.path.exists(filePath):
            self.imagePath = filePath

            sendToAct = QAction("Send to Client...", self.core.pb.mediaBrowser)
            sendToAct.triggered.connect(lambda: self.sendToDialogue(self.imagePath))
            menu.addAction(sendToAct)



    @err_catcher(name=__name__)
    def sendToDialogue(self, sourcePath):

        dlg = SetName()

        pData = self.loadData(dlg, sourcePath)             #   pData NEEDED?       TODO


        # GET MEDIA NAME FROM USER INPUT
        
        dlg.setWindowTitle("Send to Client")

        self.setPlaceholderName(dlg, load=True)

        existingFolders = self.savePaths
        dlg.cb_mediaFolders.addItems(existingFolders)

        dlg.rb_ProjectFolder.setChecked(True)

        #   Connections
        dlg.e_mediaName.textEdited.connect(lambda: self.refreshOutputName(dlg))
        dlg.but_nameReset.clicked.connect(lambda: self.setPlaceholderName(dlg))
        dlg.butGroup_folder.buttonClicked.connect(lambda: self.refreshOutputName(dlg))
        dlg.cb_mediaFolders.currentIndexChanged.connect(lambda: self.refreshOutputName(dlg))
        dlg.but_customPathSearch.clicked.connect(lambda: self.openExplorer(dlg, sourcePath, set=True))
        dlg.but_explorer.clicked.connect(lambda: self.openExplorer(dlg, sourcePath))        
        dlg.buttonBox.button(QDialogButtonBox.Save).clicked.connect(lambda: self.execute(dlg, sourcePath))
        dlg.buttonBox.button(QDialogButtonBox.Close).clicked.connect(dlg.reject)        

        self.refreshOutputName(dlg)

        dlg.exec_()


    @err_catcher(name=__name__)
    def loadData(self, dlg, sourcePath):

        pData = self.core.getConfig(config="project", dft=3)
        self.projectName = pData["globals"]["project_name"]

        self.loadSavePaths(pData)

        sourceDir = os.path.dirname(sourcePath)
        dlg.e_customLoc.setText(sourceDir)

        return pData                                                #   NEEDED??        TODO
    

    @err_catcher(name=__name__)
    def setPlaceholderName(self, dlg, load=False):

        assetData = self.core.pb.mediaBrowser.getCurrentIdentifier()

        baseName = os.path.basename(self.imagePath)
        imageName = os.path.splitext(baseName)[0]

        if self.menuContext == "MediaBrowser":
            try:
                assetName = assetData["asset_path"]
            except:
                assetName = assetData["shot"]

            task = assetData["displayName"]
            task = task.split(" ")[0]

            version = self.core.pb.mediaBrowser.getCurrentVersion()["version"]
            version = version.split(" ")[0]



            placeholderName = f"{imageName}_{version}"
#            placeholderName = f"{self.projectName}--{assetName}_{version}"


        elif self.menuContext == "Libraries":
            placeholderName = f"{self.projectName}--{imageName}"



        formattedName = self.formatName(placeholderName)
        dlg.e_mediaName.setText(formattedName)

        if not load:
            self.refreshOutputName(dlg)


    @err_catcher(name=__name__)
    def loadSavePaths(self, pData):    

        self.savePaths = []

        if pData["render_paths"]:
            renderLocs = pData["render_paths"]

            for locName, locPath in renderLocs.items():
                self.savePaths.append(locPath)

########################        #   NOT USED        TODO
#        if "recent_external_paths" in pData and pData["recent_external_paths"]:
#            recentPaths = pData["recent_external_paths"]
#
#            for path in recentPaths.items():
#                self.savePaths.append(path)
########################


    @err_catcher(name=__name__)
    def formatName(self, inputName):

        inputName = re.sub(r"[^a-zA-Z0-9_\- ]", "_", inputName)
        extension = os.path.splitext(self.imagePath)[1]

        formatedName = inputName + extension

        return formatedName


    @err_catcher(name=__name__)
    def refreshOutputName(self, dlg):

        origExt = os.path.splitext(self.imagePath)[1]
        placeholderName = dlg.e_mediaName.text()

        root, extension = os.path.splitext(placeholderName)

        if extension:
            baseName = root
        else:
            baseName = placeholderName

        outputName = baseName + origExt

        if dlg.rb_ProjectFolder.isChecked():
            outputPath = dlg.cb_mediaFolders.currentText()

        elif dlg.rb_customFolder.isChecked():
            outputPath = dlg.e_customLoc.text()

        dlg.e_outputName.setText(os.path.join(outputPath, outputName))


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


    @err_catcher(name=__name__)                             #   NOT USED        TODO
    def get_toClientMediaFolder(self):
        date = datetime.datetime.now()
        date = date.strftime("%y%m%d")
        toClient_media_folder = date + "_"
        return toClient_media_folder
    

###################          #   NOT USED        TODO
#    @err_catcher(name=__name__)                            
#    def saveRecents(self):
#
#        return
###################
    


    @err_catcher(name=__name__)
    def execute(self, dlg, path):                       #   TODO

        outputName = dlg.e_mediaName.text()

        fileName, extension = os.path.splitext(outputName)

        if fileName == "":
            self.core.popup("The Output Filename is blank.  Please enter a Filename")
            return
        
        outputPath = dlg.e_outputName.text()

        if os.path.exists(outputPath):
            # Ask the user whether to overwrite the file
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
                # User chose not to overwrite, you can handle this case accordingly
                return
            
        # Create an instance of the CopyThread
        copyThread = CopyThread(path, outputPath)

        # Connect the progress_updated signal to a slot that updates the progress bar
        copyThread.progressUpdated.connect(dlg.progressBar.setValue)

        # Create a thread for the file copy operation
        thread = threading.Thread(target=copyThread.run)

        thread.start()    



class CopyThread(QObject):
    progressUpdated = Signal(int)

    def __init__(self, path, outputPath):
        super().__init__()
        self.path = path
        self.outputPath = outputPath

    def run(self):
        # Perform the file copy operation and update the progress bar
        totalSize = os.path.getsize(self.path)
        copiedSize = 0
        with open(self.path, 'rb') as src, open(self.outputPath, 'wb') as dest:
            while True:
                chunk = src.read(4096)
                if not chunk:
                    break
                dest.write(chunk)
                copiedSize += len(chunk)
                progressPercentage = int(copiedSize / totalSize * 100)
                self.progressUpdated.emit(progressPercentage)