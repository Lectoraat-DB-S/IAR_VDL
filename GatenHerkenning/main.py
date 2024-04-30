import os
import sys

from PyQt5.QtWidgets import QApplication
from screens.InitScreen import InitScreen as App

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = App()

    if os.getenv("APPVEYOR") is None:
        sys.exit(app.exec_())