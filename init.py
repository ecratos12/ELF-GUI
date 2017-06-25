import sys
from PyQt5.QtWidgets import (QApplication,
							 QWidget,
							 QLabel,
							 QGridLayout,
							 QAction,
							 QMainWindow,
							 QPushButton,
							 QMessageBox,
							 QFileDialog,
							 QSizePolicy)
from PyQt5.QtGui import QIcon
# from PyQt5.QtCore import QCoreApplication
import pandas as pd
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

import random


class Example(QMainWindow):

	def __init__(self):
		super().__init__()
		self.interface = QWidget(
			self)  # grid layout don't working with QMainWindow, so I attached all buttons, labels, etc.. to @interface
		self.init_ui()

	def init_ui(self):
		self.statusBar().showMessage('Ready')
		menubar = self.menuBar()
		fileMenu = menubar.addMenu('&File')

		openFile = QAction('Open', self)
		openFile.setShortcut('Ctrl+O')
		openFile.setStatusTip('Load data')
		openFile.triggered.connect(self.load_file)
		fileMenu.addAction(openFile)

		exitAction = QAction('&Quit!1', self)
		exitAction.setShortcut('Ctrl+Q')
		exitAction.triggered.connect(self.closeEvent)
		exitAction.setStatusTip('Leave the app')
		fileMenu.addAction(exitAction)

		# ----------------------
		# setting the @interface
		# ----------------------
		self.setCentralWidget(self.interface)

		self.interface.load_btn = QPushButton('Load File', self.interface)
		self.interface.plot_btn = QPushButton('Plot data', self.interface)
		self.interface.topFileName = QLabel(self.interface)
		self.interface.result_log = QLabel(self.interface)

		self.grid = QGridLayout(self.interface)
		self.grid.setSpacing(10)
		self.grid.addWidget(self.interface.load_btn, 0, 0)
		self.grid.addWidget(self.interface.plot_btn, 1, 0)
		self.grid.addWidget(self.interface.topFileName, 0, 1)
		self.grid.addWidget(self.interface.result_log, 1, 1)
		self.setLayout(self.grid)

		self.interface.plot_btn.clicked.connect(self.plot)
		self.interface.load_btn.clicked.connect(self.load_file)

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

	def load_file(self):
		fname = QFileDialog.getOpenFileName(self, 'Load data')[0]
		if fname:
			self.data = pd.read_csv(fname, delimiter=' ', header=None)
			fname = fname.split('/')
			fname = fname[len(fname) - 1]
			self.interface.topFileName.setText('Loaded data file is <b>' + fname + '</b>')
			self.interface.topFileName.resize(self.interface.topFileName.sizeHint())
		else:
			pass

	def plot(self):
		# self.interface.result_log.setText('<b>research done, congrats!</b>')
		# self.interface.result_log.resize(self.interface.result_log.sizeHint())
		self.interface.graph = PlotCanvas(self.interface, width=5, height=4)
		self.grid.addWidget(self.interface.graph, 0, 2, 3, 1)


class PlotCanvas(FigureCanvas):
	def __init__(self, parent=None, width=5, height=4, dpi=100):
		fig = Figure(figsize=(width, height), dpi=dpi)
		self.axes = fig.add_subplot(111)

		FigureCanvas.__init__(self, fig)
		self.setParent(parent)
		FigureCanvas.setSizePolicy(self,
								   QSizePolicy.Expanding,
								   QSizePolicy.Expanding)
		FigureCanvas.updateGeometry(self)
		self.plot()

	def plot(self):
		data = [random.random() for i in range(25)]
		ax = self.figure.add_subplot(111)
		ax.plot(data, 'r-')
		ax.set_title('Lol(kek)')
		self.draw()


if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = Example()
	sys.exit(app.exec_())