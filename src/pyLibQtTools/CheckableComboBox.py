# authors:
# David Hernandez Lopez, david.hernandez@uclm.es

import os
import sys

from qgis.PyQt import QtCore, QtWidgets
from qgis.PyQt.uic import loadUi
from qgis.PyQt.QtWidgets import QComboBox
from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtGui import QStandardItemModel

# creating checkable combo box class
class CheckableComboBox(QComboBox):
    def __init__(self):
        super(CheckableComboBox, self).__init__()
        self.view().pressed.connect(self.handle_item_pressed)
        self.setModel(QStandardItemModel(self))

    def get_checked_texts(self):
        values = []
        for i in range(self.model().rowCount()):
            item = self.model().item(i)
            if item.checkState() == Qt.Checked:
                values.append(item.text())
        return values

    # when any item get pressed
    def handle_item_pressed(self, index):
        # getting which item is pressed
        item = self.model().itemFromIndex(index)
        # make it check if unchecked and vice-versa
        if item.checkState() == Qt.Checked:
            item.setCheckState(Qt.Unchecked)
        else:
            item.setCheckState(Qt.Checked)

    # method called by check_items
    def item_checked(self, index):
        # getting item at index
        item = self.model().item(index, 0)
        # return true if checked else false
        return item.checkState() == Qt.Checked
