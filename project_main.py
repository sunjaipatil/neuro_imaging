# -*- coding: utf-8 -*-
"""
This is a GUI aplication to visualise neuro images

Created on Wed Jul 21 13:26:42 2021

@author: sanjay.patil
"""

# imports
import sys, numpy as np
from PyQt5.QtWidgets import QDialog, QApplication, QFileDialog
from PyQt5.QtGui import QPixmap
import nibabel as nib
# The geometry of the interface is written in project_ui script
from project_ui import Ui_Dialog


# A Maindow class with Parent QDialog class is created.

class MainWindow(QDialog):
    def __init__(self):
        # initialise the parent class init method
        super().__init__()
        # get the geometry of the UI
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        # some initialisations
        self.nifti_file = None
        self.data = None
        self.ui.browse.clicked.connect(self.browse_files)
        self.ui.top_slider.sliderReleased.connect(self.top_plot)
        self.ui.side_slider.sliderReleased.connect(self.side_plot)
        self.ui.bottom_slider.sliderReleased.connect(self.bottom_plot)
        #self.ui.top_slider.valueChanged.connect(self.topplot_value)
        #self.ui.plotbutton.clicked.connect(self.plotdata)

    def browse_files(self):
        """
        This function is called to browse files and read nifti image data
        """

        fname = QFileDialog.getOpenFileName(self, 'Open file', 'D:',"*.gz" )
        self.nifti_file = fname[0]
        self.ui.selected_file.setText(self.nifti_file)


        # Read data here
        self.data = nib.load(self.nifti_file)
        self.data.get_data_dtype() == np.dtype(np.int16)
        self.data =self.data.get_fdata()
        self.ui.top_slider.setRange(0, self.data.shape[0]-1)
        self.ui.side_slider.setRange(0, self.data.shape[1]-1)
        self.ui.bottom_slider.setRange(0, self.data.shape[2]-1)

    def top_plot(self):
        """
        Plotting function

        """
        # If data is not loaded slider shouldn't work.

        if self.data == None:
            return

        slider_value = self.ui.top_slider.value()
        plot_data = self.data[slider_value]
        self.ui.topwidget.canvas.ax.imshow(plot_data)
        self.ui.topwidget.canvas.draw()


    def side_plot(self):
        """
        Plotting function for side view
        """
        if self.data == None:
            return

        slider_value = self.ui.side_slider.value()
        plot_data = self.data[:,:,slider_value]
        self.ui.sidewidget.canvas.ax.imshow(plot_data)
        self.ui.sidewidget.canvas.draw()


    def bottom_plot(self):

        if self.data == None:
            return

        slider_value = self.ui.bottom_slider.value()
        plot_data = self.data[:,slider_value,:]
        self.ui.frontwidget.canvas.ax.imshow(plot_data)
        self.ui.frontwidget.canvas.draw()





if __name__ == '__main__':
    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec_())
