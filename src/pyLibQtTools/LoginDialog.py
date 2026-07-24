# authors:
# David Hernandez Lopez, david.hernandez@uclm.es

import os
from qgis.PyQt.QtWidgets import (QDialog, QPushButton, QLabel, QLineEdit, QGridLayout, QMessageBox)
from qgis.PyQt.QtGui import QIcon

current_path = os.path.dirname(os.path.realpath(__file__))
images_path = os.path.join(current_path, 'images')
eye_visible_svg_file_path = os.path.join(images_path, "eye_visible.svg")
eye_hidden_svg_file_path = os.path.join(images_path, "eye_hidden.svg")

class PasswordLineEdit(QLineEdit):
    """
    A LineEdit with icons to show/hide password entries
    """
    CSS = '''QLineEdit {
        border-radius: 0px;
        height: 30px;
        margin: 0px 0px 0px 0px;
    }
    '''

    def __init__(self, parent):
        self.parent = parent
        super().__init__(self.parent)
        # Set styles
        self.setStyleSheet(self.CSS)
        self.visibleIcon = QIcon(eye_visible_svg_file_path)
        self.hiddenIcon = QIcon(eye_hidden_svg_file_path)
        self.setEchoMode(QLineEdit.Password)
        self.togglepasswordAction = self.addAction(self.visibleIcon, QLineEdit.TrailingPosition)
        self.togglepasswordAction.triggered.connect(self.on_toggle_password_Action)
        self.password_shown = False

    def on_toggle_password_Action(self):
        if not self.password_shown:
            self.setEchoMode(QLineEdit.Normal)
            self.password_shown = True
            self.togglepasswordAction.setIcon(self.hiddenIcon)
        else:
            self.setEchoMode(QLineEdit.Password)
            self.password_shown = False
            self.togglepasswordAction.setIcon(self.visibleIcon)

class LoginDialog(QDialog):
    def __init__(self, parent, title = None,
                 default_email = None, default_password = None, default_url = None, is_register = False):
        super().__init__(parent)
        self.is_register = is_register
        self.url = ''
        if default_url:
            self.url = default_url
        self.name = ''
        self.email = ''
        if default_email:
            self.email = default_email
        self.password = ''
        if default_password:
            self.password = default_password
        if not title:
            if not self.is_register:
                title = "Login"
            else:
                title = "Register"
        self.setWindowTitle(title)
        layout = QGridLayout()
        ncols = 5
        row = 0
        
        self.urlLineEdit = None
        if default_url:
            label_url = QLabel('Url:')
            self.urlLineEdit = QLineEdit(self.url)
            # self.lineEdit_username.setPlaceholderText('Please enter url')
            layout.addWidget(label_url, row, 0, 1, 1)
            layout.addWidget(self.urlLineEdit, row, 1, 1, ncols - 1)
            row = row + 1
        
        if self.is_register:
            label_name = QLabel('Name:')
            self.nameLineEdit = QLineEdit(self.name)
            if not self.name:
                self.nameLineEdit.setPlaceholderText('Please enter your name')
            layout.addWidget(label_name, row, 0, 1, 1)
            layout.addWidget(self.nameLineEdit, row, 1, 1, ncols - 1)
            row = row + 1

        label_email = QLabel('Email:')
        self.emailLineEdit = QLineEdit(self.email)
        if not self.name:
            self.emailLineEdit.setPlaceholderText('Please enter your email')
        layout.addWidget(label_email, row, 0, 1, 1)
        layout.addWidget(self.emailLineEdit, row, 1, 1, ncols - 1)
        row = row + 1

        label_password = QLabel('Password:')
        self.passwordLineEdit = PasswordLineEdit(self)#QLineEdit()
        self.passwordLineEdit.setPlaceholderText('Please enter your password')
        layout.addWidget(label_password, row, 0, 1, 1)
        layout.addWidget(self.passwordLineEdit, row, 1, 1,ncols - 1)
        row = row + 1

        acceptButton = QPushButton('Accept')
        acceptButton.clicked.connect(self.accept)
        layout.addWidget(acceptButton, row, ncols - 1, 1, 1)
        # layout.setRowMinimumWidth(row-1, 300)
        # self.resize(500, 3000)
        self.setMinimumWidth(300)
        self.setLayout(layout)

    def accept(self):
        if not self.urlLineEdit is None:
            self.url = self.urlLineEdit.text()
            if not self.url:
                msg = QMessageBox(self)
                msg.setText('Input url')
                msg.exec_()
                return
        if self.is_register:
            self.name = self.nameLineEdit.text()
            if not self.name:
                msg = QMessageBox(self)
                msg.setText('Input name')
                msg.exec_()
                return
        self.email = self.emailLineEdit.text()
        if not self.email:
            msg = QMessageBox(self)
            msg.setText('Input email')
            msg.exec_()
            return
        self.password = self.passwordLineEdit.text()
        if not self.password:
            msg = QMessageBox(self)
            msg.setText('Input password')
            msg.exec_()
            return
        super().accept()
        # if self.lineEdit_username.text() == 'Usernmae' and self.lineEdit_password.text() == '000':
        #     msg.setText('Success')
        #     msg.exec_()
        #     app.quit()
        # else:
		# 	msg.setText('Incorrect Password')
		# 	msg.exec_()
