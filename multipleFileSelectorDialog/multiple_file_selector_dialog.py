# -*- coding: utf-8 -*-

import sys, os

here = os.path.dirname(__file__)
sys.path.append(os.path.join(here, '.'))

# Import the PyQt and QGIS libraries
from PyQt5.QtCore import *
from PyQt5.QtGui import *
# from PyQt5 import QtCore,uic
from PyQt5 import QtGui, QtWidgets, uic
from PyQt5.QtWidgets import QDialog, QTableWidgetItem, QListWidgetItem, QFileDialog, QMessageBox

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'multiple_file_selector_dialog.ui'))

class MultipleFileSelectorDialog(QDialog, FORM_CLASS):
    """
    Brief:
    """

    def __init__(self,
                 path,
                 title,
                 fileTypes,
                 files,
                 activeFileExtensions,
                 parent=None):
        """
        Brief:
        """
        super(MultipleFileSelectorDialog, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle(title)
        self.path = path
        self.title = title
        self.fileTypes = fileTypes
        self.files = files
        self.activeFileExtensions = activeFileExtensions

        # SIGNAL/SLOT connections in order:
        self.pushButton_selectFiles.clicked.connect(self.selectFiles)
        self.pushButton_selectDirectory.clicked.connect(self.selectDirectory)
        self.pushButton_selectDirectories.clicked.connect(self.selectDirectories)
        self.pushButton_deleteSelectedFiles.clicked.connect(self.deleteSelectedFiles)
        self.acceptItPushButton.clicked.connect(self.selectAcceptIt)

        self.initialize()

    def addFilesFromDirectory(self,dir, addFromSubDir):
        fileInfoList=dir.entryInfoList()
        insertFile = False
        for fileInfo in fileInfoList:
            if fileInfo.isFile():
                fileName = fileInfo.absoluteFilePath()
                if fileName in self.files:
                    continue
                fileExtension = fileInfo.suffix().lower()
                if not fileExtension in self.activeFileExtensions:
                    continue
                filePath = fileInfo.absolutePath()
                self.path = filePath
                self.files.append(fileName)
                if not insertFile:
                    insertFile = True
            if fileInfo.isDir() and addFromSubDir:
                if fileInfo.baseName(): # para quitar el . y el ..
                    subDir = QDir(fileInfo.absoluteFilePath())
                    insertFileFromSubDir = self.addFilesFromDirectory(subDir,addFromSubDir)
                    if not insertFile and insertFileFromSubDir:
                        insertFile = True
        return insertFile

    def deleteSelectedFiles(self):
        removeFile = False
        for row in range(self.tableWidget_selectedFiles.rowCount()):
            item = self.tableWidget_selectedFiles.item(row,0)
            if item.isSelected():
                self.files.remove(item.text())
                if not removeFile:
                    removeFile = True
        if removeFile:
            self.fillTabWidget()

    def existsFileTypesChecked(self):
        existsFileTypesChecked = False
        self.activeFileExtensions = []
        for j in range(self.listWidget_fileTypes.count()):
            item = self.listWidget_fileTypes.item(j)
            if item.checkState():
                if not existsFileTypesChecked:
                    existsFileTypesChecked = True
                self.activeFileExtensions.append(item.text())
        return existsFileTypesChecked

    def fillTabWidget(self):
        for i in range(self.tableWidget_selectedFiles.rowCount()):
            self.tableWidget_selectedFiles.removeRow(0)
        i = -1
        for fileName in self.files:
            itemFileName = QTableWidgetItem(fileName)
            itemFileName.setTextAlignment(Qt.AlignHCenter)
            itemFileName.setFlags(Qt.ItemIsSelectable)
            itemFileName.setBackground(QBrush(QColor(Qt.white),Qt.SolidPattern))
            itemFileName.setForeground(QBrush(QColor(Qt.black),Qt.SolidPattern))
            i = i + 1
            self.tableWidget_selectedFiles.insertRow(i)
            self.tableWidget_selectedFiles.setItem(i, 0, itemFileName)
        self.tableWidget_selectedFiles.resizeColumnToContents(0)

    def getActiveFileExtensions(self):
        return self.activeFileExtensions

    def getFiles(self):
        return self.files

    def getPath(self):
        return self.path

    def initialize(self):
        for i in range(len(self.fileTypes)):
            type = self.fileTypes[i]
            item = QListWidgetItem(type)
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            if type in self.activeFileExtensions:
                item.setCheckState(Qt.Checked)
            else:
                item.setCheckState(Qt.Unchecked)
            self.listWidget_fileTypes.insertItem(i,item)
        if len(self.files) > 0:
            self.fillTabWidget()

    def selectAcceptIt(self):
        self.accept()

    def selectFiles(self):
        if not self.existsFileTypesChecked():
            str_msg = "Before select files you must check some file type"
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setWindowTitle('Warning:')
            msgBox.setText(str_msg)
            return
        filters="Files ("
        for j in range(self.listWidget_fileTypes.count()):
            item = self.listWidget_fileTypes.item(j)
            if item.checkState():
                filters = filters + "*." + item.text() + " "
        filters = filters + ")"
        filesNames, _ = QFileDialog.getOpenFileNames(self,self.title,self.path,filters)
        insertFile = False
        for fileName in filesNames:
            fileInfo = QFileInfo(fileName) # por las barras
            fileName = fileInfo.absoluteFilePath()
            if fileName in self.files:
                continue
            fileExtension = fileInfo.suffix().lower()
            if fileExtension in self.activeFileExtensions:
                filePath = fileInfo.absolutePath()
                self.path = filePath
                self.files.append(fileName)
                if not insertFile:
                    insertFile = True
        if insertFile:
            self.fillTabWidget()

    def selectDirectory(self):
        if not self.existsFileTypesChecked():
            str_msg = "Before select files you must check some file type"
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setWindowTitle('Warning:')
            msgBox.setText(str_msg)
            return
        strDir = QFileDialog.getExistingDirectory(self,"Select directory",self.path,
                                                  QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks)
        if strDir:
            dir = QDir(strDir)
            if self.addFilesFromDirectory(dir,False):
                self.fillTabWidget()

    def selectDirectories(self):
        if not self.existsFileTypesChecked():
            str_msg = "Before select files you must check some file type"
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Warning)
            msgBox.setWindowTitle('Warning:')
            msgBox.setText(str_msg)
            return
        strDir = QFileDialog.getExistingDirectory(self,"Select main directory",self.path,
                                                  QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks)
        if strDir:
            dir = QDir(strDir)
            if self.addFilesFromDirectory(dir,True):
                self.fillTabWidget()