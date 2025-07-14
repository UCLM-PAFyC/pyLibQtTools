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

def chauvenets_criterion(obs):
    """
    Identify and remove outliers using Chauvenet's criterion. Iterative
    From Wikipedia (https://en.wikipedia.org/wiki/Chauvenet%27s_criterion):
    "In statistical theory, Chauvenet's criterion (named for William Chauvenet)
    is a means of assessing whether one piece of experimental data — an outlier
    — from a set of observations, is likely to be spurious."
    """
    exists_outliers = True
    inliers = obs
    outliers = []
    while exists_outliers:
        # Sample size
        n = len(inliers)
        # Probability represented by one tail of the normal distribution
        P_z = 1 - (1 / (4 * n))
        # Maximum allowable deviation
        D_max = st.norm.ppf(P_z)
        # Mean
        x_bar = np.mean(inliers)
        # Sample standard deviation
        s = np.std(inliers, ddof=1)
        # z-scores
        z_scores = (inliers - x_bar) / s
        max_deviation = 0.0
        outlier_position = -1
        for i in range(len(z_scores)):
            if abs(z_scores[i]) > D_max:
                if abs(z_scores[i]) > max_deviation:
                    max_deviation = abs(z_scores[i])
                    outlier_position = i
        if outlier_position == -1:
            exists_outliers = False
        else:
            outliers.append(inliers[outlier_position])
            inliers.pop(outlier_position)
    # i prefer compute mean and std myself
    mean = 0.
    for inlier in inliers:
        mean += inlier
    mean /= len(inliers)
    std = -1.
    if len(inliers) > 1:
        std = 0.
        for inlier in inliers:
            std += (mean - inlier) ** 2.
        std = math.sqrt(std / (len(inliers) - 1))
        std = math.sqrt(std / len(inliers))
    return mean, std, inliers, outliers

def error_msg(str_msg):
    msgBox = QMessageBox()
    msgBox.setIcon(QMessageBox.Critical)
    msgBox.setWindowTitle('Error:')
    msgBox.setText(str_msg)
    # msgBox.setInformativeText("Do you want to save your changes?")
    # msgBox.setStandardButtons(QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel)
    # msgBox.setDefaultButton(QMessageBox.Save)
    ret = msgBox.exec()

def extract_parts_from_file(file_path, num_subdirectories):
    subdirectories = []
    for _ in range(num_subdirectories):
        file_path, subdirectory = os.path.split(file_path)
        subdirectories.insert(0, subdirectory)
    return subdirectories

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