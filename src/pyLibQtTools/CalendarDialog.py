
from qgis.PyQt.QtWidgets import QDialog, QCalendarWidget
from qgis.PyQt.QtCore import QDate

class CalendarDialog(QDialog):
    def __init__(self, parent, title = None, date = None):
        super().__init__(parent)
        if not title:
            title = "Select date"
        self.setWindowTitle(title)
        self.calendar = QCalendarWidget(self)
        if not date:
            date = QDate.currentDate()
        self.calendar.setSelectedDate(date)
        self.resize(300, 300)
        self.calendar.resize(300, 300)