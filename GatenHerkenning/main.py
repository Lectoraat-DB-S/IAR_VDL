import os
import sys

from Application import Application
from PyQt5.QtWidgets import QApplication

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Application()

    if os.getenv("APPVEYOR") is None:
        sys.exit(app.exec_())
