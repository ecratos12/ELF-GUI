from PyQt5.QtWidgets import  QFileDialog, QWidget, QApplication, QHBoxLayout, QPushButton


class Window(QWidget):
    def __init__(self):
        super(Window, self).__init__(None)
        layout = QHBoxLayout()
        self.button = QPushButton('click')
        layout.addWidget(self.button)
        self.setLayout(layout)
        self.button.clicked.connect(self.ask_filename)
    def ask_filename(self):
        fname = QFileDialog.getSaveFileName(self, 'title')
        print(fname)
        self.button.setText(fname[0])


app = QApplication([])
window = Window()
window.show()
app.exec_()