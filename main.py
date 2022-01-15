import sys
import random
import time
import datetime
import threading
from PySide6 import QtCore, QtWidgets, QtGui

class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        # --------------------------- Window ---------------------------
        self.setWindowTitle('Pomo Timer')
        self.setFixedSize(950,350)
        self.setStyleSheet("background: #111111;color: #e1e1e1;font-weight:bold;border-style:none;")

        # --------------------------- Widgets ---------------------------
        # Hours
        self.hour_field = QtWidgets.QLineEdit('00')
        self.hour_field.setAlignment(QtCore.Qt.AlignCenter)
        self.hour_field.setFont(QtGui.QFont('Roboto', 120))
        # Minutes
        self.minute_field = QtWidgets.QLineEdit('00')
        self.minute_field.setAlignment(QtCore.Qt.AlignCenter)
        self.minute_field.setFont(QtGui.QFont('Roboto', 120))
        # Seconds
        self.second_field = QtWidgets.QLineEdit('00')
        self.second_field.setAlignment(QtCore.Qt.AlignCenter)
        self.second_field.setFont(QtGui.QFont('Roboto', 120))
        # Colons
        self.separator1 = QtWidgets.QLabel(':')
        self.separator1.setAlignment(QtCore.Qt.AlignCenter)
        self.separator1.setFont(QtGui.QFont('Roboto', 120))
        self.separator2 = QtWidgets.QLabel(':')
        self.separator2.setAlignment(QtCore.Qt.AlignCenter)
        self.separator2.setFont(QtGui.QFont('Roboto', 120))
        # Options
        self.pomo_25_5 = QtWidgets.QPushButton('25 min | 5 min')
        self.pomo_25_5.setFixedHeight(55)
        self.pomo_25_5.setStyleSheet('background:#295299;color:#111111;font-size:28px;')
        self.pomo_45_10 = QtWidgets.QPushButton('45 min | 10 min')
        self.pomo_45_10.setFixedHeight(55)
        self.pomo_45_10.setStyleSheet('background:#295299;color:#111111;font-size:28px;')
        self.pomo_60_15 = QtWidgets.QPushButton('1 hr | 15 min')
        self.pomo_60_15.setFixedHeight(55)
        self.pomo_60_15.setStyleSheet('background:#295299;color:#111111;font-size:28px;')
        # Label
        self.tracker = QtWidgets.QLabel('O-O-O-O-O')
        self.tracker.setStyleSheet('font-size:20px;')
        self.tracker.setAlignment(QtCore.Qt.AlignCenter)
        # Button
        self.start_button = QtWidgets.QPushButton("Start")
        self.start_button.setStyleSheet('background: green;color: #111111;font-size:28px;text-transform:uppercase;')
        self.start_button.setFixedHeight(120)
        # Button
        self.stop_button = QtWidgets.QPushButton("Stop")
        self.stop_button.setStyleSheet('background: red;color: #111111;font-size:28px;text-transform:uppercase;')
        self.stop_button.setFixedHeight(55)

        # --------------------------- Layout ---------------------------
        self.layout = QtWidgets.QGridLayout(self)
        # Add time
        self.layout.addWidget(self.hour_field, 1, 0, 1, 1)
        self.layout.addWidget(self.separator1, 1, 1, 1, 1)
        self.layout.addWidget(self.minute_field, 1, 2, 1, 1)
        self.layout.addWidget(self.separator2, 1, 3, 1, 1)
        self.layout.addWidget(self.second_field, 1, 4, 1, 1)
        # Add timer options
        self.layout.addWidget(self.start_button, 2, 0, 2, 1)
        self.layout.addWidget(self.pomo_25_5, 2, 1, 1, 2)
        self.layout.addWidget(self.pomo_45_10, 2, 3, 1, 2)
        self.layout.addWidget(self.pomo_60_15, 3, 1, 1, 2)
        # Lofi Button
        # self.layout.addWidget(self.tracker, 4, 0, 2, 1)

        # --------------------------- Connect Buttons ---------------------------
        self.start_button.clicked.connect(self.startWork)
        # self.stop_button.clicked.connect(self.stopTimer)
        self.pomo_25_5.clicked.connect(lambda: self.presetTimer(0,25,0))
        self.pomo_45_10.clicked.connect(lambda: self.presetTimer(0,45,0))
        self.pomo_60_15.clicked.connect(lambda: self.presetTimer(1,0,0))

        # --------------------------- Timer Settings ---------------------------
        # Set timer
        self.hour_left = 0
        self.minute_left = 0
        self.second_left = 0
        self.total_time = 0
        self.time_left = 0
        self.preset_active = False
        self.work_timer_active = False
        self.break_timer_active = False
        self.timer_active = False

    @QtCore.Slot()
    def presetTimer(self, hour=0, minute=0, second=0):
        """Updates the UI to display the time in respect to the user's decision."""

        hour = str(hour)
        minute = str(minute)
        second = str(second)

        # Add an extra 0 to single digit numbers
        if int(hour) < 10:
            hour = '0' + hour
        if int(minute) < 10:
            minute = '0' + minute
        if int(second) < 10:
            second = '0' + second

        self.hour_field.setText(hour)
        self.minute_field.setText(minute)
        self.second_field.setText(second)
        # If true: Timer will start break time
        self.preset_active = minute
        if hour == 1:
            self.preset_active = 60

    def setTimer(self):
        """Grabs the time from the label and return the total time in seconds."""

        self.hour_left = int(self.hour_field.text())
        self.minute_left= int(self.minute_field.text())
        self.second_left = int(self.second_field.text())
        total_time_left = self.hour_left * 3600 + self.minute_left * 60 + self.second_left
        # print(total_time_left)
        return total_time_left

    def updateDisplay(self):
        """Update the text field with the current time."""

        # Calculate time left
        if self.time_left > 0:
            hour_left = str(self.time_left // 3600)
            minute_left = str((self.time_left - int(hour_left) * 3600) // 60)
            second_left = str(self.time_left % 60)
            # Add an extra 0 for single digits
            if int(hour_left) < 10:
                hour_left = '0' + hour_left
            if int(minute_left) < 10:
                minute_left = '0' + minute_left
            if int(second_left) < 10:
                second_left = '0' + second_left
            # Update the UI display
            self.hour_field.setText(hour_left)
            self.minute_field.setText(minute_left)
            self.second_field.setText(second_left)
            print(self.hour_field.text() + ':' + self.minute_field.text() + ':' + self.second_field.text())
            time.sleep(1)
            self.updateDisplay()

    def countdown(self):
        while self.time_left > 0:
            self.time_left -= 1
            time.sleep(1)
        # --------------------------
        # TODO: Segmentation fault at the end of timer
        else:
            self.stopTimer()

    def startWork(self):
        # Prevent user from clicking the start button again
        print('button disabled')
        self.start_button.setDisabled(True)
        # Get time in seconds
        self.time_left = self.setTimer()
        self.timer_active = True
        # Create threads
        work_countdown = threading.Thread(target=self.countdown)
        update_work_UI = threading.Thread(target=self.updateDisplay)
        # Start countdown
        work_countdown.start()
        update_work_UI.start()

        # ------------- BREAK ------------- 
        if self.time_left == 0:
            # Straight to break time
            if self.preset_active == 25:
                self.presetTimer(0,15,0)
            elif self.preset_active == 45:
                self.presetTimer(0,10,0)
            elif self.preset_active == 60:
                self.presetTimer(0,5,0)
            # Start button will connect to break timer
            self.start_button.clicked.connect(self.startBreak)
            self.start_button.setEnabled(True)
            print('button active')

    def startBreak(self):
        self.start_button.setDisabled(True)
        # Get time in seconds
        self.time_left = self.setTimer()
        # Create threads
        break_countdown = threading.Thread(target=self.countdown)
        update_break_UI = threading.Thread(target=self.updateDisplay)
        # Start countdown
        break_countdown.start()
        update_break_UI.start()
        # Start button will reset to work timer
        if self.time_left == 0:
            self.stopTimer()

    def stopTimer(self):
        """Resets the UI."""

        self.timer_active = False
        self.time_left = 0
        # if self.preset_active == 25:
        #     self.presetTimer(0,25,0)
        # elif self.preset_active == 45:
        #     self.presetTimer(0,45,0)
        # elif self.preset_active == 60:
        #     self.presetTimer(0,60,0)
        # else:
        self.hour_field.setText('00')
        self.minute_field.setText('00')
        self.second_field.setText('00')
        self.start_button.clicked.connect(self.startWork)
        self.start_button.setEnabled(True)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = MyWidget()
    widget.show()

    sys.exit(app.exec())
