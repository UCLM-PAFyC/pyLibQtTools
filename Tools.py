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
from PyQt5.QtWidgets import (QApplication, QMessageBox, QDialog, QTreeView,
                             QFileDialog, QPushButton, QComboBox, QPlainTextEdit, QAbstractItemView,
                             QDialogButtonBox, QVBoxLayout, QTableWidget, QTableWidgetItem)
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