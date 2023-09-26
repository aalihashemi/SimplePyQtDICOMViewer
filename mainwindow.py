
from ui_mainwindow import Ui_MainWindow
from enum import Enum
import sys
import time
import numpy as np

from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QVBoxLayout, QMainWindow, QLineEdit, QPushButton
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import QTimer
from PyQt5.QtCore import QRunnable, QObject, QThread, QThreadPool, pyqtSignal as Signal, pyqtSlot as Slot
from simple_dicom_viewer import DicomVolumeLoader

DEFAULT_DICOM_PATH = "imgs"

class mainwindow(QMainWindow):

    def __init__(self):
        super(mainwindow, self).__init__()
        self.ui = Ui_MainWindow()
        
        self.ui.setupUi(self)
        self.uiInitialize()
        self.dicom_handler = DicomVolumeLoader()
        self.multiBtnSignalAvoider = 0

    def closeEvent(self, event):
        print("close app")
        super().closeEvent(event)

    def uiInitialize(self):
        self.setup_ui_connection()
        #self.ui.groupBox_3.setEnabled(False)
        #self.ui.groupBox_2.setEnabled(False)


    def setup_ui_connection(self):
        self.set_radio_btns_connection()
        self.set_inputs_connection()
        self.init_btns_connection()
        self.set_radio_btns_connection() 
        self.set_sliders_connection()

    def set_sliders_connection(self):
        self.ui.sagital_pic_slider.valueChanged.connect(self.on_sagital_pic_slider_changed)
        self.ui.axial_pic_slider.valueChanged.connect(self.on_axial_pic_slider_changed)
        self.ui.coronal_pic_slider.valueChanged.connect(self.on_coronal_pic_slider_changed)

    def set_inputs_connection(self):
        #app.focusChanged.connect(self.lineEdits_focus_handler)
        #self.ui.lineEditLEDCurrent.editingFinished.connect(self.on_ledCurrent_changed)
        pass
        
    def init_btns_connection(self):
        self.ui.btn_load_dicoms.clicked.connect(self.on_btn_load_dicoms_clicked)

    def set_radio_btns_connection(self):
        pass #self.ui.MoveForDuration.clicked.connect(lambda: self.on_radio_btn_clicked(Mode.MOVE_IN_DURATION))
        
        
    #####Slots#####
    def on_btn_load_dicoms_clicked(self):
        if (self.multiSignalEmitsOnBtnClickedHandler() == 0):
            return
        self.dicom_handler = DicomVolumeLoader()
        self.dicom_handler.load_dicom_series(DEFAULT_DICOM_PATH)
        self.ui.axial_pic_slider.setMaximum(self.dicom_handler.get_number_of_axial_slices() - 1)
        self.ui.sagital_pic_slider.setMaximum(self.dicom_handler.get_number_of_sagital_slices() - 1)
        self.ui.coronal_pic_slider.setMaximum(self.dicom_handler.get_number_of_coronal_slices() - 1)

        self.ui.axial_pic_slider.setValue(self.dicom_handler.get_number_of_axial_slices() // 2)
        self.ui.sagital_pic_slider.setValue(self.dicom_handler.get_number_of_sagital_slices() // 2)
        self.ui.coronal_pic_slider.setValue(self.dicom_handler.get_number_of_coronal_slices() // 2)
        self.on_sagital_pic_slider_changed() 
        self.on_axial_pic_slider_changed()
        self.on_coronal_pic_slider_changed()

    def on_sagital_pic_slider_changed(self):
        try:
            self.ui.sagital_pic_label.setPixmap(self.convert_ndarray2qpixmap(
                self.dicom_handler.get_sagital_img(self.ui.sagital_pic_slider.value()).copy())
            )
        except Exception as e:
                print(e)
    def on_axial_pic_slider_changed(self):
        try:
            self.ui.axial_pic_label.setPixmap(self.convert_ndarray2qpixmap(
                self.dicom_handler.get_axial_img(self.ui.axial_pic_slider.value()).copy())
            )
        except Exception as e:
            print(e)
    def on_coronal_pic_slider_changed(self):
        try:
            self.ui.coronal_pic_label.setPixmap(self.convert_ndarray2qpixmap(
                self.dicom_handler.get_coronal_img(self.ui.coronal_pic_slider.value()).copy())
            )
        except Exception as e:
            print(e)
                            
    def multiSignalEmitsOnBtnClickedHandler(self):
        self.multiBtnSignalAvoider += 1
        if (self.multiBtnSignalAvoider < 3):
            return 0
        self.multiBtnSignalAvoider = 0
        return 1
    
    ##
    def convert_ndarray2qpixmap(self, ndarray_img):
        ndarray_img = ((ndarray_img - ndarray_img.min()) * (1/(ndarray_img.max() - ndarray_img.min()) * 255)).astype('uint8')
        # Create QImage from the numpy array
        qimage = QImage(ndarray_img, ndarray_img.shape[1], ndarray_img.shape[0], QImage.Format_Grayscale8)
        # Convert QImage to QPixmap
        return QPixmap.fromImage(qimage)

if __name__=="__main__":
    app = QApplication(sys.argv)
    a = mainwindow()
    a.show()
    sys.exit(app.exec())
