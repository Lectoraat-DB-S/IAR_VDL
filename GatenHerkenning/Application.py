import os
import sys

from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_Transform
from OCC.Core.gp import gp_Trsf, gp_Vec
from OCC.Display import OCCViewer

from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox
from OCC.Core.STEPControl import STEPControl_Reader
from PyQt5.QtWidgets import *
from OCC.Display.backend import load_backend, get_qt_modules
from OCC.Core.Graphic3d import Graphic3d_NOM_ALUMINIUM
from CadConverter import CadConverter

load_backend("pyqt5")

import OCC.Display.qtDisplay as qtDisplay


class Application(QDialog):
    def __init__(self):
        super().__init__()
        self.preview_box = None
        self.shape = None
        self.title = "PyQt5 / pythonOCC"
        self.left = 200
        self.top = 100
        self.width = 1500
        self.height = 800
        self.init_ui()

        self.index = 0

    def init_ui(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.create_vertical_layout()
        self.create_horizontal_layout()

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.horizontalGroupBox)
        self.setLayout(mainLayout)

        self.show()

        QApplication.setStyle(QStyleFactory.create('Fusion'))

        self.canvas.InitDriver()
        self.display = self.canvas._display
        self.display.EnableAntiAliasing()

    def create_vertical_layout(self):
        self.verticalGroupBox = QGroupBox("Actions")
        self.verticalGroupBox.setMaximumWidth(500)
        layout = QVBoxLayout()

        self.input_select_file = QLineEdit("No file selected.")
        layout.addWidget(self.input_select_file)

        button = QPushButton("Select File")
        button.clicked.connect(self.select_file)
        layout.addWidget(button)

        self.input_label_name = QLineEdit()
        self.input_label_name.setReadOnly(True)
        layout.addWidget(self.input_label_name)

        disp = QPushButton("Display Box", self)
        disp.clicked.connect(self.display_shape)
        layout.addWidget(disp)

        eras = QPushButton("Erase Box", self)
        eras.clicked.connect(self.erase_shape)
        layout.addWidget(eras)

        calc = QPushButton("Calculate Points", self)
        calc.clicked.connect(self.calculate_shape)
        layout.addWidget(calc)

        move1 = QPushButton("Move to position 1", self)
        move1.clicked.connect(self.move1)
        layout.addWidget(move1)

        move2 = QPushButton("Move to position 2", self)
        move2.clicked.connect(self.move2)
        layout.addWidget(move2)

        layout.addStretch(1)
        self.verticalGroupBox.setLayout(layout)

    def create_horizontal_layout(self):
        self.horizontalGroupBox = QGroupBox("Display PythonOCC")
        layout = QHBoxLayout()
        layout.addWidget(self.verticalGroupBox)

        self.canvas = qtDisplay.qtViewer3d(self)
        layout.addWidget(self.canvas)
        self.horizontalGroupBox.setLayout(layout)

    def display_shape(self):
        step_reader = STEPControl_Reader()
        step_reader.ReadFile(self.input_select_file.text())
        step_reader.TransferRoots()
        self.shape = step_reader.OneShape()
        self.step_model = self.display.DisplayShape(self.shape, material=Graphic3d_NOM_ALUMINIUM)
        self.display.FitAll()

    def erase_shape(self):
        self.display.Context.Erase(self.step_model, True)

    def calculate_shape(self):
        step = CadConverter(self.shape)
        step.find_holes_in_step()
        step.remove_bottem_positions()

        print(step.holes_list.holes)

        step.holes_list.write_csv()

        self.holes = list(step.holes_list.holes.values())
        # print("a")

    def preview_position(self, x, y, z):
        trsf = gp_Trsf()
        translation_vector = gp_Vec(x-5, y-5, z-5)  # Move the box 50 units along the X-axis
        trsf.SetTranslation(translation_vector)

        if self.preview_box is not None:
            self.display.Context.Erase(self.preview_box, True)

        preview_box = BRepPrimAPI_MakeBox(10.0, 10.0, 10.0).Shape()
        transformed_box = BRepBuilderAPI_Transform(preview_box, trsf, True).Shape()
        self.preview_box = self.display.DisplayShape(transformed_box, color="Darkgreen")[0]
        self.display.FitAll()

    def move1(self):
        self.preview_position(self.holes[self.index].location[0], self.holes[self.index].location[1],
                              self.holes[self.index].location[2])
        self.index += 1

    def move2(self):
        self.preview_position(self.holes[self.index].location[0], self.holes[self.index].location[1],
                              self.holes[self.index].location[2])
        self.index -= 1

    def select_file(self):
        options = QFileDialog.Options()
        # options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                   "STEP Files (*.stp *.step)", options=options)

        if file_name is not None:
            self.selected_file = file_name
            self.input_select_file.setText(self.selected_file)
            base_name = os.path.basename(self.selected_file)
            file_stem = os.path.splitext(base_name)[0]
            self.input_label_name.setReadOnly(False)
            self.input_label_name.setText(file_stem)
            print(f"File selected: {self.selected_file}")
