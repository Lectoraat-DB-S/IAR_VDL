import os
import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QThread, pyqtSignal
from CadConverter import CadConverter
from App import App

import numpy as np
import pycuda.driver as cuda
import pycuda.autoinit
from pycuda.compiler import SourceModule


class AppThread(QThread):
    finished = pyqtSignal()

    def __init__(self):
        super().__init__()

    def run(self):
        app = QApplication(sys.argv)
        ex = App()
        ex.show()
        if os.getenv("APPVEYOR") is None:
            sys.exit(app.exec_())
        self.finished.emit()


if __name__ == "__main__":
    thread = AppThread()
    thread.run()