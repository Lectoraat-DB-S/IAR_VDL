class Windows():
    def __init__(self, title, horizontal_offset = 600, vertical_offset = 200, width = 700, height = 600):
        self.title = "PyQt5 / pythonOCC"
        self.horizontal_offset = horizontal_offset
        self.vertical_offset = vertical_offset
        self.width = width
        self.height = height

    def show_window(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.createHorizontalLayout()

        windowLayout = QVBoxLayout()
        windowLayout.addWidget(self.horizontalGroupBox)
        self.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    (windowLayout)
        self.show()
        self.canvas.InitDriver()
        self.canvas.resize(200, 200)
        self.display = self.canvas._display
