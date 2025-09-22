# authors:
# David Hernandez Lopez, david.hernandez@uclm.es

import math
import numpy as np
import os, sys
from scipy import stats as st
import json

current_path = os.path.dirname(__file__)
sys.path.append(os.path.join(current_path, '..'))

from PyQt5.QtWidgets import QMessageBox
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import (QApplication, QMessageBox, QDialog, QTreeView, QLabel,
                             QFileDialog, QPushButton, QComboBox, QPlainTextEdit, QAbstractItemView,
                             QDialogButtonBox, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, QProgressBar)
from PyQt5.QtCore import QDir, QFileInfo, QFile, QSize

from pyLibQtTools.JsonModel import JsonModel


class SimpleJSONDialog(QDialog):
    def __init__(self,
                 title,
                 value,
                 readOnly = True):
        super().__init__()

        layout = QVBoxLayout()
        self.treeViewWidget = QTreeView(self)
        if readOnly:
            self.treeViewWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        layout.addWidget(self.treeViewWidget)
        self.setLayout(layout)
        self.setMinimumSize(QSize(440, 240))
        self.setWindowTitle(title)
        if isinstance(value, str):
            value_as_json = json.loads(value)
        elif isinstance(value, dict):
            value_as_json = json.dumps(value, indent=4, ensure_ascii=False)
        else:
            value_as_string = str(value)
            value_as_json = json.loads(value)
        model = JsonModel()
        self.treeViewWidget.setModel(model)
        self.treeViewWidget.setAlternatingRowColors(True)
        model.load(value_as_json)
        self.treeViewWidget.resizeColumnToContents(0)

class SimpleTextEditDialog(QDialog):
    def __init__(self,
                 title,
                 text,
                 readOnly):
        super().__init__()

        layout = QVBoxLayout()
        self.ptd = QPlainTextEdit(self)
        self.ptd.setReadOnly(readOnly)
        layout.addWidget(self.ptd)
        self.setLayout(layout)
        self.setMinimumSize(QSize(440, 240))
        self.setWindowTitle(title)
        self.ptd.insertPlainText(text)

    def get_text(self):
        return self.ptd.toPlainText()

def error_msg(str_msg):
    msgBox = QMessageBox()
    msgBox.setIcon(QMessageBox.Critical)
    msgBox.setWindowTitle('Error:')
    msgBox.setText(str_msg)
    # msgBox.setInformativeText("Do you want to save your changes?")
    # msgBox.setStandardButtons(QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel)
    # msgBox.setDefaultButton(QMessageBox.Save)
    ret = msgBox.exec()

def warning_msg(str_msg):
    msgBox = QMessageBox()
    msgBox.setIcon(QMessageBox.Warning)
    msgBox.setWindowTitle('Warning:')
    msgBox.setText(str_msg)
    # msgBox.setInformativeText("Do you want to save your changes?")
    # msgBox.setStandardButtons(QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel)
    # msgBox.setDefaultButton(QMessageBox.Save)
    ret = msgBox.exec()


def info_msg(str_msg):
    msgBox = QMessageBox()
    msgBox.setIcon(QMessageBox.Information)
    msgBox.setWindowTitle('Information:')
    msgBox.setText(str_msg)
    # msgBox.setInformativeText("Do you want to save your changes?")
    # msgBox.setStandardButtons(QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel)
    # msgBox.setDefaultButton(QMessageBox.Save)
    ret = msgBox.exec()

class AbsoluteValueSortedWidgetItem(QtWidgets.QTableWidgetItem):
    def __init__(self, parent=None):
        QtWidgets.QTableWidgetItem.__init__(self, parent)

    def __lt__(self, otherItem):
        try:
            return abs(float(self.text())) < abs(float(otherItem.text()))
        except ValueError:
            return self.text() < otherItem.text()


def get_file(dialog_title,
             previous_file,
             previous_path,
             file_types,
             file_mode, # 'read', 'append', 'write'
             mandatory = True):
    str_error = ''
    file_path = ''
    if dialog_title:
        if not isinstance(dialog_title, str):
            str_error = ('Dialog title must be a string and is: {}'.format(type(dialog_title).__name__))
            return str_error, file_path
    if previous_file:
        if not isinstance(previous_file, str):
            str_error = ('Previous file must be a string and is: {}'.format(type(previous_file).__name__))
            return str_error, file_path
    if previous_path:
        if not isinstance(previous_path, str):
            str_error = ('Previous path must be a string and is: {}'.format(type(previous_path).__name__))
            return str_error, file_path
    if file_types:
        if not isinstance(file_types, list):
            str_error = ('File types must be a list of strings and is: {}'.format(type(file_types).__name__))
            return str_error, file_path
        for file_type in file_types:
            if not isinstance(file_type, str):
                str_error = ('File type: {} must be a string and is: {}'.
                             format(file_type, type(file_type).__name__))
                return str_error, file_path
    if not file_mode:
        str_error = ('File mode must be a string, read, append or write, and is None')
        return str_error, file_path
    if not isinstance(file_mode, str):
        str_error = ('File mode must be a string and is: {}'.format(type(file_mode).__name__))
        return str_error, file_path
    if file_mode.casefold() != 'read' and file_mode.casefold() != 'read' and file_mode.casefold() != 'read':
        str_error = ('File mode must be a string, read, append or write, and is: {}'.format(file_mode))
        return str_error, file_path
    if not isinstance(mandatory, bool):
        str_error = ('Mandatory must be a bool and is: {}'.format(type(file_mode).__name__))
        return str_error, file_path
    path = QDir.currentPath()
    if previous_file:
        if os.path.isfile(previous_file):
            previous_file_path = os.path.dirname(previous_file)
            if os.path.isdir(previous_file_path):
                path = previous_file_path
    else:
        if previous_path:
            if os.path.isdir(previous_path):
                path = previous_path
    str_files = 'Files (*.*)'
    if file_types:
        str_files = 'Files ('
        for i in range(len(file_types)):
            if i > 0:
                str_files += ' '
            str_files += ("*" + file_types[i])
        str_files += ')'
    dlg = QFileDialog()
    if not dialog_title:
        dialog_title = 'Select file'
    dlg.setWindowTitle(dialog_title)
    dlg.setDirectory(path)
    dlg.setNameFilter(str_files)
    if file_mode.casefold() == 'read':
        dlg.setFileMode(QFileDialog.ExistingFile)
        # file_name, aux = QFileDialog.getOpenFileName(self, title, path, str_files)
    elif file_mode.casefold() == 'append':
        dlg.setFileMode(QFileDialog.ExistingFile)
        # file_name, aux = QFileDialog.getOpenFileName(self, title, path, str_files)
    elif file_mode.casefold() == 'write':
        dlg.setFileMode(QFileDialog.AnyFile)
        # file_name, aux = QFileDialog.getSaveFileName(self, title, path, str_files)
    if dlg.exec_():
        file_names = dlg.selectedFiles()
        file_name = file_names[0]
        if not file_name and mandatory:
            msg = ('File selection is mandatory')
            error_msg(msg)
            get_file(dialog_title,
                     previous_file,
                     previous_path,
                     file_types,
                     file_mode,  # 'read', 'append', 'write'
                     mandatory)
        if file_name:
            file_path = os.path.normcase(file_name)
        return str_error, file_path
    else:
        if mandatory:
            msg = ('File selection is mandatory')
            error_msg(msg)
            get_file(dialog_title,
                     previous_file,
                     previous_path,
                     file_types,
                     file_mode,  # 'read', 'append', 'write'
                     mandatory)
        else:
            return str_error, file_path
