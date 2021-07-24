import PyQt5.QtWidgets as qtw

class MainWindow(qtw.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Calculator')
        self.show()
app= qtw.QApplication([])
mw = MainWindow()
app.exec_()
