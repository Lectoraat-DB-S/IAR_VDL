from OCC.Core.STEPControl import STEPControl_Reader
from OCC.Display.backend import load_backend, get_qt_modules
from OCC.Core.Graphic3d import *
from PyQt5.QtWidgets import *
# from CadConverter import CadConverter

load_backend("pyqt5")

import OCC.Display.qtDisplay as qtDisplay


class Screen(QDialog):
    def __init__(self, horizontal_offset=450, vertical_offset=200, width=1000, height=650, title="Title"):
        super().__init__()
        self.title = title
        self.horizontal_offset = horizontal_offset
        self.vertical_offset = vertical_offset
        self.width = width
        self.height = height
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.horizontal_offset, self.vertical_offset, self.width, self.height)
        self.createVerticalLayout()

        windowLayout = QVBoxLayout()

        windowLayout.addWidget(self.verticalGroupBox)
        self.setLayout(windowLayout)

        self.show()
        # self.canvas.InitDriver()
        # self.canvas.resize(200, 200)
        # self.display = self.canvas._display

    def createVerticalLayout(self):
        self.verticalGroupBox = QGroupBox("Actions")
        layout = QVBoxLayout()

        disp = QPushButton("Display Box", self)
        disp.clicked.connect(self.displayBOX)
        layout.addWidget(disp)

        eras = QPushButton("Erase Box", self)
        eras.clicked.connect(self.eraseBOX)
        layout.addWidget(eras)

        layout.addStretch(1)

        self.verticalGroupBox.setLayout(layout)

    def displayBOX(self):
        step_reader = STEPControl_Reader()
        step_reader.ReadFile("C:\\Users\\daves\\Documents\\Minor FvdT VDL\\Solidworks\\115-04621-02.stp")
        step_reader.TransferRoots()
        shape = step_reader.OneShape()
        self.ais_box = self.display.DisplayShape(shape, material=Graphic3d_NOM_ALUMINIUM)[0]
        self.display.FitAll()

    def eraseBOX(self):
        self.display.Context.Erase(self.ais_box, True)