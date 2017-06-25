import sys
from PyQt5.QtWidgets import (QApplication, QLabel, QGridLayout,
							 QAction, QMainWindow, QPushButton,
							 QMessageBox, QFileDialog)
from PyQt5.QtGui import QIcon
# from PyQt5.QtCore import QCoreApplication





class Example(QMainWindow):

	def __init__(self):
		super().__init__()
		self.init_ui()

	def init_ui(self):
		# self.setToolTip('This is the <b>ELF</b> widget')
		self.statusBar().showMessage('Ready')

		self.menubar = self.menuBar()
		self.fileMenu = self.menubar.addMenu('&File')

		self.openFile = QAction('Open', self)
		self.openFile.setShortcut('Ctrl+O')
		self.openFile.setStatusTip('Load data')
		self.openFile.triggered.connect(self.load_file)
		self.fileMenu.addAction(self.openFile)

		self.exitAction = QAction('&Rage Quit!1', self)
		self.exitAction.setShortcut('Ctrl+Q')
		self.exitAction.triggered.connect(self.closeEvent)
		self.exitAction.setStatusTip('Leave the app')
		self.fileMenu.addAction(self.exitAction)

		self.load_btn = QPushButton('Load File', parent=self)
		self.res_btn = QPushButton('Do research!', parent=self)
		self.res_btn.resize(self.res_btn.sizeHint())  # recommended size
		self.load_btn.resize(self.res_btn.sizeHint())
		self.res_btn.move(0, 50)
		self.load_btn.move(0, 25)

		self.res_btn.clicked.connect(self.lesya_write_cod_function)
		self.load_btn.clicked.connect(self.load_file)

		self.topFileName = QLabel(self)
		self.topFileName.move(75, 30)

		self.result_log = QLabel(self)
		self.result_log.move(75, 55)

		grid = QGridLayout(self)
		grid.setSpacing(10)
		grid.addWidget(self.load_btn, 0, 0)
		grid.addWidget(self.res_btn, 1, 0)
		grid.addWidget(self.topFileName, 0, 1)

		self.setFixedSize(300, 240)
		self.setWindowTitle('ELF Data GUI')
		self.setWindowIcon(QIcon('icon.png'))

	def closeEvent(self, event):  # it is template QWidget function
		reply = QMessageBox.question(self, 'Message',
									 "Are you sure to quit?",
									 QMessageBox.Yes | QMessageBox.No)
		if reply == QMessageBox.Yes:
			event.accept()
		else:
			event.ignore()

	def load_file(self):
		fname = QFileDialog.getOpenFileName(self, 'Load data')[0].split('/')
		fname = fname[len(fname)-1]
		if fname:
			self.topFileName.setText('Loaded data file is <b>' + fname + '</b>')  #
			self.topFileName.resize(self.topFileName.sizeHint())
			with open(fname, 'r') as f:
				pass
		else:
			pass

	def lesya_write_cod_function(self):
		self.result_log.setText('<b>research done, congrats!</b>')
		self.result_log.resize(self.result_log.sizeHint())


if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = Example()
	ex.show()
	sys.exit(app.exec_())