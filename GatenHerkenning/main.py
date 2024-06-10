import os
import sys

from Application import SetupWindow, Application
from PyQt5.QtWidgets import QApplication

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = SetupWindow()
    ex.show()

    if os.getenv("APPVEYOR") is None:
        sys.exit(app.exec_())
