import csv
from OCC.Display.backend import load_backend
from OCC.Core.STEPControl import STEPControl_Reader
from OCC.Core.Graphic3d import *
from PyQt5.QtWidgets import *
from CadConverter import CadConverter

load_backend("pyqt5")

import OCC.Display.qtDisplay as qtDisplay


class App(QDialog):
    def __init__(self):
        super().__init__()
        self.title = "PyQt5 / pythonOCC"
        self.left = 200
        self.top = 100
        self.width = 1500
        self.height = 800
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.createHorizontalLayout()

        windowLayout = QVBoxLayout()
        windowLayout.addWidget(self.horizontalGroupBox)
        self.setLayout(windowLayout)
        self.show()
        self.canvas.InitDriver()
        self.canvas.resize(200, 200)
        self.display = self.canvas._display

    def createHorizontalLayout(self):
        self.horizontalGroupBox = QGroupBox("Display PythonOCC")
        layout = QHBoxLayout()

        disp = QPushButton("Display Box", self)
        disp.clicked.connect(self.displayBOX)
        layout.addWidget(disp)

        eras = QPushButton("Erase Box", self)
        eras.clicked.connect(self.eraseBOX)
        layout.addWidget(eras)

        calc = QPushButton("Calculate Points", self)
        calc.clicked.connect(self.calculateBOX)
        layout.addWidget(calc)

        self.canvas = qtDisplay.qtViewer3d(self)
        layout.addWidget(self.canvas)
        self.horizontalGroupBox.setLayout(layout)

    def displayBOX(self):
        step_reader = STEPControl_Reader()
        step_reader.ReadFile("C:\\Users\\daves\\Documents\\Minor FvdT VDL\\Solidworks\\test object 8 hoeken.STEP")
        step_reader.TransferRoots()
        shape = step_reader.OneShape()
        self.ais_box = self.display.DisplayShape(shape, material=Graphic3d_NOM_ALUMINIUM)[0]
        self.display.FitAll()

    def eraseBOX(self):
        self.display.Context.Erase(self.ais_box, True)

    def calculateBOX(self):
        step = CadConverter("C:\\Users\\daves\\Documents\\Minor FvdT VDL\\Solidworks\\test object 8 hoeken.STEP")

        step.find_holes_in_step()
        step.remove_bottem_positions()

        print(step.holes_list.holes)

        step.holes_list.write_csv()
