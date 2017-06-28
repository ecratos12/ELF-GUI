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
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolBar
from matplotlib.figure import Figure
import reader



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
		exitAction.setStatusTip('Leave the program')
		fileMenu.addAction(exitAction)

		helpMenu = menubar.addMenu('&Help')
		aboutAction = QAction('&About', self)
		aboutAction.setShortcut('F1')
		aboutAction.triggered.connect(self.on_about)
		aboutAction.setStatusTip('About the program')
		helpMenu.addAction(aboutAction)

		# ----------------------
		# setting the @interface
		# ----------------------
		self.setCentralWidget(self.interface)

		self.interface.load_btn = QPushButton('Load File', self.interface)
		self.interface.plot_btn = QPushButton('Plot data', self.interface)
		self.interface.topFileName = QLabel(self.interface)
		self.interface.dataLabel = QLabel(self.interface)
		self.interface.timeLabel = QLabel(self.interface)

		self.grid = QGridLayout(self.interface)
		self.grid.setSpacing(5)
		self.grid.addWidget(self.interface.load_btn, 0, 0)
		self.grid.addWidget(self.interface.topFileName, 1, 0)
		self.grid.addWidget(self.interface.plot_btn, 2, 0)
		self.grid.addWidget(self.interface.dataLabel, 3, 0)
		self.grid.addWidget(self.interface.timeLabel, 4, 0)
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
			self.channel1, self.channel2, self.header = reader.read_data_from_file(fname)
			fname = fname.split('/')
			fname = fname[len(fname) - 1]
			self.interface.topFileName.setText('Loaded data: <b>' + fname + '</b>. Rows: <b>'
											   + str(len(self.channel1)) + '</b>')
			self.interface.topFileName.resize(self.interface.topFileName.sizeHint())
			self.interface.dataLabel.setText('DATE: <b>' + fname[:8] + '</b>')
			self.interface.dataLabel.resize(self.interface.dataLabel.sizeHint())
			self.interface.timeLabel.setText('TIME: <b>' + fname[8:10] + ':' + fname[10:12] + '</b>')
			self.interface.timeLabel.resize(self.interface.timeLabel.sizeHint())

		else:
			pass

	def plot(self):
		self.interface.graph = PlotCanvas(self.channel1, self.channel2, self.header, self.interface, width=16, height=12)
		self.interface.plotToolBar = NavigationToolBar(self.interface.graph, self.interface)
		self.grid.addWidget(self.interface.graph, 0, 1, 10, 1)
		self.grid.addWidget(self.interface.plotToolBar, 10, 1)

	def on_about(self):
		msg = """
Gorgeous
Edi
To
R
En
Krakow
Telescope
		"""
		QMessageBox.about(self, "About the ELF-gui", msg.strip())


class PlotCanvas(FigureCanvas):
	def __init__(self, channel1, channel2, header, parent=None, width=4, height=3, dpi=100):
		self.figure = Figure(figsize=(width, height), dpi=dpi)
		self.channel1 = channel1
		self.channel2 = channel2
		self.header = header
		FigureCanvas.__init__(self, self.figure)
		self.mpl_connect('motion_notify_event', self.onMotion)
		self.setParent(parent)
		FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
		FigureCanvas.updateGeometry(self)
		self.plot()

	def plot(self):
		x = []
		if len(self.channel1) < 53000:
			for i in range(len(self.channel1)):
				x.append((i+1)/175.95)
		else:
			for i in range(len(self.channel1)):
				x.append((i+1)/887.7841)
		self.ax1 = self.figure.add_subplot(211)
		self.ax1.clear()
		self.ax1.grid()
		self.ax1.plot(x, self.channel1, color='red')
		self.ax1.plot(x, self.channel2)
		self.ax2 = self.figure.add_subplot(212)
		self.ax2.clear()
		self.ax2.grid()
		self.ax2.plot(x, self.channel1, color='red')
		self.ax2.plot(x, self.channel2)
		self.figure.tight_layout(pad=1.6)
		self.draw()

	def onMotion(self, event):
		self.parent().parent().statusBar().showMessage('%.6s, %.8s' %(event.xdata, event.ydata))


if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = Example()
	sys.exit(app.exec_())