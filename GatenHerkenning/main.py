import os
import sys
from PyQt5.QtWidgets import QApplication
from App import App


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = App()
    if os.getenv("APPVEYOR") is None:
        sys.exit(app.exec_())