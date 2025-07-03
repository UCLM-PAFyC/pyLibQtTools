# authors:
# David Hernandez Lopez, david.hernandez@uclm.es

from PyQt5.QtWidgets import (QDialog, QPushButton, QPlainTextEdit,
                                QVBoxLayout, QWidget, QProgressBar)
from PyQt5.QtCore import QProcess
from PyQt5 import QtCore
from PyQt5.uic import loadUi
import sys, os
import re
import time

here = os.path.dirname(__file__)
sys.path.append(os.path.join(here, '.'))

import defs_qprocess

class QProcessDialog(QDialog):
    """Employee dialog."""

    def __init__(self,
                 title,
                 parent=None):
        super().__init__(parent)
        loadUi(os.path.join(os.path.dirname(__file__), 'QProcessDialog.ui'), self)
        # loadUi("lib/InstrumentsDialog.ui", self)
        self.process = None
        self.terminatePushButton.clicked.connect(self.terminate)
        self.number_of_steps = None

    def process_state_message(self, s):
        self.processStatePlainTextEdit.appendPlainText(s)

    def set_progress_range(self, min, max):
        self.progressBar.setEnabled(True)
        self.progressBar.setVisible(True)
        self.progressBar.setRange(min, max)
        return

    def standard_error_message(self, s):
        self.standardErrorPlainTextEdit.appendPlainText(s)

    def standard_output_message(self, s):
        self.standardOutputPlainTextEdit.appendPlainText(s)

    def start_process(self,
                      program,
                      arguments,
                      string_to_read_number_of_steps = defs_qprocess.STRING_TO_PUBLISH_THE_NUMBER_OF_STEPS_DEFAULT,
                      string_to_read_completed_steps_percentage = defs_qprocess.STRING_TO_PUBLISH_COMPLETED_STEPS_PERCENTAGE_DEFAULT):
        if self.process is None:  # No process running.
            self.string_to_read_number_of_steps = string_to_read_number_of_steps
            self.string_to_read_completed_steps_percentage = string_to_read_completed_steps_percentage
            self.progress_number_of_steps_re = re.compile(string_to_read_number_of_steps)
            self.progress_completed_steps_percentage_re = re.compile(string_to_read_completed_steps_percentage)
            self.processStatePlainTextEdit.clear()
            self.standardErrorPlainTextEdit.clear()
            self.standardOutputPlainTextEdit.clear()
            self.standard_output_message("Executing process")
            self.process = QProcess()  # Keep a reference to the QProcess (e.g. on self) while it's running.
            self.process.readyReadStandardOutput.connect(self.handle_stdout)
            self.process.readyReadStandardError.connect(self.handle_stderr)
            self.process.stateChanged.connect(self.handle_state)
            self.process.finished.connect(self.process_finished)  # Clean up once complete.
            self.progressBar.setEnabled(False)
            self.progressBar.setVisible(False)
            self.start_time = time.time()
            self.process.start(program, arguments)

    def handle_stderr(self):
        data = self.process.readAllStandardError()
        stderr = bytes(data).decode("utf8")
        self.standard_error_message(stderr)

    def handle_stdout(self):
        data = self.process.readAllStandardOutput()
        stdout = bytes(data).decode("utf8")
        # Extract progress if it is in the data.
        if not self.progressBar.isEnabled():
            min, max = self.progress_range_parser(stdout)
            if max > 0:
                self.progressBar.setEnabled(True)
                self.progressBar.setVisible(True)
                self.progressBar.setRange(min, max)
                self.number_of_steps = max
        else:
            progress = self.progress_percent_parser(stdout)
            if progress:
                self.progressBar.setValue(progress)
        self.standard_output_message(stdout)

    def handle_state(self, state):
        states = {
            QProcess.ProcessState.NotRunning: 'Not running',
            QProcess.ProcessState.Starting: 'Starting',
            QProcess.ProcessState.Running: 'Running',
        }
        state_name = states[state]
        self.process_state_message(f"State changed: {state_name}")

    def process_finished(self):
        self.standard_output_message("Process finished.")
        self.end_time = time.time()
        elapsed_time = self.end_time - self.start_time
        str_elapsed_time_in_seconds = ("\nElapsed Time: {:.3f} seconds".format(elapsed_time))
        self.process_state_message(str_elapsed_time_in_seconds)
        if self.number_of_steps:
            self.progressBar.setValue(self.number_of_steps)
        self.process = None

    def progress_percent_parser(self, output):
        """
        Matches lines using the progress_re regex,
        returning a single integer for the % progress.
        """
        match = self.progress_completed_steps_percentage_re.search(output)
        if match:
            pc_complete = match.group(1)
            return int(pc_complete)

    def progress_range_parser(self, output):
        """
        Matches lines using the progress_re regex,
        returning a single integer for the % progress.
        """
        min = 0
        max = 0
        match = self.progress_number_of_steps_re.search(output)
        if match:
            max = int(match.group(1))
        return min, max

    def terminate(self):
        if self.process:
            self.process.kill()
            self.accept()


