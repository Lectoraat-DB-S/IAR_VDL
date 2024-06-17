import os
import random
import sys

from Hole import Hole

from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Fuse
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_Transform
from OCC.Core.gp import gp_Trsf, gp_Vec, gp_Ax2, gp_Pnt, gp_Dir, gp_Ax3, gp_Quaternion
# from OCC.Display import OCCViewer
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QColor
from vtkmodules import qt
from OCC.Core.V3d import V3d_Yneg

from StepModel import StepModel

from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox, BRepPrimAPI_MakeCylinder, BRepPrimAPI_MakeCone
from OCC.Core.STEPControl import STEPControl_Reader
from PyQt5.QtWidgets import *
from OCC.Display.backend import load_backend, get_qt_modules
from OCC.Core.Graphic3d import Graphic3d_NOM_ALUMINIUM

load_backend("pyqt5")

import OCC.Display.qtDisplay as qtDisplay


class ClickableWidget(QWidget):
    clicked = pyqtSignal(int)  # Signal now emits an integer index

    def __init__(self, index, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.index = index  # Store the index

    def mousePressEvent(self, event):
        self.clicked.emit(self.index)  # Emit the index when clicked
        super().mousePressEvent(event)


class SetupWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.logo = "./VDL.png"
        pixmap = qtDisplay.QtGui.QPixmap(self.logo)
        self.icon = pixmap.scaled(32, 32)

        self.selected_file_name = ""
        self.setWindowTitle("VDL | Hole recognition")
        self.setWindowIcon(qtDisplay.QtGui.QIcon(self.icon))
        self.setGeometry(580, 300, 800, 300)
        QApplication.setStyle(QStyleFactory.create('Fusion'))

        self.setup_ui()


    def setup_ui(self):
        layout = QVBoxLayout()

        select_layout = QHBoxLayout()
        layout.addLayout(select_layout)

        select_button = QPushButton("Select file")
        select_button.clicked.connect(self.select_file)
        select_layout.addWidget(select_button)

        self.input_select_file = QLineEdit("No file selected.")
        self.input_select_file.setReadOnly(True)
        select_layout.addWidget(self.input_select_file)

        name_layout = QHBoxLayout()
        layout.addLayout(name_layout)

        name_button = QPushButton("Name:")
        name_layout.addWidget(name_button)

        self.input_label_name = QLineEdit()
        self.input_label_name.setReadOnly(True)
        name_layout.addWidget(self.input_label_name)

        # load = QPushButton("Confirm", self)
        # # load.clicked.connect(self.button_load)
        # name_layout.addWidget(load)

        filter_layout = QHBoxLayout()
        layout.addLayout(filter_layout)

        button_layout = QVBoxLayout()
        filter_layout.addLayout(button_layout)

        filter_button = QPushButton("Filters:")
        filter_button.setMaximumWidth(80)
        button_layout.addWidget(filter_button)

        button_layout.addSpacing(120)

        add_button = QPushButton("Add Filter")
        add_button.setMaximumWidth(80)
        add_button.clicked.connect(self.add_float)
        button_layout.addWidget(add_button)

        remove_button = QPushButton("Remove")
        remove_button.setMaximumWidth(80)
        remove_button.clicked.connect(self.remove_selected)
        button_layout.addWidget(remove_button)

        self.float_list_widget = QListWidget()
        filter_layout.addWidget(self.float_list_widget)

        # Add a button to start the main application
        self.start_button = QPushButton("Start Application")
        self.start_button.clicked.connect(self.start_application)
        self.start_button.setEnabled(False)
        layout.addWidget(self.start_button)

        self.setLayout(layout)

    def select_file(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                   "STEP Files (*.stp *.step)", options=options)
        if file_name:
            self.selected_file = file_name
            self.input_select_file.setText(self.selected_file)
            base_name = os.path.basename(self.selected_file)
            file_stem = os.path.splitext(base_name)[0]
            self.input_label_name.setReadOnly(False)
            self.input_label_name.setText(file_stem)
            self.selected_file_name = file_stem

            print(f"File selected: {self.selected_file}")

            self.start_button.setEnabled(True)

    def add_float(self):
        self.setWindowIcon(qtDisplay.QtGui.QIcon(self.icon))
        float_value, ok = QInputDialog.getDouble(self, "Add filter", "Enter a hole size to add to the filters:")

        if ok:
            self.float_list_widget.addItem(str(float_value))

    def remove_selected(self):
        selected_items = self.float_list_widget.selectedItems()
        for item in selected_items:
            self.float_list_widget.takeItem(self.float_list_widget.row(item))

    def start_application(self):
        if self.selected_file_name != "":
            filters = [float(self.float_list_widget.item(i).text()) for i in range(self.float_list_widget.count())]

            self.hide()  # Hide the setup window
            self.application = Application(self.selected_file, self.selected_file_name, filters)
            self.application.show()


class Application(QWidget):
    def __init__(self, selected_file, selected_name, filters=0):
        super().__init__()
        self.index = 0
        self.insert_diameter = ["None", "M2", "M3", "M4", "M5", "M6", "M7", "M8", "M10", "M12"]
        self.insert_length = ["None", "x1", "x1.5", "x2"]
        self.preview_cone = None
        self.shape = None

        self.title = "VDL | Hole recognition | " + selected_name

        self.logo = "./VDL.png"
        pixmap = qtDisplay.QtGui.QPixmap(self.logo)
        self.icon = pixmap.scaled(32, 32)

        self.left = 200
        self.top = 100
        self.width = 1500
        self.height = 800

        self.init_ui()

        self.step = StepModel(selected_file, selected_name, filters)
        self.model = self.display.DisplayShape(self.step.shape, material=Graphic3d_NOM_ALUMINIUM)
        self.display.FitAll()
        self.create_scroll_list()

    def init_ui(self):
        self.setWindowTitle(self.title)

        self.setWindowIcon(qtDisplay.QtGui.QIcon(self.icon))

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
        self.verticalGroupBox = QGroupBox()
        self.verticalGroupBox.setMaximumWidth(800)
        layout = QVBoxLayout()

        hole_widget = self.create_hole_widget(Hole(("X", "Y", "Z"), ("rX", "rY", "rZ"), "Diameter", "Depth"), "ID", True)
        hole_widget.layout().setContentsMargins(0, 0, 15, 0)
        layout.addWidget(hole_widget)

        self.scrollArea = QScrollArea(self)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget(self)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.scrollAreaLayout = QVBoxLayout(self.scrollAreaWidgetContents)

        self.scrollAreaLayout.setContentsMargins(0, 0, 0, 0)
        self.scrollAreaLayout.setSpacing(0)

        layout.addWidget(self.scrollArea)

        get = QPushButton("Export holes to file", self)
        get.clicked.connect(self.get_selected_values)
        layout.addWidget(get)

        self.verticalGroupBox.setLayout(layout)

    def create_horizontal_layout(self):
        self.horizontalGroupBox = QGroupBox()
        layout = QHBoxLayout()
        layout.addWidget(self.verticalGroupBox)

        self.canvas = qtDisplay.qtViewer3d(self)
        layout.addWidget(self.canvas)
        self.horizontalGroupBox.setLayout(layout)

    def create_scroll_list(self):
        for i in reversed(range(self.scrollAreaLayout.count())):
            widget_to_remove = self.scrollAreaLayout.itemAt(i).widget()
            self.scrollAreaLayout.removeWidget(widget_to_remove)
            widget_to_remove.setParent(None)

        for i, hole in enumerate(self.step.holes):
            hole_widget = self.create_hole_widget(hole, i)
            hole_widget.clicked.connect(lambda index=i: self.hole_clicked(index))
            self.scrollAreaLayout.addWidget(hole_widget)

    def hole_clicked(self, index):
        print(f"Hole clicked: {index}")
        self.preview_position(*self.step.holes[index].location, *self.step.holes[index].direction)

    def create_hole_widget(self, hole, index, header=False):
        hole_widget = ClickableWidget(index, self)
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        common_style = """
                        background-color: white;
                        border: 1px solid gray;
                        padding: 2px;
                        border-radius: 3px;
                    """

        common_style_dark = """
                            background-color: lightblue;
                            border: 1px solid gray;
                            padding: 2px;
                            border-radius: 3px;
                        """

        widgets = [
            QLabel(f"Hole: {index}"),
            QLabel(f"{hole.diameter}"),
            QLabel(f"{hole.depth}"),
            QLabel(f"{hole.location[0]}"),
            QLabel(f"{hole.location[1]}"),
            QLabel(f"{hole.location[2]}"),
            QLabel(f"{hole.direction[0]}"),
            QLabel(f"{hole.direction[1]}"),
            QLabel(f"{hole.direction[2]}")
        ]

        if header:
            widgets.append(QLabel(f"Insert type"))
            widgets.append(QLabel(f"x length"))

        for widget in widgets:
            if index == "ID":
                widget.setStyleSheet(common_style)
                layout.addWidget(widget)
            elif index % 2 == 0:
                widget.setStyleSheet(common_style_dark)
                layout.addWidget(widget)
            else:
                widget.setStyleSheet(common_style)
                layout.addWidget(widget)

        if not header:
            menu_select_type = QComboBox()
            menu_select_type.addItems(self.insert_diameter)
            menu_select_type.setObjectName("menu_select_type")

            menu_select_length = QComboBox()
            menu_select_length.addItems(self.insert_length)
            menu_select_length.setObjectName("menu_select_length")

            if index % 2 == 0:
                menu_select_type.setStyleSheet("background-color: lightblue")
                menu_select_length.setStyleSheet("background-color: lightblue")

            layout.addWidget(menu_select_type)
            layout.addWidget(menu_select_length)

        hole_widget.setLayout(layout)
        return hole_widget

    def get_selected_values(self):
        for i in range(self.scrollAreaLayout.count()):
            widget = self.scrollAreaLayout.itemAt(i).widget()
            if isinstance(widget, ClickableWidget):
                for child_widget in widget.findChildren(QComboBox):
                    if child_widget.currentIndex() != -1:
                        index = widget.index
                        if child_widget.objectName() == "menu_select_type":
                            diameter = child_widget.currentText()
                            self.step.holes[index].selected_diameter = diameter
                        elif child_widget.objectName() == "menu_select_length":
                            length = child_widget.currentText()
                            self.step.holes[index].selected_length = length
        self.step.export_csv()

    def erase_shape(self):
        self.display.Context.Erase(self.model, True)

    def preview_position(self, x, y, z, rx, ry, rz):
        trsf = gp_Trsf()

        translation_vector = gp_Vec(x, y, z)

        new_direction = gp_Dir(rx, ry, rz)  # Example: align with the X-axis
        new_up_direction = gp_Dir(0, 1, 0)  # Example: align with the Y-axis

        # Define the rotation axis system using the direction vectors
        rotation_axis_system = gp_Ax3(gp_Pnt(-3, -3, -15), new_direction, new_up_direction)

        trsf.SetTransformation(rotation_axis_system)

        trsf.SetTranslation(translation_vector)

        self.display.FitAll()

        if self.preview_cone is not None:
            self.display.Context.Erase(self.preview_cone, True)

        cone_radius = 6
        cone_height = 15

        cone_position = gp_Ax2(gp_Pnt(0, 0, 0), gp_Dir(rx, ry, rz))
        cone = BRepPrimAPI_MakeCone(cone_position, cone_radius, 0, cone_height).Shape()

        transformed_cone = BRepBuilderAPI_Transform(cone, trsf, True).Shape()
        self.preview_cone = self.display.DisplayShape(transformed_cone, color="green", update=True)[0]
