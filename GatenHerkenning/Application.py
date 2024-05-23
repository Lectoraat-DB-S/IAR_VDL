import os
import random
import sys

from Hole import Hole

from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Fuse
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_Transform
from OCC.Core.gp import gp_Trsf, gp_Vec, gp_Ax2, gp_Pnt, gp_Dir, gp_Ax3
from OCC.Display import OCCViewer
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from vtkmodules import qt

from StepModel import StepModel

from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox, BRepPrimAPI_MakeCylinder, BRepPrimAPI_MakeCone
from OCC.Core.STEPControl import STEPControl_Reader
from PyQt5.QtWidgets import *
from OCC.Display.backend import load_backend, get_qt_modules
from OCC.Core.Graphic3d import Graphic3d_NOM_ALUMINIUM

load_backend("pyqt5")

import OCC.Display.qtDisplay as qtDisplay


class Application(QDialog):
    def __init__(self):
        super().__init__()
        self.preview_cone = None
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

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.horizontalGroupBox)
        self.setLayout(main_layout)

        self.show()

        QApplication.setStyle(QStyleFactory.create('Fusion'))

        self.canvas.InitDriver()
        self.display = self.canvas._display
        self.display.EnableAntiAliasing()

    def create_vertical_layout(self):
        self.verticalGroupBox = QGroupBox("Actions")
        self.verticalGroupBox.setMaximumWidth(800)
        layout = QVBoxLayout()

        self.input_select_file = QLineEdit("No file selected.")
        layout.addWidget(self.input_select_file)

        button = QPushButton("Select File")
        button.clicked.connect(self.select_file)
        layout.addWidget(button)

        self.input_label_name = QLineEdit()
        self.input_label_name.setReadOnly(True)
        layout.addWidget(self.input_label_name)

        load = QPushButton("Load Step Model", self)
        load.clicked.connect(self.button_load)
        layout.addWidget(load)

        eras = QPushButton("Erase Box", self)
        eras.clicked.connect(self.erase_shape)
        layout.addWidget(eras)

        move1 = QPushButton("Move to position 1", self)
        move1.clicked.connect(self.move1)
        layout.addWidget(move1)

        move2 = QPushButton("Move to position 2", self)
        move2.clicked.connect(self.move2)
        layout.addWidget(move2)

        self.scrollArea = QScrollArea(self)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget(self)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.scrollAreaLayout = QVBoxLayout(self.scrollAreaWidgetContents)

        self.scrollAreaLayout.setContentsMargins(0, 0, 0, 0)
        self.scrollAreaLayout.setSpacing(0)
        # self.scrollAreaWidgetContents.setContentsMargins(0, 0, 0, 0)
        # self.scrollAreaWidgetContents.setLayout(self.scrollAreaLayout)

        layout.addWidget(self.scrollArea)

        self.create_scroll_list()

        # layout.addStretch(1)
        self.verticalGroupBox.setLayout(layout)

    def create_horizontal_layout(self):
        self.horizontalGroupBox = QGroupBox("Display PythonOCC")
        layout = QHBoxLayout()
        layout.addWidget(self.verticalGroupBox)

        self.canvas = qtDisplay.qtViewer3d(self)
        layout.addWidget(self.canvas)
        self.horizontalGroupBox.setLayout(layout)

    def create_scroll_list(self):
        for i in reversed(range(self.scrollAreaLayout.count())):
            widget_to_remove = self.scrollAreaLayout.itemAt(i).widget()
            # remove it from the layout list
            self.scrollAreaLayout.removeWidget(widget_to_remove)
            # remove it from the gui
            widget_to_remove.setParent(None)

        self.holes = []

        for x in range(30):
            self.holes.append(Hole((random.randint(0, 100), random.randint(0, 100), random.randint(0, 100)),
                                   (random.randint(0, 100), random.randint(0, 100), random.randint(0, 100)),
                                   random.randint(2, 12), random.randint(2, 12)))

        for hole in self.holes:
            hole_widget = self.create_hole_widget(hole)
            self.scrollAreaLayout.addWidget(hole_widget)

    def create_hole_widget(self, hole):
        hole_widget = QWidget(self)
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        common_style = """
                        background-color: white;
                        border: 1px solid gray;
                        padding: 2px;
                        border-radius: 3px;
                    """

        widgets = [
            QLabel(f"<b> X</b>"),
            QLabel(f"{hole.location[0]}"),
            QLabel(f"<b>Y</b>"),
            QLabel(f"{hole.location[1]}"),
            QLabel(f"<b>Z</b>"),
            QLabel(f"{hole.location[2]}"),
            QLabel(f"<b>rX</b>"),
            QLabel(f"{hole.direction[0]}"),
            QLabel(f"<b>rY</b>"),
            QLabel(f"{hole.direction[1]}"),
            QLabel(f"<b>rZ</b>"),
            QLabel(f"{hole.direction[2]}")
        ]

        direction_flip_button = QPushButton("Flip")
        direction_flip_button.clicked.connect(lambda: self.flip_direction)

        for widget in widgets:
            widget.setStyleSheet(common_style)
            layout.addWidget(widget)

        hole_widget.setLayout(layout)
        return hole_widget

    def flip_direction(self, hole):
        hole.direction = tuple(-d for d in hole.direction)
        self.create_scroll_list()

    def button_load(self):
        if self.input_label_name != "No file selected.":
            self.step = StepModel(self.input_select_file.text())

        self.model = self.display.DisplayShape(self.step.shape, material=Graphic3d_NOM_ALUMINIUM)
        self.display.FitAll()
        self.create_scroll_list()

    def erase_shape(self):
        self.display.Context.Erase(self.model, True)

    def preview_position(self, x, y, z, rx, ry, rz):
        trsf = gp_Trsf()

        translation_vector = gp_Vec(x, y, z)  # Move the box 50 units along the X-axis

        new_direction = gp_Dir(rx, ry, rz)  # Example: align with the X-axis
        new_up_direction = gp_Dir(0, 1, 0)  # Example: align with the Y-axis

        # Define the rotation axis system using the direction vectors
        rotation_axis_system = gp_Ax3(gp_Pnt(-3, -3, -15), new_direction, new_up_direction)

        trsf.SetTransformation(rotation_axis_system)

        trsf.SetTranslation(translation_vector)

        if self.preview_cone is not None:
            self.display.Context.Erase(self.preview_cone, True)

        cone_radius = 6
        cone_height = 15

        cone_position = gp_Ax2(gp_Pnt(0, 0, 0), gp_Dir(rx, ry, rz))
        cone = BRepPrimAPI_MakeCone(cone_position, cone_radius, 0, cone_height).Shape()

        transformed_cone = BRepBuilderAPI_Transform(cone, trsf, True).Shape()
        self.preview_cone = self.display.DisplayShape(transformed_cone, color="green")[0]

    def move1(self):
        if self.index < len(self.step.holes) - 1:
            self.index += 1
            self.preview_position(*self.step.holes[self.index].location, *self.step.holes[self.index].direction)

    def move2(self):
        if self.index > 0:
            self.index -= 1
            self.preview_position(*self.step.holes[self.index].location, *self.step.holes[self.index].direction)

    def select_file(self):
        options = QFileDialog.Options()
        # options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                   "STEP Files (*.stp *.step)", options=options)

        if file_name:
            self.selected_file = file_name
            self.input_select_file.setText(self.selected_file)
            base_name = os.path.basename(self.selected_file)
            file_stem = os.path.splitext(base_name)[0]
            self.input_label_name.setReadOnly(False)
            self.input_label_name.setText(file_stem)
            print(f"File selected: {self.selected_file}")
