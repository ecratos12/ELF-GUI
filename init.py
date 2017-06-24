import sys
from PyQt5.QtWidgets import (QApplication, QLabel, QGridLayout, QAction, QMainWindow, QPushButton, QMessageBox)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QCoreApplication


def lesya_write_cod_function():
	print('research done, congrats!')


class Example(QMainWindow):

	def __init__(self):
		super().__init__()
		self.init_ui()

	def init_ui(self):
		# self.setToolTip('This is the <b>ELF</b> widget')
		self.statusBar().showMessage('Ready')

		menubar = self.menuBar()
		fileMenu = menubar.addMenu('&File')
		exitAction = QAction("&Rage Quit!1", self)
		exitAction.setShortcut("Ctrl+Q")
		exitAction.triggered.connect(self.closeEvent)
		exitAction.setStatusTip("Leave the app")
		fileMenu.addAction(exitAction)

		load_btn = QPushButton('Load File', parent=self)
		res_btn = QPushButton('Do research!', parent=self)
		res_btn.resize(res_btn.sizeHint())  # recommended size
		load_btn.resize(res_btn.sizeHint())
		res_btn.move(0, 50)
		load_btn.move(0, 25)

		res_btn.clicked.connect(lesya_write_cod_function)

		self.setFixedSize(300, 240)
		self.setWindowTitle('ELF Data GUI')
		self.setWindowIcon(QIcon('icon.png'))
		self.show()

	def closeEvent(self, event):  # it is template QWidget function
		reply = QMessageBox.question(self, 'Message',
									 "Are you sure to quit?",
									 QMessageBox.Yes | QMessageBox.No)
		if reply == QMessageBox.Yes:
			event.accept()
		else:
			event.ignore()

if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = Example()
	sys.exit(app.exec_())