from OCC.Core.STEPControl import STEPControl_Reader
from OCC.Display.backend import load_backend, get_qt_modules
from OCC.Core.Graphic3d import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt

load_backend("pyqt5")

import OCC.Display.qtDisplay as qtDisplay


class InitScreen(QDialog):
    def __init__(self):
        super().__init__()
        self.title = "Step Covertor"
        self.left = 200
        self.top = 100
        self.width = 1500
        self.height = 800
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.createVerticalLayout()
        self.createHorizontalLayout()
        self.createToolbar()

        windowLayout = QVBoxLayout()
        windowLayout.addWidget(self.horizontalGroupBox)
        self.setLayout(windowLayout)

        self.show()
        self.canvas.InitDriver()
        self.canvas.resize(200, 200)
        self.display = self.canvas._display

    def createVerticalLayout(self):
        self.verticalGroupBox = QGroupBox("Actions")
        layout = QVBoxLayout()

        disp = QPushButton("Display Box", self)
        disp.clicked.connect(self.displayBOX)
        layout.addWidget(disp)

        eras = QPushButton("Erase Box", self)
        eras.clicked.connect(self.eraseBOX)
        layout.addWidget(eras)

        calc = QPushButton("Calculate Points", self)
        calc.clicked.connect(self.calculateBOX)
        layout.addWidget(calc)

        layout.addStretch(1)

        self.verticalGroupBox.setLayout(layout)

    def createHorizontalLayout(self):
        self.horizontalGroupBox = QGroupBox("Display PythonOCC")
        layout = QHBoxLayout()

        layout.addWidget(self.verticalGroupBox)

        self.canvas = qtDisplay.qtViewer3d(self)
        layout.addWidget(self.canvas)
        self.horizontalGroupBox.setLayout(layout)

    def createToolbar(self):
        toolbar = QToolBar("Toolbar")
        maximizeAction = QAction("Maximize", self)
        maximizeAction.triggered.connect(self.maximizeWindow)
        toolbar.addAction(maximizeAction)

        # Here, we add the toolbar to the layout
        layout = self.layout()
        layout.addWidget(toolbar)

    def maximizeWindow(self):
        self.showMaximized()

    def displayBOX(self):
        step_reader = STEPControl_Reader()
        step_reader.ReadFile("C:\\Users\\daves\\Documents\\Minor FvdT VDL\\Solidworks\\115-04621-02.stp")
        step_reader.TransferRoots()
        shape = step_reader.OneShape()
        self.ais_box = self.display.DisplayShape(shape, material=Graphic3d_NOM_ALUMINIUM)[0]
        self.display.FitAll()

    def eraseBOX(self):
        self.display.Context.Erase(self.ais_box, True)

    @staticmethod
    def calculateBOX(self):
        # step = CadConverter("C:\\Users\\daves\\Documents\\Minor FvdT VDL\\Solidworks\\test object 8 hoeken.STEP")
        #
        # step.find_holes_in_step()
        # step.remove_bottem_positions()
        #
        # print(step.holes_list.holes)
        #
        # step.holes_list.write_csv()
        print("abc")
