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
from dataclasses import dataclass                   #   NEEDED?     TODO

from functools import partial

from SetName import SetName

class Prism_SendToClient_Functions(object):
    def __init__(self, core, plugin):
        self.core = core
        self.plugin = plugin

        #   Callbacks
        self.core.registerCallback("mediaPlayerContextMenuRequested", self.mediaPlayerContextMenuRequested, plugin=self)


        self.projectName = ""
        self.imagePath = ""
        self.savePaths = ""


    # if returns true, the plugin will be loaded by Prism
    @err_catcher(name=__name__)
    def isActive(self):
        return True
    

        
    @err_catcher(name=__name__)
    def mediaPlayerContextMenuRequested(self, origin, menu):

        if not type(origin.origin).__name__ == "MediaBrowser":
            return

        version = origin.origin.getCurrentVersion()
        if not version:
            return

        if not origin.seq:
            return

        filePath = origin.seq[0]
        if os.path.splitext(filePath)[1] in self.core.media.videoFormats:
            return

        if os.path.exists(filePath):

            self.imagePath = filePath

            sendToAct = QAction("Send to Client...", self.core.pb.mediaBrowser)
            sendToAct.triggered.connect(lambda: self.sendToDialogue(self.imagePath))
            menu.addAction(sendToAct)


    @err_catcher(name=__name__)
    def sendToDialogue(self, path):

        pData = self.loadData()

        placeholderMediaName = self.getPlaceholderName(path)

        toClientFolder = self.get_toClientFolder()


        # GET MEDIA NAME FROM USER INPUT
        dlg = SetName()
        dlg.setWindowTitle("Send to Client")

        dlg.e_mediaName.setText(placeholderMediaName)

        existingFolders = self.savePaths
        dlg.cb_mediaFolders.addItems(existingFolders)

        dlg.rb_ProjectFolder.setChecked(True)



        dlg.e_mediaName.textEdited.connect(lambda: self.refreshOutputName(dlg))
        dlg.butGroup_folder.buttonClicked.connect(lambda: self.refreshOutputName(dlg))
        dlg.cb_mediaFolders.currentIndexChanged.connect(lambda: self.refreshOutputName(dlg))

        dlg.but_explorer.clicked.connect(lambda: self.openExplorer(toClientFolder))        
        dlg.buttonBox.button(QDialogButtonBox.Save).clicked.connect(lambda: self.execute(dlg, toClientFolder, path))
        dlg.buttonBox.button(QDialogButtonBox.Close).clicked.connect(dlg.reject)        


        self.refreshOutputName(dlg)

        dlg.exec_()

    @err_catcher(name=__name__)
    def loadData(self):

        pData = self.core.getConfig(config="project", dft=3)

        self.projectName = pData["globals"]["project_name"]

        self.loadSavePaths(pData)



#        self.core.popup(f"self.savePaths:  {self.savePaths}")               #   TESTING


        return pData
    
    @err_catcher(name=__name__)
    def loadSavePaths(self, pData):    

        self.savePaths = []

        if pData["render_paths"]:
            renderLocs = pData["render_paths"]

            for locName, locPath in renderLocs.items():
                self.savePaths.append(locPath)

        if "recent_external_paths" in pData and pData["recent_external_paths"]:
            recentPaths = pData["recent_external_paths"]

            for path in recentPaths.items():
                self.savePaths.append(path)

        



#        self.core.popup(f"self.savePaths:  {self.savePaths}")               #   TESTING


    @err_catcher(name=__name__)
    def formatName(self, inputName):

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

        checkedButtonId = dlg.butGroup_folder.checkedId()

        if checkedButtonId != -1:
            checkedButton = dlg.butGroup_folder.button(checkedButtonId)
            self.core.popup(f"checkedButton:  {checkedButton.text()}")                      #   TESTING

        outputPath = dlg.cb_mediaFolders.currentText()

        dlg.e_outputName.setText(os.path.join(outputPath, outputName))


    @err_catcher(name=__name__)
    def execute(self, dlg, toClientFolder, path):                       #   TODO

        # RETRIEVE AND FORMAT USER INPUT
        toClientMediaFolder = dlg.cb_mediaFolders.currentText()
        toClientMediaFolder = re.sub(r"[^a-zA-Z0-9]", "_", toClientMediaFolder)
        toClientMediaPath = os.path.join(toClientFolder, toClientMediaFolder)
        toClientMediaName = dlg.e_mediaName.text()
        toClientMediaName = re.sub(r"[^a-zA-Z0-9]", "_", toClientMediaName)

        copyToName = dlg.e_mediaName.text()

        copyToPLoc = dlg.cb_mediaFolders.currentText()

        copyToPath = os.path.join(copyToPLoc, copyToName)

        outputPath = dlg.e_outputName.text()


        shutil.copy2(path, outputPath)                 #   TODO


    @err_catcher(name=__name__)
    def getPlaceholderName(self, path):

        data = self.core.pb.mediaBrowser.getCurrentIdentifier()
        try:
            assetName = data["asset_path"]
        except:
            assetName = data["shot"]
        task = data["displayName"]
        task = task.split(" ")[0]
        version = self.core.pb.mediaBrowser.getCurrentVersion()["version"]
        version = version.split(" ")[0]

        placeholderName = f"{self.projectName}--{assetName}_{version}"
        formattedName = self.formatName(placeholderName)

        return formattedName


    @err_catcher(name=__name__)
    def openExplorer(self, path):
        path = path.replace("/", "\\")
        cmd = "explorer " + path
        subprocess.Popen(cmd)



    @err_catcher(name=__name__)                                 #       TODO    - HARDCODED
    def get_toClientFolder(self):
        data = self.core.pb.mediaBrowser.getCurrentIdentifier()
        projectPath = os.path.dirname(data["project_path"])
        projectDirs = os.listdir(projectPath)





        dir = "04_Deliverables"

#        for dir in projectDirs:    

#            self.core.popup(f"{dir}")           #   TESTING


#            if "04_Deliverables" in dir.lower():                #       TODO    - HARDCODED

#                toClientFolder = os.path.join(projectPath, dir)

#            else:
#                self.core.popup(f"Folder does not exist: 04_Deliverables")           #   TESTING

        toClientFolder = os.path.join(projectPath, dir)

        toClientFolderFull = toClientFolder + "\\"

        return toClientFolder


    @err_catcher(name=__name__)                             #   NOT USED
    def get_toClientMediaFolder(self):
        date = datetime.datetime.now()
        date = date.strftime("%y%m%d")
        toClient_media_folder = date + "_"
        return toClient_media_folder
    

    @err_catcher(name=__name__)
    def saveRecents(self):

        return