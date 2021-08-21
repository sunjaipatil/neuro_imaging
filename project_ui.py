# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'nand_plotui.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!

# Imports
from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1108, 1039)
        self.topwidget = MplWidget(Dialog)
        self.topwidget.setGeometry(QtCore.QRect(130, 50, 381, 291))
        self.topwidget.setObjectName("topwidget")
        self.sidewidget = MplWidget(Dialog)
        self.sidewidget.setGeometry(QtCore.QRect(570, 50, 381, 291))
        self.sidewidget.setObjectName("sidewidget")
        self.frontwidget = MplWidget(Dialog)
        self.frontwidget.setGeometry(QtCore.QRect(130, 360, 381, 291))
        self.frontwidget.setObjectName("frontwidget")
        self.selected_file = QtWidgets.QLineEdit(Dialog)
        self.selected_file.setGeometry(QtCore.QRect(130, 5, 241, 31))
        self.selected_file.setObjectName("selected_file")
        self.browse = QtWidgets.QPushButton(Dialog)
        self.browse.setGeometry(QtCore.QRect(420, 5, 111, 31))
        #self.browse.setObjectName("browse")
        self.top_slider = QtWidgets.QSlider(Dialog)
        self.top_slider.setGeometry(QtCore.QRect(160, 40, 300, 22))
        self.top_slider.setOrientation(QtCore.Qt.Horizontal)
        self.top_slider.setObjectName("top_slider")

        self.side_slider = QtWidgets.QSlider(Dialog)
        self.side_slider.setGeometry(QtCore.QRect(630, 40, 300, 22))
        self.side_slider.setOrientation(QtCore.Qt.Horizontal)
        self.side_slider.setObjectName("side_slider")
        self.bottom_slider = QtWidgets.QSlider(Dialog)
        self.bottom_slider.setGeometry(QtCore.QRect(160, 650, 300, 22))
        self.bottom_slider.setOrientation(QtCore.Qt.Horizontal)
        self.bottom_slider.setObjectName("bottom_slider")

        self.top_slider.setValue(0)
        self.side_slider.setValue(0)
        self.bottom_slider.setValue(0)

        self.checkbox = QtWidgets.QCheckBox(Dialog)
        self.checkbox.setGeometry(QtCore.QRect(100, 40, 30, 22))
        self.checkbox.setChecked(False)
        # slider pagesteps
        self.top_slider.setPageStep(1)
        self.side_slider.setPageStep(1)
        self.bottom_slider.setPageStep(1)
        # slider ticks
        self.top_slider.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.side_slider.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.bottom_slider.setTickPosition(QtWidgets.QSlider.TicksBelow)


        # slider values display
        self.top_value = QtWidgets.QLineEdit(Dialog)
        self.top_value.setGeometry(QtCore.QRect(520, 40, 40, 40))

        self.browse.setText("Browse")
        self.side_value = QtWidgets.QLineEdit(Dialog)
        self.side_value.setGeometry(QtCore.QRect(980, 40, 40, 40))

        self.bottom_value = QtWidgets.QLineEdit(Dialog)
        self.bottom_value.setGeometry(QtCore.QRect(520, 630, 40, 40))



        #Push button
        self.add_button = QtWidgets.QPushButton(Dialog)
        self.add_button.setGeometry(QtCore.QRect(70, 80, 75, 40))
        self.add_button.setText("Capture")


        #Save button_press_event
        self.save_button = QtWidgets.QPushButton(Dialog)
        self.save_button.setGeometry(QtCore.QRect(70, 150, 70, 40))
        self.save_button.setText("Save")

        # Overlay select button
        self.overlaylabel = QtWidgets.QLabel(Dialog)
        self.overlaylabel.setGeometry(QtCore.QRect(720, 10, 85, 22))
        self.overlaylabel.setText("Overlay Label")
        self.overlay_checkbox = QtWidgets.QCheckBox(Dialog)
        self.overlay_checkbox.setGeometry(QtCore.QRect(900, 10, 30, 22))
        self.overlay_checkbox.setChecked(False)


        # Message Label
        self.message_label = QtWidgets.QLabel(Dialog)
        self.message_label.setGeometry(QtCore.QRect(520, 500, 180, 22))
        self.message_label.setStyleSheet("color:red")
# The matplotlib is not a standard PyQt5 widget, so a new MplWidget class has been created under the PyQt5 widget class
from mplwidget import MplWidget


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
