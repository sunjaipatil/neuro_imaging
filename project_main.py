# -*- coding: utf-8 -*-
"""
This is a GUI aplication to visualise neuro images

Created on Wed Jul 21 13:26:42 2021

@author: sanjay.patil
"""

# imports
import sys, numpy as np
import os
from PyQt5.QtWidgets import QDialog, QApplication, QFileDialog
from PyQt5.QtGui import QPixmap
import nibabel as nib, pickle,gzip
# The geometry of the interface is written in project_ui script
from project_ui import Ui_Dialog
from matplotlib.patches import Rectangle
from matplotlib.widgets import RectangleSelector
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
        self.mask_file = None
        self.mask_data = None
        self.ui.browse.clicked.connect(self.browse_files)


        # slider released for showing the image
        self.ui.top_slider.sliderReleased.connect(self.top_plot)
        self.ui.side_slider.sliderReleased.connect(self.side_plot)
        self.ui.bottom_slider.sliderReleased.connect(self.bottom_plot)
        self.ui.top_slider.valueChanged.connect(self.top_value)
        self.ui.side_slider.valueChanged.connect(self.side_value)
        self.ui.bottom_slider.valueChanged.connect(self.bottom_value)
        # value changed to connect it to value displayed




        #self.ui.topwidget.canvas.mpl_connect('key_press_event', self.shift_key)
        self.ui.topwidget.canvas.mpl_connect("button_press_event",self.top_press)
        #self.ui.topwidget.canvas.mpl_connect("button_release_event",self.on_press)


        self.rs = RectangleSelector(self.ui.topwidget.canvas.ax, self.line_select_callback,
                                                drawtype='box', useblit=False,
                                                button=[1, 3],  # don't use middle button
                                                minspanx=2, minspany=2,
                                                rectprops=dict(facecolor="green", alpha=0.2, fill=False),
                                                interactive=True)

        self.rs.set_active(False)

        # initialise rectangle co-ordinates

        self.x1, self.x2, self.y1, self.y2 = None, None, None, None
        self.ui.add_button.clicked.connect(self.add_patch)

        self.ui.save_button.clicked.connect(self.save_file)
        #self.ui.topwidget.mpl_connect("button_press_event", self.on_press)
        #self.ui.top_slider.valueChanged.connect(self.topplot_value)
        #self.ui.plotbutton.clicked.connect(self.plotdata)


    def top_press(self, event):
        if not self.ui.checkbox.isChecked():
            x_index = int(event.xdata)
            y_index = int(event.ydata)
            self.x0 = event.xdata
            self.y0 = event.ydata
            self.side_plot(index_val = y_index)
            self.bottom_plot(index_val = x_index)
        if self.ui.checkbox.isChecked():
            if event.button == 1 or event.button == 3 and not self.rs.active:
                self.rs.set_active(True)
            else:
                self.rs.set_active(False)
        return



    def line_select_callback(self, eclick, erelease):
        self.x1, self.y1 = eclick.xdata, eclick.ydata
        self.x2, self.y2 = erelease.xdata, erelease.ydata
        #print("(%3.2f, %3.2f) --> (%3.2f, %3.2f)" % (x1, y1, x2, y2))
        #print(" The button you used were: %s %s" % (eclick.button, erelease.button))


        self.rs.set_active(False)
        return


    def browse_files(self):
        """
        This function is called to browse files and read nifti image data
        """

        fname = QFileDialog.getOpenFileName(self, 'Open file', 'D:',"*nii.gz" )
        self.nifti_file = fname[0]
        self.ui.selected_file.setText(self.nifti_file)

        if not self.nifti_file:
            return
        # Read data here
        self.data = nib.load(self.nifti_file)
        self.data.get_data_dtype() == np.dtype(np.int16)
        self.data =self.data.get_fdata()
        self.ui.top_slider.setRange(0, self.data.shape[0]-1)
        self.ui.side_slider.setRange(0, self.data.shape[1]-1)
        self.ui.bottom_slider.setRange(0, self.data.shape[2]-1)
        self.output_data = np.zeros(self.data.shape)
        if self.ui.overlay_checkbox:
            output_file = self.nifti_file[:-7]+'_output.pkl.gz'
            if not os.path.exists(output_file):

                self.ui.message_label.setText("Sorry there in no output file to overlap")
            else:
                self.mask_file = output_file
                self.mask_data = pickle.load(gzip.open(self.mask_file, 'r'))

        return

    def top_plot(self):
        """
        Plotting function

        """
        # If data is not loaded slider shouldn't work.

        if not self.nifti_file:#:== None:
            return
        # plots as well as writes down the value on a label

        # if the mask file need to overlaid on top of the data value

        slider_value = self.ui.top_slider.value()
        plot_data = self.data[slider_value]
        if self.mask_file and self.ui.overlay_checkbox:
            # take the cross section corresponding to slider value
            mask_data = self.mask_data[slider_value]
            inds = np.where(mask_data==1)
            plot_data[inds] = 1.

        self.ui.topwidget.canvas.ax.imshow(plot_data)
        self.ui.topwidget.canvas.draw()
        return

    def side_plot(self, index_val = None):
        """
        Plotting function for side view
        """
        if not self.nifti_file:
            return
        if not index_val:
            slider_value = self.ui.side_slider.value()
            plot_data = self.data[:,:,slider_value]
        else:
            self.ui.side_slider.setValue(index_val)
            slider_value = self.ui.side_slider.value()
            plot_data = self.data[:,:,slider_value]
            self.side_value()
        if self.mask_file and self.ui.overlay_checkbox:
            # take the cross section corresponding to slider value
            mask_data = self.mask_data[:,:,slider_value]
            inds = np.where(mask_data==1)
            plot_data[inds] = 1.


        self.ui.sidewidget.canvas.ax.imshow(plot_data)
        self.ui.sidewidget.canvas.draw()

        return


    def bottom_plot(self, index_val = None):

        if not self.nifti_file:
            return

        if not index_val:
            slider_value = self.ui.bottom_slider.value()
            plot_data = self.data[:,slider_value,:]

        else:
            self.ui.bottom_slider.setValue(index_val)
            slider_value = self.ui.bottom_slider.value()
            plot_data = self.data[:,slider_value,:]
            self.side_value()

        if self.mask_file and self.ui.overlay_checkbox:
            # take the cross section corresponding to slider value

            mask_data = self.mask_data[:,slider_value,:]
            inds = np.where(mask_data==1)
            plot_data[inds] = 1.
        self.ui.frontwidget.canvas.ax.imshow(plot_data)
        self.ui.frontwidget.canvas.draw()
        return

    def add_patch(self):

        if not self.x1 or not self.x2 or not self.y1 or not self.y2:
            return
        i = self.ui.top_slider.value()
        j1, j2 = int(self.y1), int(self.y2)
        k1, k2 = int(self.x1), int(self.x2)

        self.output_data[i][j1:j2, k1:k2] = np.ones((abs(j2-j1), abs(k2-k1)))

        return

    def save_file(self):


        if not self.nifti_file:
            return

        output_file = self.nifti_file[:-7]+'_output.pkl.gz'
        pickle.dump(self.output_data, gzip.open(output_file,'w'))

    def top_value(self):
        self.ui.top_value.setText(str(self.ui.top_slider.value()))

    def side_value(self):
        self.ui.side_value.setText(str(self.ui.side_slider.value()))

    def bottom_value(self):
        self.ui.bottom_value.setText(str(self.ui.bottom_slider.value()))




if __name__ == '__main__':
    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec_())
